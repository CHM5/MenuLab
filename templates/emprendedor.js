let allRows = [];

// === Cargar menú ===
fetch(CSV_URL)
  .then(r => r.text())
  .then(data => {
    allRows = data.split("\n").slice(1).map(r => r.split(",").map(c => c.replace(/\"/g, "")));
    renderMenu(allRows);
  });

// === Renderizar menú agrupado ===
function renderMenu(rows) {
  const container = document.getElementById("menuTable");
  container.innerHTML = "";
  const grouped = {};
  rows.forEach(cols => {
    const [cat, sub, name, desc, price, ...flags] = cols.map(c => c.trim());
    if (!cat || !name) return;
    if (!grouped[cat]) grouped[cat] = {};
    const s = sub || "-";
    if (!grouped[cat][s]) grouped[cat][s] = [];
    grouped[cat][s].push({ name, desc, price, flags });
  });
  Object.entries(grouped).forEach(([cat, subs]) => {
    const catWrapper = document.createElement("div");
    const catTitle = document.createElement("h2");
    catTitle.textContent = cat;
    catWrapper.appendChild(catTitle);
    Object.entries(subs).forEach(([sub, items]) => {
      if (sub && sub !== "-") {
        const subTitle = document.createElement("h3");
        subTitle.textContent = sub;
        catWrapper.appendChild(subTitle);
      }
      items.forEach(item => {
        const div = document.createElement("div");
        div.className = "menu-item";
        if (item.flags.includes("destacado")) div.classList.add("destacado");
        div.innerHTML = `
          <div class="menu-plate">
            <h4>${item.name}</h4>
            <p class="menu-description">${item.desc || ""}</p>
          </div>
          <span class="menu-price">${item.price}</span>
        `;
        catWrapper.appendChild(div);
      });
    });
    container.appendChild(catWrapper);
  });
}
