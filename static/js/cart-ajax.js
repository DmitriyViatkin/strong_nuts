(function() {
    const urls = document.getElementById('cart-urls');
    if (!urls) return;

    const URL_DETAIL = urls.dataset.detail;
    const URL_UPDATE = urls.dataset.update;
    const URL_REMOVE = urls.dataset.remove;

    const popup = document.querySelector('.popup__cart');

    function openCart() {
        if (popup) popup.style.display = 'block';
    }

    function closeCart() {
        if (popup) popup.style.display = 'none';
    }

    function loadCart() {
        fetch(URL_DETAIL)
            .then(r => r.json())
            .then(data => {
                const totalEl = document.getElementById('cart-popup-total');
                if (totalEl) totalEl.textContent = data.total;

                const counter = document.querySelector('.cart-count');
                if (counter) counter.textContent = data.total_quantity;

                const container = document.getElementById('cart-popup-items');
                if (!container) return;

                container.innerHTML = '';

                if (data.items.length === 0) {
                    container.innerHTML = '<p style="padding:10px">Кошик порожній</p>';
                    return;
                }

                data.items.forEach(item => {
                    container.innerHTML += `
                        <div class="popup__cart_item">
                            <div class="row align-items-center no-gutters item_row">
                                <div class="col-md-5 col-12">
                                    <div class="item_title"><p>${item.name}</p></div>
                                </div>
                                <div class="col-md-7 col-12">
                                    <div class="row align-items-center no-gutters">
                                        <div class="col-6">
                                            <div class="item_quantity">
                                                <button type="button" class="quantity_minus" data-id="${item.product_id}">
                                                    -
                                                </button>
                                                <input type="text" value="${item.quantity}" class="quantity_input" data-id="${item.product_id}">
                                                <button type="button" class="quantity_plus" data-id="${item.product_id}">
                                                    +
                                                </button>
                                            </div>
                                        </div>
                                        <div class="col-5">
                                            <div class="item_sum">
                                                <p>${item.total} <span>грн.</span></p>
                                            </div>
                                        </div>
                                        <div class="col-1">
                                            <div class="item_close">
                                                <a href="#" class="remove-item" data-id="${item.product_id}">✕</a>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>`;
                });

                // события
                container.querySelectorAll('.quantity_plus').forEach(btn => {
                    btn.addEventListener('click', () => changeQty(btn.dataset.id, 1));
                });

                container.querySelectorAll('.quantity_minus').forEach(btn => {
                    btn.addEventListener('click', () => changeQty(btn.dataset.id, -1));
                });

                container.querySelectorAll('.remove-item').forEach(btn => {
                    btn.addEventListener('click', (e) => {
                        e.preventDefault();
                        removeItem(btn.dataset.id);
                    });
                });
            })
            .catch(err => console.error('Cart error:', err));
    }

    // 🔥 КЛИК ПО КОРЗИНЕ
    $(document).on('click', '.logo_number', function(e) {
        e.preventDefault();
        openCart();
        loadCart();
    });

    // 🔥 Закрытие при клике вне корзины
    document.addEventListener('click', function(e) {
        if (!popup) return;

        const isClickInside = popup.contains(e.target);
        const isButton = e.target.closest('.logo_number');

        if (!isClickInside && !isButton) {
            closeCart();
        }
    });

    function changeQty(productId, delta) {
        const input = document.querySelector(`.quantity_input[data-id="${productId}"]`);
        if (!input) return;

        const newQty = Math.max(1, parseInt(input.value) + delta);

        fetch(URL_UPDATE, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                product_id: productId,
                quantity: newQty
            })
        }).then(() => loadCart());
    }

    function removeItem(productId) {
        fetch(URL_REMOVE, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ product_id: productId })
        }).then(() => loadCart());
    }

    function getCookie(name) {
        const val = document.cookie.split('; ')
            .find(r => r.startsWith(name + '='));
        return val ? val.split('=')[1] : '';
    }

    window.refreshCartPopup = loadCart;
    // ✅ Автообновление при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    loadCart();
});
})();