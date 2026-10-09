(() => {
  const htmlInput = document.getElementById("hcs-html");
  const cssInput = document.getElementById("hcs-css");
  const preview = document.getElementById("hcs-preview");

  let debounce = null;

  function render() {
    const doc = `<!doctype html><html><head><style>${cssInput.value}</style></head><body>${htmlInput.value}</body></html>`;
    preview.srcdoc = doc;
  }

  function onInput() {
    clearTimeout(debounce);
    debounce = setTimeout(render, 250);
  }

  htmlInput.addEventListener("input", onInput);
  cssInput.addEventListener("input", onInput);

  async function loadStarter() {
    try {
      const resp = await fetch("/api/html-css-sandbox/starter");
      const starter = await resp.json();
      htmlInput.value = starter.html;
      cssInput.value = starter.css;
      render();
    } catch (err) {
      htmlInput.value = "<h1>Hello!</h1>";
      render();
    }
  }

  loadStarter();
})();
