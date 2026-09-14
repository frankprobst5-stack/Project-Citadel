"""Real logic behind Settings > Modules (ROADMAP.md Phase B follow-up,
2026-09-14): listing installed modules, toggling which are enabled,
regenerating docker-compose.yml's `include:` list from whatever modules
actually exist on disk, installing a new module from an uploaded .zip,
and applying a change via a real `docker compose up -d`.

Module discovery is filesystem-driven, not a hardcoded list: any
directory directly under modules/ containing a manifest.json is a real
module, whether it shipped with Citadel or was installed later via
Settings > Install Module. Nothing here special-cases "the original nine"
versus one you add tomorrow.

CRITICAL, read before touching apply_compose(): this only works because
vault-api's own docker-compose.yml entry mounts the HOST's docker.sock
AND the whole project directory at an IDENTICAL absolute path on both
sides (Docker-outside-of-Docker) -- see that file's own comment on
vault-api's volumes for the full reasoning. Calling apply_compose() with
a path that doesn't match a real host-side mount is not just "won't
work," it will send the host's dockerd bind-mount requests for a path
that only exists inside this container, which is exactly the kind of
silent-wrong-mount bug backup.py's own module docstring already warns
about elsewhere in this codebase -- hence the explicit guard rather than
just letting `docker compose` fail with a confusing error three layers
down.
"""
import json
import os
import re
import subprocess
import zipfile


MODULE_NAME_RE = re.compile(r"^[a-z0-9_-]+$")

INCLUDE_START_MARKER = "# --- MODULE INCLUDES: START (auto-generated, do not hand-edit) ---"
INCLUDE_END_MARKER = "# --- MODULE INCLUDES: END ---"


def get_enabled_profiles(env_path):
    """Returns the current COMPOSE_PROFILES as a set, or an empty set if
    .env doesn't exist yet or has no such line -- same honest-empty-
    default convention used elsewhere in this project (e.g. backup.py's
    list_backups). Public (not just an internal helper for list_modules)
    because apply_compose()'s caller needs the OLD set -- read BEFORE
    set_enabled_profiles() overwrites it -- to know which profiles are
    being turned off, see that function's own docstring for why."""
    if not os.path.exists(env_path):
        return set()
    with open(env_path) as f:
        for line in f:
            if line.startswith("COMPOSE_PROFILES="):
                value = line.rstrip("\n").split("=", 1)[1]
                return {p for p in value.split(",") if p}
    return set()


def list_modules(modules_root, env_path):
    """[{...every field from manifest.json..., "enabled": bool}], one per
    modules/<name>/manifest.json that actually exists, sorted by name.
    `enabled` is computed fresh from .env every call, never cached, so it
    can never drift from what's actually about to run."""
    enabled_profiles = get_enabled_profiles(env_path)
    modules = []
    if not os.path.isdir(modules_root):
        return modules
    for name in sorted(os.listdir(modules_root)):
        manifest_path = os.path.join(modules_root, name, "manifest.json")
        if not os.path.isfile(manifest_path):
            continue
        with open(manifest_path) as f:
            manifest = json.load(f)
        manifest["enabled"] = manifest.get("profile") in enabled_profiles
        modules.append(manifest)
    return modules


def set_enabled_profiles(env_path, profiles):
    """Rewrites .env's COMPOSE_PROFILES= line in place, preserving every
    other line untouched (byte-identical, not just "looks the same") --
    a straight line-by-line rewrite, not a regenerate-from-scratch, so a
    user's own hand-added comments/values elsewhere in .env always
    survive. Appends the line if .env somehow has none yet (shouldn't
    normally happen, install.sh always writes one) rather than silently
    doing nothing."""
    profiles_value = ",".join(sorted(p for p in profiles if p))
    with open(env_path) as f:
        lines = f.readlines()
    found = False
    for i, line in enumerate(lines):
        if line.startswith("COMPOSE_PROFILES="):
            lines[i] = f"COMPOSE_PROFILES={profiles_value}\n"
            found = True
            break
    if not found:
        lines.append(f"COMPOSE_PROFILES={profiles_value}\n")
    with open(env_path, "w") as f:
        f.writelines(lines)


