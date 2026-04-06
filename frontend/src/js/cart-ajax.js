(function() {
    const urls = document.getElementById('cart-urls');
    if (!urls) return;

    const URL_DETAIL = urls.dataset.detail;
    const URL_UPDATE = urls.dataset.update;
    const URL_REMOVE = urls.dataset.remove;

    function loadCart() {
        fetch(URL_DETAIL)
            .then(r => r.json())
            .then(data => {
                // Обновляем общую сумму
                const totalEl = document.getElementById('cart-popup-total');
                if (totalEl) totalEl.textContent = data.total;

                // Обновляем счетчик в хедере
                const counter = document.querySelector('.cart-count');
                if (counter) counter.textContent = data.total_quantity;

                const container = document.getElementById('cart-popup-items');
                if (!container) return;

                if (!data.items || data.items.length === 0) {
                    container.innerHTML = '<p style="padding:20px; text-align:center;">Корзина пуста</p>';
                    return;
                }

                // Оптимизация: собираем HTML в одну переменную
                let itemsHtml = '';
                data.items.forEach(item => {
                    itemsHtml += `
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
                                                    <i class="nut-icon icons-qty-left"></i>
                                                </button>
                                                <input type="text" value="${item.quantity}" class="quantity_input" data-id="${item.product_id}">
                                                <button type="button" class="quantity_plus" data-id="${item.product_id}">
                                                    <i class="nut-icon icons-qty-right"></i>
                                                </button>
                                            </div>
                                        </div>
                                        <div class="col-5">
                                            <div class="item_sum"><p>${item.total} <span>грн.</span></p></div>
                                        </div>
                                        <div class="col-1">
                                            <div class="item_close">
                                                <a href="#" class="remove-item" data-id="${item.product_id}">
                                                    <i class="nut-icon icons-close-button"></i>
                                                </a>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>`;
                });

                container.innerHTML = itemsHtml;

                // Навешиваем события (делегирование внутри контейнера)
                attachEvents(container);
            })
            .catch(err => console.error('Cart error:', err));
    }

    function attachEvents(container) {
        container.querySelectorAll('.quantity_plus').forEach(btn => {
            btn.onclick = () => changeQty(btn.dataset.id, 1);
        });
        container.querySelectorAll('.quantity_minus').forEach(btn => {
            btn.onclick = () => changeQty(btn.dataset.id, -1);
        });
        container.querySelectorAll('.remove-item').forEach(btn => {
            btn.onclick = (e) => {
                e.preventDefault();
                removeItem(btn.dataset.id);
            };
        });
        // Добавляем обработку ручного ввода
        container.querySelectorAll('.quantity_input').forEach(input => {
            input.onchange = () => {
                let val = parseInt(input.value);
                if (isNaN(val) || val < 1) val = 1;
                updateQtyRequest(input.dataset.id, val);
            };
        });
    }

    // Слушаем клик по корзине для загрузки данных
    $(document).on('click', '.logo_number', function() {
        loadCart();
    });

    function changeQty(productId, delta) {
        const input = document.querySelector(`.quantity_input[data-id="${productId}"]`);
        if (!input) return;
        const newQty = Math.max(1, parseInt(input.value) + delta);
        updateQtyRequest(productId, newQty);
    }

    function updateQtyRequest(productId, quantity) {
        fetch(URL_UPDATE, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({product_id: productId, quantity: quantity})
        }).then(r => {
            if (r.ok) loadCart();
        });
    }

    function removeItem(productId) {
        fetch(URL_REMOVE, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({product_id: productId})
        }).then(r => {
            if (r.ok) loadCart();
        });
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    window.refreshCartPopup = loadCart;
})();