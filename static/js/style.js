// ================= PROFILE DROPDOWN =================
function toggleProfileDropdown() {
  const dropdown = document.getElementById('profileDropdown');
  dropdown.style.display = (dropdown.style.display === "flex") ? "none" : "flex";
}

document.addEventListener('click', function (event) {
  const dropdown = document.getElementById('profileDropdown');
  const profileBtn = document.getElementById('profile-btn')?.parentElement;
  if (dropdown && profileBtn && !dropdown.contains(event.target) && !profileBtn.contains(event.target)) {
    dropdown.style.display = "none";
  }
});

document.addEventListener('DOMContentLoaded', function () {
  const dropdown = document.getElementById('profileDropdown');
  if (dropdown) {
    dropdown.onclick = function (event) {
      event.stopPropagation();
    };
  }

  // ================= PRODUCT CAROUSEL =================
  const carousel = document.getElementById('product-carousel');
  if (carousel) {
    const cardWidth = carousel.querySelector('.product-card').offsetWidth + 24;
    const totalCards = carousel.children.length;
    const visible = 4;
    let index = 0;

    function updateCarousel() {
      if (index < 0) index = 0;
      if (index > totalCards - visible) index = totalCards - visible;
      carousel.style.transform = `translateX(${-cardWidth * index}px)`;
    }

    document.getElementById('carousel-next').onclick = () => { if (index < totalCards - visible) { index++; updateCarousel(); } };
    document.getElementById('carousel-prev').onclick = () => { if (index > 0) { index--; updateCarousel(); } };
    updateCarousel();
  }

  // ================= BANNER SLIDER =================
  const slides = document.querySelectorAll(".slide");
  const dots = document.querySelectorAll(".dot");
  const prevBtn = document.querySelector(".prev");
  const nextBtn = document.querySelector(".next");
  const slidesContainer = document.querySelector(".slides");
  let currentIndex = 0;

  if (slidesContainer && slides.length > 0) {
    function showSlide(index) {
      if (index >= slides.length) index = 0;
      if (index < 0) index = slides.length - 1;
      currentIndex = index;
      slidesContainer.style.transform = `translateX(${-index * 100}%)`;
      dots.forEach(dot => dot.classList.remove("active"));
      if (dots[index]) dots[index].classList.add("active");
    }

    prevBtn?.addEventListener("click", () => showSlide(currentIndex - 1));
    nextBtn?.addEventListener("click", () => showSlide(currentIndex + 1));
    dots.forEach(dot => dot.addEventListener("click", (e) => showSlide(parseInt(e.target.dataset.index))));
    setInterval(() => showSlide(currentIndex + 1), 5000);
  }

  // ================= PACK SELECTION =================
  const packs = document.querySelectorAll('.pack');
  const defaultPack = document.querySelector('.pack.active');
  if (defaultPack) updateDetails(defaultPack);

  packs.forEach(function (pack) {
    pack.addEventListener('click', function () {
      packs.forEach(p => {
        p.classList.remove('active');
        p.querySelector('.pack-check')?.remove();
      });
      this.classList.add('active');
      const checkmark = document.createElement('span');
      checkmark.className = 'pack-check';
      checkmark.textContent = '✓';
      this.appendChild(checkmark);
      updateDetails(this);
    });
  });

  function updateDetails(pack) {
    document.getElementById('main-weight').textContent = pack.dataset.weight || '';
    document.getElementById('main-mrp').textContent = '₹' + (pack.dataset.mrp || '');
    document.getElementById('main-price').textContent = pack.dataset.price || '';
    document.getElementById('main-priceperg').textContent = `(₹${pack.dataset.priceperg || ''} / g)`;
    document.getElementById('main-discount').textContent = (pack.dataset.discount || '') + '% OFF';
  }

  // ================= SEARCH SUGGESTIONS =================
  const searchInput = document.getElementById("searchInput");
  const suggestionsBox = document.getElementById("searchSuggestions");

  if (searchInput) {
    searchInput.addEventListener("input", function () {
      const query = this.value.trim();
      if (query.length === 0) {
        suggestionsBox.style.display = "none";
        suggestionsBox.innerHTML = "";
        return;
      }

      fetch(`/products/search_suggest/?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
          suggestionsBox.innerHTML = "";
          if (data.results.length > 0) {
            const header = document.createElement("div");
            header.classList.add("suggestion-header");
            header.innerHTML = `Showing results for '<b>${data.query}</b>'`;
            suggestionsBox.appendChild(header);

            data.results.forEach(item => {
              const row = document.createElement("div");
              row.classList.add("suggestion-row");
              row.innerHTML = `
                <img src="${item.image}" alt="${item.name}" class="suggestion-img">
                <div style="flex:1;">
                  <div class="suggestion-name">${item.name}</div>
                  <div class="suggestion-weight">${item.weight || ""}</div>
                </div>
                <div class="suggestion-price">₹${item.price}</div>
                ${item.discount_percent ? `<div class="suggestion-discount">${item.discount_percent}% OFF</div>` : ""}
                <input type="number" value="1" min="1" class="suggestion-qty">
                <button class="suggestion-add" onclick="addToCart('${item.id}')">Add</button>
              `;
              suggestionsBox.appendChild(row);
            });
            suggestionsBox.style.display = "block";
          } else {
            suggestionsBox.style.display = "none";
          }
        })
        .catch(err => console.error("Search error:", err));
    });

    searchInput.addEventListener("keydown", function (e) {
      if (e.key === "Enter") {
        e.preventDefault();
        const query = this.value.trim();
        if (query.length > 0) {
          window.location.href = `/products/search/?q=${encodeURIComponent(query)}`;
        }
      }
    });

    document.addEventListener("click", (e) => {
      if (!searchInput.contains(e.target) && !suggestionsBox.contains(e.target)) {
        suggestionsBox.style.display = "none";
      }
    });
  }

  // ================= PROFILE TABS =================
  const tabButtons = document.querySelectorAll(".profile-tab-btn");
  const tabContents = document.querySelectorAll(".profile-tab-section");
  tabButtons.forEach(btn => {
    btn.addEventListener("click", function () {
      tabButtons.forEach(b => b.classList.remove("active"));
      this.classList.add("active");
      tabContents.forEach(content => content.classList.remove("active"));
      const tabId = this.getAttribute("data-tab");
      document.getElementById(tabId)?.classList.add("active");
    });
  });

  // ================= WISHLIST & CART =================
  const csrftoken = getCookie('csrftoken');

  document.querySelectorAll('.bookmark-btn').forEach(btn => {
    btn.addEventListener('click', function () {
      const productId = this.getAttribute('data-product-id');
      fetch(`/products/wishlist/add/${productId}/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrftoken, 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_id: productId }),
      })
      .then(resp => resp.json())
      .then(data => {
        if (data.status === 'success') alert('Added to wishlist!');
        else alert('Failed to add to wishlist');
      })
      .catch(() => alert('Error adding to wishlist'));
    });
  });
});