def sync_compose_include(compose_path, modules_root):
    """Rewrites ONLY the text between the START/END marker comments in
    docker-compose.yml to list exactly the compose.fragment.yml files
    that exist under modules_root right now (sorted, for a stable diff
    every run). Deliberately narrow -- matches on explicit markers rather
    than trying to parse/regenerate the whole YAML file, so everything
    else a human wrote in this file (comments, the actual service
    definitions) is never at risk of being reformatted or dropped.
    Returns the list of fragment paths written. Raises RuntimeError if
    the markers are missing -- refuses to guess where the include: list
    should go rather than inserting one somewhere that might be wrong."""
    fragments = []
    if os.path.isdir(modules_root):
        for name in sorted(os.listdir(modules_root)):
            if not MODULE_NAME_RE.match(name):
                continue
            fragment = os.path.join(modules_root, name, "compose.fragment.yml")
            if os.path.isfile(fragment):
                fragments.append(f"modules/{name}/compose.fragment.yml")

    with open(compose_path) as f:
        content = f.read()

    start_idx = content.find(INCLUDE_START_MARKER)
    end_idx = content.find(INCLUDE_END_MARKER)
    if start_idx == -1 or end_idx == -1 or end_idx < start_idx:
        raise RuntimeError(
            "docker-compose.yml is missing the module-includes markers "
            f"({INCLUDE_START_MARKER!r} / {INCLUDE_END_MARKER!r}) -- "
            "refusing to guess where to insert the include: list."
        )

    include_lines = "\n".join(["include:"] + [f"  - {p}" for p in fragments])
    new_block = f"{INCLUDE_START_MARKER}\n{include_lines}\n{INCLUDE_END_MARKER}"
    content = content[:start_idx] + new_block + content[end_idx + len(INCLUDE_END_MARKER):]

    with open(compose_path, "w") as f:
        f.write(content)
    return fragments


_SERVICE_KEY_RE = re.compile(r"^  ([A-Za-z0-9_.-]+):\s*(?:#.*)?$")


def _service_names_in_fragment(fragment_path):
    """Every top-level (exactly 2-space-indented) `<name>:` key under a
    compose.fragment.yml's `services:` block -- e.g. ["cloud9"] for
    education, or ["scanner", "intercept"]-style multiple names for a
    module whose one profile bundles more than one container. Plain text
    scan, not a real YAML parse (matches this file's own
    sync_compose_include(), which does the same for the same reason: no
    YAML dependency is installed in vault-api's image, and these
    fragments are hand-written in a single, consistent style anyway)."""
    names = []
    with open(fragment_path) as f:
        for line in f:
            m = _SERVICE_KEY_RE.match(line.rstrip("\n"))
            if m:
                names.append(m.group(1))
    return names


def _service_names_for_profile(modules_root, profile):
    """The real container service names (e.g. "cloud9") backing a given
    module profile (e.g. "education") -- resolved from that module's own
    manifest.json + compose.fragment.yml, not from asking `docker
    compose` to resolve the profile itself. See apply_compose()'s
    CRITICAL #1 for why: asking compose to act on "everything in a given
    --profile scope" also silently includes every un-profiled core
    service (cockpit, vault-api), so this function exists specifically
    to get an exact, explicit list of just this profile's own services
    instead."""
    if not os.path.isdir(modules_root):
        return []
    for name in sorted(os.listdir(modules_root)):
        manifest_path = os.path.join(modules_root, name, "manifest.json")
        if not os.path.isfile(manifest_path):
            continue
        with open(manifest_path) as f:
            manifest = json.load(f)
        if manifest.get("profile") != profile:
            continue
        fragment_path = os.path.join(modules_root, name, "compose.fragment.yml")
        if os.path.isfile(fragment_path):
            return _service_names_in_fragment(fragment_path)
    return []


