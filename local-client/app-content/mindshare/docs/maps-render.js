(function () {
  const manifest = window.MAPS_MANIFEST;

  if (!manifest) {
    return;
  }

  function line(depth, text) {
    const indent = "  ".repeat(depth);
    return `${indent}${text}`;
  }

  function renderTree() {
    const target = document.querySelector("[data-maps-tree]");
    if (!target) {
      return;
    }

    const lines = ["maps/"];
    lines.push(line(1, "docs/"));
    manifest.pages.forEach((page) => lines.push(line(2, page.file)));
    lines.push(line(2, "styles.css"));
    lines.push(line(2, "maps-manifest.js"));
    lines.push(line(2, "maps-render.js"));

    lines.push(line(1, "phases/"));
    manifest.phases.forEach((phase) => lines.push(line(2, phase)));

    lines.push(line(1, "skills/"));
    manifest.skills.forEach((skill) => {
      lines.push(line(2, `${skill.name}/`));
      skill.files.forEach((file) => lines.push(line(3, file)));
    });

    lines.push(line(1, "templates/"));
    manifest.templates.forEach((template) => lines.push(line(2, template)));

    lines.push(line(1, "catalogs/"));
    manifest.catalogs.forEach((catalog) => lines.push(line(2, catalog)));

    target.textContent = lines.join("\n");
  }

  function renderResourceList(selector, items, renderItem) {
    const target = document.querySelector(selector);
    if (!target) {
      return;
    }
    target.innerHTML = "";
    items.forEach((item) => {
      const li = document.createElement("li");
      renderItem(li, item);
      target.appendChild(li);
    });
  }

  function renderResources() {
    const phase = document.body.getAttribute("data-maps-phase") || "0";
    const phaseResources = manifest.phaseResources?.[phase] || {};
    const skillItems = (phaseResources.skills || []).map((name) => manifest.skills.find((skill) => skill.name === name)).filter(Boolean);
    const repoItems = (phaseResources.repos || []).map((label) => manifest.repos.find((repo) => repo.label === label)).filter(Boolean);
    const toolItems = phaseResources.tools || [];
    const templateItems = phaseResources.templates || [];
    const catalogItems = phaseResources.catalogs || [];

    renderResourceList("[data-maps-skills]", skillItems, (li, skill) => {
      const strong = document.createElement("strong");
      strong.textContent = skill.displayName || (skill.name === "scaffold" ? "/scaffold" : skill.name);
      li.appendChild(strong);
      li.append(` includes ${skill.files.join(", ")}.`);
    });

    renderResourceList("[data-maps-repos]", repoItems, (li, repo) => {
      const anchor = document.createElement("a");
      anchor.href = repo.url;
      anchor.textContent = repo.label;
      li.appendChild(anchor);
    });

    renderResourceList("[data-maps-tools]", toolItems, (li, tool) => {
      const strong = document.createElement("strong");
      strong.textContent = tool;
      li.appendChild(strong);
    });

    renderResourceList("[data-maps-templates]", templateItems, (li, template) => {
      const code = document.createElement("code");
      code.textContent = `templates/${template}`;
      li.appendChild(code);
    });

    renderResourceList("[data-maps-catalogs]", catalogItems, (li, catalog) => {
      const code = document.createElement("code");
      code.textContent = `catalogs/${catalog}`;
      li.appendChild(code);
    });
  }

  renderTree();
  renderResources();
})();