// ================= HELPERS =================
function scrollBasket(direction) {
  const container = document.getElementById('basketScroll');
  if (container) {
    const scrollAmount = container.offsetWidth;
    container.scrollBy({ left: scrollAmount * direction, behavior: 'smooth' });
  }
}

function changeImage(element) {
  const mainImage = document.getElementById("mainImage");
  if (mainImage) {
    mainImage.src = element.src;
    document.querySelectorAll(".thumbnails img").forEach(img => img.classList.remove("active"));
    element.classList.add("active");
  }
}

function toggleDiscountBlock() {
  const options = document.getElementById('discountOptions');
  const arrow = document.getElementById('discountArrow');
  if (!options || !arrow) return;
  const isHidden = options.style.display === 'none' || options.style.display === '';
  options.style.display = isHidden ? 'block' : 'none';
  arrow.textContent = isHidden ? '\u25B2' : '\u25BC';
}

function applyFilters() {
  let url = new URL(window.location.href);
  url.searchParams.delete('price');
  url.searchParams.delete('brand');
  url.searchParams.delete('discount');

  document.querySelectorAll('input[name="price"]:checked').forEach(el => url.searchParams.append('price', el.value));
  document.querySelectorAll('input[name="brand"]:checked').forEach(el => url.searchParams.append('brand', el.value));

  const discount = document.querySelector('input[name="discount"]:checked');
  if (discount) url.searchParams.set('discount', discount.value);

  const sortSelect = document.getElementById('sortSelect');
  if (sortSelect?.value) url.searchParams.set('sort', sortSelect.value);

  window.location.href = url.toString();
}

document.querySelectorAll('input[name="discount"]').forEach(radio => {
  radio.addEventListener('click', function () {
    if (this.previousChecked) {
      this.checked = false;
      this.previousChecked = false;
      applyFilters();
    } else {
      document.querySelectorAll('input[name="discount"]').forEach(r => r.previousChecked = false);
      this.previousChecked = true;
    }
  });
});

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}



