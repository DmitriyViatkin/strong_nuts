(function(e){e(document).ready(function(){e.Scrollax&&e.Scrollax(),e(document).on(`click`,`a[href='#']`,function(e){e.preventDefault()});let t=e(`.top-header`);t.length&&!e(`.mobile-menu`).length&&(t.before(`
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
			`),e(`.menu_top`).first().clone().appendTo(`.mobile-menu`)),e(document).on(`click`,`.mobile-menu-button, .mobile-menu .icons-close-button`,function(){e(`.mobile-menu`).stop().slideToggle(),e(`.top-header`).toggleClass(`d-none`)}),e(`.lang-menu`).length&&e(`.logo_tel_mobile, .logo_button_mobile`).insertBefore(`.lang-menu`),e(`.mobile-line`).length&&(e(`.line_social, .log_in`).clone().appendTo(`.mobile-line`),e(`.mobile-line ul.log_in`).removeClass(`d-none`));let n=e(`.news-container .swiper-button-next`),r=e(`.news-container .swiper-button-prev`),i=e(`.news .wrap .navigation`);n.length&&i.length&&n.insertBefore(i),r.length&&i.length&&r.insertBefore(i);let a=e(`.timer`);a.length&&e(window).on(`scroll.counter`,function(){let t=a.offset();t&&e(window).scrollTop()>t.top-e(window).height()/2&&(e.fn.countTo&&e(`.timer__single`).countTo(),e(window).off(`scroll.counter`))}),e(document).on(`click`,`ul.tabs__caption li:not(.active)`,function(){e(this).addClass(`active`).siblings().removeClass(`active`).closest(`.tabs`).find(`.tabs__content`).removeClass(`active`).eq(e(this).index()).addClass(`active`)});function o(t){e(document).on(`click`,t+` input[type="radio"]`,function(){let t=e(`.`+e(this).val());e(`.box`).not(t).hide(),t.show()})}o(`.radio__wrap`),o(`.radio__wrapper_click`),e(document).on(`click`,`.radio__wrapper_click .radio-custom_last`,function(){e(`.box`).hide()}),e.fn.tooltipster&&e(`.tooltip`).tooltipster({animation:`fade`,delay:200,maxWidth:106}),e.fn.basictable&&(e(`#table`).basictable(),e(`#table-breakpoint`).basictable({breakpoint:768})),e(document).on(`click`,`.popup__cart`,function(e){e.stopPropagation()}),typeof Stickyfill<`u`&&Stickyfill.add(e(`.sticky`));let s=document.getElementById(`lang-menu`);if(s){let e=s.querySelector(`.title`);document.addEventListener(`click`,function(t){let n=t.target;for(;n&&n!==document;){if(n===s){t.target.tagName===`A`&&(e.innerHTML=t.target.textContent,e.style.backgroundImage=getComputedStyle(t.target).backgroundImage),s.classList.toggle(`open`);return}n=n.parentNode}s.classList.remove(`open`)})}document.querySelector(`.news-container`)&&typeof Swiper<`u`&&new Swiper(`.news-container`,{slidesPerView:3,spaceBetween:30,loop:!0,navigation:{nextEl:`.swiper-button-next`,prevEl:`.swiper-button-prev`},autoplay:{delay:2500,disableOnInteraction:!1},breakpoints:{1024:{slidesPerView:3},920:{slidesPerView:2},578:{slidesPerView:1}}}),e(`.swiper-container`).hover(function(){this.swiper&&this.swiper.autoplay.stop()},function(){this.swiper&&this.swiper.autoplay.start()});let c=`/${window.location.pathname.split(`/`)[1]}/products/api`,l=document.querySelector(`#flavor-select`),u=document.querySelector(`#mass-select`);if(l&&u){function t(e){let t=e?`${c}/mass/?flavor=${encodeURIComponent(e)}`:`${c}/mass/`;fetch(t).then(e=>e.json()).then(e=>{u.innerHTML=`<option value=''>Оберіть масу</option>`,e.mass.forEach(e=>{let t=document.createElement(`option`);t.value=e,t.textContent=e+` г.`,u.appendChild(t)}),d(u)}).catch(e=>console.error(`Mass error:`,e))}fetch(`${c}/flavors/`).then(e=>e.json()).then(e=>{l.innerHTML=`<option value='' selected>Оберіть смак</option>`,e.flavors.forEach(e=>{let t=document.createElement(`option`);t.value=e,t.textContent=e,l.appendChild(t)}),l.value=``,d(l),t(``)}).catch(e=>console.error(`Flavors error:`,e)),e(document).on(`change`,`#flavor-select`,function(){t(this.value)}),e(document).on(`click`,`#price-sort`,function(){let t=e(this).data(`order`)||``,n;t===``?(n=`asc`,e(this).find(`span`).text(`Ціна ↑`),e(this).find(`i`).css(`transform`,`rotate(180deg)`)):t===`asc`?(n=`desc`,e(this).find(`span`).text(`Ціна ↓`),e(this).find(`i`).css(`transform`,`rotate(0deg)`)):(n=``,e(this).find(`span`).text(`Сортування`),e(this).find(`i`).css(`transform`,`rotate(0deg)`)),e(this).data(`order`,n)}),e(document).on(`click`,`.production__filter_button .button`,function(t){t.preventDefault();let n=e(`#flavor-select`).val(),r=e(`#mass-select`).val(),i=e(`#price-sort`).data(`order`)||``,a=new URLSearchParams;n&&a.append(`flavor`,n),r&&a.append(`mass`,r),i&&a.append(`order`,i),fetch(`${c}/products/?${a.toString()}`).then(e=>e.json()).then(e=>{let t=document.getElementById(`products-container`);if(t){if(!e.products||!e.products.length){t.innerHTML=`<p class="col-12">Товари не знайдені.</p>`;return}t.innerHTML=e.products.map(e=>f(e)).join(``),t.querySelectorAll(`.products-container`).forEach(e=>{new Swiper(e,{slidesPerView:1,loop:!0,navigation:{nextEl:e.querySelector(`.swiper-button-next`),prevEl:e.querySelector(`.swiper-button-prev`)},autoplay:{delay:2500,disableOnInteraction:!1}})})}}).catch(e=>console.error(`Filter error:`,e))}),e(document).on(`click`,`.button_close`,function(e){e.preventDefault(),location.reload()})}function d(t){let n=e(t);n.next(`.select-styled`).remove(),n.next(`.select-options`).remove();let r=e(`<div class="select-styled"></div>`),i=e(`<ul class="select-options"></ul>`);n.after(r),r.text(n.find(`:selected`).text()),n.children(`option`).each(function(){e(`<li />`,{text:e(this).text(),rel:e(this).val()}).appendTo(i)}),r.after(i),r.on(`click`,function(t){t.stopPropagation(),e(`.select-styled.active`).not(this).removeClass(`active`).next().hide(),e(this).toggleClass(`active`).next().toggle()}),i.on(`click`,`li`,function(){let t=e(this);r.text(t.text()).removeClass(`active`),n.val(t.attr(`rel`)).trigger(`change`),i.hide()}),e(document).off(`click.customSelect`).on(`click.customSelect`,function(){e(`.select-styled`).removeClass(`active`),e(`.select-options`).hide()})}function f(e){let t=e.images&&e.images.length?e.images.map(t=>`
					<div class="swiper-slide">
						<a href="#">
							<img src="${t}" alt="${e.name}"/>
						</a>
					</div>`).join(``):`<div class="swiper-slide">
						<a href="#">
							<img src="/static/img/no-image.png" alt="${e.name}"/>
						</a>
					</div>`,n=e.is_sale&&e.old_price?`<div class="sum_item_old"><p>${e.old_price} <i>грн.</i></p></div>`:``;return`
				<div class="col-lg-4 col-md-6 col-12">
					<div class="wrap">
						<div class="production__item">

							<div class="products-container swiper-container">
								<div class="swiper-wrapper">
									${t}
								</div>
								<div class="swiper-button-prev"></div>
								<div class="swiper-button-next"></div>
								<img class="zoom" src="/static/img/zoom.svg" alt="">
							</div>

							<div class="wrap">
								<div class="production__item_title">${e.name}</div>
								<div class="production__item_art">
									<span>Арт:</span> ${e.articul||``}
								</div>
								<div class="production__item_descr">${e.summary||``}</div>

								<div class="production__item_weight">
									<div class="weight_item">
										<div class="weight_item_icon">
											<i class="nut-icon icons-food-scale-tool"></i>
										</div>
										<div class="weight_item_descr">
											<p>Вага</p>
											<p><span>${e.mass}<i>г.</i></span></p>
										</div>
									</div>
								</div>

								<div class="production__item_sum">
									<div class="sum_item">
										${n}
										<div class="sum_item_new">
											<p>${e.price} <i>грн.</i></p>
										</div>
									</div>
									<div class="sum_item">
										<div class="sum_item_button">
											<a href="#"
											   class="button add-to-cart-btn"
											   data-product-id="${e.id}">Купити</a>
										</div>
									</div>
								</div>
							</div>

						</div>
					</div>
				</div>
			`}let p=document.getElementById(`load-more-btn`);p&&p.addEventListener(`click`,function(e){e.preventDefault();let t=parseInt(this.dataset.page);this.textContent=`Завантаження...`,fetch(`/api/products?page=${t}&per_page=6`).then(e=>e.json()).then(e=>{if(!e||!e.length){this.style.display=`none`;return}let n=document.getElementById(`products-container`);n&&e.forEach(e=>{n.insertAdjacentHTML(`beforeend`,f(e))}),this.dataset.page=t+1,this.textContent=`Завантажити ще`})})})})(jQuery),window.initMap=function(){let e=document.getElementById(`map`);if(typeof google>`u`||!e)return;let t=parseFloat(e.dataset.lat),n=parseFloat(e.dataset.lng);if(console.log(`lat:`,t,`lng:`,n),isNaN(t)||isNaN(n))return;let r={lat:t,lng:n},i=new google.maps.Map(e,{zoom:15,center:r});new google.maps.Marker({position:r,map:i})};