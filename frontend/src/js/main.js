// инициализируем параллакс
jQuery(document).ready(function($){
  'use strict';
  $.Scrollax();
});

// функция гугл карты
function initMap() {
	var odessa = {lat: 46.484600, lng: 30.732600};
	var map = new google.maps.Map(document.getElementById('map'), {
		zoom: 15,
		center: odessa,
		styles: [
			{
				"featureType": "road",
				"elementType": "geometry",
				"stylers": [{"lightness": 100}, {"visibility": "simplified"}]
			},
			{
				"featureType": "water",
				"elementType": "geometry",
				"stylers": [{"visibility": "on"}, {"color": "#C6E2FF"}]
			},
			{
				"featureType": "poi",
				"elementType": "geometry.fill",
				"stylers": [{"color": "#C5E3BF"}]
			},
			{
				"featureType": "road",
				"elementType": "geometry.fill",
				"stylers": [{"color": "#D1D1B8"}]
			}
		]
	});
	var marker = new google.maps.Marker({
		position: odessa,
		map: map,
		icon: 'img/marker.svg'
	});
}

(function ($) {

	// :: PreventDefault a Click
	$("a[href='#']").on('click', function ($) {
		$.preventDefault();
	});

	// создаем html под мобильное меню
	$('.top-header').before('<div class="mobile-menu d-lg-none"><div class="row"><div class="col-12"><a href="/" class="logo"><img src="img/logo.png" alt="alt"><span>ОРЕХ<br> ПРИЧЕРНОМОРЬЯ</span></a><i class="nut-icon icons-close-button">');

	// клонируем меню
	$('.menu_top').clone().appendTo('.mobile-menu');

	// показать/скрыть меню
	$('.mobile-menu-button, .mobile-menu .icons-close-button').click(function() {
		$('.mobile-menu').stop().slideToggle();
		$('.top-header').toggleClass('d-none');
	});

	// наполняем блок с меню другими элементами
	$('.logo_tel_mobile').insertBefore('.lang-menu');
	$('.logo_button_mobile').insertBefore('.lang-menu');
	$('.line_social').clone().appendTo('.mobile-line');
	$('.log_in').clone().appendTo('.mobile-line');
	$('.mobile-line ul.log_in').removeClass('d-none');

	// переносим навигацию слайдера
	$('.news-container .swiper-button-next').insertBefore('.news .wrap .navigation');
	$('.news-container .swiper-button-prev').insertBefore('.news .wrap .navigation');

	// инициализация таймера при скролле к блоку
	var blockScrolled = $('.timer');

	$(window).on('scroll', function () {
		if ( $(window).scrollTop() > blockScrolled.offset().top - $(window).height() / 2 ) {
			$('.timer__single').countTo();
			$(window).off('scroll');
		}
	});

	// tabs
	$('ul.tabs__caption').on('click', 'li:not(.active)', function() {
		$(this)
			.addClass('active').siblings().removeClass('active')
			.closest('div.tabs').find('div.tabs__content').removeClass('active').eq($(this).index()).addClass('active');
	});

	// В зависимости от выбранной радио кнопки показ блока
	$(document).ready(function(){
		$('.radio__wrap input[type="radio"]').click(function(){
			var inputValue = $(this).attr("value");
			var targetBox = $("." + inputValue);
			$(".box").not(targetBox).hide();
			$(targetBox).show();
		});
	});

	$(document).ready(function(){
		$('.radio__wrapper_click input[type="radio"]').click(function(){
			var inputValue = $(this).attr("value");
			var targetBox = $("." + inputValue);
			$(".box").not(targetBox).hide();
			$(targetBox).show();
		});

		$('.radio__wrapper_click .radio-custom_last').click(function(){
			$(".box").css('display', 'none');
		});
	});

	// tooltip
	$('.tooltip').tooltipster({
		animation: 'fade',
		delay: 200,
		maxWidth: 106
	});

	// tables responsive
	$('#table').basictable();
	$('#table-breakpoint').basictable({ breakpoint: 768 });
	$('#table-container-breakpoint').basictable({ containerBreakpoint: 485 });
	$('#table-swap-axis').basictable({ swapAxis: true });
	$('#table-force-off').basictable({ forceResponsive: false });
	$('#table-no-resize').basictable({ noResize: true });
	$('#table-two-axis').basictable();
	$('#table-max-height').basictable({ tableWrapper: true });

	// окно корзины
	$('.logo_number').click(function() {
		$('.popup__cart').stop().slideToggle('swing');
	});

	$(document).mouseup(function (e){
		var div = $(".popup__cart");
		if (!div.is(e.target) && div.has(e.target).length === 0) {
			div.slideUp();
		}
	});

	// fixed sidebar
	var elements = $('.sticky');
	Stickyfill.add(elements);

	// выпадающий список выбора языков
	var menuElem = document.getElementById('lang-menu'),
		titleElem = menuElem.querySelector('.title');
	document.onclick = function(event) {
		var target = elem = event.target;
		while (target != this) {
			if (target == menuElem) {
				if (elem.tagName == 'A') {
					titleElem.innerHTML = elem.textContent;
					titleElem.style.backgroundImage = getComputedStyle(elem, null)['backgroundImage'];
				}
				menuElem.classList.toggle('open');
				return;
			}
			target = target.parentNode;
		}
		menuElem.classList.remove('open');
	};

	// swiper — новости
	var swiper = new Swiper('.news-container', {
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
			1024: { slidesPerView: 3, spaceBetween: 30 },
			920:  { slidesPerView: 2, spaceBetween: 30 },
			578:  { slidesPerView: 1, spaceBetween: 10 }
		}
	});

	$(".swiper-container").hover(function() {
		(this).swiper.autoplay.stop();
	}, function() {
		(this).swiper.autoplay.start();
	});

	// swiper — производитель
	var swiperManufacturer = new Swiper('.manufacturer-container', {
		slidesPerView: 1,
		spaceBetween: 30,
		loop: true,
		speed: 400,
		navigation: {
			nextEl: '.swiper-button-next',
			prevEl: '.swiper-button-prev',
		},
		autoplay: {
			delay: 2500,
			disableOnInteraction: false,
		},
		breakpoints: {
			1024: { slidesPerView: 1, spaceBetween: 30 },
			920:  { slidesPerView: 1, spaceBetween: 30 },
			578:  { slidesPerView: 1, spaceBetween: 10 }
		}
	});

	// swiper — карточки товаров
	var swiperProducts = new Swiper('.products-container', {
		slidesPerView: 1,
		spaceBetween: 30,
		loop: true,
		speed: 400,
		navigation: {
			nextEl: '.swiper-button-next',
			prevEl: '.swiper-button-prev',
		},
		autoplay: 10000000,
		zoom: true,
		noSwiping: false,
		breakpoints: {
			1024: { slidesPerView: 1, spaceBetween: 30 },
			920:  { slidesPerView: 1, spaceBetween: 30 },
			578:  { slidesPerView: 1, spaceBetween: 10 }
		}
	});

	// скролл плагин
	$('.manufacturer .wrapper').addClass('mCustomScrollbar').attr('data-mcs-theme', 'dark');
	$(".manufacturer .wrapper").mCustomScrollbar({ theme: "dark" });

	// select
	$('select').each(function(){
		var $this = $(this), numberOfOptions = $(this).children('option').length;

		$this.addClass('select-hidden');
		$this.wrap('<div class="select"></div>');
		$this.after('<div class="select-styled"></div>');

		var $styledSelect = $this.next('div.select-styled');
		$styledSelect.text($this.children('option').eq(0).text());

		var $list = $('<ul />', { 'class': 'select-options' }).insertAfter($styledSelect);

		for (var i = 0; i < numberOfOptions; i++) {
			$('<li />', {
				text: $this.children('option').eq(i).text(),
				rel: $this.children('option').eq(i).val()
			}).appendTo($list);
		}

		var $listItems = $list.children('li');

		$styledSelect.click(function(e) {
			e.stopPropagation();
			$('div.select-styled.active').not(this).each(function(){
				$(this).removeClass('active').next('ul.select-options').hide();
			});
			$(this).toggleClass('active').next('ul.select-options').toggle();
		});

		$listItems.click(function(e) {
			e.stopPropagation();
			$styledSelect.text($(this).text()).removeClass('active');
			$this.val($(this).attr('rel'));
			$list.hide();
		});

		$(document).click(function() {
			$styledSelect.removeClass('active');
			$list.hide();
		});
	});

	// ========= ЗАГРУЗИТЬ ЕЩЕ =========

	function initProductSwiper(container) {
		new Swiper(container, {
			slidesPerView: 1,
			spaceBetween: 30,
			loop: true,
			speed: 400,
			navigation: {
				nextEl: container.querySelector('.swiper-button-next'),
				prevEl: container.querySelector('.swiper-button-prev'),
			},
		});
	}

	var loadMoreBtn = document.getElementById('load-more-btn');
	if (loadMoreBtn) {
		loadMoreBtn.addEventListener('click', function(e) {
			e.preventDefault();

			var btn = this;
			var page = parseInt(btn.dataset.page);
			btn.textContent = 'Загрузка...';

			fetch('/api/products?page=' + page + '&per_page=6')
				.then(function(res) { return res.json(); })
				.then(function(products) {

					if (products.length === 0) {
						document.getElementById('load-more-wrapper').style.display = 'none';
						return;
					}

					var container = document.getElementById('products-container');
					products.forEach(function(p) {
						container.insertAdjacentHTML('beforeend', renderCard(p));
					});

					// Инициализируем swiper только на новых карточках
					document.querySelectorAll('.products-container:not(.swiper-initialized)')
						.forEach(function(el) {
							initProductSwiper(el);
						});

					btn.dataset.page = page + 1;
					btn.textContent = 'Загрузить еще';

					if (products.length < 6) {
						document.getElementById('load-more-wrapper').style.display = 'none';
					}
				});
		});
	}

	function renderCard(p) {
		var slides = p.images && p.images.length > 0
			? p.images.map(function(url) {
				return '<div class="swiper-slide"><a href="#"><img src="' + url + '" alt="' + p.name + '"/></a></div>';
			}).join('')
			: '<div class="swiper-slide"><a href="#"><img src="/static/img/no-image.png" alt="' + p.name + '"/></a></div>';

		return '\
		<div class="col-lg-4 col-md-6 col-12">\
			<div class="wrap">\
				<div class="production__item">\
					<div class="products-container swiper-container">\
						<div class="swiper-wrapper">' + slides + '</div>\
						<div class="swiper-button-prev"></div>\
						<div class="swiper-button-next"></div>\
					</div>\
					<div class="wrap">\
						<div class="production__item_title">' + p.name + '</div>\
						<div class="production__item_art"><span>Арт:</span> ' + p.articul + '</div>\
						<div class="production__item_descr">' + p.summary + '</div>\
						<div class="production__item_weight">\
							<div class="weight_item">\
								<div class="weight_item_icon"><i class="nut-icon icons-food-scale-tool"></i></div>\
								<div class="weight_item_descr"><p>Масса</p><p><span>' + p.mass + '<i>г.</i></span></p></div>\
							</div>\
							<div class="weight_item">\
								<div class="weight_item_icon"><i class="nut-icon icons-group"></i></div>\
								<div class="weight_item_descr"><p>Упаковка</p><p><span>' + p.packaging + '</span></p></div>\
							</div>\
						</div>\
						<div class="production__item_sum">\
							<div class="sum_item">\
								<div class="sum_item_title"><p>Цена: </p></div>\
								<div class="sum_item_new"><p>' + p.price + ' <i>грн.</i></p></div>\
							</div>\
							<div class="sum_item">\
								<div class="sum_item_button"><a href="#" class="button">Купить</a></div>\
							</div>\
						</div>\
					</div>\
				</div>\
			</div>\
		</div>';
	}

})(jQuery);