// Helper to get CSRF token for AJAX POST
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


// cart code

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    document.cookie.split(';').forEach(function(cookie) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
      }
    });
  }
  return cookieValue;
}
const csrftoken = getCookie('csrftoken');

function updateCartQty(cartId, delta) {
  const qtyElem = document.getElementById('cart-qty-' + cartId);
  let qty = parseInt(qtyElem.innerText) + delta;
  qty = Math.max(1, qty);

  fetch(`/cart/update/${cartId}/`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrftoken},
    body: JSON.stringify({ quantity: qty })
  })
  .then(res => res.json())
  .then(data => {
    if (data.status === 'success') {
      qtyElem.innerText = data.quantity;
      document.getElementById('cart-item-subtotal-' + cartId).innerText = "₹ " + data.row_total.toFixed(2);
      document.querySelector('.cart-subtotal-bar strong').innerText = `Subtotal (${data.total_items} item${data.total_items > 1 ? 's' : ''}) : ₹ ${data.subtotal.toFixed(2)}`;
      document.querySelector('.cart-savings').innerText = `Savings: ₹ ${data.savings.toFixed(2)}`;
      location.reload();
    }
  });
}

function deleteCartItem(cartId) {
  if (!confirm("Remove this item from your cart?")) return;
  fetch(`/cart/delete/${cartId}/`, {
    method: 'POST',
    headers: {'X-CSRFToken': csrftoken}
  })
  .then(res => res.json())
  .then(data => {
    if (data.status === 'success') {
      document.querySelector(`.cart-product-card[data-cart-id="${cartId}"]`).remove();
      location.reload();
    }
  });
}

