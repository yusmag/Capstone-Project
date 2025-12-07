// Simple "fake" cart count handling
const cartCountEl = document.getElementById("cart-count");
const addButtons = document.querySelectorAll(".add-to-cart");
let cartCount = 0;

addButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
        cartCount++;
        cartCountEl.textContent = cartCount;
        const card = btn.closest(".product-card");
        const title = card.querySelector(".product-title").textContent.trim();
        alert(`Added "${title}" to cart.`);
    });
});

// Current year in footer
document.getElementById("year").textContent = new Date().getFullYear();