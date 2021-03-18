let ingredientsContainer = document.getElementById("ingredients-container");

//Remove ingredient row function
function removeIng() {
    //Remove the last child in line unless its first child
    //ingredientsContainer.childNodes actually has one extra text field. For that reason we need to increment the number in the condition of while loop.
    if (ingredientsContainer.childNodes.length > 2) {
        ingredientsContainer.removeChild(ingredientsContainer.lastChild);
    }
}

//Add ingredient row function
function addIng() {
    let newRow = document.createElement("div");
    newRow.className = "row";

    let newIngredient = document.createElement("div");
        newIngredient.className = "input-field col s12 m4";
        newIngredient.innerHTML = `
                <input id="ingredient_name" name="ingredient_name" type="text" class="validate" pattern="^[a-zA-Z][a-zA-Z\\s']+$" title="The ingredient name can only contain alphabetic characters, apostrophe and whitespace. The ingredient name can only start with a alphabetic character" required>
                <label for="ingredient_name">Name</label>`;

    let newQuantity = document.createElement("div");
        newQuantity.className = "input-field col s12 m4";
        newQuantity.innerHTML = `
                <input id="quantity" name="quantity" type="text" class="validate" pattern="\\d+" title="Please enter a number" required>
                <label for="quantity">Quantity</label>`;

    let newUnit = document.createElement("div");
        newUnit.className = "input-field col s12 m4";
        newUnit.innerHTML = `
                <select id="unit" name="unit" class="browser-default unit-select" required>
                    <option value="" disabled selected>Units</option>
                    <option value="Ml">Ml</option>
                    <option value="Litre">Litre</option>
                    <option value="Ounce">Ounce</option>
                    <option value="Gram">Gram</option>
                    <option value="Teaspoon">Teaspoon</option>
                    <option value="Tablespoon">Tablespoon</option>
                    <option value="Pinch">Pinch</option>
                    <option value="None">None</option>
                </select>
                <label for="Unit"></label>`

        //Append columns to row
        newRow.appendChild(newIngredient);
        newRow.appendChild(newQuantity);
        newRow.appendChild(newUnit);
        //Append row to container
        ingredientsContainer.appendChild(newRow);
}