// document.querySelectorAll('.add-btn').forEach(btn => {
//   btn.addEventListener('click', function () {
//     const productId = this.getAttribute('data-product-id');
//     fetch(`/cart/add/${productId}/`, {
//       method: 'POST',
//       headers: {
//         'X-CSRFToken': getCookie('csrftoken'),
//         'Content-Type': 'application/json'
//       },
//       body: JSON.stringify({ quantity: 1 })
//     })
//     .then(res => res.json())
//     .then(data => {
//       if (data.status === 'success') {
//         document.querySelector('.cart-badge').textContent = data.cart_count;
//         console.log("count:",data.cart_count)
//         alert('Added to cart!');
//         location.reload();
//         // Optionally update cart icon/count
//       }
//     });
//   });
// });

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        document.cookie.split(';').forEach(function(cookie) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            }
        });
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.add-btn').forEach(function(btn) {
        btn.addEventListener('click', function () {
            const productId = btn.getAttribute('data-product-id');
            fetch(`/cart/add/${productId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ quantity: 1 })
            })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'success') {
                    location.reload()
                    alert('Added to cart!');
                    
                    // Optionally, update cart icon/count or redirect
                } else {
                    alert('Failed to add to cart.');
                }
            })
            .catch(() => alert('Error adding to cart.'));
        });
    });
});


function switchProfileEdit(showEdit) {
  document.getElementById('profile-display').style.display = showEdit ? 'none' : '';
  document.getElementById('profile-edit-section').style.display = showEdit ? '' : 'none';
}

// Optional: Automatically return to display mode after form submit (AJAX version)
// For classic POST/redirect, not needed.


document.addEventListener('DOMContentLoaded', function () {
  const menuBtns = document.querySelectorAll('.profile-menu-btn');
  const tabSections = document.querySelectorAll('.account-tab-content');
  menuBtns.forEach(btn => {
    btn.addEventListener('click', function () {
      menuBtns.forEach(b => b.classList.remove('active'));
      tabSections.forEach(sec => sec.classList.remove('active'));
      btn.classList.add('active');
      const tabId = btn.getAttribute('data-tab');
      document.getElementById(tabId).classList.add('active');
    });
  });
});


function showEditProfile() {
  document.getElementById('profile-view').style.display = 'none';
  document.getElementById('profile-edit').style.display = 'block';
}

function hideEditProfile() {
  document.getElementById('profile-edit').style.display = 'none';
  document.getElementById('profile-view').style.display = 'block';
}

///////
document.getElementById('changeAddressBtn').onclick = function() {
    document.querySelector('.address-summary-box').style.display = 'none';
    document.getElementById('addressSelectionBox').style.display = '';
};
function showAddAddressForm() {
    document.getElementById('addAddressForm').style.display = '';
}


document.getElementById("buy").addEventListener("click", async () => {
  const resp = await fetch("/payments/checkout/", {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({
      amount: 49900,          // amount in paise
      currency: "inr",
      name: "Wireless Headphones",
      reference: "ORD123"
    })
  });
  const data = await resp.json();
  if (data.checkout_url) {
    window.location.href = data.checkout_url;
  } else {
    alert(data.error || "Unable to start checkout");
  }
});


// WHISLIST DELETION WHEN ADDED TO CART
// function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         const cookies = document.cookie.split(';');
//         for (let i = 0; i < cookies.length; i++) {
//             const cookie = cookies[i].trim();
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }


// document.querySelectorAll(".move-to-cart-btn").forEach(btn => {
//     btn.addEventListener("click", function() {
//         let productId = this.dataset.id;
//         fetch(`/wishlist/move-to-cart/${productId}/`, {   // ✅ your correct URL
//             method: "POST",
//             headers: {
//                 "X-CSRFToken": csrftoken,
//                 "Content-Type": "application/json"
//             },
//             body: JSON.stringify({product_id: productId})
//         })
//         .then(res => res.json())
//         .then(data => {
//             if (data.status === "success") {
//                 // remove item without full reload
//                 this.closest(".wishlist-item").remove();
//             } else {
//                 alert("Failed: " + data.message);
//             }
//         })
//         .catch(err => console.error("Error:", err));
//     });
// });

// shopbycatcode
// style.js

function showDropBox() {
    const dropdown = document.getElementById("shopDropdown");
    dropdown.classList.toggle("show"); // toggle CSS class
}

// Optional: close dropdown if clicked outside
window.addEventListener("click", function(event) {
    if (!event.target.closest("#shopDropdown")) {
        document.getElementById("shopDropdown").classList.remove("show");
    }
});
// console.log("debug mode");

// const dropdown = document.getElementById("shopDropdown");
// const btn = document.getElementById("shopDropdownBtn");
// const panel = document.getElementById("shopDropdownPanel");

// console.log("btn:", btn, "panel:", panel);

// // Toggle dropdown on button click
// if (btn && panel) {
//   btn.addEventListener("click", function (e) {
//     console.log("clicked on shopby");
//     e.stopPropagation();
//     panel.style.display = panel.style.display === "block" ? "none" : "block";
//   });
// }

// // Close dropdown on outside click
// document.addEventListener("click", function (e) {
//   if (!dropdown.contains(e.target)) {
//     panel.style.display = "none";
//   }
// });

// // Hover for sub-panels
// document.querySelectorAll(".shop-main-item").forEach(main => {
//   main.addEventListener("mouseover", () => {
//     const sub = main.querySelector(".shop-sub-panel");
//     if (sub) sub.style.display = "block";
//   });
//   main.addEventListener("mouseout", () => {
//     const sub = main.querySelector(".shop-sub-panel");
//     if (sub) sub.style.display = "none";
//   });
// });

// document.querySelectorAll(".shop-sub-item").forEach(sub => {
//   sub.addEventListener("mouseover", () => {
//     const subsub = sub.querySelector(".shop-sub-sub-panel");
//     if (subsub) subsub.style.display = "block";
//   });
//   sub.addEventListener("mouseout", () => {
//     const subsub = sub.querySelector(".shop-sub-sub-panel");
//     if (subsub) subsub.style.display = "none";
//   });
// });


// ================= REMOVE FROM WISHLIST =================
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".remove-wishlist-btn").forEach(btn => {
    btn.addEventListener("click", function () {
      const itemId = this.dataset.id;   // data-id="{{ item.id }}" in template
      if (!confirm("Remove this item from your wishlist?")) return;

      fetch(`/wishlist/remove/${itemId}/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrftoken,
          "Content-Type": "application/json"
        }
      })
      .then(res => res.json())
      .then(data => {
        if (data.status === "success") {
          // remove wishlist item from DOM
          document.getElementById(`wishlist-item-${itemId}`).remove();

          // optionally update wishlist count in navbar
          const countElem = document.querySelector(".wishlist-badge");
          if (countElem && data.wishlist_count !== undefined) {
            countElem.textContent = data.wishlist_count;
          }
        } else {
          alert("Failed to remove from wishlist.");
        }
      })
      .catch(() => alert("Error removing wishlist item."));
    });
  });
});