def apply_compose(project_dir, modules_root, disabled_profiles=()):
    """Runs a real `docker compose up -d` against project_dir to start/
    recreate whatever should now be running, plus an explicit `docker
    compose stop <service names>` for every service backing a profile in
    disabled_profiles. Requires project_dir to be mounted at this exact
    same absolute path both here and on the host (see this module's own
    docstring) -- checks that the path at least exists and contains a
    docker-compose.yml before shelling out, since a DooD path mismatch
    otherwise fails in a confusing place (the HOST's dockerd, several
    layers away from whatever error message reaches the browser). Raises
    RuntimeError with the real stderr on failure -- never swallowed.

    CRITICAL #1, found live 2026-09-14, part one: `docker compose up` is
    additive-only by design -- turning a profile OFF in COMPOSE_PROFILES
    and then running plain `up -d` does NOT stop that profile's already-
    running containers (confirmed live: disabling "education" left
    cloud9 and kolibri running). So disabling a profile needs an
    explicit stop.

    CRITICAL #1, part two: the obvious way to do that stop --
    `docker compose --profile <name> stop` with no service names -- is
    itself dangerous and WAS tried and WAS live-tested here: a bare
    `stop` with no service arguments stops every service currently in
    scope for that invocation, and un-profiled core services (cockpit,
    vault-api) are unconditionally "in scope" for every `--profile`
    invocation regardless of which profile you named. Confirmed live:
    `docker compose --profile education stop` took down cockpit AND
    vault-api as collateral damage, crash-looping the whole dashboard a
    second time in the same session this feature was built. Fix: never
    run a project-wide subcommand with no explicit service list again --
    _service_names_for_profile() resolves the disabled profile's own
    real container names from its module folder (not from asking compose
    to interpret the profile), so the stop only ever names exactly the
    containers that should actually go down.

    CRITICAL #2, found live 2026-09-14 (separately): this command runs
    INSIDE vault-api's own container. A plain `docker compose up -d` (no
    service list) also considers vault-api's own service -- and this
    session's docker-compose.yml changes (new volumes/environment on
    vault-api itself) meant the very first real run of this recreated
    vault-api, which killed the container that was still in the middle
    of running the command, which left most of the rest of the fleet
    stuck mid-recreate ("Created" but never started). Recovered by re-
    running `docker compose up -d` from the HOST, which isn't self-
    destructive the same way. Fix here: explicitly excludes vault-api
    from the service list passed to `up`, so this call can never again
    tear down the container running it -- a module toggle never needs to
    touch vault-api's own service anyway, only modules' containers plus
    cockpit (which reads COMPOSE_PROFILES at its own startup, so it does
    legitimately need to recreate on every real toggle)."""
    if not project_dir:
        raise RuntimeError(
            "CITADEL_HOST_PATH isn't set -- re-run install.sh (it writes this "
            "automatically), or set it by hand in .env to the real absolute "
            "path Citadel is installed at on this machine, then restart "
            "vault-api (`docker compose up -d vault-api`) once to pick it up."
        )
    if not os.path.isfile(os.path.join(project_dir, "docker-compose.yml")):
        raise RuntimeError(
            f"CITADEL_HOST_PATH is set to {project_dir!r}, but no "
            "docker-compose.yml was found there from inside this container -- "
            "it must be mounted at the identical path on the host and in "
            "vault-api's own container for this to work. See docker-compose.yml's "
            "comment on vault-api's volumes."
        )

    errors = []
    output_parts = []

    to_stop = []
    for profile in sorted(p for p in disabled_profiles if p):
        to_stop.extend(_service_names_for_profile(modules_root, profile))

    if to_stop:
        stop_result = subprocess.run(
            ["docker", "compose", "stop"] + to_stop,
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=120,
        )
        if stop_result.returncode != 0:
            errors.append(f"stopping {to_stop}: {stop_result.stderr.strip() or stop_result.stdout.strip()}")
        else:
            output_parts.append(stop_result.stdout)

    services_result = subprocess.run(
        ["docker", "compose", "config", "--services"],
        cwd=project_dir,
        capture_output=True,
        text=True,
        timeout=60,
    )
    if services_result.returncode != 0:
        raise RuntimeError(services_result.stderr.strip() or "docker compose config --services failed")
    services = [s for s in services_result.stdout.split() if s != "vault-api"]

    up_result = subprocess.run(
        ["docker", "compose", "up", "-d"] + services,
        cwd=project_dir,
        capture_output=True,
        text=True,
        timeout=300,
    )
    if up_result.returncode != 0:
        errors.append(up_result.stderr.strip() or up_result.stdout.strip() or "docker compose up -d failed")
    else:
        output_parts.append(up_result.stdout)

    if errors:
        raise RuntimeError("; ".join(errors))
    return "\n".join(output_parts)


