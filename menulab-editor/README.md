### Step 1: Update HTML Structure

1. **Create the "formato" button**.
2. **Add a grid for the format options**.
3. **Add checkboxes for category placements**.

Here's how you can modify the HTML:

```html
<!-- Replace the existing formato section with this -->
<section id="formato">
  <button id="formatoBtn">Formato</button>
  <div id="formatoOptions" style="display: none;">
    <div class="grid-opciones">
      <button data-format="1-column-right">1 Columna (Header a la derecha)</button>
      <button data-format="1-column-centered">1 Columna (Header centrado)</button>
      <button data-format="2-columns-centered">2 Columnas (Header centrado)</button>
      <button data-format="2-columns-left">2 Columnas (Header a la izquierda)</button>
      <button data-format="3-columns-centered">3 Columnas (Header centrado)</button>
      <button data-format="3-columns-left">3 Columnas (Header a la izquierda)</button>
    </div>
    <div class="categoria-options">
      <label><input type="radio" name="categoryPosition" value="left"> Categorías a la izquierda</label>
      <label><input type="radio" name="categoryPosition" value="center"> Categorías centradas</label>
      <label><input type="radio" name="categoryPosition" value="right"> Categorías a la derecha</label>
    </div>
  </div>
</section>
```

### Step 2: Update JavaScript Logic

Next, we need to add the functionality to show/hide the format options when the "formato" button is clicked and to handle the selection of formats and category positions.

Here's how you can modify the JavaScript:

```javascript
// Add this code to your existing script

// Toggle formato options
const formatoBtn = document.getElementById("formatoBtn");
const formatoOptions = document.getElementById("formatoOptions");

formatoBtn.addEventListener("click", () => {
  formatoOptions.style.display = formatoOptions.style.display === "none" ? "block" : "none";
});

// Handle format selection
document.querySelectorAll("#formatoOptions .grid-opciones button[data-format]").forEach(btn => {
  btn.addEventListener("click", () => {
    const format = btn.dataset.format;
    sendToPreview("format", format); // Send the selected format to the preview
  });
});

// Handle category position selection
document.querySelectorAll(".categoria-options input[name='categoryPosition']").forEach(radio => {
  radio.addEventListener("change", () => {
    const position = radio.value;
    sendToPreview("categoryPosition", position); // Send the selected category position to the preview
  });
});
```

### Step 3: Adjust CSS for Layout

You may want to add some CSS to style the grid and ensure it looks good. Here’s a simple example:

```css
#formatoOptions {
  margin-top: 10px;
}

.grid-opciones {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.grid-opciones button {
  background: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 10px;
  cursor: pointer;
  transition: background 0.2s;
}

.grid-opciones button:hover {
  background: #0056b3;
}

.categoria-options {
  margin-top: 10px;
}
```

### Step 4: Ensure Items are Distributed Evenly

To ensure that items are listed in 2 or 3 columns evenly distributed, you will need to adjust the CSS for the items in the preview area. You can use CSS Grid or Flexbox to achieve this. Here’s an example using CSS Grid:

```css
/* Example CSS for items in the preview area */
.items-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); /* Adjust as needed */
  gap: 10px;
}
```

### Summary

With these changes, you will have a single "formato" button that toggles a grid of options for different column formats and category placements. The selected options will be sent to the preview area, and the items will be displayed in the specified format. Adjust the CSS as needed to fit your design preferences.