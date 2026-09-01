# Project Citadel: Your Home Command Center When the Internet Fails

When the power grid collapses, the internet goes dark, or your neighborhood loses connectivity for days, most people are left scrambling. Their smart home becomes dumb. Their media libraries are inaccessible. Their emergency protocols are locked behind cloud services. Their medical references are unreachable.

But what if you had **everything you needed running on hardware you own, serving your entire home network, regardless of what happens to the outside world?**

That's Project Citadel.

---

## The Grid-Down Reality

Let's be honest: infrastructure failures happen more often than we'd like to admit.

- **2024 saw record-breaking power outages** — Texas, California, and other regions experienced cascading grid failures lasting days
- **ISP outages are routine** — the average American experiences 4-6 significant internet outages per year
- **Cyberattacks target infrastructure** — critical systems are increasingly vulnerable
- **Natural disasters isolate regions** — hurricanes, floods, and wildfires cut off communications for weeks

When an outage hits, you lose:
- Access to your media libraries (everything's in the cloud now)
- Smart home automation (most systems phone home constantly)
- Medical and emergency references (Google's down)
- Communication tools (your phone can't reach cloud servers)
- Data and records (backed up "safely" offsite)
- Any sense of local control

**The solution isn't to panic. It's to build local infrastructure.**

---

## Introducing Project Citadel

Project Citadel is a **complete, self-hosted home command center** that runs entirely on your own hardware — a single machine running Docker — and serves your entire household (and your LAN) with **zero dependence on the internet**.

Think of it as a local-first operating system for your home. Open a browser to `http://localhost:8085` (or from any device on your network), and you have access to:

### 🛡️ **Command Cockpit Dashboard**
A unified command center with 12 integrated modules:

- **Media Vault** — Your entire video, audio, and PDF library organized by category, streaming offline
- **Offline AI Assistant** — Local AI models (Ollama) for research, writing, analysis — no cloud, no tracking, no latency
- **Encyclopedia & Knowledge Base** — Full Wikipedia, medical references, technical manuals, survival guides — all cached locally
- **Home Education Platform** — Thousands of interactive lessons for children, searchable offline
- **Secure Notes** — Encrypted markdown storage for sensitive plans, protocols, and documentation
- **Emergency Medical Reference** — Offline trauma protocols, first-aid procedures, medication databases
- **Smart Home Control** — Local device registry and relay control for cameras, power monitoring, and automation
- **Homestead Logistics** — Complete inventory tracking for food, fuel, PPE, livestock, and crops
- **Communications Hub** — Radio frequency logs, scanner data, tactical notes
- **And more** — all accessible from one screen

### 📊 **Production-Grade Inventory System**

Citadel includes a full **SQLite-backed logistics database** for serious preparedness:

- **Food Storage Ledger** — Track provisions, freeze-dried storage, shelf life dates, calorie counts
- **Fuel Management** — Monitor gasoline, diesel, propane, rotation schedules
- **PPE Stock** — Manage masks, respirators, protective kits, inspection status
- **Orchard & Livestock** — Log fruit trees, animal herds, health records, production yields
- **Botanical Garden Database** — Year-over-year crop records (2025–2028), spring/fall planting cycles, fertilization schedules, pest management, total yield tracking

When the internet is gone and you need to know how much food is in storage or which trees are producing this season, **Citadel has the answer**.

### 🏠 **Smart Home Hub (Project Vigil)**

An embedded IoT controller that works **completely offline**:

- Register DIY smart devices (ESP32 relays, cameras, sensors) via simple HTTP heartbeat
- Toggle devices on/off from the dashboard
- Monitor solar power systems and off-grid power levels
- Track device state persistently across reboots
- Zero cloud dependencies — all communication is LAN-local

Includes a complete **Arduino sketch for ESP32** so you can build your own smart relay hardware.

---

## Why This Matters: The Grid-Down Scenario

Imagine this: It's 3 AM. A storm knocked out power in your region. The grid is down. Internet is gone. Cell towers are offline.

**Without Citadel:**
- Your "smart home" is now just a house full of dead devices
- You can't access your medical files or emergency protocols
- Your kids need to study, but their learning platform is in the cloud
- You need to check your food inventory, but your tracking app is on your phone, which has no service
- You can't control solar power systems or water pumps
- You're flying blind, making decisions without data

**With Citadel:**
- Your entire home infrastructure keeps running on local power
- You open a browser (on laptop, tablet, any device) and access the command center
- You see how much fuel you have, what food is in storage, which crops are ready
- Kids have access to full educational materials offline
- You can control lights, pumps, relays, and monitor power systems
- You have medical references, emergency protocols, and communication logs right there
- Your home is still a functioning command center, not a dark box

**This is not hypothetical.** People in Texas, California, and disaster zones are living this reality right now.

---

## It's Not Just for Doomsday Preppers

You don't have to be building a bunker to benefit from Citadel.

- **Homesteaders** use it to manage their orchard, livestock, and crop rotation data
- **Homeschooling families** rely on the offline education platform and media library
- **Remote workers** appreciate local media access and offline AI without cloud latency
- **Privacy-conscious people** love that nothing leaves their network
- **Disaster preparedness planners** build their infrastructure knowing it survives outages
- **Parents** want their kids to have access to educational materials without relying on internet service

**Everyone benefits from local infrastructure.**

---

## The Technical Reality: It Actually Works

Citadel runs on Docker, meaning it works on:
- **Linux** (desktop, server, NAS, even old laptops)
- **macOS** (Intel or Apple Silicon)
- **Windows** (with Docker Desktop)
- Essentially any hardware with 4 GB RAM and a modern OS

First run takes a few minutes to pull the containerized services. Then:

- **Press one button** and everything starts
- **Open a browser** — your command center is live
- **Add your content** — drop media files in folders, download offline encyclopedias, populate your inventory database
- **Network access** — any device on your LAN can access the dashboard and services
- **Works offline** — immediately and indefinitely

The stack includes battle-tested open-source tools:
- **Ollama** — production-grade offline LLM inference
- **Open WebUI** — mature AI chat interface
- **Kiwix** — proven offline content server
- **Kolibri** — learning platform built by Learning Equality
- **Flatnotes** — lightweight markdown storage
- **nginx** — rock-solid reverse proxy

This isn't a hobby project that might break. It's built on infrastructure designed for reliability.

---

## What Makes Citadel Different

### ✅ **Truly Offline-First**
Not "cloud-optional." Not "works better offline." **Actually offline.**

When your internet is down, Citadel doesn't degrade. It doesn't phone home. It doesn't sync with a cloud service. Everything keeps working exactly as it did before.

### ✅ **Comprehensive**
You're not stitching together a dozen single-purpose tools. You get a unified command center where media, education, emergency reference, home automation, and logistics all live in one place.

### ✅ **Hardware You Own**
No subscriptions. No vendor lock-in. No company holding your data hostage. You buy a used laptop or NAS, run Docker, and you own your entire infrastructure.

### ✅ **LAN-First**
Your entire household (and anyone on your local network) can access services, even when the internet is down. Smart devices register and get controlled. Computers and phones can stream media. It's a network hub, not just a personal tool.

### ✅ **Free and Open Source**
Licensed under GPL-3.0, so you can modify it, fork it, audit it, and contribute back. No corporate interests. No surveillance.

### ✅ **Actually Tested**
The ROADMAP is public and honest. Known gaps are documented. It's built by someone who actually uses this to run their home.

---

## Getting Started: It's Easier Than You Think

**Installation takes 5 minutes:**

1. Download and unzip Project Citadel
2. Run `install.sh` (Linux/macOS) or `install.bat` (Windows)
3. Open `http://localhost:8085` in your browser
4. Your command center is live

**Then populate it:**
- Drop videos, audio, and PDFs into folders
- Download offline encyclopedias from Kiwix
- Add items to your inventory and logistics ledgers
- Connect smart home devices (or don't — it works great solo)
- Start using it today, knowing it'll be here tomorrow

**No cloud account needed. No registration. No tracking. Just your infrastructure, running on your hardware.**

---

## The Homestead Angle

If you're growing food, keeping livestock, or managing land, Citadel is a **complete management tool**:

- Track seed varieties and crop yields year-over-year
- Log fertilization schedules and pest pressures
- Monitor livestock health and production
- Manage orchard inventory and tree locations
- Store survival guides, medical references, and emergency protocols
- All searchable, all local, all persistent

When you need to know "What varieties did I plant in 2024, and what was the yield?" — Citadel has the answer.

---

## The Emergency Preparedness Angle

If you're building a resilient home:

- **Grid Down:** All your infrastructure keeps running
- **Internet Down:** Your home network keeps functioning
- **Power Restored:** Services restart automatically
- **Long-term Outage:** You have everything cached and ready

Citadel is the central nervous system of a resilient home. It's what keeps you functional when commercial services fail.

---

## The Privacy Angle

If you're tired of corporate cloud services:

- **Zero cloud sync** — everything stays on your hardware
- **No tracking** — nothing phones home
- **No ads** — no business model demanding your attention
- **No surveillance** — you own your data, not a company
- **No subscriptions** — one-time setup, runs forever

Just local infrastructure, doing its job.

---

## Real Talk: What It Isn't

Citadel is genuinely excellent, but it's not a magic solution:

- **Not a backup to the cloud** — it's a replacement for cloud dependency, not a supplement
- **Not a network security fortress** — it's designed for your local network, not public exposure
- **Not a phone system** — you'll need other tools for real communications
- **Not production-enterprise** — it's built for homes and small operations, not Fortune 500 infrastructure

What it *is*, is a **genuinely capable, offline-first home infrastructure platform**. And that's enough.

---

## The Future: What's Coming

The roadmap is public and exciting:

- **Raspberry Pi support** — running Citadel on modest hardware
- **Project IBRIS radar integration** — local signal tracking
- **SDRTrunk radio decoding** — P25 trunked-radio support for serious communications
- **Kubernetes-ready containerization** — scale to larger deployments
- **Better version management** — keep embedded services in sync with upstream

The project is actively developed and transparent about its direction.

---

## Why Now?

Grid resilience is no longer theoretical. It's immediate and practical.

- Infrastructure is aging and stressed
- Extreme weather is increasing in frequency and intensity
- Cyber threats to critical systems are real
- Supply chains are fragile
- Centralized services create single points of failure

**Building local infrastructure isn't paranoia. It's prudence.**

Citadel gives you the tools to do it easily, comprehensively, and affordably.

---

## Get Started Today

**Project Citadel is ready. It's free. It's open source. It works.**

1. **Visit the repository:** https://github.com/frankprobst5-stack/Project-Citadel
2. **Download the code**
3. **Run the installer**
4. **Open http://localhost:8085**
5. **Start building your resilient home**

The internet will fail. The grid might go down. But your home infrastructure? That stays up. That keeps you connected. That keeps you informed and in control.

**That's Project Citadel.**

---

## Questions?

- **What if I lose power?** Citadel runs on whatever powers your home — laptop, NAS, desktop. Pair it with a UPS or solar system and you're golden.
- **Can multiple people access it?** Yes. Anyone on your network can use it simultaneously.
- **What if I want to expand it?** The code is open source. Contribute features, fork it, modify it. It's yours.
- **Is this legal?** Absolutely. It's your hardware, your network, your data.
- **What about Raspberry Pi?** Not officially supported yet, but it's on the roadmap. For now, use a laptop or desktop.

---

## The Bottom Line

In a world where connectivity fails, where cloud services disappear, where corporate infrastructure crumbles under pressure, **you want something you own and control.**

Citadel is exactly that.

It's your home command center. It's your media library. It's your emergency reference. It's your smart home hub. It's your logistics database. It's your insurance policy against infrastructure failure.

**And it's waiting for you to download it.**

---

*Project Citadel is free, open-source software licensed under GPL-3.0-or-later. Built for resilience. Built for privacy. Built to stay up when everything else goes down.*
