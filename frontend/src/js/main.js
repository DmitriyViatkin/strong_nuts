// main.js — jQuery береться з window (підключений через CDN в base.html)

(function ($) {
	'use strict';

	$(document).ready(function () {

		// ================= INIT =================
		if ($.Scrollax) {
			$.Scrollax();
		}

		// ================= LINKS =================
		$(document).on('click', "a[href='#']", function (e) {
			e.preventDefault();
		});

		// ================= MOBILE MENU =================
		const $header = $('.top-header');
		if ($header.length && !$('.mobile-menu').length) {

			// Беремо логотип з вже відрендереного хедера
			const $existingLogo = $header.find('.logo').first();
			const logoHTML = $existingLogo.length
				? $existingLogo[0].outerHTML
				: `<a href="/" class="logo">
					<img src="${document.body.dataset.logoUrl || '/static/img/logo.png'}" alt="logo">
				   </a>`;

			$header.before(`
				<div class="mobile-menu d-lg-none">
					<div class="row">
						<div class="col-12">
							${logoHTML}
							<i class="nut-icon icons-close-button"></i>
						</div>
					</div>
				</div>
			`);

			$('.menu_top').first().clone().appendTo('.mobile-menu');
		}

		$(document).on('click', '.mobile-menu-button, .mobile-menu .icons-close-button', function () {
			$('.mobile-menu').stop().slideToggle();
			$('.top-header').toggleClass('d-none');
		});

		// ================= DOM MOVES =================
		if ($('.lang-menu').length) {
			$('.logo_tel_mobile, .logo_button_mobile').insertBefore('.lang-menu');
		}
		if ($('.mobile-line').length) {
			$('.line_social, .log_in').clone().appendTo('.mobile-line');
			$('.mobile-line ul.log_in').removeClass('d-none');
		}

		const $newsNext = $('.news-container .swiper-button-next');
		const $newsPrev = $('.news-container .swiper-button-prev');
		const $newsNav = $('.news .wrap .navigation');
		if ($newsNext.length && $newsNav.length) $newsNext.insertBefore($newsNav);
		if ($newsPrev.length && $newsNav.length) $newsPrev.insertBefore($newsNav);

		// ================= COUNTER =================
		const $timerBlock = $('.timer');
		if ($timerBlock.length) {
			$(window).on('scroll.counter', function () {
				const offset = $timerBlock.offset();
				if (offset && $(window).scrollTop() > offset.top - $(window).height() / 2) {
					if ($.fn.countTo) {
						$('.timer__single').countTo();
					}
					$(window).off('scroll.counter');
				}
			});
		}

		// ================= TABS =================
		$(document).on('click', 'ul.tabs__caption li:not(.active)', function () {
			$(this)
				.addClass('active').siblings().removeClass('active')
				.closest('.tabs')
				.find('.tabs__content')
				.removeClass('active')
				.eq($(this).index())
				.addClass('active');
		});

		// ================= RADIO =================
		function initRadioToggle(selector) {
			$(document).on('click', selector + ' input[type="radio"]', function () {
				const val = $(this).val();
				const $target = $('.' + val);
				$('.box').not($target).hide();
				$target.show();
			});
		}

		initRadioToggle('.radio__wrap');
		initRadioToggle('.radio__wrapper_click');

		$(document).on('click', '.radio__wrapper_click .radio-custom_last', function () {
			$('.box').hide();
		});

		// ================= TOOLTIP =================
		if ($.fn.tooltipster) {
			$('.tooltip').tooltipster({
				animation: 'fade',
				delay: 200,
				maxWidth: 106
			});
		}

		// ================= TABLE =================
		if ($.fn.basictable) {
			$('#table').basictable();
			$('#table-breakpoint').basictable({ breakpoint: 768 });
		}

		// ================= POPUP CART =================
		$(document).on('click', '.popup__cart', function (e) {
			e.stopPropagation();
		});

		// ================= STICKY =================
		if (typeof Stickyfill !== 'undefined') {
			Stickyfill.add($('.sticky'));
		}

		// ================= LANG MENU =================
		// Логіка в header.html — тут нічого не дублюємо

		// ================= SWIPERS =================
		if (document.querySelector('.news-container') && typeof Swiper !== 'undefined') {
			new Swiper('.news-container', {
				slidesPerView: 3,
				spaceBetween: 30,
				loop: true,
				navigation: {
					nextEl: '.swiper-button-next',
					prevEl: '.swiper-button-prev',
				},
				autoplay: {
					delay: 2500,
					disableOnInteraction: false,
				},
				breakpoints: {
					1024: { slidesPerView: 3 },
					920:  { slidesPerView: 2 },
					578:  { slidesPerView: 1 }
				}
			});
		}

		$('.swiper-container').hover(
			function () { if (this.swiper) this.swiper.autoplay.stop(); },
			function () { if (this.swiper) this.swiper.autoplay.start(); }
		);

		// ================= SELECTS WITH API =================
		const langPrefix = window.location.pathname.split('/')[1];
		const BASE_URL = '/' + langPrefix + '/products/api';

		const flavorSelect = document.querySelector('#flavor-select');
		const massSelect   = document.querySelector('#mass-select');

		if (flavorSelect && massSelect) {

			function loadMass(flavor) {
				const url = flavor
					? BASE_URL + '/mass/?flavor=' + encodeURIComponent(flavor)
					: BASE_URL + '/mass/';

				fetch(url)
					.then(res => res.json())
					.then(data => {
						massSelect.innerHTML = "<option value=''>Оберіть вагу</option>";
						data.mass.forEach(m => {
							const option = document.createElement('option');
							option.value = m;
							option.textContent = m + ' г.';
							massSelect.appendChild(option);
						});
						rebuildSelect(massSelect);
					})
					.catch(err => console.error('Mass error:', err));
			}

			fetch(BASE_URL + '/flavors/')
				.then(res => res.json())
				.then(data => {
					flavorSelect.innerHTML = "<option value='' selected>Оберіть смак</option>";
					data.flavors.forEach(flavor => {
						const option = document.createElement('option');
						option.value = flavor;
						option.textContent = flavor;
						flavorSelect.appendChild(option);
					});
					flavorSelect.value = '';
					rebuildSelect(flavorSelect);
					loadMass('');
				})
				.catch(err => console.error('Flavors error:', err));

			$(document).on('change', '#flavor-select', function () {
				loadMass(this.value);
			});

			// ================= PRICE SORT =================
			$(document).on('click', '#price-sort', function () {
				const current = $(this).data('order') || '';
				let next;
				if (current === '') {
					next = 'asc';
					$(this).find('span').text('Ціна ↑');
					$(this).find('i').css('transform', 'rotate(180deg)');
				} else if (current === 'asc') {
					next = 'desc';
					$(this).find('span').text('Ціна ↓');
					$(this).find('i').css('transform', 'rotate(0deg)');
				} else {
					next = '';
					$(this).find('span').text('За замовч.');
					$(this).find('i').css('transform', 'rotate(0deg)');
				}
				$(this).data('order', next);
			});

			// ================= FILTER BUTTON =================
			$(document).on('click', '.production__filter_button .button', function (e) {
				e.preventDefault();

				const flavor = $('#flavor-select').val();
				const mass   = $('#mass-select').val();
				const order  = $('#price-sort').data('order') || '';

				const params = new URLSearchParams();
				if (flavor) params.append('flavor', flavor);
				if (mass)   params.append('mass', mass);
				if (order)  params.append('order', order);

				fetch(BASE_URL + '/products/?' + params.toString())
					.then(res => res.json())
					.then(data => {
						const container = document.getElementById('products-container');
						if (!container) return;

						if (!data.products || !data.products.length) {
							container.innerHTML = '<p class="col-12">Товари не знайдено.</p>';
							return;
						}

						container.innerHTML = data.products.map(p => renderCard(p)).join('');

						container.querySelectorAll('.products-container').forEach(el => {
							new Swiper(el, {
								slidesPerView: 1,
								loop: true,
								navigation: {
									nextEl: el.querySelector('.swiper-button-next'),
									prevEl: el.querySelector('.swiper-button-prev'),
								},
								autoplay: { delay: 2500, disableOnInteraction: false }
							});
						});
					})
					.catch(err => console.error('Filter error:', err));
			});

			$(document).on('click', '.button_close', function (e) {
				e.preventDefault();
				location.reload();
			});

		} // END if (flavorSelect && massSelect)

		// ================= REBUILD SELECT =================
		function rebuildSelect(select) {
			const $select = $(select);

			$select.next('.select-styled').remove();
			$select.next('.select-options').remove();

			const $styled = $('<div class="select-styled"></div>');
			const $list   = $('<ul class="select-options"></ul>');

			$select.after($styled);
			$styled.text($select.find(':selected').text());

			$select.children('option').each(function () {
				$('<li />', {
					text: $(this).text(),
					rel:  $(this).val()
				}).appendTo($list);
			});

			$styled.after($list);

			$styled.on('click', function (e) {
				e.stopPropagation();
				$('.select-styled.active').not(this).removeClass('active').next().hide();
				$(this).toggleClass('active').next().toggle();
			});

			$list.on('click', 'li', function () {
				const $li = $(this);
				$styled.text($li.text()).removeClass('active');
				$select.val($li.attr('rel')).trigger('change');
				$list.hide();
			});

			$(document).off('click.customSelect').on('click.customSelect', function () {
				$('.select-styled').removeClass('active');
				$('.select-options').hide();
			});
		}

		// ================= RENDER CARD =================
		function renderCard(p) {
			const staticUrl = document.body.dataset.staticUrl || '/static/';
			const noImage   = staticUrl + 'img/no-image.png';
			const zoomIcon  = staticUrl + 'img/zoom.svg';

			const slides = p.images && p.images.length
				? p.images.map(url => `
					<div class="swiper-slide">
						<a href="#">
							<img src="${url}" alt="${p.name}"/>
						</a>
					</div>`).join('')
				: `<div class="swiper-slide">
						<a href="#">
							<img src="${noImage}" alt="${p.name}"/>
						</a>
					</div>`;

			const saleBlock = p.is_sale && p.old_price
				? `<div class="sum_item_old"><p>${p.old_price} <i>грн.</i></p></div>`
				: '';

			return `
				<div class="col-lg-4 col-md-6 col-12">
					<div class="wrap">
						<div class="production__item">
							<div class="products-container swiper-container">
								<div class="swiper-wrapper">
									${slides}
								</div>
								<div class="swiper-button-prev"></div>
								<div class="swiper-button-next"></div>
								<img class="zoom" src="${zoomIcon}" alt="">
							</div>
							<div class="wrap">
								<div class="production__item_title">${p.name}</div>
								<div class="production__item_art">
									<span>Арт:</span> ${p.articul || ''}
								</div>
								<div class="production__item_descr">${p.summary || ''}</div>
								<div class="production__item_weight">
									<div class="weight_item">
										<div class="weight_item_icon">
											<i class="nut-icon icons-food-scale-tool"></i>
										</div>
										<div class="weight_item_descr">
											<p>Вага</p>
											<p><span>${p.mass}<i>г.</i></span></p>
										</div>
									</div>
								</div>
								<div class="production__item_sum">
									<div class="sum_item">
										${saleBlock}
										<div class="sum_item_new">
											<p>${p.price} <i>грн.</i></p>
										</div>
									</div>
									<div class="sum_item">
										<div class="sum_item_button">
											<a href="#"
											   class="button add-to-cart-btn"
											   data-product-id="${p.id}">Купити</a>
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
			`;
		}

		// ================= LOAD MORE =================
		const btnLoad = document.getElementById('load-more-btn');
		if (btnLoad) {
			btnLoad.addEventListener('click', function (e) {
				e.preventDefault();
				const page = parseInt(this.dataset.page);
				this.textContent = 'Завантаження...';

				fetch('/api/products?page=' + page + '&per_page=6')
					.then(res => res.json())
					.then(products => {
						if (!products || !products.length) {
							this.style.display = 'none';
							return;
						}
						const container = document.getElementById('products-container');
						if (container) {
							products.forEach(p => {
								container.insertAdjacentHTML('beforeend', renderCard(p));
							});
						}
						this.dataset.page = page + 1;
						this.textContent = 'Завантажити ще';
					});
			});
		}

	}); // END READY

})(window.jQuery);


// ================= GOOGLE MAP =================
// ВАЖЛИВО: поза jQuery обгорткою, щоб Google Maps міг знайти функцію
window.initMap = function () {
	const el = document.getElementById('map');
	if (typeof google === 'undefined' || !el) return;

	const lat = parseFloat(el.dataset.lat);
	const lng = parseFloat(el.dataset.lng);

	if (isNaN(lat) || isNaN(lng)) return;

	const location = { lat, lng };
	const map = new google.maps.Map(el, { zoom: 15, center: location });
	new google.maps.Marker({ position: location, map });
};