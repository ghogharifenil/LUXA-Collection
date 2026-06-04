let qty = 1;
const price = parseInt(document.getElementById("price").value);

function updateTotal() {
    document.getElementById("qty").innerText = qty;
    document.getElementById("total").innerText = price * qty;
    document.getElementById("quantity_input").value = qty;
}

function increase() {
    qty++;
    updateTotal();
}

function decrease() {
    if (qty > 1) {
        qty--;
        updateTotal();
    }
}