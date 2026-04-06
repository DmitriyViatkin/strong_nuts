(function ($) {
	'use strict';

	$(document).ready(function () {

		// ================= INIT =================
		if ($.Scrollax) {
			$.Scrollax();
		}

		// ================= LINKS =================
		// Отключаем переход по пустым ссылкам
		$(document).on('click', "a[href='#']", function (e) {
			e.preventDefault();
		});

		// ================= MOBILE MENU =================
		const $header = $('.top-header');
		if ($header.length && !$('.mobile-menu').length) {
			$header.before(`
				<div class="mobile-menu d-lg-none">
					<div class="row">
						<div class="col-12">
							<a href="/" class="logo">
								<img src="/static/img/logo.png" alt="logo">
								<span>Strong<br> Nuts</span>
							</a>
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

		// ================= DOM MOVES (Безопасные) =================
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

		// ================= COUNTER (ИСПРАВЛЕНО) =================
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
				const $target = $("." + val);
				$(".box").not($target).hide();
				$target.show();
			});
		}

		initRadioToggle('.radio__wrap');
		initRadioToggle('.radio__wrapper_click');

		$(document).on('click', '.radio__wrapper_click .radio-custom_last', function () {
			$(".box").hide();
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

		// ================= POPUP CART (ИСПРАВЛЕНО) =================
		// Делегирование события клика, чтобы работало после AJAX
	$(document).on('click', '.popup__cart', function (e) {
    e.stopPropagation();
});

		// ================= STICKY =================
		if (typeof Stickyfill !== 'undefined') {
			Stickyfill.add($('.sticky'));
		}

		// ================= LANG MENU =================
		const menuElem = document.getElementById('lang-menu');
		if (menuElem) {
			const titleElem = menuElem.querySelector('.title');
			document.addEventListener('click', function (event) {
				let target = event.target;
				while (target && target !== document) {
					if (target === menuElem) {
						if (event.target.tagName === 'A') {
							titleElem.innerHTML = event.target.textContent;
							titleElem.style.backgroundImage = getComputedStyle(event.target).backgroundImage;
						}
						menuElem.classList.toggle('open');
						return;
					}
					target = target.parentNode;
				}
				menuElem.classList.remove('open');
			});
		}

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
					920: { slidesPerView: 2 },
					578: { slidesPerView: 1 }
				}
			});
		}

		$('.swiper-container').hover(
			function () { if (this.swiper) this.swiper.autoplay.stop(); },
			function () { if (this.swiper) this.swiper.autoplay.start(); }
		);

		// ================= SELECT (ИСПРАВЛЕНО) =================
		$('select').each(function () {
			const $this = $(this);
			if ($this.hasClass('select-hidden')) return;

			const $styled = $('<div class="select-styled"></div>');
			const $list = $('<ul class="select-options"></ul>');

			$this.addClass('select-hidden').wrap('<div class="select"></div>').after($styled);
			$styled.text($this.find(':selected').text());

			$this.children('option').each(function () {
				$('<li />', {
					text: $(this).text(),
					rel: $(this).val()
				}).appendTo($list);
			});

			$styled.after($list);

			$styled.on('click', function (e) {
				e.stopPropagation();
				$('.select-styled.active').not(this).removeClass('active').next().hide();
				$(this).toggleClass('active').next().toggle();
			});

			$list.on('click', 'li', function () {
				$styled.text($(this).text()).removeClass('active');
				$this.val($(this).attr('rel')).trigger('change');
				$list.hide();
			});
		});

		$(document).on('click', function () {
			$('.select-styled').removeClass('active');
			$('.select-options').hide();
		});

		// ================= LOAD MORE =================
		const btnLoad = document.getElementById('load-more-btn');
		if (btnLoad) {
			btnLoad.addEventListener('click', function (e) {
				e.preventDefault();
				const page = parseInt(this.dataset.page);
				this.textContent = 'Загрузка...';

				fetch(`/api/products?page=${page}&per_page=6`)
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
						this.textContent = 'Показать еще';
					});
			});
		}

		function renderCard(p) {
			return `
				<div class="col-lg-4 col-md-6 col-12">
					<div class="production__item">
						<div class="production__item_title">${p.name}</div>
						<div class="production__item_descr">${p.summary || ''}</div>
						<div class="production__item_price">${p.price}</div>
					</div>
				</div>
			`;
		}

	}); // END READY

})(jQuery);

// ================= GOOGLE MAP =================
function initMap() {
	if (typeof google === 'undefined' || !document.getElementById('map')) return;
	const odessa = { lat: 46.4846, lng: 30.7326 };
	const map = new google.maps.Map(document.getElementById('map'), {
		zoom: 15,
		center: odessa
	});
	new google.maps.Marker({
		position: odessa,
		map: map
	});
}