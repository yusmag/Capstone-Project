// Use relative URL if the page is served by the same Flask app
const API_URL = "/products_list";

const COLOUR_MAP = {
  "Carbon Fiber": "#111827",
  "White": "#ffffff",
  "Blue": "#3b82f6",
  "Red": "#ef4444",
  "Orange": "#f97316",
  "Teal": "#14b8a6",
  "Black": "#000000"
};

function normaliseImagePath(path) {
  if (!path) {
    return "https://via.placeholder.com/400x500?text=No+Image";
  }
  if (path.startsWith("http://") || path.startsWith("https://")) return path;
  if (!path.startsWith("/")) return "/" + path;
  return path; // e.g. "/assets/Boards/..."
}

async function loadProducts() {
  try {
    const res = await fetch(API_URL);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);

    const data = await res.json();
    const grouped = groupByProductName(data);

    renderProducts(grouped);
  } catch (err) {
    console.error("Failed to load products:", err);
    const grid = document.getElementById("product-grid");
    if (grid) {
      grid.innerHTML = `
        <p style="color:#b91c1c; padding:1rem; background:#fee2e2; border-radius:0.5rem;">
          Could not load products from <code>${API_URL}</code>. Is the Flask server running?
        </p>`;
    }
  }
}

// 1 card = 1 product_name, with multiple variants (each variant = different colour/image)
function groupByProductName(products) {
  const map = {};

  products.forEach((p) => {
    const key = p.product_name;
    if (!map[key]) {
      map[key] = {
        base: p,
        variants: [] // full variant objects (colour + image + id)
      };
    }
    map[key].variants.push({
      id: p.id,
      colour: p.colour,
      image: p.image,
      traction_colour: p.traction_colour
    });
  });

  return Object.values(map).map((entry) => {
    const base = entry.base;
    const coloursSet = new Set();
    entry.variants.forEach((v) => {
      if (v.colour) coloursSet.add(v.colour);
    });

    return {
      id: base.id,
      name: base.product_name,
      brand: base.brand,
      category: base.category,
      price: base.price,
      size: base.size,
      shape: base.shape,
      image: base.image,            // default image (we will override with first variant if present)
      traction_colour: base.traction_colour,
      variants: entry.variants,     // [{id, colour, image, traction_colour}, ...]
      colours: Array.from(coloursSet)
    };
  });
}

function renderProducts(products) {
  const grid = document.getElementById("product-grid");
  if (!grid) return;

  grid.innerHTML = "";

  const countEl = document.getElementById("product-count");
  if (countEl) countEl.textContent = products.length;

  products.forEach((product) => {
    const {
      id,
      name,
      brand,
      price,
      size,
      shape,
      traction_colour,
      image,
      variants,
      colours
    } = product;

    // Default image: first variant image if available, else base image
    const defaultVariantImage =
      (variants && variants[0] && variants[0].image) || image;
    const defaultImageUrl = normaliseImagePath(defaultVariantImage);

    const card = document.createElement("article");
    card.className = "product-card";
    card.dataset.productId = id;

    // Build HTML
    card.innerHTML = `
      <div class="image-wrapper">
        <img class="product-image" src="${defaultImageUrl}" alt="${name}">
        <button
          class="add-to-cart"
          type="button"
          aria-label="Add ${name} to cart"
        >
          🛒
        </button>
      </div>

      <div class="card-body">
        <h2 class="product-title">${name}</h2>

        <div class="product-meta">
          <span class="product-price">$${Number(price).toFixed(2)}</span>
          <span class="product-tagline">
            ${brand ? brand + " · " : ""}${shape || ""}${size ? ` · ${size}&quot;` : ""}
          </span>
        </div>

        <div class="colour-row">
          <span class="colour-label">Colours</span>
          <div class="colour-dots">
            ${
              colours && colours.length
                ? colours.map((c, index) =>
                    colourDotHtml(
                      c,
                      variants.find((v) => v.colour === c),
                      index === 0 // first colour = active by default
                    )
                  ).join("")
                : `<span class="colour-none">N/A</span>`
            }
          </div>
        </div>

        <div class="traction-row">
          <span class="colour-label">Traction</span>
          <span class="traction-text">${traction_colour || "varies"}</span>
        </div>
      </div>
    `;

    grid.appendChild(card);
  });

  attachCartHandlers();
  attachColourChipHandlers();
}

function colourDotHtml(colourName, variant, isActive) {
  const baseColor = COLOUR_MAP[colourName] || "#9ca3af";
  const imagePath = variant ? normaliseImagePath(variant.image) : "";

  return `
    <span
      class="colour-dot ${isActive ? "active" : ""}"
      title="${colourName}"
      data-colour="${colourName}"
      data-image="${imagePath}"
      style="background:${baseColor};"
    ></span>
  `;
}

function attachCartHandlers() {
  const cartCountEl = document.getElementById("cart-count");
  let cartCount = Number(cartCountEl?.textContent || 0);

  document.querySelectorAll(".add-to-cart").forEach((btn) => {
    btn.addEventListener("click", () => {
      const card = btn.closest(".product-card");
      const title = card.querySelector(".product-title").textContent.trim();

      cartCount++;
      if (cartCountEl) cartCountEl.textContent = cartCount;

      alert(`Added "${title}" to cart.`);
      // Optional: POST to /cart with product & colour, etc.
    });
  });
}

function attachColourChipHandlers() {
  document.querySelectorAll(".colour-dot").forEach((dot) => {
    dot.addEventListener("click", () => {
      const newImage = dot.dataset.image;
      if (!newImage) return;

      const card = dot.closest(".product-card");
      if (!card) return;

      const img = card.querySelector(".product-image");
      if (!img) return;

      // Change the main image
      img.src = newImage;

      // Update active state on chips within this card
      const siblings = card.querySelectorAll(".colour-dot");
      siblings.forEach((s) => s.classList.remove("active"));
      dot.classList.add("active");
    });
  });
}

document.addEventListener("DOMContentLoaded", loadProducts);