class UnsafeModuleArchiveError(Exception):
    """A module .zip contains a path-traversal entry, doesn't have the
    expected one-top-level-folder shape, or is missing manifest.json/
    compose.fragment.yml -- never extracted."""


def install_module_zip(zip_path, modules_root):
    """Validates and extracts a module .zip into modules/<name>/, where
    <name> comes from the zip's own single top-level folder. Checked, in
    order, before anything is extracted:
      1. every member's path is safe (no zip-slip traversal, no absolute paths)
      2. the zip has exactly one top-level folder (that's the module name)
      3. that name is a safe module name (lowercase/digits/-/_ only)
      4. manifest.json and compose.fragment.yml both exist at its top level
      5. a module by that name doesn't already exist (never silently overwrites)
    Returns the installed module's name. Does NOT enable it or call
    sync_compose_include()/apply_compose() -- the caller (the Flask route)
    does that explicitly, so each step's failure is attributable."""
    with zipfile.ZipFile(zip_path) as zf:
        names = zf.namelist()
        if not names:
            raise UnsafeModuleArchiveError("empty archive")

        top_levels = set()
        for member in names:
            norm = os.path.normpath(member)
            if norm.startswith("..") or os.path.isabs(norm):
                raise UnsafeModuleArchiveError(f"unsafe path in archive: {member!r}")
            top_levels.add(norm.split(os.sep)[0])

        if len(top_levels) != 1:
            raise UnsafeModuleArchiveError(
                "expected exactly one top-level folder in the zip (the module "
                f"name), found: {sorted(top_levels)}"
            )
        module_name = next(iter(top_levels))
        if not MODULE_NAME_RE.match(module_name):
            raise UnsafeModuleArchiveError(
                f"module folder name {module_name!r} must be lowercase "
                "letters/digits/-/_ only"
            )

        stripped_names = {n.rstrip("/") for n in names}
        required = {f"{module_name}/manifest.json", f"{module_name}/compose.fragment.yml"}
        if not required.issubset(stripped_names):
            raise UnsafeModuleArchiveError(
                "archive must contain manifest.json and compose.fragment.yml "
                "at its top level"
            )

        dest = os.path.join(modules_root, module_name)
        if os.path.exists(dest):
            raise UnsafeModuleArchiveError(
                f"a module named {module_name!r} already exists -- remove it "
                "manually first if you're intentionally replacing it"
            )

        zf.extractall(modules_root)

    return module_name


if __name__ == "__main__":
    import sys

    _here = os.path.dirname(os.path.abspath(__file__))
    _compose_path = os.path.join(_here, "..", "..", "docker-compose.yml")
    _modules_root = os.path.join(_here, "..", "..", "modules")
    if len(sys.argv) > 1 and sys.argv[1] == "--sync":
        written = sync_compose_include(_compose_path, _modules_root)
        print(f"Synced {len(written)} module(s) into docker-compose.yml's include: list:")
        for f in written:
            print(f"  - {f}")
    else:
        print("Usage: python3 modules_manager.py --sync")
        sys.exit(1)
