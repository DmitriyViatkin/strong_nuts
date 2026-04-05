(function ($) {
	'use strict';

	// ================= INIT =================
	$(document).ready(function () {

		// Scrollax
		if ($.Scrollax) {
			$.Scrollax();
		}

		// ================= LINKS =================
		$("a[href='#']").on('click', function (e) {
			e.preventDefault();
		});

		// ================= MOBILE MENU =================
		$('.top-header').before(`
			<div class="mobile-menu d-lg-none">
				<div class="row">
					<div class="col-12">
						<a href="/" class="logo">
							<img src="img/logo.png" alt="logo">
							<span>Твій<br> бренд</span>
						</a>
						<i class="nut-icon icons-close-button"></i>
					</div>
				</div>
			</div>
		`);

		$('.menu_top').clone().appendTo('.mobile-menu');

		$('.mobile-menu-button, .mobile-menu .icons-close-button').on('click', function () {
			$('.mobile-menu').stop().slideToggle();
			$('.top-header').toggleClass('d-none');
		});

		// ================= DOM MOVES =================
		$('.logo_tel_mobile, .logo_button_mobile').insertBefore('.lang-menu');
		$('.line_social, .log_in').clone().appendTo('.mobile-line');
		$('.mobile-line ul.log_in').removeClass('d-none');

		$('.news-container .swiper-button-next').insertBefore('.news .wrap .navigation');
		$('.news-container .swiper-button-prev').insertBefore('.news .wrap .navigation');

		// ================= COUNTER =================
		var blockScrolled = $('.timer');

		if (blockScrolled.length) {
			$(window).on('scroll.counter', function () {
				if ($(window).scrollTop() > blockScrolled.offset().top - $(window).height() / 2) {
					if ($.fn.countTo) {
						$('.timer__single').countTo();
					}
					$(window).off('scroll.counter');
				}
			});
		}

		// ================= TABS =================
		$('ul.tabs__caption').on('click', 'li:not(.active)', function () {
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
			$(selector + ' input[type="radio"]').on('click', function () {
				var val = $(this).val();
				var target = $("." + val);
				$(".box").not(target).hide();
				target.show();
			});
		}

		initRadioToggle('.radio__wrap');
		initRadioToggle('.radio__wrapper_click');

		$('.radio__wrapper_click .radio-custom_last').on('click', function () {
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

		// ================= POPUP CART =================
		$('.logo_number').on('click', function () {
			$('.popup__cart').stop().slideToggle();
		});

		$(document).on('mouseup', function (e) {
			var div = $(".popup__cart");
			if (!div.is(e.target) && div.has(e.target).length === 0) {
				div.slideUp();
			}
		});

		// ================= STICKY =================
		if (typeof Stickyfill !== 'undefined') {
			Stickyfill.add($('.sticky'));
		}

		// ================= LANG MENU =================
		var menuElem = document.getElementById('lang-menu');

		if (menuElem) {
			var titleElem = menuElem.querySelector('.title');

			document.addEventListener('click', function (event) {
				var target = event.target;

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
		function initSwiper(selector, options) {
			if (document.querySelector(selector)) {
				return new Swiper(selector, options);
			}
		}

		initSwiper('.news-container', {
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

		// FIX hover
		$('.swiper-container').hover(
			function () {
				if (this.swiper) this.swiper.autoplay.stop();
			},
			function () {
				if (this.swiper) this.swiper.autoplay.start();
			}
		);

		// ================= SELECT =================
		$('select').each(function () {
			var $this = $(this);
			var $styled = $('<div class="select-styled"></div>');
			var $list = $('<ul class="select-options"></ul>');

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
				$this.val($(this).attr('rel'));
				$list.hide();
			});

			$(document).on('click', function () {
				$styled.removeClass('active');
				$list.hide();
			});
		});

		// ================= LOAD MORE =================
		var btn = document.getElementById('load-more-btn');

		if (btn) {
			btn.addEventListener('click', function (e) {
				e.preventDefault();

				var page = parseInt(this.dataset.page);
				this.textContent = 'Загрузка...';

				fetch(`/api/products?page=${page}&per_page=6`)
					.then(res => res.json())
					.then(products => {
						if (!products.length) return;

						var container = document.getElementById('products-container');

						products.forEach(p => {
							container.insertAdjacentHTML('beforeend', renderCard(p));
						});

						this.dataset.page = page + 1;
						this.textContent = 'Загрузить ещё';
					});
			});
		}

		function renderCard(p) {
			return `
				<div class="col-lg-4 col-md-6 col-12">
					<div class="production__item">
						<div class="production__item_title">${p.name}</div>
						<div class="production__item_descr">${p.summary}</div>
						<div class="production__item_price">${p.price}</div>
					</div>
				</div>
			`;
		}

	}); // END READY

})(jQuery);


// ================= GOOGLE MAP =================
function initMap() {
	if (typeof google === 'undefined') return;

	var odessa = { lat: 46.4846, lng: 30.7326 };

	var map = new google.maps.Map(document.getElementById('map'), {
		zoom: 15,
		center: odessa
	});

	new google.maps.Marker({
		position: odessa,
		map: map
	});
}