const owlCarousel = require('owl.carousel');
import 'jquery-validation';
require('jquery-validation/dist/localization/messages_es.min.js');
require('jquery-validation/dist/additional-methods.min.js')
import 'jquery.steps';
import 'multiple-select';
import 'multiple-select/dist/locale/multiple-select-es-ES';
const dayjs = require('dayjs');
import 'select2';
require('select2/dist/js/i18n/es');



function toggleShowHideFilterTags() {
    let filterActivate = jQuery(".block-list-result-main .block-applied-filters .active-filters-show .tag")
    let filters = jQuery(".block-list-result-main .block-applied-filters");

    if (filterActivate.length > 0) {
        jQuery(filters).css("display", "block");
    } else {
        jQuery(filters).css("display", "none");
    }
}





/*=============== GLOBAL VARS ===============*/

let screenWidth = $(window).width();

/*==================== SLIDERS ====================*/

function initSliderBannerHome() {
    $('.banner-home .banner-list').addClass("owl-carousel").owlCarousel({
        items: 1,
        nav: false,
        dots: true,
        loop: true,
        autoplay: true,
        autoplayTimeout: 8000,
        autoplayHoverPause: true,
        responsive: {
            768: {
                nav: true,
                dots: true
            }
        },
        onInitialized: () => {
            $('.loading').fadeOut();
        }
    });
}

function initSliderBenefitsHome() {
    $('.benefits-items').addClass("owl-carousel").owlCarousel({
        items: 1,
        nav: false,
        dots: true,
        loop: true,
        margin: 15,
        responsive: {
            768: {
                nav: false,
                dots: true,
                items: 2,
                margin: 20,
            },
            992: {
                nav: true,
                dots: true,
                items: 3,
                margin: 20,
            }
        }
    });
}

function initSliderProjectsHome() {
    if ($('.projects-home-list').length) {
        $('.projects-home-list').addClass("owl-carousel").owlCarousel({
            items: 1,
            nav: false,
            dots: true,
            loop: true,
            center: true,
            responsive: {
                0: {
                    items: 1,
                    stagePadding: 50,
                    margin: 12,
                },
                768: {
                    dots: true,
                    items: 2,
                    margin: 10,
                    stagePadding: 0,
                    center: false,
                    autoWidth: true,
                },
                992: {
                    items: 3,
                    center: false,
                    nav: true,
                    autoWidth: true,
                    margin: 15,
                },
            },
            onInitialized: initSliderTagsProjectsCard
        });
    }
}

function initSliderNewsHome() {
    if ($('.news-home-list').length) {
        $('.news-home-list').addClass("owl-carousel").owlCarousel({
            items: 1,
            nav: false,
            dots: true,
            loop: true,
            center: true,
            margin: 18,
            responsive: {
                0: {
                    items: 1,
                    stagePadding: 50,
                },
                768: {
                    dots: true,
                    items: 2,
                    stagePadding: 0,
                    center: false,
                },
                992: {
                    items: 3,
                    center: true,
                    nav: true,
                },
            },
            onInitialized: initSliderTagsNewsCard
        });
    }
}

function initSliderEducationalHome() {
    $('.educational-home-list').addClass("owl-carousel").owlCarousel({
        items: 1,
        nav: false,
        dots: true,
        loop: true,
        center: true,
        margin: 18,
        responsive: {
            0: {
                items: 1,
                stagePadding: 50,
            },
            768: {
                dots: true,
                items: 2,
                stagePadding: 0,
                center: false,
            },
            992: {
                items: 3,
                center: true,
                nav: true,
            },
        },
        onInitialized: initSliderTagsEducationalCard
    });
}

function initSliderTestimonialsHome() {
    $('.testimonials-home-list').addClass("owl-carousel").owlCarousel({
        items: 1,
        nav: false,
        dots: true,
        loop: true,
        center: true,
        margin: 11,
        responsive: {
            768: {
                dots: true,
                nav: true,
            },
        }
    });
}

function initSliderAnalisysProvider() {
    function createSlider() {
        $('.card-welcome-provider-analysis .analysis-boxes').addClass("owl-carousel").owlCarousel({
            items: 2,
            nav: false,
            dots: false,
            loop: true,
            margin: 10,
            center: false,
            autoWidth: true,
        });
    }

    function removeSlider() {
        $('.card-welcome-provider-analysis .analysis-boxes').owlCarousel("destroy");
        $('.card-welcome-provider-analysis .analysis-boxes').removeClass("owl-carousel");
    }

    if ($(window).width() < 1400) {
        createSlider();
    }

    $(window).on('resize', function () {
        if ($(window).width() < 1400) {
            createSlider();
        } else {
            removeSlider()
        }
    })

}

function initSliderCardActivity() {
    $('.content-cards-activity').addClass("owl-carousel").owlCarousel({
        items: 1,
        nav: false,
        dots: true,
        loop: false, // antes true
        center: true,
        responsive: {
            0: {
                items: 1,
                margin: 20,
                stagePadding: 0,
                center: true,
                autoWidth: true,
            },
            768: {
                items: 1,
                margin: 10,
                stagePadding: 0,
                center: false,
                nav: true,
                autoWidth: true,
            },
            992: {
                items: 1,
                center: false,
                nav: true,
                autoWidth: true,
                margin: 30,
            },
        }
    });
}

function initSliderProjectsProvider() {
    if ($('.related-projects-list-provider').length) {

        $('.related-projects-list-provider').addClass("owl-carousel").owlCarousel({
            items: 1,
            nav: false,
            dots: true,
            loop: true,
            center: true,
            responsive: {
                0: {
                    items: 1,
                    margin: 20,
                    stagePadding: 0,
                    center: true,
                    autoWidth: true,
                },
                768: {
                    dots: true,
                    items: 2,
                    margin: 10,
                    stagePadding: 0,
                    center: false,
                    nav: true,
                    autoWidth: true,
                },
                992: {
                    items: 3,
                    center: false,
                    nav: true,
                    autoWidth: true,
                    margin: 20,
                },
            },
            onInitialized: initSliderTagsProjectsCard
        });
    }
}

function initSliderDetailRelatedProjects() {
    if ($('.detail__related-projects__list').length) {
        $('.detail__related-projects__list').addClass("owl-carousel").owlCarousel({
            items: 1,
            nav: false,
            dots: true,
            loop: true,
            center: true,
            margin: 18,
            responsive: {
                0: {
                    items: 1,
                    stagePadding: 50,
                },
                768: {
                    dots: true,
                    items: 2,
                    stagePadding: 0,
                    center: false,
                },
                992: {
                    items: 3,
                    center: true,
                    nav: true,
                },
            },
            onInitialized: initSliderTagsProjectsCard
        });
    }
}

function initSliderDetailRelatedNews() {
    if ($('.detail__related-news__list').length) {
        $('.detail__related-news__list').addClass("owl-carousel").owlCarousel({
            items: 1,
            nav: false,
            dots: true,
            loop: true,
            center: true,
            margin: 18,
            responsive: {
                0: {
                    items: 1,
                    stagePadding: 50,
                },
                768: {
                    dots: true,
                    items: 2,
                    stagePadding: 0,
                    center: false,
                },
                992: {
                    items: 3,
                    center: true,
                    nav: true,
                },
                1400: {
                    items: 4,
                    center: false,
                    nav: true,
                }
            },
            onInitialized: initSliderTagsNewsCard
        });
    }
}

function initSliderDetailGallery() {
    $('.detail__gallery__wrapper').addClass("owl-carousel").owlCarousel({
        items: 1,
        nav: false,
        dots: true,
        loop: true,
        center: true,
        margin: 15,
        responsive: {
            0: {
                items: 1,
                stagePadding: 15,
            },
            390: {
                autoWidth: true,
                stagePadding: 0,
            },
            768: {
                dots: true,
                items: 2,
                center: false,
                autoWidth: true,
            },
            992: {
                items: 3,
                center: false,
                autoWidth: true,
                dots: true,
                nav: true,
                stagePadding: 300,
            },
        },
        onInitialized: function () {
            // Añadimos clase "container", para que este centrado segun Bootstrap
            $('.detail__gallery__wrapper .owl-nav').addClass('container');
            $('.detail__gallery__wrapper .owl-dots').addClass('container');
        }
    });
}

function initSliderTagsProjectsCard() {
    $('.projectscard .projectscard__taxonomies').addClass("owl-carousel").owlCarousel({
        items: 1,
        nav: true,
        dots: false,
        margin: 4,
        autoWidth: true,
    });
    // En perfil proveedor proyectos relacionados    
    $('.card-list-project-item .card-list-project-item-taxonomies').addClass("owl-carousel").owlCarousel({
        items: 1,
        nav: true,
        dots: false,
        margin: 4,
        autoWidth: true,
    });
}

function initSliderTagsNewsCard() {
    // Para tarjetas News

    $('.news__item__tags').addClass("owl-carousel").owlCarousel({
        items: 1,
        nav: true,
        dots: false,
        margin: 5,
        autoWidth: true,
    });

}

function initSliderTagsEducationalCard() {
    // Para tarjetas Educational home

    $('.educational-home-item-tags').addClass("owl-carousel").owlCarousel({
        items: 1,
        nav: true,
        dots: false,
        margin: 5,
        autoWidth: true,
    });

}

function allPageSliders() {
    initSliderBannerHome();
    initSliderBenefitsHome();
    initSliderProjectsHome();
    initSliderNewsHome();
    initSliderEducationalHome();
    initSliderTestimonialsHome();
    initSliderAnalisysProvider();
    initSliderCardActivity();
    initSliderProjectsProvider();
    initSliderDetailRelatedProjects();
    initSliderDetailRelatedNews();
    initSliderDetailGallery();
    initSliderTagsProjectsCard();
    initSliderTagsNewsCard();
    initSliderTagsEducationalCard();
}

/*==================== YOUTUBE VIDEO MODAL ====================*/

/**
 * @author       Rob W <gwnRob@gmail.com>
 * @website      https://stackoverflow.com/a/7513356/938089
 * @version      20190409
 * @description  Executes function on a framed YouTube video (see website link)
 *               For a full list of possible functions, see:
 *               https://developers.google.com/youtube/js_api_reference
 * @param String frame_id The id of (the div containing) the frame
 * @param String func     Desired function to call, eg. "playVideo"
 *        (Function)      Function to call when the player is ready.
 * @param Array  args     (optional) List of arguments to pass to function func*/
function callPlayer(frame_id, func, args) {
    if (window.jQuery && frame_id instanceof jQuery) frame_id = frame_id.get(0).id;
    let iframe = document.getElementById(frame_id);
    if (iframe && iframe.tagName.toUpperCase() != 'IFRAME') {
        iframe = iframe.getElementsByTagName('iframe')[0];
    }

    // When the player is not ready yet, add the event to a queue
    // Each frame_id is associated with an own queue.
    // Each queue has three possible states:
    //  undefined = uninitialised / array = queue / .ready=true = ready
    if (!callPlayer.queue) callPlayer.queue = {};
    let queue = callPlayer.queue[frame_id],
        domReady = document.readyState == 'complete';

    if (domReady && !iframe) {
        // DOM is ready and iframe does not exist. Log a message
        window.console && console.log('callPlayer: Frame not found; id=' + frame_id);
        if (queue) clearInterval(queue.poller);
    } else if (func === 'listening') {
        // Sending the "listener" message to the frame, to request status updates
        if (iframe && iframe.contentWindow) {
            func = '{"event":"listening","id":' + JSON.stringify('' + frame_id) + '}';
            iframe.contentWindow.postMessage(func, '*');
        }
    } else if ((!queue || !queue.ready) && (
        !domReady ||
        iframe && !iframe.contentWindow ||
        typeof func === 'function')) {
        if (!queue) queue = callPlayer.queue[frame_id] = [];
        queue.push([func, args]);
        if (!('poller' in queue)) {
            // keep polling until the document and frame is ready
            queue.poller = setInterval(function () {
                callPlayer(frame_id, 'listening');
            }, 250);
            // Add a global "message" event listener, to catch status updates:
            messageEvent(1, function runOnceReady(e) {
                if (!iframe) {
                    iframe = document.getElementById(frame_id);
                    if (!iframe) return;
                    if (iframe.tagName.toUpperCase() != 'IFRAME') {
                        iframe = iframe.getElementsByTagName('iframe')[0];
                        if (!iframe) return;
                    }
                }
                if (e.source === iframe.contentWindow) {
                    // Assume that the player is ready if we receive a
                    // message from the iframe
                    clearInterval(queue.poller);
                    queue.ready = true;
                    messageEvent(0, runOnceReady);
                    // .. and release the queue:
                    while (tmp = queue.shift()) {
                        callPlayer(frame_id, tmp[0], tmp[1]);
                    }
                }
            }, false);
        }
    } else if (iframe && iframe.contentWindow) {
        // When a function is supplied, just call it (like "onYouTubePlayerReady")
        if (func.call) return func();
        // Frame exists, send message
        iframe.contentWindow.postMessage(JSON.stringify({
            "event": "command",
            "func": func,
            "args": args || [],
            "id": frame_id
        }), "*");
    }
    /* IE8 does not support addEventListener... */
    function messageEvent(add, listener) {
        let w3 = add ? window.addEventListener : window.removeEventListener;
        w3 ?
            w3('message', listener, !1)
            :
            (add ? window.attachEvent : window.detachEvent)('onmessage', listener);
    }
}

// Get and autoplay Video from data
function videoYouTubeModal() {
    $("body").find('[data-tagVideo]').each(function () {
        let theModal = $(this).data('bs-target'),
            videoSRC = $(this).attr('data-tagVideo'),
            videoSRCauto = videoSRC + '?autoplay=0&modestbranding=1&showinfo=0&enablejsapi=1';

        // Añade src al iframe
        $(theModal + ' iframe').attr('src', videoSRCauto);

        // Obtenemos id del iframecontainer
        let idIframeContainer = $(theModal + ' iframe').parent().attr('id');

        let $theModal = document.querySelector(theModal);
        // Estos eventos de Bootstrap 5, solo se pueden añadir por vainilla JS

        // Evento para pausar video al cerrar modal
        $theModal.addEventListener('hidden.bs.modal', event => {
            callPlayer(idIframeContainer, 'pauseVideo');
        });
    });
}

function allPageVideoModals() {
    videoYouTubeModal();
}

/*==================== DROPDOWN SEARCH MENU ====================*/

function showDropdownSearchMenu(event) {
    $('.dropdownSearchMenu').addClass('show');
}

function eventsDropdownSearchMenu() {
    // Abrir cuando se hace focus o click en el input
    $('header .navbar .search-records .input-group input#id_title').on({
        'click': showDropdownSearchMenu,
        'focus': showDropdownSearchMenu
    });
    $('header .navbar .search-records .input-group input#id_name').on({
        'click': showDropdownSearchMenu,
        'focus': showDropdownSearchMenu
    });
    // Abrir o cerrar en mobile
    $('#btnDropdownSearchMobile').on('click', function () {
        $(this).toggleClass('active');
        $('.dropdownSearchMenu').toggleClass('show');
    });

    // Cerrar cuando se abre el menú principal
    closeDropdownSearchMenu();
}

function closeDropdownSearchMenu() {
    // Cuando abrimos el menu principal
    $('#btnMenuBurguer').on('click', function () {
        if ($('.dropdownSearchMenu').hasClass('show')) {
            $('.dropdownSearchMenu').removeClass('show');
            $('#btnDropdownSearchMobile').removeClass('active');
        }

        $(this).toggleClass('open');

        if ($('body #btnMenuBurguer').hasClass('open')) {
            $('body').addClass('overflow-hidden');
        } else {
            $('body').removeClass('overflow-hidden');
        }

        closeMenuPrimary();
    });
}

function closeMenuPrimary() {
    // Cuando abrimos el menu principal
    $('#navbarTogglerMenu .btn-close').on('click', function () {
        $('body').removeClass('overflow-hidden');
        $('#btnMenuBurguer').removeClass('open');
    });
}

/*==================== WINDOW EVENTS ====================*/

function windowEvents() {
    $(window).on('click', function (event) {

        // Cerrar DropdownSearchMenu cuando se hace click por fuera del menu
        if (event.target == $('.dropdownSearchMenu')[0]) {
            $('.dropdownSearchMenu').removeClass('show');
        }

        // Cerrar Menú principal cuando se hace click por fuera del menu
        if (event.target == $('.navbarTogglerMenu')[0]) {
            $('.navbarTogglerMenu').removeClass('show');
            $('#btnMenuBurguer').removeClass('open').addClass('collapsed').attr('aria-expanded', 'false');
            $('body').removeClass('overflow-hidden');
        }

    });

    $(window).on('scroll', function () {
        clearTimeout(throttlescroll)

        let throttlescroll = setTimeout(function () { // throttle code inside scroll to once every 300 milliseconds
            let screenWidth = $(window).width();
            // Cerrar DropdownSearchMenu cuando se hace scroll en desktop
            if (screenWidth >= 992) {
                $('.dropdownSearchMenu').removeClass('show');
            }
        }, 300);

    });

    $(window).on('resize', function () {
        delay(function () {
            closeModalBackdrop();
        }, 500);
    });
}

let delay = (function () {
    let timer = 0;
    return function (callback, ms) {
        clearTimeout(timer);
        timer = setTimeout(callback, ms);
    };
})();

/*==================== ANIMATIONS ON SCROLL ====================*/

function animateOnScroll() {

    let options = {
        root: null,
        rootMargin: '0px 0px -400px 0px',
    }

    const observer = new IntersectionObserver((entries) => {

        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add('show')
            } else {
                entry.target.classList.remove('show')
                if (!entry.target.classList.contains('show')) {
                    entry.target.classList.add('show');
                }
            }
        })

    }, options);

    const hiddenElemts = jQuery('.hidden');

    hiddenElemts.each((i, elem) => observer.observe(elem))
}

function addTransitionToElements(selector) {
    $(selector).each(function (index) {
        let claseidentificadora = "transition transition-" + (index + 1);
        $(this).addClass(claseidentificadora);
    });
}

function initTransitions() {
    // Agregamos transiciones en:
    //  los items de beneficios home
    addTransitionToElements('.benefits-card');
    // Items Proyectos home
    addTransitionToElements('.projects-home-item');
    // Items noticia home
    addTransitionToElements('.news-home-item');
    // Items educativo home
    addTransitionToElements('.educational-home-item');
}

/*==================== ACTIVE USER ROL ====================*/
function activeUserRol() {

    if ($(".login-screen .container-fluid .row .card-container form.login-form .input-container input#id_username").length > 0) {
        $(".login-screen .container-fluid .row .card-container form.login-form .input-container input#id_username").attr("placeholder", "Ingrese su correo")
        $(".login-screen .container-fluid .row .card-container form.login-form .input-container input#id_password").attr("placeholder", "********")
    }

    $("section .container-fluid .row .card-container .user-rol ul > li").each(function (i, value) {
        $(this).attr("id", `userRol-${i}`)
    })
    $("section .container-fluid .row .card-container .user-rol ul > li#userRol-0").addClass("active")

    $("section .container-fluid .row .card-container .user-rol ul > li").on('click', function (event) {
        let itemClick = $(this).attr('id')
        $("section .container-fluid .row .card-container .user-rol ul li.active").removeClass("active")
        $(`section .container-fluid .row .card-container .user-rol ul li#${itemClick}`).addClass("active")
    })

}

/*==================== VALIDATE INPUTS RECOVERY PASS ====================*/

function validateRecoveryPass() {

    if ($('form#recovery-form').length) {
        $('form#recovery-form input[type="password"]').on('change blur', function () {
            if ($(this).val().length >= 1 && !$(this).hasClass('error')) {
                $(this).closest('.input-container').addClass("correct-pass");
                $(this).closest('.input-container').removeClass("wrong-pass");
            } else {
                $(this).closest('.input-container').removeClass("correct-pass");
                $(this).closest('.input-container').addClass("wrong-pass");
            }
        })
    }
}

/*==================== EVENT BUTTON SLIDER  ====================*/

function eventButtonSliderActivity(event) {
    if ($('.inventory-followed-cards').length || $('.block-activities-content').length) {
        $('.button-slider input').on('click', function () {
            if ($(this).is(':checked')) {
                $(this).closest('.cards-activity-item-header').addClass('active');
            } else {
                $(this).closest('.cards-activity-item-header').removeClass('active');
            }
        })
    }
}

/*==================== EVENT INPUT RANGE  ====================*/

function eventInputRangePorcentege(event) {
    if ($('#range-question-perfil').length) {
        let InputRange = document.querySelector('#range-question-perfil');
        InputRange.style.setProperty("--value", InputRange.value);
        let widthElement = parseInt(window.getComputedStyle(InputRange, null).getPropertyValue('width'));
        let tagPorcentege = $('.input-range-primary .value-percentage');

        if (tagPorcentege) {
            tagPorcentege.text(InputRange.value + "%");
            let pxls = widthElement / 100;
            tagPorcentege.css('left', ((InputRange.value * pxls) - 36) + 'px')
        }
    }
}

function eventInputRangePorcentegeAll(element) {
    if ($('.' + element + '').length) {
        let InputRange = document.querySelectorAll('.' + element + ' input');
        InputRange.forEach(InputRangeItem => {
            InputRangeItem.style.setProperty("--value", InputRangeItem.value);
            let widthElement = parseInt(window.getComputedStyle(InputRangeItem, null).getPropertyValue('width'));
            let tagPorcentege = InputRangeItem.nextElementSibling;

            if (tagPorcentege) {
                tagPorcentege.innerHTML = InputRangeItem.value + "%";
                let pxls = widthElement / 100;
                if (InputRangeItem.value == 100) {
                    tagPorcentege.style.left = ((InputRangeItem.value * pxls) - 34) + 'px';
                } else if (InputRangeItem.value > 96) {
                    tagPorcentege.style.left = ((InputRangeItem.value * pxls) - 23) + 'px';
                } else {
                    tagPorcentege.style.left = ((InputRangeItem.value * pxls) - 15) + 'px';
                }
            }

        });
    }

}

/*==================== PROVIDER MAIN FUNCTIONS ====================*/
function closeModalBackdrop() {
    // Verificamos que estemos desde tablet
    if ($(window).width() >= 768) {
        // Verificamos que la seccion exista
        if ($('.filterModal__modal').length) {
            // Verificamos que el backdrop del modal exista y lo quitamos
            if ($('.modal-backdrop.show').length) {
                $('.modal-backdrop.show').detach();
            }
        }
    }

}

/**
 * @version      20221010
 * @description  Agrupa Labels y su respectivo elemento de formulario(input, select, textarea)
 *               en etiquetas <fieldset>
 * @param String container  la clase o el id del contenedor de los labels e inputs
 * @param Array elements    un array con los atributos "for" de los label e "id" de los 
 *                          input (deben coincidir)
 *        (Function)      Function to call when the player is ready.
 * @param String  target    La clase o id del contenedor destino de los fildset*/
function groupLabelInput(container, elements, target) {
    // Iteramos por cada item del array
    for (let i = 0; i < elements.length; i++) {
        let template = `<fieldset class="form-field" id="field-${i}"><div class="form-element"></div></fieldset>`;
        // Añadimos elemento <fieldset> al destino
        $(target).append(template);
        // Obtenemos label e insertamos en el <fielset> creado
        $('#field-' + i).prepend($(container).find('label[for="' + elements[i] + '"'));
        // Obtenemos elemento del formulario e insertamos en el <fielset> creado
        $('#field-' + i).find('.form-element').append($(container).find('#' + elements[i]));
    }
}

function formFiltrosProviders() {
    // Si existe el formulario
    if ($('form.filterModal__form').length) {
        // Agrupamos campos
        // groupLabelInput('form.provider-main-form', ['id_name', 'id_type', 'id_status'], '.provider-main-form-group');
        // Agregar label search input
        $('form.filterModal__form').find('.form__element--searchinput input#id_name').attr('placeholder', 'Palabra clave');
    }

    if ($('.form-filter-provider-list').length) {
        $('.form-element-search').addClass('input-search').find('input').attr('placeholder', 'Palabra clave');
        $('.form-filter-provider-list').find('input[type="checkbox"]').addClass('checkboxinput');
        $('.form-filter-provider-list').find('#id_custody option[value="unknown"]').remove();
        $('.form-filter-provider-list').find('#id_custody').prepend("<option value='' selected >Seleccione una opción</option>");
    }
}

/*==================== EVENT CLICK BUTTON FILTER MOBILE  ====================*/

/* Calling the function eventClickButtonFilter when the button is clicked. */
function eventClickButtonFilter() {
    if ($('.filter-primary-filtermobile').length) {
        $('.btn-filter-mobile').on('click', function (e) {
            e.preventDefault();

            if (screenWidth > 767 && screenWidth <= 992) {
                $('.filter-primary-filterdesktop').slideToggle('fast');
            }
        });

        $('.filter-primary-filterdesktop .btn-close-filter').on('click', function (e) {
            e.preventDefault();
            $('.filter-primary-filterdesktop').slideToggle('slow');
        });

        $('.filter-primary-filterdesktop #accordionButton').on('click', function () {
            let blockResult = $('.block-show-result');

            if (blockResult.hasClass('expande')) {
                $('.block-show-result').removeClass('expande');
                $('#row-pagination-list').removeClass('justify-content-center').addClass('justify-content-end');
                $('#row-pagination-list .col-pagination').addClass('col-lg-8');
            } else {
                setTimeout(() => {
                    $('.block-show-result').addClass('expande');
                    $('#row-pagination-list').removeClass('justify-content-end').addClass('justify-content-center');
                    $('#row-pagination-list .col-pagination').removeClass('col-lg-8');
                }, 500);
            }
        })

    }
}

/* A function that is called when the user clicks on the filter button. */
function showModalFilterMobile() {
    if ($('.filter-primary-filtermobile').length) {
        let screenWidth = $(window).width();
        if (screenWidth < 768) {
            $('.block-main .filter-primary-filterdesktop .btn-close-filter').remove();
            $('.block-main .filter-primary-filterdesktop form').appendTo('#modalFilterMobile .modal-body .container');
            $('.block-main .filter-primary-filterdesktop').remove();
        }
    }
}

/*==================== EVENT CLICK MENU HEAD UNIT  ====================*/

/* A function that is called when the user clicks on the menu head unit. */
function eventClickMenuHeadUnit(statesPages) {
    if ($('#groupsProfile').length) {
        let loaderContent = $('#groupsProfileMain .loading');
        let isMobile = screenWidth < 992 ? true : false;

        // show loader Content 
        function showLoader() {
            if (isMobile) {
                $('#groupsProfileMain').css({ height: '40vh', overflow: 'hidden' });
                $('#groupsProfileMainContent').addClass('d-none');
            }
            loaderContent.find('.loading__text').removeClass('d-none');
            loaderContent.find('.loading__text--error').addClass('d-none');
            loaderContent.removeClass('d-none');
        }

        // hide loader Content
        function showLoaderError() {
            $('#groupsProfileMain .loading__text').addClass('d-none');
            $('#groupsProfileMain .loading__text--error').removeClass('d-none');
        }

        // hide loader Content
        function hideLoader() {
            setTimeout(() => {
                loaderContent.addClass('d-none');
                $('#groupsProfileMain').removeAttr('style');
                $('#groupsProfileMainContent').removeClass('d-none');
            }, 200);
        }

        // LOAD PAGES OF PROFILE USER 
        function loadPagesProfileuser(urlLink, numPages) {

            if (numPages !== undefined) {
                urlLink = `${urlLink}?day=${numPages}`;
            }

            $("#groupsProfileMainContent").load(urlLink, function (responseText, textStatus, req) {
                if (textStatus != "error") {
                    if ($('.list-transfers').length && numPages !== undefined) {
                        $('#groupsProfileMenuSidebar .tab-sidebar-nav-item.active .link').attr('data-page', numPages);
                        if (numPages !== 0) {
                            $('#title-today').addClass('d-none');
                            $('#title-others').removeClass('d-none');

                        }
                    }

                    hideLoader();

                    // Funcion para el slider de la actividad
                    if ($('.content-cards-activity').length) {
                        initSliderCardActivity();
                        eventButtonSliderActivity();
                    }
                    // Funcion bitácora
                    if ($('.block-binacle-body').length) {
                        tabsBinacle();
                    }
                    // Funcion seguir Inventario | Solicitud
                    followDemandInventory();
                    eventClickAccordionBlockActivityManagement();
                    notificationConfirmationModal();
                    getEvaluationQuestions();
                    profilefilterSearchAccessRraa();
                } else {
                    showLoaderError();
                }
            });

            return false;
        }


        if (statesPages == 'ready') {
            let tabProfileUser = localStorage.getItem('tabProfile');
            if (tabProfileUser !== '' && tabProfileUser !== null) {
                // Leer el link
                $('#groupsProfileMenuSidebar .tab-sidebar-nav-item').each(function () {
                    let urlLink = $(this).find('.link').attr('data-link');
                    if (urlLink == tabProfileUser) {
                        $(this).addClass('active');

                        if (isMobile) {
                            let coord = $('#groupsProfileMenuSidebar .tab-sidebar-nav-item.active').position();
                            $('#groupsProfileMenuSidebar .tab-sidebar').animate({
                                scrollLeft: "+=" + coord.left + "px"
                            }, "slow");
                        }
                    }
                });
                loadPagesProfileuser(tabProfileUser);

            } else {
                // Active the first menu and show to content
                let firstMenu = $('#groupsProfileMenuSidebar .tab-sidebar-nav-item:first');
                let urlLink = firstMenu.find('.link').attr('data-link');
                firstMenu.addClass('active');
                showLoader();

                $("#groupsProfileMainContent").load(urlLink, function (responseText, textStatus, req) {
                    if (textStatus != "error") {
                        setTimeout(() => {
                            hideLoader();
                        }, 200);
                    } else {
                        showLoaderError();
                    }
                });
            }
        }

        if (statesPages == 'load') {
            $('#groupsProfileMenuSidebar .tab-sidebar-nav-item .link').each(function () {
                $(this).removeClass('none-event');
                $('.loading:first').addClass('d-none');
            })

            $('#groupsProfileMenuSidebar .tab-sidebar-nav-item').on('click', function (event) {
                event.preventDefault();
                showLoader();

                $('.tab-sidebar-nav-item').each(function () {
                    $(this).removeClass('active');
                })
                $(this).addClass('active');

                let urlLink = $(this).find('.link').attr('data-link');
                localStorage.setItem('tabProfile', urlLink);

                loadPagesProfileuser(urlLink);

            });

            $('body').on('click', '.list-transfers .list-transfers-buttons button', function (event) {
                event.preventDefault();
                showLoader();
                let dataButton = $(this).attr('data-button');
                let menuSidebar = $('#groupsProfileMenuSidebar');

                let urlLink = menuSidebar.find('.tab-sidebar-nav-item.active .link').attr('data-link');
                let numPages = parseInt(menuSidebar.find('.tab-sidebar-nav-item.active .link').attr('data-page'));

                if (dataButton == 'next') {
                    numPages = numPages + 1;
                }
                if (dataButton == 'prev') {
                    numPages = numPages - 1;
                }

                loadPagesProfileuser(urlLink, numPages);

            })
        }

    }
}

/* Navegación tabs bitácora */
function tabsBinacle() {

    // Active the first item menu and show content
    // let firstMenu = $('.block-binacle-body .nav-pills .nav-link:first');
    // let urlLink = firstMenu.attr('href');
    // firstMenu.addClass('active');
    // $("#v-pills-tabContent").load(urlLink);

    // Añadir evento click en los tabs
    let $tabItems = $('.block-binacle-body .nav-pills .nav-link');
    $tabItems.on('click', function (event) {
        event.preventDefault();
        // Remover clase active
        $tabItems.each(function () {
            $(this).removeClass('active');
        });
        // Añadir clase active
        $(this).addClass('active');
        // cargar contenido
        let urlLink = $(this).attr('data-link');
        $('#v-pills-tabContent .loading').removeClass('d-none');
        $("#v-pills-tabContent").load(urlLink, function () {
            $('#v-pills-tabContent .loading').addClass('d-none');

            // Añadir placeholder caja comentarios
            $('.block-form-notes #id_commentary').attr('placeholder', 'Escriba su comentario... ');

            // Modal confirmación Hilo/comentario
            let $modalConfirmationBinacle = $('#modalConfirmationBinacle');
            if ($modalConfirmationBinacle.length > 0) {

                let modalBsBinacle = bootstrap.Modal.getOrCreateInstance(document.getElementById('modalConfirmationBinacle'));
                let urlAction, $form, threadId, commentId;
                const binacleMessages = [
                    {
                        "title": "Eliminar tema",
                        "description": "¿Está seguro de eliminar el tema y todos sus comentarios?",
                    },
                    {
                        "title": "Eliminar comentario",
                        "description": "¿Está seguro de eliminar el comentario?",
                    }
                ];
                let urlApi = window.location.origin;

                // Abrir modal Tema
                $('body').on('click', '.binacle__thread-info__delete', function (event) {
                    event.preventDefault();
                    // Obtener form
                    $form = $(this).parents('form');
                    // Obtener accion url
                    urlAction = $(this).parents('form').attr('action');
                    threadId = $(this).parents('form').attr('data-threadid');
                    // Seteamos texto del modal
                    $modalConfirmationBinacle.find('.modal-title').html(binacleMessages[0]['title']);
                    $modalConfirmationBinacle.find('.description').html(binacleMessages[0]['description']);
                    // Mostramos modal
                    modalBsBinacle.show();
                    commentId = '';
                });

                // binacle__comment__delete
                // Abrir modal Comentario
                $('body').on('click', '.binacle__comment__delete', function (event) {
                    event.preventDefault();
                    // Obtener form
                    $form = $(this).parents('form');
                    // Obtener accion url
                    urlAction = $(this).parents('form').attr('action');
                    commentId = $(this).parents('form').attr('data-commentid');
                    // Seteamos texto del modal
                    $modalConfirmationBinacle.find('.modal-title').html(binacleMessages[1]['title']);
                    $modalConfirmationBinacle.find('.description').html(binacleMessages[1]['description']);
                    // Mostramos modal
                    modalBsBinacle.show();
                    threadId = '';
                });

                // Eliminar tema/comentario bitacora
                $('body').on('click', '#modalConfirmationBinacle .action-binacle', function (event) {
                    event.preventDefault();

                    // Verificamos si es borrar tema o comentario
                    if (threadId !== '') {
                        // Mostramos loader
                        $modalConfirmationBinacle.find('.loading').removeClass('d-none');
                        // $deleteForm.submit();

                        // Hacemos petición Ajax
                        $.ajax({
                            method: 'POST',
                            url: `${urlApi}${urlAction}`,
                            data: $form.serialize(),
                            success: function (res) {
                                // console.log("Respuesta server: ",res);
                                if (res.success === "True") {
                                    // // Seteamos mensaje en el modal
                                    $modalConfirmationBinacle.find('.description').html(`Se ha eliminado el tema.`);
                                } else if (res.fail === "True") {
                                    // Seteamos mensaje en el modal
                                    $modalConfirmationBinacle.find('.description').html(`Ha ocurrido un error al eliminar.`);
                                } else {
                                    // Seteamos mensaje en el modal
                                    $modalConfirmationBinacle.find('.description').html(`Ha ocurrido un problema inesperado.`);
                                }
                            },
                            error: function (jqXHR, estado, error) {
                                // Seteamos mensaje en el modal
                                $modalConfirmationBinacle.find('.description').html(`Ha ocurrido un error inesperado: ${error}`);
                            },
                            complete: function (jqXHR, estado) {
                                // console.log(estado);
                                // removemos el tema del DOM
                                // elimina el tab
                                let $tabItems = $('.block-binacle-body .nav-pills .nav-link');
                                $tabItems.each(function () {
                                    let tabId = $(this).attr('data-link').split('/');
                                    if (tabId[tabId.length - 1] === threadId) {
                                        $(this).remove();
                                    }
                                });

                                if($('body .block-binacle-body .nav-pills .nav-link').length) {
                                    // setea nuevo contenido del tab content
                                    $("#v-pills-tabContent").html(`<p>Haz clic en algún tema para ver la discusión</p>
                                        <div class="loading loading--absolute d-none">
                                            <div class="loader"></div>
                                            <p class="loading__text">Cargando...</p>
                                            <p class="loading__text loading__text--error d-none"></p>
                                        </div>`
                                    );
                                }else {
                                    window.location.reload();
                                }
                                // Cerramos modal de confirmación
                                modalBsBinacle.hide();
                                // Ocultamos loader
                                $modalConfirmationBinacle.find('.loading').addClass('d-none');
                            },
                        });
                    } else if (commentId !== '') {
                        // Mostramos loader
                        $modalConfirmationBinacle.find('.loading').removeClass('d-none');
                        // $deleteForm.submit();

                        // Hacemos petición Ajax
                        $.ajax({
                            method: 'POST',
                            url: `${urlApi}${urlAction}`,
                            data: $form.serialize(),
                            success: function (res) {
                                // console.log("Respuesta server: ",res);
                                if (res.success === "True") {

                                    // // Seteamos mensaje en el modal
                                    $modalConfirmationBinacle.find('.description').html(`Se ha eliminado el tema.`);
                                } else if (res.fail === "True") {
                                    // Seteamos mensaje en el modal
                                    $modalConfirmationBinacle.find('.description').html(`Ha ocurrido un error al eliminar.`);
                                } else {
                                    // Seteamos mensaje en el modal
                                    $modalConfirmationBinacle.find('.description').html(`Ha ocurrido un problema inesperado.`);
                                }
                            },
                            error: function (jqXHR, estado, error) {
                                // Seteamos mensaje en el modal
                                $modalConfirmationBinacle.find('.description').html(`Ha ocurrido un error inesperado: ${error}`);
                            },
                            complete: function (jqXHR, estado) {
                                // console.log(estado);
                                // removemos el comentario del DOM
                                let $commentItems = $('.block-binacle-body .card-type-notes-list-item');
                                $commentItems.each(function () {
                                    let itemcommentId = $(this).attr('data-commentid');
                                    if (itemcommentId === commentId) {
                                        $(this).remove();
                                    }
                                });
                                // Cerramos modal de confirmación
                                modalBsBinacle.hide();
                                // Ocultamos loader
                                $modalConfirmationBinacle.find('.loading').addClass('d-none');
                            },
                        });
                    }

                });
            }

        });
    });

    // Cargar formulario crear thread
    $('#createThread').on('click', function (event) {
        event.preventDefault();

        $tabItems.each(function () {
            $(this).removeClass('active');
        });

        // cargar contenido
        let urlLink = $(this).attr('data-link');
        $("#v-pills-tabContent").load(urlLink, function () {
            $('body').on('click', '#createThreadForm input[type="submit"]', function (event) {
                event.preventDefault();
                $('#v-pills-tabContent .loading').removeClass('d-none');
                confirmationThreadModal('#createThreadForm');
            });
        });
    });

}

function confirmationThreadModal(form) {
    // Obtenemos url origin
    let urlApi = window.location.origin;
    let $form = $(form), formAction, actualMessages;

    actualMessages = {
        'title': 'Crear nuevo Tema',
        'description': 'Se ha creado el nuevo tema en bitácora.'
    };

    // Modal de confirmación
    let modalBsThread = bootstrap.Modal.getOrCreateInstance(document.getElementById('modalConfirmationThread')),
        $modalConfirmationThread = $('#modalConfirmationThread');

    // Acción formulario
    formAction = $form.attr('action');

    // Hacemos petición Ajax
    $.ajax({
        method: 'POST',
        url: `${urlApi}${formAction}`,
        data: $form.serialize(),
        success: function (res) {
            // Seteamos mensaje en el modal
            $modalConfirmationThread.find('.description').html(actualMessages["description"]);
            // Cambiamos icono del modal
            $modalConfirmationThread.find('.modal-alert__wrapper-icon').html(`<span class="icon-icon-check"></span>`);
        },
        error: function (jqXHR, estado, error) {
            // Seteamos mensaje en el modal
            $modalConfirmationThread.find('.description').html(`Ha ocurrido un error inesperado ${error}`);
            // Cambiamos icono del modal
            $modalConfirmationThread.find('.modal-alert__wrapper-icon').html(`<span class="icon-alert"></span>`);
        },
        complete: function (jqXHR, estado) {
            // Seteamos mensaje en el modal
            $modalConfirmationThread.find('.modal-title').html(actualMessages["title"]);
            // Ocultamos loader
            $('#v-pills-tabContent .loading').addClass('d-none');
            // Mostramos modal
            modalBsThread.show();
        },
    });

    // Escuchamos evento boton crear nuevo
    $('.create-new').on('click', function (event) {
        event.preventDefault();
        window.location.reload();
    });

}

function getEvaluationQuestions(){

    $('body').on('click', '.openEvaluationQuestions', function(event){
        event.preventDefault();
        // Obtener url para pedir preguntas
        let urlLink = $(this).attr('data-link');
        // Verificar si ya se evaluo o no
        let evAnswered = $(this).attr('data-answer');
        // Obtener id evaluación
        let evId = $(this).parents('.evTr').find('.evId').text().trim();
        // Obtener nombre solicitud
        let demandTitle = $(this).parents('.evTr').find('.evDemandTitle').text().trim();
        // Armamos mensajes modal
        let messages = {
            "title" : `Evaluación #${evId}`,
            "description" : `Evaluar la solicitud <b>${demandTitle}</b>`
        }

        // Modal
        let $modalEvaluationQuestions = $('#modalEvaluationQuestions');

        if($modalEvaluationQuestions.length > 0){
            let modalBsEvQuestions = bootstrap.Modal.getOrCreateInstance(document.getElementById('modalEvaluationQuestions'));

            // Seteamos mensaje en el modal
            $modalEvaluationQuestions.find('.modal-title').html(messages["title"]);
            $modalEvaluationQuestions.find('.description').html(messages["description"]);
            // Mostramos loader
            $modalEvaluationQuestions.find('.loading').removeClass('d-none');
            // Mostramos modal
            modalBsEvQuestions.show();
            
            // Añadimos formulario de preguntas al modal
            $('#questionsWrapper').load(`${urlLink} #answer`, function () {
                let $Questionsform = $('#questionsWrapper').find('form#answer');
                // Si ya se evaluo
                if(evAnswered === 'true'){
                    // Ocultamos boton evaluar del modal
                    $('.action-send-form').addClass('d-none');
                    // Deshabilitamos input radios
                    $Questionsform.find(':input').each(function (i, item) {
                        if ($(item).is(':radio')) {
                            $(item).prop('disabled', true);
                            $(item).addClass('radioinput');
                        }
                    });
                }else{
                    $('.action-send-form').removeClass('d-none');
                }
                // Quitamos loader
                $modalEvaluationQuestions.find('.loading').addClass('d-none');
                

                // Validamosformulario
                $Questionsform.validate({
                    errorPlacement: function (error, element) {
                        let type = $(element).attr("type");
                        if (type === "radio") {
                            error.appendTo(element.closest('div.content-radio'));
                        } else {
                            error.insertAfter(element);
                        }
                    },
                    highlight: function (element, errorClass, validClass) {
                        let type = $(element).attr("type");
                        if (type === "radio") {
                            $(element).closest('div.content-radio').addClass(errorClass);
                        } else {
                            $(element).addClass(errorClass);
                        }
                    },
                    unhighlight: function (element, errorClass, validClass) {
                        let type = $(element).attr("type");
                        if (type === "radio") {
                            $(element).closest('div.content-radio').removeClass(errorClass);
                        } else {
                            $(element).removeClass(errorClass);
                        }
                    },
                });

                // Escuchamos click para enviar form
                $('.action-send-form').on('click', function(event){
                    event.preventDefault();
                    // $Questionsform.trigger( "submit" );
                    // Si todo es valido se envia
                    if( $Questionsform.valid() ){
                        // Obtenemos url origin
                        let urlApi = window.location.origin;
                        // Hacemos petición Ajax
                        $.ajax({
                            method: 'POST',
                            url: `${urlApi}${urlLink}`,
                            data: $Questionsform.serialize(),
                            complete: function (jqXHR, estado) {
                                // console.log(estado);
                                location.reload();
                            },
                        });                        
                    }
                });

            });
        }
    });
}

function followDemandInventory() {
    // Funcion "Seguir Solicitud" | "Seguir inventario"
    if ($('#requestCardList').length) {
        // Mostramos opción de seguir
        $('.cards-activity-item-header .content-option').fadeIn();

        let urlApi = window.location.origin;
        let following;
        // Modal de confirmación
        let modalConfirmacionFollow = new bootstrap.Modal(document.getElementById('follow-demand'));
        let modalConfirm = $('#follow-demand');

        function requestOrInventory($selector) {
            // Verificamos si es solicitud o inventario
            let attr = $selector.attr('data-idsolicitud');
            if (typeof attr !== 'undefined' && attr !== false) {
                return {
                    'attribute': 'data-idsolicitud',
                    'url': 'seguir-solicitud',
                    'tipo': 'solicitud'
                };
            }
            attr = $selector.attr('data-idinventario');
            if (typeof attr !== 'undefined' && attr !== false) {
                return {
                    'attribute': 'data-idinventario',
                    'url': 'seguir-inventario',
                    'tipo': 'inventario'
                };
            }
        }

        function followTemplateTexts(follow, tipo, spantxt) {
            // Retorna los template Strings para el modal de confirmación
            let tipoSeguimiento = tipo === 'solicitud' ? "la solicitud" : "el inventario";
            // Si ya se sigue
            if (follow === 'True') {
                return {
                    'modalTitle': `Dejar de seguir ${tipoSeguimiento}`,
                    'modalDesc': `Está seguro que quiere dejar de seguir ${tipoSeguimiento} <strong><span>${spantxt}</span></strong>`
                };
            } else {
                return {
                    'modalTitle': `Seguir ${tipoSeguimiento}`,
                    'modalDesc': `Está seguro que quiere seguir ${tipoSeguimiento} <strong><span>${spantxt}</span></strong>`
                };
            }
        }

        function addLoading() {
            modalConfirm.css('pointer-events', 'none');
            modalConfirm.find('.loading__text').removeClass('d-none');
            modalConfirm.find('.loading__text--error').addClass('d-none');
            modalConfirm.find('.loading').addClass('d-flex');
            modalConfirm.find('.modal-header .btn-close-modal').attr('disabled', true)
        }

        function removeLoading() {
            setTimeout(() => {
                modalConfirm.css('pointer-events', 'auto');
                modalConfirm.find('.loading').removeClass('d-flex');
                modalConfirm.find('.modal-header .btn-close-modal').attr('disabled', false)
            }, 1000);
        }

        function removeLoadingError(message) {
            setTimeout(() => {
                modalConfirm.css('pointer-events', 'none');
                modalConfirm.find('.loading__text').addClass('d-none');
                modalConfirm.find('.loading__text--error').text(message).removeClass('d-none');
                modalConfirm.find('.modal-header .btn-close-modal').attr('disabled', true)
            }, 1000);
        }

        $('body').on('click', '.button-slider input', function (event) {
            event.preventDefault();
            // Verfificamos si se sigue
            following = $(this).attr('data-follow');
            // console.log('El data-following', following);
            let cardItem = $(this).closest('.cards-activity-item');
            let tipoSeguimiento = requestOrInventory($(this).closest('.cards-activity-item-header'));
            let idRequest = $(this).closest('.cards-activity-item-header').attr(tipoSeguimiento.attribute);
            let titleDemand = cardItem.find('.cards-activity-item-body .item-description').text().trimStart().trimEnd();
            // Obtenemos los textos para el modal
            let modalTexts = followTemplateTexts(following, tipoSeguimiento.tipo, titleDemand);
            // Seteamos titulo del modal
            $('#follow-demand').find('.modal-title').text(modalTexts.modalTitle);
            // Seteamos descripción del modal
            $('#follow-demand').find('.description').html(modalTexts.modalDesc);
            $('#follow-demand .btn-acept-modal').attr(tipoSeguimiento.attribute, idRequest);
            // Abrimos modal de confirmación
            modalConfirmacionFollow.show();
            // $('#follow-demand').modal('show');
        });

        // Evento click modal
        $('body').on('click', '#follow-demand .btn-acept-modal', function () {
            let tipoSeguimiento = requestOrInventory($(this));
            let idRequest = $(this).attr(tipoSeguimiento.attribute);
            let elementCard = $('#requestCardList .cards-activity-item-header[' + tipoSeguimiento.attribute + '=' + idRequest + ']');

            addLoading();

            $.ajax({
                type: 'GET',
                url: `${urlApi}/${tipoSeguimiento.url}/${idRequest}`,
                success: function (res) {
                    if (res.success === "True") {
                        // Si ya se seguía
                        if (following === "True") {
                            elementCard.removeClass('active');
                            elementCard.find('.button-slider input').prop('checked', false);
                            $('#follow-demand .btn-acept-modal').removeAttr(tipoSeguimiento.attribute);
                            elementCard.find('.button-slider input').attr('data-follow', 'False');
                        } else {
                            elementCard.addClass('active');
                            elementCard.find('.button-slider input').prop('checked', true);
                            $('#follow-demand .btn-acept-modal').removeAttr(tipoSeguimiento.attribute);
                            elementCard.find('.button-slider input').attr('data-follow', 'True');
                        }
                        // Cerramos modal de confirmación
                        // modalConfirmacionFollow.hide();
                        // removeLoading();
                    }
                    if (res.fail === "True") {
                        // elementCard.addClass('active');
                        // elementCard.find('.button-slider input').prop('checked', true);
                        $('#follow-demand .btn-acept-modal').removeAttr(tipoSeguimiento.attribute);
                        // elementCard.find('.button-slider input').attr('data-follow', 'True');

                        // Show modal of error
                        removeLoadingError("Error al enviar la notificación.");
                        // setTimeout(() => {
                        //     modalConfirmacionFollow.hide();
                        //     removeLoading();
                        // }, 4000);
                    }

                },
                error: function (XMLHttpRequest, textStatus, errorThrown) {
                    if (textStatus === "error") {
                        elementCard.removeClass('active');
                        elementCard.find('.button-slider input').prop('checked', false);
                        $('#follow-demand .btn-acept-modal').removeAttr(tipoSeguimiento.attribute);

                    }
                    removeLoadingError("Error inesperado.");
                    // setTimeout(() => {
                    //     modalConfirmacionFollow.hide();
                    //     removeLoading();
                    // }, 5000);
                },
                complete: function (jqXHR, estado) {
                    // Cerramos modal de confirmación
                    modalConfirmacionFollow.hide();
                    removeLoading();
                },
            });
        });
    }
}

function profilefilterSearchAccessRraa(){

    let isHeadUnit = false;
    let prevDataUser = '', prevDataInventory = '';
    let currentpage = 1;
    let $searchUser = $("#id_user");
    let $searchInventory = $("#id_inventory");
    
    function profilSearchAccessRraa(){

        $searchUser = $("#id_user");
        $searchInventory = $("#id_inventory");

        if($searchUser.length > 0){
            isHeadUnit = true;
            // Escuchamos cambios
            $searchUser.on('change', function () {
                prevDataUser = $(this).val();
            });
        }
        if($searchInventory.length > 0){
            // Escuchamos cambios
            $searchInventory.on('change', function () {
                prevDataInventory = $(this).val();
            });
        }
        // Seteamos data previa si la hay
        if(prevDataUser !== ''){
            $searchUser.val(prevDataUser);
        }
        if(prevDataInventory !== ''){
            $searchInventory.val(prevDataInventory);
        }

        // Array con los ids de selects para añadirles buscador
        let selectsAccessRraa = [
            "#id_inventory",
            "#id_user"
        ];
        // Añade buscador a los selects
        addSearchForSelects(selectsAccessRraa);

    }

    // Escuchamos click boton para buscar
    $('body').on('click', '#search-rra', function (event) {
        event.preventDefault();
        // Obtenemos url para hacer la peticion
        let urlLink = getUrlLink();
        // Hacemos la petición
        loadFilterAccess(urlLink);
    });

    // Escuchamos click enlaces paginador
    $('body').on('click', '.access-pagination .pagination a', function (event) {
        event.preventDefault();
        // Obtenemos número de página
        currentpage = $(this).attr('href').slice(-1);
        // Obtenemos url para hacer la peticion
        let urlLink = getUrlLink();
        // Hacemos la petición
        loadFilterAccess(urlLink);
    });

    // Escuchamos click boton limpiar filtros
    $('body').on('click', '#reset-rra', function (event) {
        event.preventDefault();
        // Borramos valores select y data previa
        $searchUser.val('');
        $searchInventory.val('');
        prevDataUser = '';
        prevDataInventory = '';
        currentpage = 1;
        // Obtenemos url para hacer la peticion
        let urlLink = getUrlLink();
        // Hacemos la petición
        loadFilterAccess(urlLink);
    });
    
    function getUrlLink(){
        // Obtenemos valores en campos
        let inventory = $("#id_inventory").val();
        let user = $("#id_user").val();
        let urlLink;
        if(isHeadUnit){
            urlLink = `/usuario/acceso-rraa/?inventory=${inventory}&user=${user}&page=${currentpage}`;
        }else{
            urlLink = `/usuario/acceso-registros/?inventory=${inventory}&page=${currentpage}`;
        }
        return urlLink;
    }

    function loadFilterAccess(urlLink){
        // Cargamos la data filtrada
        $("#groupsProfileMainContent").load(urlLink, function(){
            // llamamos recursivamente a la función, para escuchar cliks y eventos en los nuevos elementos insertados en el DOM
            profilSearchAccessRraa();
        });
    }

    profilSearchAccessRraa();

}

/*==================== UPDATE SELECT FROM URL ====================*/
function updateSelectFromURL(selectElement) {
    // Obtenemos el "name" del "select"
    let searchParametro = $(selectElement).attr('name');

    // Obtenemos los parametros de la URL
    let params = new URLSearchParams(document.location.search);

    // Obtenemos el valor del parametro de acuerdo al "select"
    let paramValue = params.get(searchParametro);

    // Si contiene valor
    if (paramValue) {
        // Asignamos "value" al select
        $(selectElement).val(paramValue).prop('selected', true);
        // Se selecciona la "option"
        $(selectElement).find('option[value=' + paramValue + ']').attr('selected', true);
    }
}


/*==================== SHOW TAG FILTER  ====================*/

/* A function that show the tag filter result. */
function showTagFilterResult() {
    if ($('.filter-primary-filterdesktop').length) {
        let contentShowFilter = $('.active-filters-show');
        let inputChecked = false;
        $('.filter-primary-filterdesktop input[type="checkbox"]').each(function () {
            if ($(this).prop("checked")) {
                inputChecked = true;
                let text = $(this).closest('label').text().trim();
                let idCheckbox = $(this).attr('id');

                let tagButton = `<div class="tag">
                                    <span class="tag-text">${text}</span>
                                    <button class="btn tag-button" data-id="${idCheckbox}">
                                        <span class="icon-close-icon"></span>
                                    </button>
                                </div>`;

                contentShowFilter.append(tagButton);
            }
        });

        // Para "Selects"
        let optionSelected = false;

        $('.filter-primary-filterdesktop select').each(function () {
            // Actualizamos el select según la URL
            updateSelectFromURL(this);
            let idSelect = $(this).attr('id');

            // Añadimos los tags

            // Obtenemos la opcion seleccionada
            let currentOption = $(this).find('option:selected')
            // Si no es opcion por defecto
            if (currentOption.val() !== "") {
                optionSelected = true;
                let text = currentOption.text();
                let valor = currentOption.val();

                let tagButton = `<div class="tag">
                                <span class="tag-text">${text}</span>
                                <button class="btn tag-button" data-optionval="${valor}" data-idselect="${idSelect}">
                                    <span class="icon-close-icon"></span>
                                </button>
                            </div>`;

                contentShowFilter.append(tagButton);

            }

        });

        // Para "date"
        $('.filter-primary-filterdesktop input[type="date"]').each(function(){
            let fecha = $(this).val();
            if(fecha !== ''){
                inputChecked = true;
                let iddate = $(this).attr('id');
                let message = $(this).parents('.input-field').find('.input-field-title').text().trim();

                let tagButton = `<div class="tag">
                                    <span class="tag-text">${message}: ${fecha}</span>
                                    <button class="btn tag-button" data-valdate="${fecha}" data-iddate="${iddate}">
                                        <span class="icon-close-icon"></span>
                                    </button>
                                </div>`;

                contentShowFilter.append(tagButton);
            }
        });

        if (inputChecked || optionSelected) {
            $('.active-filters .clear-filter').addClass('px-4');
        }
    }
}

/* A function that removes the tag filter result. */
function removeTagFilterResult() {
    if ($('.filter-primary-filterdesktop').length) {
        let buttonSubmit = $('#form-filter input[type="submit"]');

        // Remove tag of filter
        $('.active-filters .tag-button').on('click', function (e) {
            let idCheck = $(this).attr('data-id');
            if (typeof idCheck !== 'undefined' && idCheck !== false) {
                $('#' + idCheck + '').trigger('click');
            }
            // Para "selects"
            let valOption = $(this).attr('data-optionval');
            let idSelect = $(this).attr('data-idselect');
            if (typeof idSelect !== 'undefined' && idSelect !== false) {
                $('.filter-primary-filterdesktop select#' + idSelect).find(":selected").each(function () {
                    let valor = $(this).val();
                    if (valor === valOption) {
                        $(this).attr('selected', false);
                        $(this).parent('select').prop('selectedIndex', 0);
                    }
                });
            }
            // Para "date"
            let valDate = $(this).attr('data-valdate');
            let idDate = $(this).attr('data-iddate');
            if (typeof idDate !== 'undefined' && idDate !== false) {
                $('.filter-primary-filterdesktop #' + idDate).val('');
            }

            buttonSubmit.trigger('click');
        })

        // Clear filter
        $('.active-filters .clear-filter').on('click', function (e) {
            e.preventDefault()
            $('.active-filters-show').text('');
            $('.filter-primary-filterdesktop input[type="checkbox"]').each(function () {
                $(this).prop('checked', false);
            });
            // Para "selects"
            $('.filter-primary-filterdesktop select').find(":selected").each(function () {
                $(this).attr('selected', false);
                $(this).parent('select').prop('selectedIndex', 0);
            });
            // Para "date"
            $('.filter-primary-filterdesktop input[type="date"]').each(function(){
                $(this).val('');
            });

            buttonSubmit.trigger('click');
        })
    }
}

/*==================== CLEAR INPUT FILTER WITH LOAD PAGES  ====================*/

/* Clearing the input filter. */
function clearInputFilter() {
    if ($('#form-filter').length) {
        $('#form-filter input[type="text"]').val('')
    }
}

/*==================== FILTER ORDER BY ====================*/

function sendFilterOrderBy() {
    // Comprobamos que exista el formulario de filtros lateral
    if ($('.filter-primary-filterdesktop').length) {
        let $orderBySelect = $('.block-result-header .order-by select');
        let $buttonSubmit = $('#form-filter input[type="submit"]');

        // Asociamos "select" con el formulario de filtros
        $orderBySelect.attr('form', 'form-filter');

        // Actualizamos select según URL
        updateSelectFromURL($orderBySelect);

        // Escuchamos cambios en el select
        $orderBySelect.on('change', function () {
            $buttonSubmit.trigger('click');
        });
    }
}

/*==================== FORMS VALIDATIONS ====================*/

function validateLoginForm() {
    // Initialize form validation on the registration form.
    // It has the name attribute "registration"
    if ($("form#login-form").length > 0) {
        const capctchaValiation = () => {
            let response = grecaptcha.getResponse();
            if (response.length == 0) {
                // console.log("error")
                $(".login-screen .container-fluid .row .card-container form.login-form .captcha-container #label-captcha").addClass("active");
                return false;
            } else {
                // console.log("success")
                return true;
            }
        }

        // hidden and show password
        $("#login-form .input-container.password .icon-password").on("click", function () {
            if ($(this).hasClass("icon-eye-blocked")) {
                $(this).removeClass("icon-eye-blocked").addClass("icon-eye");
                $(this).closest('.input-container').find('input').attr("type", "text");
            } else if ($(this).hasClass("icon-eye")) {
                $(this).removeClass("icon-eye").addClass("icon-eye-blocked");
                $(this).closest('.input-container').find('input').attr("type", "password");
            }
        });

        $.validator.addMethod("emailValidate", function (value, element) {
            if (/^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/i.test(value)) {
                return true;
            } else {
                return false;
            };
        }, "Ingrese un correo electrónico válido");

        $("form#login-form").validate({
            // Specify validation rules
            rules: {
                // The key name on the left side is the name attribute
                // of an input field. Validation rules are defined
                // on the right side
                remember_me: {
                    checked: false,
                    required: false,
                },
                username: {
                    required: true,
                    // Specify that email should be validated
                    // by the built-in "email" rule
                    // email: true,
                    emailValidate: true
                },
                password: {
                    required: true,
                    minlength: 5
                },

            },
            // Specify validation error messages
            messages: {

                password: {
                    required: "Ingrese su contraseña",
                    minlength: "Mínimo 5 caracteres"
                },
                username: "Ingrese un correo válido",

            },
            // Make sure the form is submitted to the destination defined
            // in the "action" attribute of the form when valid
            submitHandler: function (form) {
                if (capctchaValiation()) {
                    $('header .user-actions .btn-user-login').css('pointer-events', 'none');
                    $('.loading').removeClass('d-none');
                    localStorage.removeItem('tabProfile');
                    form.submit();
                }
            }
        });
        if ($(".error-forms p").text() !== "") {
            $("form#login-form").addClass("error-forms")
        }
    }
}

/*==================== IDENTIFY STEPS & STEPS TITLES ====================*/
function identifySteps() {
    $(".create-provider .container .row .col-md-4 .container-steps .step").each(function (i, value) {
        $(this).attr("id", `step-${i}`)
    })

    $(".create-provider .container .row .col-md-4 .container-steps .step .step-title").each(function (i, value) {
        $(this).attr("id", `step-${i}`)
    })

    $(".create-provider .container .row .col-md-4 .container-steps .step .step-title").on('click', function (e) {
        let step = $(this).attr("id")
        // console.log(step)
        $(`.create-provider .container .row .col-md-4 .container-steps .step.active`).removeClass("active")
        $(`.create-provider .container .row .col-md-4 .container-steps .step#${step}`).addClass("active")
    })


    $(".create-provider .container .row .col-md-7 form .container-buttons input#continuar").on('click', function (e) {

        let InputsStep1 = $('.create-provider .container .row .col-md-7 form.demand-create  .step1 .input-container input').map(function () {
            return $(this).val();
        }).get();
        let emptyInputsStep1 = InputsStep1.filter(function (el) {
            return el !== "";
        });
        if (emptyInputsStep1.length <= 0) {
            $(".create-provider .container .row .col-md-7 form .input-container p.auth-error").addClass("active")
            $('.create-provider .container .row .col-md-7 form.demand-create  .step1 .input-container input').addClass("error")
            $('.create-provider .container .row .col-md-7 form.demand-create  .step1 .input-container select').addClass("error")
        } else {
            $(".create-provider .container .row .col-md-7 form .container-buttons input#volver").addClass("active")
            $(".create-provider .container .row .col-md-7 form .input-container p.auth-error").removeClass("active")
            $(".create-provider .container .row .col-md-7 form .container-step.active.step1").removeClass("active")
            $(".create-provider .container .row .col-md-7 form .container-step.step2").addClass("active")
            $(`.create-provider .container .row .col-md-4 .container-steps .step#step-0.active`).removeClass("active")
            $(`.create-provider .container .row .col-md-4 .container-steps .step#step-1`).addClass("active")
        }
    });

    $(".create-provider .container .row .col-md-7 form .container-buttons input#volver").on('click', function (e) {
        // console.log("click")
        $(".create-provider .container .row .col-md-7 form .container-step.active.step2").removeClass("active")
        $(".create-provider .container .row .col-md-7 form .container-step.step1").addClass("active")
        $(`.create-provider .container .row .col-md-4 .container-steps .step#step-1.active`).removeClass("active")
        $(`.create-provider .container .row .col-md-4 .container-steps .step#step-0`).addClass("active")
    });
}

/*==================== TAB ACTIVE ON PAGE RELOAD ====================*/

function setActiveTab() {

    // Verificamos que existan tabs
    if ($('a[data-bs-toggle="tab"]').length) {
        let tabEls = document.querySelectorAll('a[data-bs-toggle="tab"]')
        tabEls.forEach(tab => {

            tab.addEventListener('shown.bs.tab', function (event) {
                event.target // newly activated tab
                event.relatedTarget // previous active tab    
                sessionStorage.setItem('activeTab', $(event.target).attr('href'));
            });
        });

        let activeTab = sessionStorage.getItem('activeTab');
        if (activeTab) {
            let tabEl = document.querySelector('.nav-tabs a[href="' + activeTab + '"]');
            let tab = new bootstrap.Tab(tabEl);
            tab.show();

            // Añadimos animación de scroll hacia la pestaña activa
            tabEl.scrollIntoView({
                block: 'nearest',
                behavior: 'smooth',
                inline: 'center'
            });
        }
    }
}

/*==================== COPY EMAIL TO CLIPBOARD ====================*/

function copyEmailParticipante() {
    if ($('.card-type-participants').length) {
        let tooltipList = '';

        function initTooltip() {
            let tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
            tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
                return new bootstrap.Tooltip(tooltipTriggerEl)
            });
        }
        initTooltip();

        function destroyTooltip() {
            tooltipList.forEach(tooltip => {
                tooltip.dispose();
            });

            initTooltip();
        }


        $('.card-type-participants .btn-copy').on('click', function (e) {
            e.preventDefault();
            let email = $(this).closest('.participant-data-email').find('.participant-email').text().trim();
            navigator.clipboard.writeText(email);

            $(this).attr('data-bs-title', 'Copiado');
            destroyTooltip();
            let tooltipCopied = new bootstrap.Tooltip($(this));
            tooltipCopied.show();

            setTimeout(() => {
                $(this).attr('data-bs-title', 'Copiar');
                tooltipCopied.hide();
                destroyTooltip();
            }, 5000);
        });
    }

}

/*==================== MULTI LIST INPUT ====================*/

function createMultiList() {
    $('.form__element--multilist input[type="text"]').flexdatalist({
        selectionRequired: true,
        multiple: true,
        minLength: 0,
        maxShownResults: 7,
        noResultsText: 'No se encontraron resultados para "{keyword}"',
    });

    $('.form__element.form__element--flexdatalist input[type="text"]').flexdatalist({
        selectionRequired: true,
        noResultsText: 'No se encontraron resultados para "{keyword}"',
    })
}

function addStyleScrollFormDatalist() {
    $('body').on('show:flexdatalist.results', function (event, itens) {
        $('.flexdatalist-results').addClass('style-scrooll');
        $('.form__field.select-with-flexdatalist .flexdatalist-multiple').addClass('style-scrooll');
    });
}

/*==================== FUNCTIONS BOX RESULT ====================*/

// Show and hide acordion of box result
function boxResultAccordion() {
    if ($('#accordionActivityManagement').length) {
        // Show accordion active
        let pathnameActivity = location.pathname.split('/');
        let nameActivityCurrent = pathnameActivity[pathnameActivity.length - 2];
        $('.result-box-body .accordion-item').each(function () {
            if ($(this).attr('data-accordion-item') == nameActivityCurrent) {
                $(this).attr('data-active', 'active');

                $(this).find('.accordion-button').removeClass('collapse').attr('aria-expanded', 'true');
                $(this).find('.accordion-collapse').addClass('show');

                // Grab height of fixed header
                let headHeight = $('header').outerHeight();

                // Animamos scroll hacia el acordeon activo
                $('html, body').animate({
                    scrollTop: $(this).offset().top - headHeight - 20
                }, 800);

                setTimeout(() => {
                    $('#accordionActivityManagement .loading').addClass('d-none');
                }, 1000);

            } else {
                $(this).find('.accordion-button').addClass('collapsed').attr('aria-expanded', false);
                $(this).find('.accordion-collapse').removeClass('show');
            }
        })


        // Enable the second accordion panel
        function enableSecondAccordion() {
            $('#accordionActivityManagement .accordion-item:nth-child(2) .accordion-button').attr('disabled', false).css('pointer-events', 'auto');
        }
        // enableSecondAccordion();

        // show previous acordion
        function showPreviousAccordion() {
            let parentAcordion = $('#accordionActivityManagement');
            let acordionCurrent = parentAcordion.find('.accordion-item .accordion-button').not('.collapsed');
            let acordionFirst = parentAcordion.find('.accordion-item:first-child .accordion-button');

            if (acordionCurrent.attr('data-bs-target') !== acordionFirst.attr('data-bs-target')) {
                let acordionItemCurrent = acordionCurrent.closest('.accordion-item');
                let acordionPrev = acordionItemCurrent.prev();

                acordionItemCurrent.find('.accordion-header .accordion-button').addClass('collapsed').attr('aria-expanded', false);
                acordionItemCurrent.find('.accordion-collapse').removeClass('show');

                acordionPrev.find('.accordion-header .accordion-button').removeClass('collapsed').attr('aria-expanded', true);
                acordionPrev.find('.accordion-collapse').addClass('show');
            }
        }

        // Modify message jquery validation
        $.extend($.validator.messages, {
            required: "Este campo es obligatorio.",
        });

        // Show subprocess of process
        let nameSubprocess = $('.result-box-body').attr('data-name');
        if (nameSubprocess !== undefined || nameSubprocess !== '') {
            $('#progressbar [data-name="' + nameSubprocess + '"]').addClass('current');
            $('.container-steps-forms .content-step[data-name="' + nameSubprocess + '"]').addClass('active');

            // Show subprocess completed
            $('#progressbar .progressbar-step').each(function () {
                if ($(this).hasClass('current')) {
                    return false;
                } else {
                    $(this).addClass('is-done');
                }
            })

            if (nameSubprocess === "demand-validation" && $('#formStep1 select option:selected').val() === "de") {
                let modalShowStatesProcess = new bootstrap.Modal(document.querySelector('#showStatesProcess'));

                let modalStatesProcess = $('#showStatesProcess');
                modalStatesProcess.find('.modal-header .modal-title').text('Estado de Recepción');
                modalStatesProcess.find('.modal-body .description').html('En estos momentos el estado de recepción se encuentra rechazado. <strong>¿Desea cambiar el estado de la recepción?</strong>');
                let urlDetailsMP = $('nav[aria-label=breadcrumb] .breadcrumb-item.active').prev().find('a').attr('href');

                modalStatesProcess.find('.btn-close-modal').on('click', function (e) {
                    e.preventDefault();
                    modalShowStatesProcess.hide();
                    $('.loading').removeClass('d-none');
                    window.location.href = `${window.location.origin}${urlDetailsMP}`;
                });

                modalStatesProcess.find('.btn-acept-modal').on('click', function (e) {
                    e.preventDefault();
                    modalShowStatesProcess.hide();
                })

                setTimeout(() => {
                    modalShowStatesProcess.show();
                }, 1100);

            }
        }

        // Validate form of process
        function validateFormProcess(nameForm) {
            $("#" + nameForm + "").validate({
                errorElement: "label",
                errorPlacement: function (error, element) {
                    let type = $(element).attr("type");
                    if (type === "radio") {
                        error.insertAfter(element.closest('div.content-radio'));
                    } else {
                        error.insertAfter(element);
                    }
                },
                highlight: function (element, errorClass, validClass) {
                    let type = $(element).attr("type");
                    if (type === "radio") {
                        $(element).closest('div.content-radio').addClass(errorClass);
                    } else {
                        $(element).addClass(errorClass);
                    }
                },
                unhighlight: function (element, errorClass, validClass) {
                    let type = $(element).attr("type");
                    if (type === "radio") {
                        $(element).closest('div.content-radio').removeClass(errorClass);
                    } else {
                        $(element).removeClass(errorClass);
                    }
                },
                onkeyup: function (element) {

                    if (!this.checkable(element) && (element.name in this.submitted || !this.optional(element))) {
                        this.element(element);
                    }
                },
                submitHandler: function (form) {
                    form.submit();
                },
                rules: {
                    /* recepción/proceso*/
                    // Paso 3: Notificación Solicitud
                    comment: {
                        maxlength: 300, // máx 300 caracteres
                    },
                    /* recepción revision */
                    comment_revision: {
                        maxlength: 300, // máx 300 caracteres
                    },
                    /* recepción finalizado */
                    comment_finalized: {
                        maxlength: 300, // máx 300 caracteres
                    },
                    /* relacionamiento/proceso */
                    // Paso 5: Estructuración del Convenio
                    consideration: {
                        maxlength: 35, // máx 35 caracteres
                    },
                }
            });
        }

        // Show avance of activity and show next form
        $('.btn-form-continue').on('click', function (e) {

            // Validate if have subprocess
            let nameSubprocess = $('.result-box-body').attr('data-name');
            if (nameSubprocess !== undefined && nameSubprocess !== '') {
                let nameSubprocessCurrent = $(this).closest('.content-step').attr('data-name');
                if (nameSubprocessCurrent === nameSubprocess) {
                    let nameForm = $(this).closest('form').attr('id');
                    validateFormProcess(nameForm);
                } else {
                    e.preventDefault();
                    let parentContent = $(this).closest('.content-step'),
                        StepCurrent = $('#progressbar .current'),
                        StepNext = StepCurrent.next();
                    // let StepLast = $('#progressbar .progressbar-step:last-child');

                    StepCurrent.removeClass('current').addClass('is-done');
                    StepNext.addClass('current');
                    parentContent.removeClass('active');
                    parentContent.next().addClass('active');

                }

            } else {
                // Esta en un proceso normal

                let nameProcess = $(this).closest('.accordion-item').attr('data-active');
                if (nameProcess !== undefined && nameProcess === 'active') {
                    let nameForm = $(this).closest('form').attr('id');
                    validateFormProcess(nameForm);
                }
            }

        });

        // Show back of activity and show previous form
        $('.btn-form-back').on('click', function (e) {
            e.preventDefault();
            let containerSteps = $(this).closest('.container-steps');

            // Verificar si es el boton para regresar al anterior acordeon
            if ($(this).hasClass('btn-accordeon-back')) {
                // Obtenemos el pathname
                let urlPathName = window.location.pathname;

                // Creamos array de strings
                urlPathName = urlPathName.split('/');
                // Filtramos eliminando elementos del array vacios
                urlPathName = urlPathName.filter((el) => {
                    return el != '';
                });

                if (urlPathName.indexOf('proceso') >= 0) {
                    // Eliminamos del array el ultimo elemento ('proceso'), y añadimos al final del array ('inicio')
                    urlPathName.pop();
                    urlPathName.push('inicio');
                } else if (urlPathName.indexOf('revision') >= 0) {
                    urlPathName.pop();
                    urlPathName.push('proceso');
                } else if (urlPathName.indexOf('finalizado') >= 0) {
                    urlPathName.pop();
                    urlPathName.push('revision');
                }

                // Volvemos a convertir a string
                urlPathName = urlPathName.toString();
                // Cambiamos ',' por '/'
                urlPathName = urlPathName.replaceAll(',', '/');
                urlPathName = '/' + urlPathName + '/';

                // Creamos una nueva URL
                let url = window.origin + urlPathName;
                url = new URL(window.origin + urlPathName);

                // Seteamos los parametros
                url.searchParams.set('regresar', true);

                // Redireccionamos a la nueva url
                window.location.href = url;
            }

            if (containerSteps.find('#progressbar').length) {
                let parentContent = $(this).closest('.content-step');
                let StepCurrent = $('#progressbar .current');
                let StepFirst = $('#progressbar .progressbar-step:first-child');

                if (StepCurrent.attr('id') !== StepFirst.attr('id')) {
                    let StepPrev = StepCurrent.prev();
                    StepCurrent.removeClass('current');
                    StepPrev.removeClass('is-done').addClass('current');

                    parentContent.removeClass('active');
                    parentContent.prev().addClass('active');

                    // Animamos scroll hacia el contentspet activo
                    let headHeight = $('header').outerHeight();
                    $('html, body').animate({
                        scrollTop: parentContent.prev().offset().top - headHeight - 40
                    }, 100);

                } else {
                    showPreviousAccordion();
                    // enableSecondAccordion();
                }
            }

            if (containerSteps.find('.card-informative-left').length) {
                showPreviousAccordion();
            }
        });

        MPAcordeonNav();
    }
}

function MPAcordeonNav() {
    // Cambia el enlace del acordeon por un boton para que funcione el acordeon activo
    let urlPathName = window.location.pathname;
    // Creamos array de strings según URL
    urlPathName = urlPathName.split('/');

    let datosMP = {
        'inicio': {
            'data-bs-target': '#initiation',
            'aria-controls': 'initiation',
            'text': 'Inicio'
        },
        'proceso': {
            'data-bs-target': '#process',
            'aria-controls': 'process',
            'text': 'En proceso'
        },
        'revision': {
            'data-bs-target': '#review',
            'aria-controls': 'review',
            'text': 'En revisión'
        },
        'finalizado': {
            'data-bs-target': '#finalized',
            'aria-controls': 'finalized',
            'text': 'Finalizado'
        }
    };

    function changeLinkWithButton(link, data) {
        $(link).html(`<button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="${data['data-bs-target']}" aria-expanded="true" aria-controls="${data['aria-controls']}">${data['text']}</button>`);
    }

    if (urlPathName.indexOf('inicio') >= 0) {
        changeLinkWithButton('#accordion-initiation', datosMP['inicio']);
    } else if (urlPathName.indexOf('proceso') >= 0) {
        changeLinkWithButton('#accordion-process', datosMP['proceso']);
    } else if (urlPathName.indexOf('revision') >= 0) {
        changeLinkWithButton('#accordion-review', datosMP['revision']);
    } else if (urlPathName.indexOf('finalizado') >= 0) {
        changeLinkWithButton('#accordion-finalized', datosMP['finalizado']);
    }
}

/*==================== RECEPTION FUNCTIONS ====================*/

// Guarda datos en Local storage para que persistan al hacer otras acciones
function persistentReceptionData() {
    if ($('#accordionActivityManagement').length) {

        // "En Proceso" Paso 2 - "Verificación y Completitud"
        if ($('.demand-reception #formStep2 input[name="demand_assessment"]').length > 0) {
            // Indicamos la clave a buscar en LocalStorage
            const claveLocal = 'demandReceptionStep2';
            // Selectores de los campos a guardar en localStorage
            let selectorFields = [".demand-reception #formStep2 input[name='demand_assessment']"];

            // Guarda en LocalStorage los campos del form del "paso 5:Estructuración del convenio"/"Proceso"
            setAndGetLocalStorageDemandData(selectorFields, claveLocal);
        }

        // "En Proceso" Paso 3 - "Notificación Solicitud"
        let $inputDateTentPres = $('#id_date_tentative_presentation');
        if ($inputDateTentPres.length) {

            // Obtenemos id solicitud
            let demandId = $inputDateTentPres.closest('form').attr('data-iddemand');

            // Verfificamos que se encuentre en ese sub-proceso
            let nameSubprocess = $('.result-box-body').attr('data-name');
            if (nameSubprocess === 'demand-notification') {
                // Escuchamos cambios en input fecha
                $inputDateTentPres.on('change', function () {
                    // Obtenemos fecha seleccionada
                    let selectedDate = $(this).val();
                    // Creamos objeto con id solicitud y fecha seleccionada
                    let objSelected = {
                        "demandId": demandId,
                        "dateVal": selectedDate
                    }
                    // Guardamos en localStorage(string)
                    // localStorage.setItem('demandDateTentativePresentation', JSON.stringify(objSelected));
                    // Guardamos clave por 2 semanas = 1209600000 milisegundos
                    setWithExpiry('demandDateTentativePresentation', objSelected, 1209600000);
                });
            }

            // Si existe valor seleccionado previamente, se marca
            // let prevSelectedVal = localStorage.getItem('demandDateTentativePresentation');
            let prevSelectedVal = getWithExpiry('demandDateTentativePresentation');
            if (prevSelectedVal) {
                // Convertimos string a objeto
                let prevSelectedObj = JSON.parse(prevSelectedVal);
                // Verificamos que el id de la solicitud corresponda con el guardado
                if (prevSelectedObj.demandId === demandId) {
                    $inputDateTentPres.val(prevSelectedObj.dateVal);
                }
            }
        }
    }

}

function addCharacterCountReception(){
    // Recepción Proceso
    // array con selectores de los campos a añadirles contador de caracteres
    const fields = [
        '#id_comment',
        '#id_comment_revision',
        '#id_comment_finalized'
    ];
    // Añadimos contador de caracteres
    addCharacterCounter(fields);
}

function allReceptionFunctions() {
    persistentReceptionData();
    addCharacterCountReception();
}

/*==================== TRANSFER FUNCTIONS ====================*/

function validateTransferBeginform() {
    if ($('#transferBeginform').length > 0) {
        $('#transferBeginform').validate({
            rules: {
                number_deliveries: {
                    required: true,
                    // number: true
                },
                date_delivery: {
                    required: true
                },
                comment: {
                    required: true,
                    maxlength: 600, //máx 600 caracteres
                },
            },
            messages: {
                number_deliveries: {
                    required: 'Este campo es requerido, ejemplo: 1 de 3',
                    // number: 'Solo se permiten números'
                }
            },
            errorClass: 'error-validacion', // Clase para las alertas de validación
            errorElement: 'p', // Elemento "html" para mostrar el error
        });
    }
}

function validateTransferReview() {
    // Valida modal revisar transferencia
    if ($('.form-review-transfer').length > 0) {
        $('.form-review-transfer').each(function () {
            $(this).validate({
                rules: {
                    date_review: {
                        required: true
                    },
                    hour_review: {
                        required: true
                    },
                    open_base: {
                        required: true
                    },
                    expected_size: {
                        required: true
                    },
                    meets_terms: {
                        required: true
                    },
                    approve_reception_bd: {
                        required: true
                    },
                    comment_review: {
                        required: true,
                        maxlength: 800, //máx 800 caracteres
                    },
                },
                errorClass: 'error-validacion', // Clase para las alertas de validación
                errorElement: 'p', // Elemento "html" para mostrar el error
            });
        });
    }
}

function transferIsReviewed(button) {
    return $(button).attr('data-name') === 'False';
}

function reviewTransfer() {
    let $reviewBtns = $('.list-of-transfer-item-column.col-buttons button.review');
    // Verificamos que estemos en el acordeon indicado y que los elementos existan
    if (($('#accordionActivityManagement .accordion-item[data-active="active"]').attr('data-accordion-item') === 'revision') && ($reviewBtns.length > 0)) {

        // Obtenemos todos los botones de "revisar" y convertimos ese objeto a array
        let reviewTransferBtns = $.map($reviewBtns, function (value, index) {
            return [value];
        });
        // Deshabilitamos submit
        let $submitBtn = $('#reviewTransferForm input[type="submit"]');
        $submitBtn.prop('disabled', true);
        // Obtenemos enlace del acordeon "finalizado"
        let $finalizedAccordionLink = $('#accordion-finalized a'),
            finalizedAccordionHref = $finalizedAccordionLink.attr('href');

        // Si ninguna se ha revisado
        if (reviewTransferBtns.every(transferIsReviewed) === true) {
            $submitBtn.prop('disabled', true);
            $finalizedAccordionLink.attr('href', '');
        } else {
            $submitBtn.prop('disabled', false);
            $finalizedAccordionLink.attr('href', finalizedAccordionHref);
        }

    }
}

function confirmTransfer() {
    // Encargado de abrir el modal de confirmación de transferencia
    // enviado el id del formulario y del modal anterior
    $('.finalizeTransferOpenModal').on('click', function (event) {
        event.preventDefault();

        // Obtenemos id formulario
        let idForm = $(this).attr('data-form-id');
        // Validamos campos formulario
        validateFormFinalizedTransfer('#formFinalizedTransfer-' + idForm);
        // Obtenemos instancia de este modal
        let firstModal = bootstrap.Modal.getOrCreateInstance(document.getElementById('modalFinalizedTransfer-' + idForm));

        // Si el formulario es valido abrimos el modal de confirmación
        if ($('#formFinalizedTransfer-' + idForm).valid()) {
            // Modal de confirmación
            let myModal = new bootstrap.Modal(document.getElementById('modalConfirmationTransfer'));
            // Obtenemos boton submit
            let $btnSubmitform = $('#modalConfirmationTransfer input[type="submit"]');

            // Obtenemos btn volver
            $('#modalConfirmationTransfer .btn[aria-label="Volver"]').attr('data-bs-target', '#modalFinalizedTransfer-' + idForm);

            // Asociamos submit con formulario
            $btnSubmitform.attr('form', 'formFinalizedTransfer-' + idForm);
            // Cerramos modal anterior
            firstModal.hide();
            // Abrimos modal de confirmación
            myModal.show();
        }

    });
}

function transferIsFinalize(button) {
    return $(button).attr('data-name') === 'False';
}

function finalizeTransferContinue() {
    let $finalizeBtns = $('.list-of-transfer-item-column.col-buttons button.finalize');
    // Verificamos que estemos en el acordeon indicado y que los elementos existan
    if (($('#accordionActivityManagement .accordion-item[data-active="active"]').attr('data-accordion-item') === 'finalizado') && ($finalizeBtns.length > 0)) {
        // Obtenemos todos los botones de "finalizar" y convertimos ese objeto a array
        let finalizeTransferBtns = $.map($finalizeBtns, function (value, index) {
            return [value];
        });
        // Deshabilitamos "Continuar"
        let $submitBtn = $('#finalizeTransferContinue input[type="submit"]');
        $submitBtn.prop('disabled', true);

        // Si ninguna se ha revisado
        if (finalizeTransferBtns.every(transferIsFinalize) === true) {
            $submitBtn.prop('disabled', true);
        } else {
            $submitBtn.prop('disabled', false);
        }
    }
}

function setMonthURLParams(select) {
    // Obtenemos la opción seleccionada
    let selectedOptionVal = $(select).find(":selected").val();
    // Obtenemos la URL
    let url = new URL(window.location);
    let params = new URLSearchParams(url.search);

    if (selectedOptionVal !== '') {
        // Seteamos los parametros en la URL (key=value)
        params.set('month', selectedOptionVal);
        window.location.search = params;
    } else {
        params.delete('month');
        window.location.search = params;
    }
}

function getMonthSelected() {
    // Obtenemos el "select" donde escogemos el mes de la transferencia
    let $selectsMonth = $('.demand-transfer select[name="month"]');

    // setMonthURLParams($selectMonth);

    $selectsMonth.each(function () {
        updateSelectFromURL(this);

        $(this).on('change', function () {
            setMonthURLParams(this);
        });
    });
}

function validateFormFinalizedTransfer(formId) {
    $(formId).validate({
        rules: {
            'finalized-hour-transfer': {
                required: true
            },
            'finalized-date-transfer': {
                required: true
            },
            'finalize_comment': {
                required: true,
                minlength: 4,
                maxlength: 800,
            },
        },
        errorClass: 'error-validacion', // Clase para las alertas de validación
        errorElement: 'p', // Elemento "html" para mostrar el error
    });
}

function allTransferFunctions() {
    validateTransferBeginform();
    reviewTransfer();
    validateTransferReview();
    confirmTransfer();
    getMonthSelected();
    finalizeTransferContinue();
}

/*==================== DEMAND LOCAL STORAGE UTILITIES ====================*/

function setWithExpiry(key, value, ttl) {
	const now = new Date();

	// `item` is an object which contains the original value
	// as well as the time when it's supposed to expire
	const item = {
		value: value,
		expiry: now.getTime() + ttl,
	}
	localStorage.setItem(key, JSON.stringify(item));
}

function getWithExpiry(key) {
	const itemStr = localStorage.getItem(key);
	// if the item doesn't exist, return null
	if (!itemStr) {
		return null;
	}
	const item = JSON.parse(itemStr);
	const now = new Date();
	// compare the expiry time of the item with the current time
	if (now.getTime() > item.expiry) {
		// If the item is expired, delete the item from storage
		// and return null
		localStorage.removeItem(key);
		return null;
	}
	return item.value;
}

function getPrevLocalStorageDemandData(claveSearch) {
    /*  Funcion para verificar si hay data en localStorage
        claveSearch --> la clave a buscar en LocalStorage
        retorna un array de objetos con la data guardada o array vacio
    */
    // Verificar si hay data en LocalStorage
    // let prevLocalData = localStorage.getItem(claveSearch);
    let prevLocalData = getWithExpiry(claveSearch);
    let prevDataArrObj;
    if (prevLocalData) {
        // Convertimos string a array de objetos
        // prevDataArrObj = JSON.parse(prevLocalData);
        prevDataArrObj = prevLocalData;
    } else {
        prevDataArrObj = [];
    }
    return prevDataArrObj;
}

function setPrevLocalStorageDemandData(prevDataArrObj, currentDemandId, currentSelectorField) {
    /*  Funcion para actualizar los campos del form con data previamente guardada
        prevDataArrObj --> corresponde a la data anterior
        currentDemandId --> id de solicitud actual
        currentIdField --> id del campo para Actualizar
    */
    // Verificamos que el array tenga algo
    if (prevDataArrObj.length > 0) {
        prevDataArrObj.forEach((demand) => {
            // Si el objeto corresponde al id de la solicitud actual
            if (demand.demandId === currentDemandId) {
                // Si en el obj solicitud, existe el campo, se actualiza en el DOM
                if (demand.fields[currentSelectorField]) {
                    // Obtenemos campo por "id"
                    let $field = $('#' + demand.fields[currentSelectorField]["fieldId"]);
                    // si el elemento es radio asignamos el checked
                    if ($field.is(':radio')) {
                        $field.prop('checked', 'true');
                    } else {
                        // Es otro elemento, asignamos el value
                        $field.val(demand.fields[currentSelectorField]["fieldValue"]);
                    }
                }
            }
        });
    }
}

function setAndGetLocalStorageDemandData(arraySelectorFields, claveLocal) {
    /*  Funcion para:
            - guardar en localStorage
            - actualizar campos DOM con data de localStorage

        arraySelectorFields --> array de selector de los campos
        claveLocal --> clave de localStorage para buscar/actualizar

        NOTA: necesita poner en el formulario el atributo 'data-iddemand'
    */

    // Ejecutamos por cada campo
    arraySelectorFields.forEach((selectorfield) => {

        // Verificar que el campo exista
        if ($(selectorfield).length) {
            // Obtenemos id solicitud
            let demandId = $(selectorfield).closest('form').attr('data-iddemand');

            // Obtenemos la data previamente guardada o un array vacio si no existe
            let prevDataArrObj = getPrevLocalStorageDemandData(claveLocal);

            // Actualizamos en el DOM la data previamente guardada
            setPrevLocalStorageDemandData(prevDataArrObj, demandId, selectorfield);

            // Escuchamos cambios campo
            $(selectorfield).on('change', function () {
                let fieldValue = $(this).val(),
                    fieldId = $(this).attr('id');

                // Verificar si id de solicitud existe en dataLocal
                let existingDemand = false;
                // Para settear data previamente guardada o la nueva si no existe
                let prevDataArrObj = getPrevLocalStorageDemandData(claveLocal);
                // Si existe data anterior
                if (prevDataArrObj.length > 0) {
                    prevDataArrObj.forEach((demand) => {
                        // Si el objeto corresponde al id de la solicitud actual
                        if (demand.demandId === demandId) {
                            demand.fields[selectorfield] = {
                                "fieldId": fieldId,
                                "fieldValue": fieldValue
                            };
                            existingDemand = true;
                        }
                    });
                }
                // Si no existia solicitud en la dataLocal
                if (!existingDemand) {
                    let currentObject = {
                        "demandId": demandId,
                        "fields": {}
                    };
                    currentObject.fields[selectorfield] = {
                        "fieldId": fieldId,
                        "fieldValue": fieldValue
                    };
                    prevDataArrObj.push(currentObject);
                }

                // Guardamos en localStorage(string)
                // localStorage.setItem(claveLocal, JSON.stringify(prevDataArrObj));
                // Guardamos clave por 2 semanas = 1209600000 milisegundos
                setWithExpiry(claveLocal, prevDataArrObj, 1209600000);

            });
        }
    });
}

function deleteDemandMPLocalStorage() {
    /* MP 1 : Recepción */
    // Si estamos en: Recepción|Revisión
    if ($('.demand-reception .accordion-item[data-active="active"]').attr('data-accordion-item') === 'revision') {
        // Indicamos la clave a borrar
        localStorage.removeItem('demandReceptionStep2');
        localStorage.removeItem('demandDateTentativePresentation');
    }

    /* MP 2 : Relacionamiento (negociación) */
    // Si estamos en : Relacionamiento|Revisión
    if ($('.demand-relation .accordion-item[data-active="active"]').attr('data-accordion-item') === 'revision') {
        // Borramos data acordeon anterior (proceso)
        localStorage.removeItem('demandNegotiationStep5');
    }
    // Si estamos en : Relacionamiento|Finalizado
    if ($('.demand-relation .accordion-item[data-active="active"]').attr('data-accordion-item') === 'finalizado') {
        // Borramos data acordeon anterior (revisión)
        localStorage.removeItem('demandNegotiationRevision');
    }

    /* MP 4 : Preparación */
    // Si estamos en : Preparación|Revisión
    if ($('.demand-preparation .accordion-item[data-active="active"]').attr('data-accordion-item') === 'revision') {
        // Borramos data acordeon anterior (proceso)
        localStorage.removeItem('demandPreparationStep1');
        localStorage.removeItem('demandPreparationStep2');
        localStorage.removeItem('demandPreparationStep3');
        localStorage.removeItem('demandPreparationStep4');
    }

}

/*==================== NEGOTIATION (RELACIONAMIENTO) FUNCTIONS ====================*/

function enableBeginContinueNegotiation() {
    // Verificamos que exista el formulario
    if ($('#beginRelationForm').length > 0) {
        // Custom validation select multiple proveedores "relacionamiento" 
        let $inputMultiList = $('#initiation .accordion-body #id_multilist');
        let $submitBtn = $('#beginRelationForm input[type="submit"]');

        function multiListIsValid($input) {
            if ($input.val() === '') {
                // Mostramos error validación
                if ($('.form__element--multilist .error-validacion.requerido').length <= 0) {
                    $('.form__element--multilist').append(`<p class="error-validacion requerido">Este campo es requerido.</p>`);
                }
                return false;
            } else {
                // Quitamos mensaje validación
                if ($('.form__element--multilist .error-validacion').hasClass('requerido')) {
                    $('.form__element--multilist .error-validacion.requerido').remove();
                }
                return true;
            }
        }

        $submitBtn.on('click', function (event) {
            event.preventDefault();
            // Si es valido
            if (multiListIsValid($inputMultiList)) {
                $('#beginRelationForm').trigger('submit');
            }
        });

        // Verificamos cada vez que cambie el input
        $inputMultiList.on('change', function () {
            multiListIsValid($(this));
        });
    }
}

function agreementDropdown() {
    // let dropdownWrapperClassName = '.agreement__dropdown-wrapper';
    let dropdownClassName = '.agreement__dropdown';
    let btnTriggerDropdownClassName = '.agreement__dropdown-btn';
    let tagsWrapperClassName = '.agreement__tags-wrapper';
    let addAgreementBtnClassName = '.agreement__add-btn';
    let $dropdowns = $(dropdownClassName);
    // Obtenemos id solicitud
    let demandId = $dropdowns.closest('form').attr('data-iddemand');

    $dropdowns.each(function (index, dropdown) {
        // Añadir atributos "data-bs-target" a los botones trigger dropdown, y "id" a los dropdowns
        $(dropdown).siblings(btnTriggerDropdownClassName).attr('data-bs-target', '#agreementDropdownMenu-' + index);
        $(dropdown).attr('id', 'agreementDropdownMenu-' + index);

    });

    function deleteTag() {
        // Evento eliminar tag
        $(document).on('click', '.agreement__cancel', function () {
            // Obtenemos id proveedor
            let providerId = $(this).closest(tagsWrapperClassName).attr('data-provider-id');
            // Obtenemos texto tag
            let txtTag = $(this).parent().text();

            prevDataArrObj.forEach((demand) => {
                // Si el objeto corresponde al id de la solicitud actual
                if (demand.demandId === demandId) {
                    // Accedemos al array de objetos (c/u por proveedor)
                    demand.agreementList.forEach((agreement) => {
                        // verificamos si existe el proveedor
                        if (providerId === agreement.providerId) {
                            // Eliminamos del array y guardamos en local
                            agreement.tags.splice(agreement.tags.indexOf(txtTag), 1);
                            return;
                        }
                    });
                    return;
                }
            });

            // Guardamos en localStorage(string)
            // localStorage.setItem('demandAgreement', JSON.stringify(prevDataArrObj));
            // Guardamos clave por 2 semanas = 1209600000 milisegundos
            setWithExpiry('demandAgreement', prevDataArrObj, 1209600000);

            // Eliminamos del DOM
            $(this).parent().remove();
        });
    }

    function createTag($selector, tagid, tagtxt) {
        // Crea un tag y lo añade al DOM
        $selector.prepend(`<div class="agreement__tag"><span class="icon-close-icon agreement__cancel"></span>${tagtxt}<input type="hidden" name="agreementTag[]" value="provId-${tagid}_tagName-${tagtxt}" /></div>`);

        // añadimos evento para eliminar tag
        deleteTag();
    }

    let prevDataArrObj;
    // Verificar si hay data en LocalStorage
    // let prevLocalData = localStorage.getItem('demandAgreement');
    let prevLocalData = getWithExpiry('demandAgreement');
    
    if (prevLocalData) {
        // Convertimos string a array de objetos
        prevDataArrObj = JSON.parse(prevLocalData);

        prevDataArrObj.forEach((demand) => {
            // Si el objeto corresponde al id de la solicitud actual
            if (demand.demandId === demandId) {
                // Accedemos al array de objetos (c/u por proveedor)
                demand.agreementList.forEach((agreement) => {
                    let providerId = agreement.providerId;
                    let $selector = $(tagsWrapperClassName + '[data-provider-id=' + providerId + ']');
                    // Recorremos array de strings
                    agreement.tags.forEach((tag) => {
                        // Añadimos tag
                        createTag($selector, providerId, tag);
                    });
                });
            }
        });
    } else {
        prevDataArrObj = [];
    }

    // Añadir tags
    $(addAgreementBtnClassName).on('click', function (e) {
        e.preventDefault();
        // Obtener nombre tag
        let tagtxt = $(this).parents(dropdownClassName).find('input[name="name-agreement"]').val().trim();

        // Verificamos que no este vacio
        if (tagtxt !== "") {
            // Verificar que ya no exista
            let currentTags = $(this).parents(tagsWrapperClassName).find('.agreement__tag');
            let repeated = false;

            if ($(currentTags).length > 0) {
                // console.log("length current tags: ", $(currentTags).length);
                currentTags.each(function (index, tag) {
                    // Si ya existe el tag
                    if ($(tag).text() === tagtxt) {
                        repeated = true;
                        return;
                    }
                    // console.log("indice: ", index, " elemento: ", tag, "Texto: ", $(tag).text());
                });
            }

            // Si no existe se añade
            if (!repeated) {
                // Obtenemos id proveedor
                let tagid = $(this).parents(tagsWrapperClassName).attr('data-provider-id');

                // Añadimos tag
                createTag($(this).parents(tagsWrapperClassName), tagid, tagtxt);

                // Verificar si id de solicitud existe en dataLocal
                let existingDemand = false;
                if (prevDataArrObj.length > 0) {
                    prevDataArrObj.forEach((demand) => {
                        // Si el objeto corresponde al id de la solicitud actual
                        if (demand.demandId === demandId) {
                            let existingProvider = false;
                            // Accedemos al array de objetos (c/u por proveedor)
                            demand.agreementList.forEach((agreement) => {
                                // verificamos si existe el proveedor
                                if (tagid === agreement.providerId) {
                                    // guardamos en el array de tags el nuevo tag
                                    agreement.tags.push(tagtxt);
                                    existingProvider = true;
                                }
                            });
                            // Si no existia proveedor en la solicitud
                            if (!existingProvider) {
                                demand.agreementList.push({
                                    "providerId": tagid,
                                    "tags": [tagtxt]
                                });
                            }
                            existingDemand = true;
                        }
                    });
                }
                // Si no existia solicitud en la dataLocal
                if (!existingDemand) {
                    prevDataArrObj.push({
                        "demandId": demandId,
                        "agreementList": [
                            {
                                "providerId": tagid,
                                "tags": [tagtxt]
                            }
                        ]
                    });
                }

                // Guardamos en localStorage(string)
                // localStorage.setItem('demandAgreement', JSON.stringify(prevDataArrObj));
                // Guardamos clave por 2 semanas = 1209600000 milisegundos
                setWithExpiry('demandAgreement', prevDataArrObj, 1209600000);
            }
        }

        // Borrar valor input
        $(this).parents(dropdownClassName).find('input[name="name-agreement"]').val('');

        // Cerrar dropdown
        let dropdownId = $(this).parents(dropdownClassName).attr('id');

        let $theDropdown = document.querySelector('#' + dropdownId);

        $theDropdown = bootstrap.Dropdown.getOrCreateInstance($theDropdown);

        $theDropdown.hide();

    });

}

// Negociación/Proceso/step2
function checkSelectedAgreement() {
    // obtenemos los checkbox
    let $checks = $('.agreement__card input[name="selected-agreement"]');
    // Obtener el boton submit para continuar al step3
    let $btnSubmit = $('.demand-relation #formStep2 input[type="submit"]');

    function verifySelected() {
        // Si existe alguno seleccionado
        let oneChecked = $('.agreement__card input[name="selected-agreement"]').is(':checked');

        $checks.each(function () {
            let $check = $(this);
            let $btn = $check.parent('.agreement__header__right').find('.btn');

            if (oneChecked) {
                if ($check.prop("checked")) {
                    if ($btn.length > 0) {
                        $btn.addClass('hide');
                    }
                } else {
                    $check.addClass('hide');
                    if ($btn.length > 0) {
                        $btn.removeClass('hide');
                    }
                }
                // Habilitamos submit
                $btnSubmit.prop('disabled', false);
            } else {
                $check.removeClass('hide');
                if ($btn.length > 0) {
                    $btn.addClass('hide');
                }
                // Deshabilitamos submit
                $btnSubmit.prop('disabled', true);
            }
        });
    }

    // Verificar si desde back envian uno seleccionado
    verifySelected();

    // Cuando cambian los checkbox
    $checks.on('change', function () {
        verifySelected();
    });

}

function persistentNegotiationData() {

    // Verificamos que el formulario del "paso 5:Estructuración del convenio"/"Proceso" exista
    if ($('.demand-relation .form-stpe-5')) {
        // Indicamos la clave a buscar en LocalStorage
        const claveLocal = 'demandNegotiationStep5';
        // Ids de los campos a guardar en localStorage
        let idFields = ['#date_agreed', '#time', '#type_time', '#channel', '#date_agreement', '#type_time', '#consideration'];

        // Guarda en LocalStorage los campos del form del "paso 5:Estructuración del convenio"/"Proceso"
        setAndGetLocalStorageDemandData(idFields, claveLocal);
    }

    // Verificamos que el formulario del acordeon "Revisión" exista
    if ($('.demand-relation .form-stpe-review')) {
        // Indicamos la clave a buscar en LocalStorage
        const claveLocal = 'demandNegotiationRevision';
        // Obtenemos los id de los selects de preguntas
        let idFields = []
        $('.demand-relation .form-stpe-review select').each((index, element) => {
            idFields.push("#" + $(element).attr('id'));
        });

        // Guarda en LocalStorage los campos del form del acordeon "Revisión"
        setAndGetLocalStorageDemandData(idFields, claveLocal);
    }
}

function validateFinalizedRelation(){
    // Añadimos contador de caracteres
    addCharacterCounter(['#formFinalizedRelation #comment_finalized']);

    $('#formFinalizedRelation').validate({
        rules: {
            comment_finalized: {
                required: true,
                maxlength: 300, // máx 300 caracteres
            },
        }
    });
}

// NEGOCIOACIÓN(RELACIONAMIENTO)
function allNegotiationFunctions() {
    enableBeginContinueNegotiation();
    agreementDropdown();
    checkSelectedAgreement();
    persistentNegotiationData();
    validateFinalizedRelation();
}

/*==================== PREPARATION FUNCTIONS ====================*/

function validatebeginPreparationForm() {
    // Valida formulario de inicio en "Preparación"
    let $beginPreparationForm = $('#beginPreparationForm');
    if ($beginPreparationForm.length > 0) {

        // Si el primer acordeon está activo
        if ($('.demand-preparation__begin').attr('data-active') === 'active') {
            // Si no hay transferencias, cambiamos el link del segundo acordeon
            let $selectTransfer = $('#transfer'),
                $transferOptions = $selectTransfer.find('option'),
                currentOption = $selectTransfer.find('option:selected');

            if ($transferOptions.length <= 1 || currentOption.val() === '') {
                $('.accordion-item.demand-preparation__process .accordion-header a.accordion-button').attr('href', '#beginPreparationForm')
            }

        }

        // Validaci+on form
        $beginPreparationForm.validate({
            rules: {
                transfer: {
                    required: true
                },
                date: {
                    required: true
                },
                hour: {
                    required: true
                },
                coments: {
                    required: true,
                    maxlength: 800, //máx 800 caracteres
                },
            },
            errorClass: 'error-validacion', // Clase para las alertas de validación
            errorElement: 'p', // Elemento "html" para mostrar el error
        });
    }
}

function validateProcessStep1Preparation() {
    // Valida formulario "proceso" "paso 1"
    let $processStep1PrepaForm = $('.demand-preparation #formStep1');
    if ($processStep1PrepaForm.length > 0) {
        $processStep1PrepaForm.validate({
            rules: {
                consistency_question_1: {
                    required: true
                },
                consistency_question_2: {
                    required: true
                },
                consistency_question_3: {
                    required: true
                }
            },
            errorElement: 'label', // Elemento "html" para mostrar el error
            errorPlacement: function (error, element) {
                let type = $(element).attr("type");
                if (type === "radio") {
                    error.appendTo(element.closest('div.content-radio'));
                } else {
                    error.insertAfter(element);
                }
            },
            highlight: function (element, errorClass, validClass) {
                let type = $(element).attr("type");
                if (type === "radio") {
                    $(element).closest('div.content-radio').addClass(errorClass);
                } else {
                    $(element).addClass(errorClass);
                }
            },
            unhighlight: function (element, errorClass, validClass) {
                let type = $(element).attr("type");
                if (type === "radio") {
                    $(element).closest('div.content-radio').removeClass(errorClass);
                } else {
                    $(element).removeClass(errorClass);
                }
            },
        });
    }
}

function validateProcessStep2Preparation() {
    // Valida formulario "Proceso"|"Paso 2"
    let $processStep2PrepaForm = $('.demand-preparation #formStep2');
    if ($processStep2PrepaForm.length > 0) {
        $processStep2PrepaForm.validate({
            rules: {
                standarization_question_1: {
                    required: true
                },
                standarization_question_2: {
                    required: true
                },
                standarization_question_3: {
                    required: true
                }
            },
            errorElement: 'label', // Elemento "html" para mostrar el error
            errorPlacement: function (error, element) {
                let type = $(element).attr("type");
                if (type === "radio") {
                    error.appendTo(element.closest('div.content-radio'));
                } else {
                    error.insertAfter(element);
                }
            },
            highlight: function (element, errorClass, validClass) {
                let type = $(element).attr("type");
                if (type === "radio") {
                    $(element).closest('div.content-radio').addClass(errorClass);
                } else {
                    $(element).addClass(errorClass);
                }
            },
            unhighlight: function (element, errorClass, validClass) {
                let type = $(element).attr("type");
                if (type === "radio") {
                    $(element).closest('div.content-radio').removeClass(errorClass);
                } else {
                    $(element).removeClass(errorClass);
                }
            },
        });
    }
}

function validateProcessStep3Preparation() {
    // Valida formulario "Proceso"|"Paso 3"
    let $processStep3PrepaForm = $('.demand-preparation #formStep3');
    if ($processStep3PrepaForm.length > 0) {
        $processStep3PrepaForm.validate({
            rules: {
                detection_question_1: {
                    required: true
                },
                detection_question_2: {
                    required: true
                },
                detection_question_3: {
                    required: true
                }
            },
            errorElement: 'label', // Elemento "html" para mostrar el error
            errorPlacement: function (error, element) {
                let type = $(element).attr("type");
                if (type === "radio") {
                    error.appendTo(element.closest('div.content-radio'));
                } else {
                    error.insertAfter(element);
                }
            },
            highlight: function (element, errorClass, validClass) {
                let type = $(element).attr("type");
                if (type === "radio") {
                    $(element).closest('div.content-radio').addClass(errorClass);
                } else {
                    $(element).addClass(errorClass);
                }
            },
            unhighlight: function (element, errorClass, validClass) {
                let type = $(element).attr("type");
                if (type === "radio") {
                    $(element).closest('div.content-radio').removeClass(errorClass);
                } else {
                    $(element).removeClass(errorClass);
                }
            },
        });
    }
}

function validateProcessStep4Preparation() {
    // Valida formulario "Proceso"|"Paso 4"
    let $processStep4PrepaForm = $('.demand-preparation #formStep4');
    if ($processStep4PrepaForm.length > 0) {
        $processStep4PrepaForm.validate({
            rules: {
                anonymization_question_1: {
                    required: true
                },
                anonymization_question_2: {
                    required: true
                },
                anonymization_question_3: {
                    required: true
                }
            },
            errorElement: 'label', // Elemento "html" para mostrar el error
            errorPlacement: function (error, element) {
                let type = $(element).attr("type");
                if (type === "radio") {
                    error.appendTo(element.closest('div.content-radio'));
                } else {
                    error.insertAfter(element);
                }
            },
            highlight: function (element, errorClass, validClass) {
                let type = $(element).attr("type");
                if (type === "radio") {
                    $(element).closest('div.content-radio').addClass(errorClass);
                } else {
                    $(element).addClass(errorClass);
                }
            },
            unhighlight: function (element, errorClass, validClass) {
                let type = $(element).attr("type");
                if (type === "radio") {
                    $(element).closest('div.content-radio').removeClass(errorClass);
                } else {
                    $(element).removeClass(errorClass);
                }
            },
        });
    }
}

function persistentPreparationData() {
    // Guarda en LocalStorage los campos del form de "Preparación"|"Proceso"|"Paso 1: Consistencia"
    if ($('.demand-preparation #formStep1').length > 0) {

        // Indicamos la clave a buscar en LocalStorage
        const claveLocal = 'demandPreparationStep1';
        // Selector de los campos a guardar en localStorage
        let selectorFields = [
            ".demand-preparation #formStep1 input[name='consistency_question_1']",
            ".demand-preparation #formStep1 input[name='consistency_question_2']",
            ".demand-preparation #formStep1 input[name='consistency_question_3']",
            ".demand-preparation #formStep1 #consistency_functionary"
        ];

        setAndGetLocalStorageDemandData(selectorFields, claveLocal);
    }
    // Guarda en LocalStorage los campos del form de "Preparación"|"Proceso"|"Paso 2: Estandarización y Normalización"
    if ($('.demand-preparation #formStep2').length > 0) {

        // Indicamos la clave a buscar en LocalStorage
        const claveLocal = 'demandPreparationStep2';
        // Selector de los campos a guardar en localStorage
        let selectorFields = [
            ".demand-preparation #formStep2 input[name='standarization_question_1']",
            ".demand-preparation #formStep2 input[name='standarization_question_2']",
            ".demand-preparation #formStep2 input[name='standarization_question_3']",
            ".demand-preparation #formStep2 #standardization_functionary"
        ];

        setAndGetLocalStorageDemandData(selectorFields, claveLocal);
    }
    // Guarda en LocalStorage los campos del form de "Preparación"|"Proceso"|"Paso 3: Detección de anomalías"
    if ($('.demand-preparation #formStep3').length > 0) {

        // Indicamos la clave a buscar en LocalStorage
        const claveLocal = 'demandPreparationStep3';
        // Selector de los campos a guardar en localStorage
        let selectorFields = [
            ".demand-preparation #formStep3 input[name='detection_question_1']",
            ".demand-preparation #formStep3 input[name='detection_question_2']",
            ".demand-preparation #formStep3 input[name='detection_question_3']",
            ".demand-preparation #formStep3 #anomaly_functionary"
        ];

        setAndGetLocalStorageDemandData(selectorFields, claveLocal);
    }
    // Guarda en LocalStorage los campos del form de "Preparación"|"Proceso"|"Paso 4: Anonimización y completitud"
    if ($('.demand-preparation #formStep4').length > 0) {

        // Indicamos la clave a buscar en LocalStorage
        const claveLocal = 'demandPreparationStep4';
        // Selector de los campos a guardar en localStorage
        let selectorFields = [
            ".demand-preparation #formStep4 input[name='anonymization_question_1']",
            ".demand-preparation #formStep4 input[name='anonymization_question_2']",
            ".demand-preparation #formStep4 input[name='anonymization_question_3']",
            ".demand-preparation #formStep4 #anonymization_functionary"
        ];

        setAndGetLocalStorageDemandData(selectorFields, claveLocal);
    }

}

function validateReviewPreparationForm() {
    // Valida formulario de "revisión" en "Preparación"
    let $reviewPreparationForm = $('.demand-preparation #formReview');
    if ($reviewPreparationForm.length > 0) {
        $reviewPreparationForm.validate({
            rules: {
                date: {
                    required: true
                },
                hour: {
                    required: true
                },
                'review-question-1': {
                    required: true
                },
                'review-question-2': {
                    required: true
                },
                'review-question-3': {
                    required: true
                },
                coments: {
                    required: true,
                    maxlength: 800, //máx 800 caracteres
                },
            },
            errorClass: 'error-validacion', // Clase para las alertas de validación
            errorElement: 'p', // Elemento "html" para mostrar el error
        });
    }
}

function validateFinalizePreparationForm() {
    // Valida formulario de "revisión" en "Preparación"
    let $finalizePreparationForm = $('.demand-preparation #formFinalize');
    if ($finalizePreparationForm.length > 0) {
        $finalizePreparationForm.validate({
            rules: {
                date_finalize: {
                    required: true
                },
                hour_finalize: {
                    required: true
                },
                coments_finalize: {
                    required: true,
                    maxlength: 800, //máx 800 caracteres
                },
            },
            errorClass: 'error-validacion', // Clase para las alertas de validación
            errorElement: 'p', // Elemento "html" para mostrar el error
        });
    }
}

function deliveryProcessPreparation(){
    let $selectTransfer = $('select#transfer');
    // Actualizar select segun url
    // Obtenemos los parametros de la URL
    let params = new URLSearchParams(document.location.search);

    // Obtenemos el valor del parametro
    let paramValue = params.get('preparation');

    // Si contiene valor
    if (paramValue) {
        // Asignamos "value" al select
        $selectTransfer.val(paramValue).prop('selected', true);
        // Se selecciona la "option"
        $selectTransfer.find('option[value=' + paramValue + ']').attr('selected', true);
    }

    // escuchar evento cambio del select
    $selectTransfer.on('change', function(){
        let idTransfer = $(this).val();
        if(idTransfer !== ''){
            // Creamos nueva url
            let url = new URL(window.origin + window.location.pathname);
            // Seteamos los parametros
            url.searchParams.set('preparation', idTransfer);
            // Redireccionamos a la nueva url
            window.location.href = url;            
        }
    });
}

function setSearchSelectsPreparation(){
    // añadir buscador a selects de preparación
    let searchSelectsArray = [
        '#consistency_functionary',
        '#standardization_functionary',
        '#anomaly_functionary',
        '#anonymization_functionary'
    ];
    addSearchForSelects(searchSelectsArray);
}

function allPreparationFunctions() {
    validatebeginPreparationForm();
    deliveryProcessPreparation();
    validateProcessStep1Preparation();
    validateProcessStep2Preparation();
    validateProcessStep3Preparation();
    validateProcessStep4Preparation();
    persistentPreparationData();
    validateReviewPreparationForm();
    validateFinalizePreparationForm();
    setSearchSelectsPreparation();
}

/*==================== EVALUATION FUNCTIONS ====================*/

function validatebeginEvaluationForm($form) {
    // Valida formulario de inicio en "Evaluación"
    $form.validate({
        rules: {
            evaluation_functionary: {
                required: true
            },
            evaluation_frequency: {
                required: true
            },
            date_notification: {
                required: true
            },
            finish_date: {
                required: true,
            },
        },
        errorClass: 'error-validacion', // Clase para las alertas de validación
        errorElement: 'p', // Elemento "html" para mostrar el error
    });
}

function formatISODate(fecha){
    // Formatea fecha a string "yyyy-mm-dd"
    return fecha.getFullYear().toString() + '-' + (fecha.getMonth() + 1).toString().padStart(2, 0) + '-' + fecha.getDate().toString().padStart(2, 0);
}

function setMinDate(fecha, $input){
    let currentFormated = formatISODate(fecha);
    $input.attr('min', currentFormated);
}

function calculateMinEndingDate(fecha, months){
    // calcula la fecha de finalización de X meses más 2 días segun la fecha
    // UTC-05:00  +'T12:00:00Z'
    let fechaFinal = new Date( formatISODate(fecha)+'T12:00:00.000Z' );
    // Sumamos meses
    fechaFinal.setMonth(fechaFinal.getMonth() + months);
    // Sumamos 2 días
    let futureDay = fechaFinal.getDate() + 2;    
    fechaFinal.setDate(futureDay);
    // fechaFinal.setDate(fechaFinal.getDate() + 2);

    return fechaFinal;
}

function setUpEvaluationDates(){

    let $inputNotificationDate = $('#evaluation_init #date_notification');
    let $inputFinishDate = $('#evaluation_init #finish_date');
    let $selectFrecuencia = $('#evaluation_frequency');
    // Revisamos el valor del select de frecuancia, si no tiene valor asignamos por defecto 2 meses
    let aditionalMonths =  function (){
        return $selectFrecuencia.val() !== '' ? parseInt($selectFrecuencia.val()) : 2;
    }
    
    const currentDate = new Date();
    // Seteamos valor min inicial en campo "fecha de notificación"
    setMinDate(currentDate, $inputNotificationDate );
    // Seteamos valor min inicial en campo "fecha de finalización"
    let endingDate = calculateMinEndingDate(currentDate, aditionalMonths());
    setMinDate(endingDate, $inputFinishDate );

    $inputNotificationDate.on('change', function(){
        let nuevaFechaInicial = new Date( $(this).val() );
        // Calculamos y seteamos nueva fecha final 
        endingDate = calculateMinEndingDate(nuevaFechaInicial, aditionalMonths());
        setMinDate(endingDate, $inputFinishDate );
    });

    $selectFrecuencia.on('change', function(){
        // Si no hay fecha de notificacion escogida, se asigna el día actual
        let nuevaFechaInicial = $inputNotificationDate.val() !== '' ? new Date( $inputNotificationDate.val() ) : new Date();
        // Calculamos y seteamos nueva fecha final 
        endingDate = calculateMinEndingDate(nuevaFechaInicial, aditionalMonths());
        setMinDate(endingDate, $inputFinishDate );
    });
    
}

function evaluateDemandModal(){
    $('.demand-evaluate').on("click", function(event){
        event.preventDefault();
        // Obtener id evaluación
        let evaluationId = $(this).parents('.list-of-evaluation-item').attr('data-idevaluation');

        let modalMessage = `Hacer una observación para la evaluación con <b>id : ${evaluationId}</b>`;

        // Modal de confirmación
        let $modalEvaluateDemand = $('#evaluateDemand');
        if($modalEvaluateDemand.length > 0){
            // Modal bootstrap
            let modalBsEvaluate = bootstrap.Modal.getOrCreateInstance(document.getElementById('evaluateDemand'));

            // Seteamos mensaje en el modal
            $modalEvaluateDemand.find('.description').html(modalMessage);

            // Seteamos valor en el input hidden del form del modal
            $('#formInterview #id_evaluation').val(evaluationId);

            // Mostramos modal
            modalBsEvaluate.show();
        }
    });


}

function validateFinalizeEvaluation(){
    $('.demand-evaluation #formFinalize').validate({
        rules: {
            coments_finalize: {
                required: true,
                maxlength: 800, // máx 800 caracteres
            },
        },
        errorClass: 'error-validacion', // Clase para las alertas de validación
        errorElement: 'p', // Elemento "html" para mostrar el error
    });
}

function allEvaluationFunctions() {
    // formulario de inicio en "Evaluación"
    let $beginEvaluationForm = $('#evaluation_init');
    if ($beginEvaluationForm.length > 0) {
        validatebeginEvaluationForm($beginEvaluationForm);
        setUpEvaluationDates();
        evaluateDemandModal();
    }
    validateFinalizeEvaluation();
}

/*==================== MULTISTEP FORM CREATE RRAA ====================*/

let createRRAAvalidatorObj;

function validateCreateRRAAForm() {
    $.validator.addMethod('greaterThan', function (value, element, params) {
        if ($(params[0]).val() !== '') {
            if (!/Invalid|NaN/.test(new Date(value))) {
                return new Date(value) > new Date($(params[0]).val());
            }
            return isNaN(value) && isNaN($(params[0]).val()) || (Number(value) > Number($(params[0]).val()));
        };
        return true;
    }, 'El valor debe ser mayor');

    $.validator.addMethod("extensionConditional", function (value, element, param) {
        param = $(param + ' option:selected').text().toString().replace(/\./g, '').trim();
        // param = typeof param === "string" ? param.replace( /,/g, "|" ) : "png|jpe?g|gif";
        return this.optional(element) || value.match(new RegExp("\\.(" + param + ")$", "i"));
    }, $.validator.format("Solo se permiten archivos con el formato seleccionado."));

    $.validator.addMethod("accept", function (value, element, param) {
        // Split mime on commas in case we have multiple types we can accept
        var typeParam = typeof param === "string" ? param.replace(/\s/g, "") : "image/*",
            optionalValue = this.optional(element),
            i, file, regex;


        if ($(element).attr("type") === "file") {

            // Escape also "/*" as "/.*" as a wildcard
            typeParam = typeParam
                .replace(/[\-\[\]\/\{\}\(\)\+\?\.\\\^\$\|]/g, "\\$&")
                .replace(/,/g, "|")
                .replace(/\/\*/g, "/.*");

            // Check if the element has a FileList before checking each file
            if (element.files && element.files.length) {
                regex = new RegExp(".?(" + typeParam + ")$", "i");
                for (i = 0; i < element.files.length; i++) {
                    file = element.files[i];

                    // Grab the mimetype from the loaded file, verify it matches
                    if (!file.type.match(regex)) {
                        return false;
                    }
                }
            }
        }

        // Either return true because we've validated each file, or because the
        // browser does not support element.files and the FileList feature
        return true;
    }, $.validator.format("Solo se permiten archivos con el formato seleccionado."));

    $.validator.addMethod("emailValidate", function (value, element) {
        if (/^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/i.test(value)) {
            return true;
        } else {
            return false;
        };
    }, "Ingrese un correo electrónico válido");

    return $('#createRraaForm').validate({
    // createRRAAvalidatorObj = $('#createRraaForm').validate({
        rules: {
            /* TAB1 Identificacion del RRAA */
            title: {
                required: true,
                maxlength: 75, // máx 75 caracteres
            },
            record_choice: {
                required: true
            },
            objective: {
                required: true,
                maxlength: 300, // máx 300 caracteres
            },
            target_population:{
                required: true,
                maxlength: 75, // máx 75 caracteres
            },
            inventory_thematic_asociate: {
                required: true,
            },
            inventory_theme_asociate: {
                required: true,
            },
            /* TAB2 Caracteristicas del RRAA */
            // Select ¿Qué norma soporta la creación del RA?
            use_laws_decrees: {
                required: true,
            },
            // Condicionales select
            political_constitution: {
                required: true,
            },
            law: {
                required: true,
            },
            decree: {
                required: true,
            },
            choice_laws_decrees: {
                required: true,
            },
            decree_other: {
                required: true,
            },
            year_creation: {
                required: true,
                digits: true,
                minlength: 4,
                maxlength: 4
            },
            // Fecha de inicio de la última recolección de información
            date_start_collection: {
                required: true,
            },
            date_finish_collection: {
                required: true,
                greaterThan: ['#id_date_start_collection'],
            },
            // Select ¿El registro administrativo es proporcionado a otra(s) institución(es) del Estado?
            provided_government: {
                required: true
            },
            provided_government_which: { //condicional
                required: true,
                maxlength: 75, // máx 75 caracteres
            },
            // Select ¿Existe alguna restricción  para la entrega de información al INE?
            restriction: {
                required: true
            },
            restriction_which :{ //condicional
                required: true
            },
            year_creation_bd:{
                required: true,
                digits: true,
                minlength: 4,
                maxlength: 4
            },
            // Select ¿El RA cuenta con alguno de documentos metodológicos o funcionales?
            method_document: {
                required: true
            },
            // Condicional Select ¿Cuáles documentos métodológicos usa?
            document_choice: {
                required: true
            },
            // Condicional select
            other_methodologycal_document: {
                required: true
            },
            // Select ¿El RA utiliza nomenclaturas y/o clasificaciones?
            nomenclature_choice: {
                required: true
            },
            // Condicional select si
            yes_nomenclature: {
                required: true
            },
            // Condicional select no
            not_nomenclature: {
                required: true
            },
            // Select ¿Qué método utiliza para la recolección de datos?
            method_collections_choice: {
                required: true
            },
            // Condicional select otros
            other_methods_collections: {
                required: true
            },
            // Select ¿Con qué frecuencia hace recolección de datos?
            frequency_choice: {
                required: true
            },
            // Condicional select frecuencia
            other_frequency_collections: {
                required: true
            },
            // Select Indique cuáles de las herramientas utiliza para el procesamiento de datos
            processing_choice: {
                required: true
            },
            // Condicional select herramientas
            other_proccesing_tools: {
                required: true
            },
            geographic_coverages_type: {
                required: true
            },
            other_geographic_coverages_type: { //condicional
                required: true,
                maxlength: 75, // máx 75 caracteres
            },
            /* TAB3 Identificacion de los responsables del RRAA */
            director_name: {
                required: true
            },
            director_email: {
                required: true,
                // email: true
                emailValidate: true
            },
            director_phone: {
                digits: true,
                minlength: 10,
            },
            responsible_custody: {
                maxlength: 75, // máx 75 caracteres
            },
            responsible_report: {
                maxlength: 75, // máx 75 caracteres
            },
            responsible_name: {
                required: true
            },
            responsible_email: {
                required: true,
                // email: true
                emailValidate: true
            },
            responsible_phone: {
                digits: true,
                minlength: 10,
            },
            generate_information: {
                maxlength: 200, // máx 200 caracteres
            },
            observations: {
                maxlength: 300, // máx 300 caracteres
            },
            /* TAB4 Características secundarias del RRAA */
            other_security_imformation: {
                required: true,
                maxlength: 255, // máx 255 caracteres
            },
            object_rra: {
                maxlength: 150, // máx 150 caracteres
            },
            /* TAB5 Sample Data */
            size_sample_data: {
                minlength: 1,
            },
            count_sample_data: {
                minlength: 1,
            },
            name_file: {
                maxlength: 53, // máx 53 caracteres
            },
            // type_format_data_asociate: {
            //     // Si el campo de tipo file tiene un valor, este se vuelve requerido
            //     required: function(element){
            //         // Campo del que depende para ser requerido
            //         let $dependsOnField = $("#id_file_example_sample_data");
            //         if( $dependsOnField.val() !== ''){
            //             $(element).parents('.form__field').addClass('required');
            //         }else{
            //             $(element).parents('.form__field').removeClass('required');
            //         }
            //         return ( $dependsOnField.val() !== '');
            //     },
            // },
            seperated_columns_file: {
                required: true,
            },
            file_example_sample_data: {
                // Le pasamos el selector del select del que depende el formato
                extensionConditional: '#id_type_format_data_asociate'
            }
        },
        messages: {
            date_finish_collection: {
                greaterThan: 'La fecha de finalización debe ser mayor a la de inicio.',
            }
        },
        errorClass: 'error-validacion', // Clase para las alertas de validación
        errorElement: 'p', // Elemento "html" para mostrar el error
        submitHandler: function (form) {
            $('.loading').removeClass('d-none');
            // form.submit();
            confirmationRRAAmodal(form);
        }
    });
}

function confirmationRRAAmodal(form) {
    // Obtenemos url origin
    let urlApi = window.location.origin;
    let $rraaForm = $(form), formAction, actualMessages;


    const RRAAmessages = [
        {
            'title': 'Crear registro administrativo',
            'description': 'Se ha creado el registro administrativo.'
        },
        {
            'title': 'Editar registro administrativo',
            'description': 'Se ha editado el registro administrativo.'
        }
    ];

    let pathName = window.location.pathname;
    // Si estamos en edición de inventario
    if (pathName.includes("editar")) {
        actualMessages = RRAAmessages[1];
        // Ocultamos boton crear nuevo registro
        $('.create-new').addClass('d-none');
    } else {
        actualMessages = RRAAmessages[0];
        // Mostramos botones
        $('#modalConfirmationRRAA .create-new').removeClass('d-none');
        $('#modalConfirmationRRAA .goto-list').removeClass('d-none');
        $('#modalConfirmationRRAA .btn-close-modal').addClass('d-none');
    }

    // Modal de confirmación
    let modalBsRRAA = bootstrap.Modal.getOrCreateInstance(document.getElementById('modalConfirmationRRAA')),
        $modalConfirmationRRAA = $('#modalConfirmationRRAA');

    // Acción formulario
    formAction = $rraaForm.attr('action');

    let data = new FormData($rraaForm[0]);

    // Hacemos petición Ajax
    $.ajax({
        method: 'POST',
        url: `${urlApi}${formAction}`,
        // data: $rraaForm.serialize(),
        data: data,
        contentType: false,
        processData: false,
        success: function (res) {
            // Seteamos mensaje en el modal
            $modalConfirmationRRAA.find('.description').html(actualMessages["description"]);
            // Cambiamos icono del modal
            $modalConfirmationRRAA.find('.modal-alert__wrapper-icon').html(`<span class="icon-icon-check"></span>`);
        },
        error: function (jqXHR, estado, error) {
            // Seteamos mensaje en el modal
            $modalConfirmationRRAA.find('.description').html(`Ha ocurrido un error inesperado ${error}`);
            // Cambiamos icono del modal
            $modalConfirmationRRAA.find('.modal-alert__wrapper-icon').html(`<span class="icon-alert"></span>`);
            // Ocultamos botones acciones
            $('#modalConfirmationRRAA .create-new').addClass('d-none');
            $('#modalConfirmationRRAA .goto-list').addClass('d-none');
            // Mostramos boton volver
            $('#modalConfirmationRRAA .btn-close-modal').removeClass('d-none');
        },
        complete: function (jqXHR, estado) {
            // Seteamos mensaje en el modal
            $modalConfirmationRRAA.find('.modal-title').html(actualMessages["title"]);
            // Ocultamos loader
            $('.loading').addClass('d-none');
            // Mostramos modal
            modalBsRRAA.show();
        },
    });

    // Escuchamos evento boton crear nuevo registro
    $('.create-new').on('click', function (event) {
        event.preventDefault();
        window.location.reload();
    });

}

function setOrUnsetRequiredFields(arrayFields, setOrUnset) {
    /*  Funcion para:
            - Añadir asterisco al ".form__field"
            - Añadir propiedad "required" al campo del form

        Parametros:
            - arrayFields --> array con selectores de los campos
            - setOrUnset --> booleano, 'true' para setear
    */

    arrayFields.forEach(function (field) {
        if (setOrUnset) {
            // Añadimos clase al field, para mostrar asterisco
            $(field).parents('.form__field').addClass('required');
            // Seteamos propiedad required en el campo
            $(field).prop('required', true);
        } else {
            // Quitamos clase al field
            $(field).parents('.form__field').removeClass('required');
            // Quitamos propiedad required en el campo
            $(field).prop('required', false);
        }
    });
}

function setAcceptAttrFileSampleDataRraa() {
    /* Funcion para:
        - setear el attributo "accept" en el input type file del sample data
    */

    // Obtenemos campo donde se selecciona tipo de formato
    let $selectTypeFormat = $('#id_type_format_data_asociate');
    // input type file sample data
    let $fileSample = $('#id_file_example_sample_data');

    // Obtenemos valor actual campo
    let currentOption = $selectTypeFormat.find('option:selected');

    // Si tiene algun valor diferente a nada
    if (currentOption.val() !== "") {
        // Obtenemos la extensión seleccionada
        let formatFile = $(currentOption).text().trim(),
            mimeType;
        // Se settea el atributo en el input file, para que solo acepte archivos con esa extension
        if (formatFile === '.xls') {
            mimeType = "application/vnd.ms-excel";
        } else if (formatFile === '.xlsx') {
            mimeType = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";
        }
        $fileSample.rules("add", {
            extension: formatFile.slice(1, formatFile.length - 1),
            accept: mimeType
        });
        $fileSample.attr('accept', formatFile);
    } else {
        // Removemos atributo "accept"
        $fileSample.removeAttr('accept');
        $fileSample.rules("remove", {
            extension,
            accept
        });
    }
}

function fileSampleDataRraa() {
    // Requeridos: "tipo extensión archivo", "Nombre archivo", "Fecha subida"
    let camposRequeridos = [
        '#id_type_format_data_asociate',
        '#id_name_file',
        '#id_date_load_field'
    ];
    if ($('#createRraaForm').length > 0) {
        $('#id_file_example_sample_data').on('change', function () {
            let fileValue = $(this).val();
            if (fileValue !== '') {
                // Obtenemos la extensión del archivo subido
                let fileExtension = fileValue.split('.')[1];
                fileExtension = "." + fileExtension;
                // Obtenemos todas las opciones
                $('#id_type_format_data_asociate option').each(function () {
                    // Obtenemos texto y valor opcion
                    let optionText = $(this).text().trim(),
                        optionValue = $(this).val();
                    // Si el texto es igual a la extensión
                    if (optionText === fileExtension) {
                        // asignamos valor de la opción al select
                        $('#id_type_format_data_asociate').val(optionValue);
                        $('#id_type_format_data_asociate').trigger('change');
                    }
                });


                // Seteamos requeridos el nombre del archivo y el tipo de extension
                setOrUnsetRequiredFields(camposRequeridos, true);
            } else {
                setOrUnsetRequiredFields(camposRequeridos, false);
            }
        });
    }
}

function hideLawFields() {
    // Validación custom select selectedOption
    // Muestra o no, otros campos del formulario dependiendo de la opción del select
    let hiddenLawFields = [
        'id_political_constitution',
        'id_law',
        'id_decree',
        'id_choice_laws_decrees',
        'id_decree_other'
    ];

    function showHideFields(animate = false) {
        // Obtenemos la opcion(es) seleccionada(s) (en caso de select multiple)
        let selectedVals = $('#id_use_laws_decrees').find(":selected");

        hiddenLawFields.forEach(function (field) {
            let $field = $('#' + field).parents('.form__field');
            let dataValue = $field.attr('data-value');

            selectedVals.each(function () {
                if (this.value === dataValue) {
                    animate ? $field.slideDown("medium") : $field.show();
                } else if ((this.value === 'D.N' || this.value === 'D.D' || this.value === 'D.M') && dataValue.charAt(0) === 'D') {
                    animate ? $field.slideDown("medium") : $field.show();
                } else {
                    animate ? $field.slideUp("medium") : $field.hide();
                    // Borramos datos de campo oculto
                    $('#' + field).val('');
                }
            });
        });
    }

    showHideFields(false);

    $('#id_use_laws_decrees').on('change', function () {
        showHideFields(true);
        // validateCreateRRAAForm();
        // createRRAAvalidatorObj.element(this);
    });
}

function showHideFields(animate = false, arrayFields, idSelect) {
    // Obtenemos la opcion(es) seleccionada(s) (en caso de select multiple)
    let selectedVals = $(idSelect).find(":selected");
    arrayFields.forEach(function (field) {
        let $formField = $('#' + field);
        let $field = $formField.parents('.form__field');
        let dataValue = $field.attr('data-value');
        selectedVals.each(function () {
            if (this.value === dataValue) {
                animate ? $field.slideDown("medium") : $field.show();
            } else {
                animate ? $field.slideUp("medium") : $field.hide();
                // Borramos datos de campo oculto
                if( $formField.is('select') ){
                    $formField.find(":selected").each(function () {
                        $(this).attr('selected', false);
                    });
                    $formField.val([]);
                    $formField.prop('selectedIndex', 0);
                }else{
                    $formField.val('');
                }
                $formField.trigger('change');
            }
        });
    });
}

function showHideRRAAConditional(selectSelector, arrayFields) {
    // Muestra o no, otros campos del formulario dependiendo de la opción del select
    showHideFields(false, arrayFields, selectSelector);

    $(selectSelector).on('change', function () {
        showHideFields(true, arrayFields, selectSelector);
        // validateCreateRRAAForm();
        // createRRAAvalidatorObj.element(this);
    });
}

function hideDelimitado() {
    // Validación custom select selectedOption
    // Muestra o no, otros campos del formulario dependiendo de la opción del select
    let hiddenDelimitadoFields = [
        'id_seperated_columns_file'
    ];
    let inputFile = $('#id_file_example_sample_data');

    function showHideFields(animate = false) {
        // Obtenemos la opcion(es) seleccionada(s) (en caso de select multiple)
        let selectedVals = $('#id_type_format_data_asociate').find(":selected");

        hiddenDelimitadoFields.forEach(function (field) {
            let $formField = $('#' + field);
            let $field = $formField.parents('.form__field');

            selectedVals.each(function () {
                if (($(this).text().trim() === '.csv') || ($(this).text().trim() === '.txt')) {
                    animate ? $field.slideDown("medium") : $field.show();
                } else {
                    animate ? $field.slideUp("medium") : $field.hide();
                    // Borramos datos de campo oculto
                    $formField.find(":selected").each(function () {
                        $(this).attr('selected', false);
                    });
                    $formField.val([]);
                    $formField.prop('selectedIndex', 0);

                }
            });
        });
    }

    showHideFields(false);

    // Escuchamos evento change en selector de tipo de formato
    $('#id_type_format_data_asociate').on('change', function () {
        inputFile.removeAttr('accept');
        let fileSelected = $(this).val();
        let formatFile = $(this).find('option[value="' + fileSelected + '"]').text().trim();
        inputFile.attr('accept', formatFile);

        showHideFields(true);
        // validateCreateRRAAForm();
        // createRRAAvalidatorObj.element(this);
    });

    inputFile.on('focus', function () {
        let fileSelected = $('#id_type_format_data_asociate').val();
        let formatFile = $('#id_type_format_data_asociate').find('option[value="' + fileSelected + '"]').text().trim();
        $(this).attr('accept', formatFile);
    })

    inputFile.on('focusout', function(){
        inputFile.removeAttr('accept');
    });

    inputFile.on('change', function () {
        if ($(this).val() !== '') {
            $(this).removeAttr('accept');
        }
    })

    $('#createRraaSubmit').on('click', function () {
        inputFile.removeAttr('accept');
    });

}

function allCreateRRAAConditionals() {
    hideLawFields();
    // hide document_choice
    showHideRRAAConditional('#id_method_document', ['id_document_choice']);
    // hide other_methodologycal_document
    showHideRRAAConditional('#id_document_choice', ['id_other_methodologycal_document']);
    // hide nomenclature_choice
    showHideRRAAConditional('#id_nomenclature_choice', ['id_yes_nomenclature', 'id_not_nomenclature']);
    // hide method_collections_choice
    showHideRRAAConditional('#id_method_collections_choice', ['id_other_methods_collections']);
    // hide frequency_choice
    showHideRRAAConditional('#id_frequency_choice', ['id_other_frequency_collections']);
    // hide processing_choice
    showHideRRAAConditional('#id_processing_choice', ['id_other_proccesing_tools']);
    // hide organism_document_choice
    showHideRRAAConditional('#id_organism_document_choice', ['id_documents_organization', 'id_others_standars']);
    // hide security_choice
    showHideRRAAConditional('#id_security_choice', ['id_other_security_imformation']);
    // hide information_stored_choice
    showHideRRAAConditional('#id_information_stored_choice', ['id_information_choice']);
    // hide information_choice
    showHideRRAAConditional('#id_information_choice', ['id_other_security_imformations']);
    // hide main_choice - ¿Cuál es la razón principal por la cual no se permite el acceso a los datos del RA?
    showHideRRAAConditional('#id_external_user', ['id_main_choice']);
    // hide other_main_not_permissed - ¿Qué otra razón principal tiene para no permitir el acceso a los datos del RA?
    showHideRRAAConditional('#id_main_choice', ['id_other_main_not_permissed']);
    // hide ods_indicator - ¿Cuál es el indicador ODS?
    showHideRRAAConditional('#id_requierements_choice', ['id_ods_indicator']);
    // hide "delimitado por"
    hideDelimitado();
    // hide provided_government_which
    showHideRRAAConditional('#id_provided_government', ['id_provided_government_which']);
    // hide restriction_which
    showHideRRAAConditional('#id_restriction', ['id_restriction_which']);
    // hide other_geographic_coverages_type
    showHideRRAAConditional('#id_geographic_coverages_type', ['id_other_geographic_coverages_type']);
}

function isEmptyObject(obj) {
    return JSON.stringify(obj) === '{}'
}

function createDivipolasSelectors(selectSelector) {
    let $divipolasWrapper = $('#divipolasWrapper');
    if ($divipolasWrapper.length > 0) {
        let $selectOculto = $(selectSelector);
        let arrayFieldIndex = 1;

        /* Codigos de la divipola según país
            1 --> Colombia
            1185 --> Bolivia
            1647 --> Chile
            2066 --> Perú
        */
        const divipolaPaises = {
            'co': '1',
            'bo': '1185',
            'cl': '1647',
            'pe': '2066'
        };

        function getCurrentCountryCode() {
            let $body = $('body');
            return divipolaPaises[$body.attr('class')];
        }

        const currentCountry = getCurrentCountryCode();

        function hideNextSubSelectors(field) {
            // Array de todos los campos(incluyendo el oculto)
            let arrayFields = $divipolasWrapper.find('.form__field'),
                actualIndex = $(field).parents('.form__field').attr('data-index');
            // Verificamos si es el primer select
            // El select oculto tiene indice = 0
            if (actualIndex === '1') {
                // Ocultamos todos los demas hermanos
                $(field).parents('.form__field').siblings().slideUp("medium");
                // Seteamos el valor del select oculto en nada
                $selectOculto.val('');
            } else {
                // Ocultamos los hermanos siguientes
                // Si indice del elemento es menor que el total de elementos
                if (actualIndex < arrayFields.length - 1) {
                    // Desde el siguiente elemento empezamos a ocultar campos
                    for (let i = parseInt(actualIndex) + 1; i <= arrayFields.length; i++) {
                        $(arrayFields[i]).slideUp("medium");
                    }
                }
                // Obtenemos valor del select anterior
                let prevSelectedVal = $(arrayFields[parseInt(actualIndex) - 1]).find('option:selected').val();
                // Seteamos el valor en el select oculto
                $selectOculto.val(prevSelectedVal);
            }
        }

        function getDivipola(idDivipola) {
            /*  Funcion para:
                    - Hacer petición servicio 'hijo-divipola/<int:id_divipola>'
                    - Crear campos select divipolas

                Parametros:
                    - idDivipola --> entero id divipola a buscar
            */

            let urlApi = window.location.origin;
            $.getJSON(`${urlApi}/hijo-divipola/${idDivipola}`, function (data) {
                // Vefificar que data no sea vacia
                if (isEmptyObject(data)) {
                    // Si esta vacia, significa que hemos llegado al ultimo elemento seleccionable
                    // Obtenemos el valor del último select
                    let lastValueSelected = $divipolasWrapper.find('.form__field').last().find('option:selected').val();
                    // Seteamos el valor en el select oculto(el que van a leer en back)
                    $selectOculto.val(lastValueSelected)
                } else {
                    let selectOptions = ["<option value='' selected >Seleccione una opción</option>"];
                    let selectLabel;
                    // Por cada item en la data, añadimos al array una opción del select.
                    $.each(data, function (clave, valor) {
                        selectOptions.push(`<option value='${clave}'>${valor['name']}</option>`);
                        selectLabel = valor['type'].trim();
                    });
                    // Crear select template
                    let selectTemplate = `<fieldset class="form__field w-100" data-index="${arrayFieldIndex}">
                                            <label for="${selectLabel}">${selectLabel}</label>
                                            <div class="form__element form__element--select">
                                              <select name="${selectLabel}" id="${selectLabel}">
                                              ${selectOptions.join("")}
                                              </select>
                                            </div>
                                        </fieldset>`;
                    // Verificamos que no exista el elemento antes de añadir al DOM
                    if ($(`#${selectLabel}`).length <= 0) {
                        // Añadir select al DOM
                        $divipolasWrapper.append(selectTemplate);
                        // Aumentamos indice del field
                        arrayFieldIndex++;

                        // Añadimos clase required a primer selector de divipola
                        // Array de todos los campos(incluyendo el oculto)
                        let arrayFields = $('#divipolasWrapper').find('.form__field');
                        // Tomamos el primer select creado de divipola
                        $(arrayFields[1]).addClass('required');
                        // Seteamos propiedad required en el campo
                        $(arrayFields[1]).find('select').prop('required', true);
                        $(arrayFields[1]).find('select').rules('add', { required: true });

                    } else {
                        // Añadimos las opciones al select previamente creado
                        $(`#${selectLabel}`).html(`${selectOptions.join("")}`);
                        // Mostramos el select oculto
                        $(`#${selectLabel}`).parents('.form__field').slideDown("medium");
                    }

                    // Escuchar evento "change" select creado
                    $('body').on('change', `#${selectLabel}`, function () {
                        // Obtenemos valor de la opcion seleccionada
                        let valueSelect = $(this).find('option:selected').val(),
                            $field = $(this);
                        // Si no es opcion por defecto
                        if (valueSelect !== "") {
                            // Ocultamos los hermanos siguientes, para que no queden con valores antiguos que puedan ser seleccionados
                            hideNextSubSelectors($field);
                            // Seteamos el valor en el select oculto(el que van a leer en back)
                            $selectOculto.val(valueSelect);
                            // Creamos el nuevo select recursivamente
                            getDivipola(valueSelect);
                        } else {
                            // Ocultamos los hermanos siguientes
                            hideNextSubSelectors($field);
                        }
                    });
                }

            });
        }

        function editarDivipola() {
            // Obtenemos valor y texto del select oculto
            let actualValue = $selectOculto.find('option:selected').val(),
                actualText = $selectOculto.find('option:selected').text();
            // Si no tenia cobertura geografica
            // Crear select template
            let selectTemplate = `<fieldset class="form__field w-100" id="actualDivipolaField">
                                    <label for="actualDivipola">Cobertura geográfica actual del RRAA</label>
                                    <div class="form__element form__element--select">
                                    <select name="actualDivipola" id="actualDivipola">
                                        <option value=''>Seleccione esta opción para cambiar</option>
                                        <option value='${actualValue}' selected >${actualText}</option>
                                    </select>
                                    </div>
                                </fieldset>`;
            // Verificamos que no exista el elemento antes de añadir al DOM
            if ($('#actualDivipolaField').length <= 0) {
                // Añadir select al DOM
                $divipolasWrapper.append(selectTemplate);
            }
            // Escuchar evento "change" select creado
            $('body').on('change', '#actualDivipola', function () {
                // Obtenemos valor de la opcion seleccionada
                let valueSelect = $(this).find('option:selected').val();
                // Si es opcion por defecto
                if (valueSelect === "") {
                    // Removemos campo del DOM
                    $('#actualDivipolaField').remove();
                    // Creamos el primer select de divipola
                    getDivipola(currentCountry);
                }
            });
        }

        // Compobamos Si estamos en edición de inventario

        // Obtenemos el valor del campo oculto
        let actualValue = $selectOculto.find('option:selected').val();
        // si contiene algun valor, estamos en "edición"
        if (actualValue !== "") {
            // Crea el select para cambiar cobertura
            editarDivipola();
        } else {
            // Creamos el primer select de divipola
            getDivipola(currentCountry);
        }

    }
}

function validateCurrentStep(tab) {
    // Hace una validación parcial de los campos mostrados en la pestaña(tab) actual del formulario
    let isValid = true;

    $(tab).find(':input').each(function (i, item) {
        if (!$(item).valid()) {
            isValid = false;
        }
    });

    return isValid;
}

function inventoryCreateMultistepForm() {
    let $formulario = $('#createRraaForm');
    let pasosValidos = [];
    let $submitBtn = $('#createRraaSubmit');
    // Añadimos un elemento con valor "false" al array por cada paso
    for (let i = 0; i < $formulario.find('.step-tab-panel').length; i++) {
        pasosValidos.push(false);
    }
    // Deshabilitamos el boton de "submit"
    let pathName = window.location.pathname;
    // Si estamos en edición de inventario habilitamos el boton
    if (pathName.includes("editar")) {
        $submitBtn.prop('disabled', false);
    } else {
        $submitBtn.prop('disabled', true);
    }

    // Establecemos validación
    let formValidator = validateCreateRRAAForm();
    // validateCreateRRAAForm();

    // Escuchamos evento "input" en cada campo del formulario
    $formulario.find(':input').on('input', function(){
        // Validamos el elemento cuyo valor cambio
        // createRRAAvalidatorObj.element(this);
        formValidator.element(this);
    });

    function allStepsValid(paso, index) {
        let currentTab = $formulario.find('.step-tab-panel')[index];
        pasosValidos[index] = validateCurrentStep(currentTab);

        return pasosValidos[index];
    }

    function enableSubmitBtn() {
        // Habilitamos el boton "submit" si todos los pasos son validos
        if (pasosValidos.every(allStepsValid) === true) {
            $submitBtn.prop('disabled', false);
        } else {
            $submitBtn.prop('disabled', true);
        }
    }

    // Creamos la navegación "step wizard"
    let stepObjRraa = $('#createRraa').steps({
        // Cada vez que hacemos click para cambiar de paso
        onChange: function (currentIndex, newIndex, stepDirection) {
            // Grab height of fixed header
            let headHeight = $('header').outerHeight();
            if (stepDirection === 'forward') {
                let currentTab = $formulario.find('.step-tab-panel')[currentIndex];
                // Animamos scroll hacia el tab activo
                $('html, body').animate({
                    scrollTop: $('#createRraaForm').offset().top - headHeight - 20
                }, 800);

                return validateCurrentStep(currentTab);
            }
            if (stepDirection === 'backward') {
                formValidator.resetForm();
                // createRRAAvalidatorObj.resetForm();
                // Animamos scroll hacia el tab activo
                $('html, body').animate({
                    scrollTop: $('#createRraaForm').offset().top - headHeight - 20
                }, 800);
            }
            // Si es ultimo paso
            if (currentIndex === $formulario.find('.step-tab-panel').length - 1) {
                // Habilitamos submit
                $submitBtn.prop('disabled', false);
                if (stepDirection === 'forward') {
                    let currentTab = $formulario.find('.step-tab-panel')[currentIndex];
                    return validateCurrentStep(currentTab);
                }
            }

            return true;
        },
        // Cuando acabamos el formulario validamos si se habilita el submit
        onFinish: function () {
            enableSubmitBtn();
        }
    });

}

function searchForSelectsRraaCreate(){
    // Array con todos los ids de selects a convertir en crear rraa
    let selectsRraa = [
        '#id_inventory_thematic_asociate',
        '#id_inventory_theme_asociate',
        '#id_tag_sample_data_asociate',
        '#id_variables_sample_data_asociate'
    ];

    // Añade buscador a los selects normales y múltiples
    addSearchForSelects(selectsRraa);
}

function addCharacterCounterCreateRraa(){
    // array con selectores de los campos a añadirles contador de caracteres
    const fields = [
        '#id_objective',
        '#id_observations',
        '#id_target_population',
        '#id_object_rra'
    ];
    // Añadimos contador de caracteres
    addCharacterCounter(fields);
}

function allCreateRRAAfunctions() {
    // Todas las funciones para formulario de "crear|editar RRAA o inventario"
    inventoryCreateMultistepForm();
    allCreateRRAAConditionals();
    if ($('#createRraaForm').length > 0) {
        createDivipolasSelectors('#id_geographic_coverages');
    }
    fileSampleDataRraa();
    // setAcceptAttrFileSampleDataRraa();
    searchForSelectsRraaCreate();
    addCharacterCounterCreateRraa();
}

/*==================== MULTISTEP FORM CREATE PROVIDER ====================*/

function validateProviderCreate() {
    // añadimos contador caracteres campos
    let counterfields =[
        '#id_sicode',
        '#id_description'
    ];

    addCharacterCounter(counterfields);

    $('input[type="file"]').on('change', function () {
        let inputSelect = $(this)
        inputSelect.removeData('imageWidth');
        inputSelect.removeData('imageHeight');
        let file = this.files[0];
        let img = new Image();
        img.src = window.URL.createObjectURL(file);
        img.onload = function () {
            inputSelect.data('imageWidth', this.width);
            inputSelect.data('imageHeight', this.height);
        }
    });
    // Añadimos validacion custom para tamaño de la imagen
    $.validator.addMethod('dimention', function (value, element, param) {
        if (element.files.length === 0) {
            return true;
        }
        let width = $(element).data('imageWidth');
        let height = $(element).data('imageHeight');
        if (width === param[0] && height === param[1]) {
            return true;
        } else {
            return false;
        }
    }, 'Las imágenes deben ser exactamente de {0}x{1} píxeles.');

    // Modify message jquery validation
    $.extend($.validator.messages, {
        extension: "Solo se permiten imágenes jpg, jpeg, png",
    });

    $.validator.addMethod("emailValidate", function (value, element) {
        if (/^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/i.test(value)) {
            return true;
        } else {
            return false;
        };
    }, "Ingrese un correo electrónico válido");

    $.validator.addMethod("letterwithbasicpunc", function (value, element) {
        if (/^[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1 ]*$/.test(value)) {
            return true;
        } else {
            return false;
        };
    }, "Ingrese solo letras y espacios");

    $.validator.addMethod("domainvalid", function (value, element) {
        const pattern = new RegExp(
            '^(https?:\\/\\/)?' + // protocol
              '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|' + // domain name
              '((\\d{1,3}\\.){3}\\d{1,3}))' + // OR ip (v4) address
              '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*' + // port and path
              '(\\?[;&a-z\\d%_.~+=-]*)?' + // query string
              '(\\#[-a-z\\d_]*)?$', // fragment locator
            'i'
        );
        return pattern.test(value);
    }, "Ingrese un dominio válido");

    return $('#create-provider-form').validate({
        rules: {
            /* Paso 1: Identificación de la entidad proveedora */
            name: {
                required: true,
                maxlength: 255, // máx 255 caracteres
            },
            identification_number: {
                required: true,
                digits: true,
                maxlength: 25, // máx 25 caracteres
            },
            description: {
                required: true,
                maxlength: 255, // máx 255 caracteres
            },
            sector: {
                required: true,
            },
            type: {
                required: true,
            },
            image: {
                required: true,
                extension: "jpg|jpeg|png|ico|bmp",
                dimention: [80, 80],
            },
            mision: {
               maxlength: 255, // máx 255 caracteres
            },
            sicode: {
                // required: true,
                maxlength: 15, // máx 15 caracteres
            },
            /* Paso 2: Ubicación del proveedor */
            territorial_level: {
                maxlength: 255, // máx 255 caracteres
            },
            web: {
                maxlength: 255, // máx 255 caracteres
            },
            mail: {
                required: true,
                // email: true,
                emailValidate: true,
                maxlength: 255, // máx 255 caracteres
            },
            telephone: {
                digits: true,
                minlength: 10,
                maxlength: 25, // máx 25 caracteres
            },
            // location: {
            //     required: true,
            // },
            /* Paso 3: Identificación del contacto */
            agent_mame: {
                required: true,
                letterwithbasicpunc: true,
                maxlength: 255, // máx 255 caracteres
            },
            agent_position: {
                maxlength: 255, // máx 255 caracteres
            },
            official_name: {
                required: true,
                letterwithbasicpunc: true,
                maxlength: 255, // máx 255 caracteres
            },
            official_position: {
                maxlength: 255, // máx 255 caracteres
            },
            official_mail: {
                required: true,
                // email: true,
                emailValidate: true,
                maxlength: 255, // máx 255 caracteres
            },
            official_telephone: {
                digits: true,
                minlength: 10,
                maxlength: 25, // máx 25 caracteres
            },
            /* Paso 4: Información secundaria */
            domain: {
                required: true,
                // url2: true
                domainvalid: true,
                maxlength: 255, // máx 255 caracteres
            },
            status: {
                required: true,
            },
            category: {
                required: true,
            },
            topic: {
                required: true,
            },
        },
        messages:{
            domain: {
                url2: "Ingrese un dominio valido (http://... o https://...)"
            }
        },
        errorClass: 'error-validacion', // Clase para las alertas de validación
        errorElement: 'p', // Elemento "html" para mostrar el error
        submitHandler: function (form) {
            $('.loading').removeClass('d-none');
            // form.submit();
            confirmationProvidermodal(form);
        },
    });
}

function confirmationProvidermodal(form) {
    // Obtenemos url origin
    let urlApi = window.location.origin;
    let $form = $(form), formAction, actualMessages;

    actualMessages = {
        'title': 'Crear nueva entidad proveedora',
        'description': 'Se ha creado la nueva entidad proveedora.'
    };

    // Modal de confirmación
    let modalBsProvider = bootstrap.Modal.getOrCreateInstance(document.getElementById('modalConfirmationProvider')),
        $modalConfirmationProvider = $('#modalConfirmationProvider');

    // Acción formulario
    formAction = $form.attr('action');

    let data = new FormData($form[0]);

    // Hacemos petición Ajax
    $.ajax({
        method: 'POST',
        url: `${urlApi}${formAction}`,
        // data: $form.serialize(),
        data: data,
        contentType: false,
        processData: false,
        success: function (res) {
            // Seteamos mensaje en el modal
            $modalConfirmationProvider.find('.description').html(actualMessages["description"]);
            // Cambiamos icono del modal
            $modalConfirmationProvider.find('.modal-alert__wrapper-icon').html(`<span class="icon-icon-check"></span>`);
        },
        error: function (jqXHR, estado, error) {
            // Seteamos mensaje en el modal
            $modalConfirmationProvider.find('.description').html(`Ha ocurrido un error inesperado ${error}`);
            // Cambiamos icono del modal
            $modalConfirmationProvider.find('.modal-alert__wrapper-icon').html(`<span class="icon-alert"></span>`);
        },
        complete: function (jqXHR, estado) {
            // Seteamos mensaje en el modal
            $modalConfirmationProvider.find('.modal-title').html(actualMessages["title"]);
            // Ocultamos loader
            $('.loading').addClass('d-none');
            // Mostramos modal
            modalBsProvider.show();
        },
    });

    // Escuchamos evento boton crear nuevo
    $('.create-new').on('click', function (event) {
        event.preventDefault();
        window.location.reload();
    });

}

function providerCreateMultistepForm() {
    let $formulario = $('#create-provider-form');
    let pasosValidos = [];
    let $submitBtn = $('#createProviderSubmit');

    if ($formulario.length > 0) {
        // Añadimos un elemento con valor "false" al array por cada paso
        for (let i = 0; i < $formulario.find('.step-tab-panel').length; i++) {
            pasosValidos.push(false);
        }
        // Deshabilitamos el boton de "submit"
        $submitBtn.prop('disabled', true);

        // Creamos divipolas
        createDivipolasSelectors('#id_location');

        // Establecemos validación
        let formValidator = validateProviderCreate();

        function allStepsValid(paso, index) {
            let currentTab = $formulario.find('.step-tab-panel')[index];
            pasosValidos[index] = validateCurrentStep(currentTab);

            return pasosValidos[index];
        }

        function enableSubmitBtn() {
            // Habilitamos el boton "submit" si todos los pasos son validos
            if (pasosValidos.every(allStepsValid) === true) {
                $submitBtn.prop('disabled', false);
            } else {
                $submitBtn.prop('disabled', true);
            }
        }

        // Creamos la navegación "step wizard"
        let stepObjProv = $('#createProvider').steps({
            // Cada vez que hacemos click para cambiar de paso
            onChange: function (currentIndex, newIndex, stepDirection) {
                // Grab height of fixed header
                let headHeight = $('header').outerHeight();
                if (stepDirection === 'forward') {
                    let currentTab = $formulario.find('.step-tab-panel')[currentIndex];
                    // Animamos scroll hacia el tab activo
                    $('html, body').animate({
                        scrollTop: $formulario.offset().top - headHeight - 20
                    }, 800);
                    return validateCurrentStep(currentTab);
                }
                if (stepDirection === 'backward') {
                    formValidator.resetForm();
                    // Animamos scroll hacia el tab activo
                    $('html, body').animate({
                        scrollTop: $formulario.offset().top - headHeight - 20
                    }, 800);
                }
                // Si es ultimo paso
                if (currentIndex === $formulario.find('.step-tab-panel').length - 1) {
                    // Habilitamos submit
                    $submitBtn.prop('disabled', false);
                    if (stepDirection === 'forward') {
                        let currentTab = $formulario.find('.step-tab-panel')[currentIndex];
                        return validateCurrentStep(currentTab);
                    }
                }

                return true;
            },
            // Cuando acabamos el formulario validamos si se habilita el submit
            onFinish: function () {
                enableSubmitBtn();
            }
        });
    }
}

/*==================== MULTI SELECT CHECKBOX ====================*/

function createMultiSelectCheck() {
    // Hace que un select multiple, se vea como un select normal y sus opciones como unos checkboxes
    $('.news .form__element--select-multiple-check select').multipleSelect({
        placeholder: 'Seleccione tags',
        locale: 'es-ES', // traducir mensajes
        maxHeight: '100' // altura en px del dropdown
        // formatSelectAll: function () {
        //     return '[Seleccionar todas]'
        // },
        // formatAllSelected: function () {
        //     return 'Todas seleccionadas'
        // },
        // formatCountSelected: function (count, total) {
        //     return count + ' de ' + total + ' seleccionadas'
        // }
    });
}

/*==================== VALIDATE CREATE USER FORM ====================*/

function validateCreateUser() {
    if ($('#createUser').length > 0) {

        $('#id_profile_image').on('change', function () {
            let inputSelect = $(this)
            inputSelect.removeData('imageWidth');
            inputSelect.removeData('imageHeight');
            let file = this.files[0];
            let img = new Image();
            img.src = window.URL.createObjectURL(file);
            img.onload = function () {
                inputSelect.data('imageWidth', this.width);
                inputSelect.data('imageHeight', this.height);
                // console.log('width: ' + this.width + ' height: ' + this.height+'');
            }
        });

        // Añadimos validacion custom para tamaño de la imagen
        $.validator.addMethod('dimention', function (value, element, param) {
            if (element.files.length === 0) {
                return true;
            }
            let width = $(element).data('imageWidth');
            let height = $(element).data('imageHeight');
            if (width === param[0] && height === param[1]) {
                return true;
            } else {
                return false;
            }
        }, 'Las imágenes deben ser exactamente de {0}x{1} píxeles.');

        $.validator.addMethod("valueNotEquals", function (value, element, arg) {
            return value !== 'no';
        }, "Value must not equal arg.");
        $.validator.addMethod("validate_password", function (value, element) {
            return !!(/^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[@#$*%&])/.test(value));
        }, function (value, element) {
            let password = $(element).val();
            if (!(/^(?=.*[A-Z])/.test(password))) {
                return 'La contraseña debe contener al menos una mayúscula.';
            }
            else if (!(/^(?=.*[a-z])/.test(password))) {
                return 'La contraseña debe contener al menos una minúscula.';
            }
            else if (!(/^(?=.*[0-9])/.test(password))) {
                return 'La contraseña debe contener al menos un dígito.';
            }
            else if (!(/^(?=.*[@#$%&])/.test(password))) {
                return "La contraseña debe contener al menos un carácter especial @#$%&";
            }
        });
        $.validator.addMethod("letterwithbasicpunc", function (value, element) {
            if (/^[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1 ]*$/.test(value)) {
                return true;
            } else {
                return false;
            };
        }, "Ingrese solo letras y espacios");
        $.validator.addMethod("emailValidate", function (value, element) {
            if (/^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/i.test(value)) {
                return true;
            } else {
                return false;
            };
        }, "Ingrese un correo electrónico válido");
        $.validator.addMethod("onlyLetters", function (value, element) {
            if (/^[a-zA-Z]*$/i.test(value)) {
                return true;
            } else {
                return false;
            };
        }, "Ingrese solo letras");
        $.validator.addMethod("alphaNum", function (value, element) {

            if (/[a-zA-Z0-9 -()+]+$/i.test(value)) {
                return true;
            } else {
                return false;
            };
        });
        $('#createUser').validate({
            rules: {
                nombre: {
                    required: true,
                    letterwithbasicpunc: true,
                    maxlength: 30,
                    // onlyLetters: true
                },
                apellido: {
                    required: true,
                    letterwithbasicpunc: true,
                    maxlength: 30,
                    // onlyLetters: true
                },
                username: {
                    required: true,
                    // email: true
                    emailValidate: true
                },
                password1: {
                    required: true,
                    minlength: 8,
                    nowhitespace: true,
                    validate_password: true,
                },
                password2: {
                    required: true,
                    minlength: 8,
                    equalTo: "#id_password1"
                },
                identification_number: {
                    required: true,
                    // alphaNum: true,
                    digits: true,
                    minlength: 5,
                    maxlength: 255,
                },
                profile_image: {
                    required: true,
                    dimention: [150, 150],
                },
                group: {
                    required: true,
                }
            },
            messages: {
                nombre: {
                    required: "Este campo es requerido",
                    maxlength: "Máximo 30 caracteres",
                },
                apellido: {
                    required: "Este campo es requerido",
                    maxlength: "Máximo 30 caracteres",
                },
                username: "Ingrese un correo electrónico válido",
                password1: {
                    required: "Ingrese su contraseña",
                    minlength: "Minímo 8 caracteres",
                },
                password2: {
                    required: "Ingrese su contraseña",
                    minlength: "Minímo 8 caracteres",
                    equalTo: "Debe ser la misma contraseña",
                },
                identification_number: {
                    required: "Ingrese su número de identificación",
                    alphaNum: "Ingrese un número de indentifación válido",
                    minlength: "Minímo 5 caracteres",
                },
                group: {
                    required: "Este campo es requerido",
                }
            },
            errorClass: 'error-validacion', // Clase para las alertas de validación
            errorElement: 'p', // Elemento "html" para mostrar el error
        });
    }
}

/*==================== SCROLL MOBILE PROGRESSBAR ====================*/

function progressbarScroll() {
    // Verificamos que exista
    if ($('#progressbar').length) {
        // Verificamos tamaño pantalla mobile y tablet unicamente
        let screenWidth = $(window).width();
        if (screenWidth < 992) {
            // Opciones de Intersection observer
            let options = {
                root: null,
                rootMargin: '0px',
            }

            // Obtenemos el contenedor de los pasos
            let targetObserver = document.querySelector('.progressbar');

            function animateScrollLeft($element) {
                let elOffset = $element.offset().left;
                let elWidth = $element.width();
                let windowWidth = $(window).width();
                let offset;

                if (elOffset >= windowWidth || elOffset > (windowWidth / 2)) {
                    offset = elOffset - ((windowWidth / 2) - (elWidth / 2));
                } else if (elOffset <= (windowWidth / 2)) {
                    offset = 0;
                } else {
                    offset = elOffset;
                }

                $('#progressbar').animate({
                    scrollLeft: offset
                }, 800);
            }

            const observer = new IntersectionObserver((entries) => {

                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        // obtenemos item step

                        let elements = [];

                        if ($('.progressbar-step.current').length) {
                            elements.push($('.progressbar-step.current'));
                        }
                        if ($('.progressbar-step.active').length) {
                            elements.push($('.progressbar-step.active'));
                        }
                        elements.forEach((stepitem) => {
                            animateScrollLeft(stepitem)
                        });

                    }
                })

            }, options);

            observer.observe(targetObserver);

        }

    }
}

/*==================== SMOOTH SCROLL ====================*/
function smoothScroll() {
    // Hace scroll animado para un link bookmark

    // Select all links with hashes
    $('a[href*="#"]')
        // Remove links that don't actually link to anything
        .not('[href="#"]')
        .not('[href="#0"]')
        .on('click', function (event) {
            // Grab height of fixed header
            let headHeight = $('header').outerHeight();
            // On-page links
            if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
                // Store hash
                let hash = this.hash;
                // Figure out element to scroll to
                let target = $(hash);
                // Does a scroll target exist?
                if (target.length) {
                    // Only prevent default if animation is actually gonna happen
                    // event.preventDefault();
                    $('html, body').animate({
                        scrollTop: target.offset().top - headHeight - 20
                    }, 800, function () {
                        // Callback after animation
                        // Must change focus
                        let $target = $(target);
                        $target.trigger('focus');
                        if ($target.is(":focus")) { // Checking if the target was focused
                            // Add hash (#) to URL when done scrolling (default click behavior)
                            window.location.hash = hash;
                            return false;
                        } else {
                            $target.attr('tabindex', '-1'); // Adding tabindex for elements not focusable
                            $target.trigger('focus'); // Set focus again
                            $target.css('outline', 'none');
                        };
                    });
                }
            }
        });
}

/*==================== FOOTER COPY ====================*/

function changeFooterCopy() {
    let country = jQuery("body").attr("class")
    switch (country) {
        case 'co':
            jQuery("footer.footer .second-footer .col-md-6 .policy-content .policy-description").text("© 2023 DANE – Departamento Nacional de Estadística");
            break;
        case 'cl':
            jQuery("footer.footer .second-footer .col-md-6 .policy-content .policy-description").text("© 2023 INE – Instituto Nacional de Estadísticas");
            break;
        case 'bo':
            jQuery("footer.footer .second-footer .col-md-6 .policy-content .policy-description").text("© 2023 INE – Instituto Nacional de Estadística");
            break;
        case 'pe':
            jQuery("footer.footer .second-footer .col-md-6 .policy-content .policy-description").text("© 2023 INEI – Instituto Nacional de Estadística e Informática ");
            break;

        default:
            jQuery("footer.footer .second-footer .col-md-6 .policy-content .policy-description").text("not country detected");
            break;
    }
}

/*==================== PROJECT DESCRIPTION ====================*/

function changeProjectsDescription() {
    let pathName = window.location.pathname
    if (pathName.includes("editar")) {
        jQuery(".projects-create__desc").text("En esta sección podrá editar la información completa de un proyecto.")
    } else {
        jQuery(".projects-create__desc").text("En esta sección podrá crear y registrar la información completa de un proyecto. ")
    }
}

/*==================== DELETE PROJECT OF LIS PROJECT ====================*/

function deleteProjectListProject() {
    if (jQuery('.projects-list .projects-list-result .card-list').length) {
        const myModal = new bootstrap.Modal(document.getElementById('modalDeleteProject'));

        jQuery('.projectscard .projectscard__actions form .btn').on('click', function (e) {
            e.preventDefault();
            let card = jQuery(this).closest('.projectscard');
            let titleProject = card.find('.projectscard__title a').text();
            let formDelete = card.find('form')

            jQuery('#modalDeleteProject .modal-body .description span').text(titleProject.toLowerCase());
            myModal.show();

            // onsubimit
            jQuery('#modalDeleteProject .modal-body .container-button .btn-confirm-modal').on('click', function (e) {
                e.preventDefault();
                formDelete.submit();
            });

        })
    }
}

/*==================== EDIT PROFILE FUNCTIONS ====================*/

let photoCameraPicture = false;

function takePhotoCamera() {
    // Definimos tamaño para el elemento video, canvas y fotografía
    const width = 150;
    const height = 150;

    // The various HTML elements we need to configure or control. These
    // will be set by the startup() function.
    let video = null;
    let canvas = null;
    let photo = null;
    let startbutton = null;
    // Verificamos que los elementos existan
    if ($('#video').length > 0 && $('#canvas').length > 0 && $('#photo').length > 0 && $('#takePhotoBtn').length > 0) {
        video = document.getElementById("video");
        canvas = document.getElementById("canvas");
        photo = document.getElementById("photo");
        startbutton = document.getElementById("takePhotoBtn");
    } else {
        return;
    }

    function startup() {
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            // access video stream from cam
            navigator.mediaDevices.getUserMedia({ video: true, audio: false })
                .then((stream) => {
                    // on success, stream it in video tag
                    window.localStream = stream;
                    video.srcObject = stream;
                    video.play();
                })
                .catch((err) => {
                    console.error(`An error occurred: ${err}`);
                    // Añadimos mensaje de error en el modal
                    $('#modalTakePhoto .modal-body .description.hidden').removeClass('hidden');
                    // Ocultamos boton de hacer captura
                    $('#takePhotoBtn').addClass('d-none');
                });
        }

    }

    function takepicture() {
        // Capture a photo by fetching the current contents of the video
        // and drawing it into a canvas, then converting that to a PNG
        // format data URL. By drawing it on an offscreen canvas and then
        // drawing that to the screen, we can change its size and/or apply
        // other changes before drawing it.
        let context = canvas.getContext("2d");

        canvas.width = width;
        canvas.height = height;
        context.drawImage(video, 0, 0, width, height);

        // Para mostrar el thubnail de la foto tomada
        let data = canvas.toDataURL("image/png");
        photo.setAttribute("src", data);

        // Guardamos la imagen del canvas al input type file
        // convert to Blob (async)
        canvas.toBlob((blob) => {
            let file = new File([blob], "mycanvas.png", { type: 'image/png' });
            // build a DataTransfer object
            let dT = new DataTransfer();
            // append the File to the DataTransfer's items list
            dT.items.add(file);

            // set the .files property of your <input type="file"> to the DataTransfer's .files
            document.querySelector("input#id_profile_image").files = dT.files;
            $("input#id_profile_image").trigger('change');
        });
    }

    // Escuchamos evento click en el boton que abre el modal de tomar captura
    $('#showModalTake').on('click', function () {
        startup();
    });

    // Detenemos video streaming si damos click en volver del modal
    $('button[data-bs-target="#editProfileModal"]').on('click', function () {
        if (window.localStream) {
            window.localStream.getTracks().forEach(function (track) {
                if (track.readyState == 'live' && track.kind === 'video') {
                    track.stop();
                }
            });
        }
    });

    // Cuando hacemos click para tomar la captura
    startbutton.addEventListener("click", (ev) => {
        ev.preventDefault();
        photoCameraPicture = true;
        takepicture();
        // stop video streaming if any
        if (window.localStream) {
            window.localStream.getTracks().forEach(function (track) {
                if (track.readyState == 'live' && track.kind === 'video') {
                    track.stop();
                }
            });
        }
        // Retornamos al modal anterior
        $('button[data-bs-target="#editProfileModal"]').trigger('click');
    });
}

function readURL(input) {
    let $photoInput = $(input);
    if (!photoCameraPicture) {
        // Eliminados data previa del input type file
        $photoInput.removeData('imageWidth');
        $photoInput.removeData('imageHeight');
        if (input.files && input.files[0]) {
            let reader = new FileReader();

            reader.onload = function (e) {
                // Ponemos la imagen en el src de la imagen
                // $('#photo').attr('src', e.target.result);
                let img = new Image();
                img.src = reader.result;

                img.onload = function () {
                    // Obtenemos el tamaño intrinseco(real sin estilos) de la imagen
                    let imageWidth = img.naturalWidth;
                    let imageHeight = img.naturalHeight;
                    // Se guarda en la data del input type file
                    $photoInput.data('imageWidth', imageWidth);
                    $photoInput.data('imageHeight', imageHeight);
                    // Validamos el input type file
                    let validator = validateProfileImage();
                    validator.element($photoInput);
                    if (imageWidth === 150 && imageHeight === 150) {
                        // Ponemos la imagen en el src de la imagen
                        $('#photo').attr('src', img.src);
                    }
                };
            }

            reader.readAsDataURL(input.files[0]);
        }
    } else {
        // Se guarda en la data del input type file
        $photoInput.data('imageWidth', 150);
        $photoInput.data('imageHeight', 150);
    }
}

function validateProfileImage() {

    // Quitamos attr "required" del input de imagen
    $('#id_profile_image').removeAttr('required');

    // Añadimos validacion custom para tamaño de la imagen
    $.validator.addMethod('dimention', function (value, element, param) {
        if (element.files.length === 0) {
            return true;
        }
        let width = $(element).data('imageWidth');
        let height = $(element).data('imageHeight');
        if (width === param[0] && height === param[1]) {
            return true;
        } else {
            return false;
        }
    }, 'Las imágenes deben ser exactamente de {0}x{1} píxeles.');

    // Modify message jquery validation
    $.extend($.validator.messages, {
        extension: "Solo se permiten imágenes jpg, jpeg y png",
    });

    return $('.update-user__form').validate({
        ignore: [], // solo para este form para validar campo file oculto
        rules: {
            profile_image: {
                // required: true,
                extension: "jpg|jpeg|png|ico|bmp",
                dimention: [150, 150],
                accept: "image/*",
            },
            identification_number: {
                digits: true,
            }
        },
        messages: {
            profile_image: {
                extension: "Solo se permiten imágenes jpg, jpeg y png",
            },
        },
        errorClass: 'error-validacion', // Clase para las alertas de validación
        errorElement: 'p', // Elemento "html" para mostrar el error
        errorPlacement: function (error, element) {
            if (element.attr("name") === 'profile_image') {
                $('.form__element--filecustom').prepend(error);
            } else {
                error.insertAfter(element);
            }
        },
        focusInvalid: false, // para que no intente hacer focus en campo oculto de imagen cuando es invalido, genera error
    });
}

function customUploadFile() {
    // Validamos campos formulario
    validateProfileImage();
    // Validacion para imagen requerida y no salga el error  :
    // https://radu.link/fix-invalid-form-control-not-focusable/

    // $('.update-user__form .update-user__form__actions .btn').on('click', function (event) {
    //     event.preventDefault();
    //     // let inputFileValue = $('.update-user__form #id_profile_image').val();
    //     // // Si no tiene nada, creamos mensaje de error
    //     // if (inputFileValue === '') {
    //     //     if ($('.form__element--filecustom .error-validacion.requerido').length <= 0) {
    //     //         $('.form__element--filecustom').prepend(`<p class="error-validacion requerido">La imagen es requerida</p>`);
    //     //     }
    //     //     return;
    //     // } else {
    //     //     if ($('.form__element--filecustom .error-validacion').hasClass('requerido')) {
    //     //         $('.form__element--filecustom .error-validacion.requerido').remove();
    //     //     }
    //     // }
    //     // Si todo esta ok enviamos el form
    //     if ($('.update-user__form').valid()) {
    //         $('.update-user__form').trigger('submit');
    //     }
    // });

    // Escuchamos cambios en el campo de imagen
    // $('.update-user__form #id_profile_image').on('change', function () {
    //     let inputFileValue = $(this).val();
    //     if ($('.form__element--filecustom .error-validacion.requerido').length > 0 && (inputFileValue !== '')) {
    //         $('.form__element--filecustom .error-validacion.requerido').remove();
    //     }
    // });

    $('#customUploadBtn').on('click', function () {
        photoCameraPicture = false;
        // Obtenemos el input type file
        let $inputFile = $(this).parents('.form__element--filecustom').find('input[type="file"]');
        // Disparamos click en input type file oculto
        $inputFile.trigger('click');
        // Escuchamos cambios input type file
        // $inputFile.on('change', function () {
        //     readURL(this);
        // });
    });

    // Escuchamos cambios input type file
    let $inputFile = $("input#id_profile_image");
    $inputFile.on('change', function () {
        readURL(this);
    });

}

/*==================== ADD PDF FOR POLITICAS DE PRIVAVIDAD NEWSLETTER ====================*/
function addLinkPoliticaNewsletter() {
    let termLinks = {
        'co': 'https://www.dane.gov.co/index.php/servicios-al-ciudadano/tramites/transparencia-y-acceso-a-la-informacion-publica/terminos-de-uso',
        'bo': 'https://www.ine.gob.bo/index.php/transparencia/normativa-general/#1590593734184-331f1b15-30f1',
        'cl': 'https://www.ine.gob.cl/terminos-de-uso-y-licencia-de-datos-abiertos',
        'pe': 'https://www.gob.pe/institucion/pcm/informes-publicaciones/698037-politica-de-privacidad-de-gob-pe'
    };

    function getCurrentCountrytermLink() {
        let $body = $('body');
        return termLinks[$body.attr('class')];
    }

    const currentCountryLink = getCurrentCountrytermLink();

    // Cambiamos enlace de terminos y condiciones Newsletter
    if ($('.newsletter-region').length) {
        $('.newsletter-form label[for="id_terms"]').html(`Al inscribirte reconoces y aceptas nuestras <a href="${currentCountryLink}" target="_blank">Políticas de privacidad</a>`);
    }
    // Cambiamos enlace de terminos y condiciones footer copy
    $('.terms-policy-content .terms-and-policy .policy-link').each(function(){
        $(this).attr('href', currentCountryLink);
    });
}

/*==================== VALIDATE FORM CREATE PROJECT ====================*/

function validateCreateProject() {
    if ($("#createNewProject").length > 0) {

        searchForSelectsProjectCreate();

        $('input[type="file"]').on('change', function () {
            let inputSelect = $(this)
            inputSelect.removeData('imageWidth');
            inputSelect.removeData('imageHeight');
            let file = this.files[0];
            let img = new Image();
            img.src = window.URL.createObjectURL(file);
            img.onload = function () {
                inputSelect.data('imageWidth', this.width);
                inputSelect.data('imageHeight', this.height);
                // console.log('width: ' + this.width + ' height: ' + this.height+'');
            }
        });

        // Modify message jquery validation
        $.extend($.validator.messages, {
            required: "Este campo es obligatorio.",
            extension: "Solo se permiten imágenes jpg, jpeg y png",
        });

        // Custom validation width and height of images
        $.validator.addMethod('dimention', function (value, element, param) {
            if (element.files.length == 0) {
                return true;
            }
            let width = $(element).data('imageWidth');
            let height = $(element).data('imageHeight');
            if (width == param[0] && height == param[1]) {
                return true;
            } else {
                // console.log('Vwidth: ' + this.width + ' Vheight: ' + this.height+'');
                return false;
            }
        }, 'Por favor suba una imagen con las especificaciones de la descripción.');

        $.validator.addMethod("idyoutube", function (value, element) {
            return /[0-9A-Za-z_-]{10}[048AEIMQUYcgkosw]/g.test(value);
        }, "Ingrese un código válido.");

        // Validate form
        $('form#createNewProject').validate({
            rules: {
                name: {
                    required: true,
                },
                objetive_project: {
                    required: true,
                },
                tag_project: {
                    required: true,
                },
                provider_project: {
                    required: true,
                },

                description_uno: {
                    required: true,
                },
                // Validate images
                image_project_desk: {
                    extension: "jpg|jpeg|png|ico|bmp",
                    dimention: [1170, 660]
                },
                image_project_mob: {
                    extension: "jpg|jpeg|png|ico|bmp",
                    dimention: [370, 230]
                },

                description_dos: {
                    required: true,
                },
                // Validate images
                image_left_project_desk: {
                    extension: "jpg|jpeg|png|ico|bmp",
                    dimention: [600, 350]
                },
                image_left_project_mob: {
                    extension: "jpg|jpeg|png|ico|bmp",
                    dimention: [370, 230]
                },
                // Validate images
                image_right_project_desk: {
                    extension: "jpg|jpeg|png|ico|bmp",
                    dimention: [600, 350]
                },
                image_right_project_mob: {
                    extension: "jpg|jpeg|png|ico|bmp",
                    dimention: [370, 230]
                },
                youtube: {
                    required: {
                        depends: function (element) {
                            return $("body #id_youtube").val().length > 0;
                        }
                    },
                    minlength: function () {
                        return $("body #id_youtube").val().length > 0 ? 11 : false;
                    },
                    idyoutube: {
                        depends: function (element) {
                            return $("body #id_youtube").val().length > 0;
                        }
                    },
                },
            },
            errorClass: 'error-validacion', // Clase para las alertas de validación
            errorElement: 'p', // Elemento "html" para mostrar el error
            errorPlacement: function (error, element) {
                if ( $(element).is('select') ) {
                    error.insertAfter(element.parent().find('.select2'));
                } else {
                    error.insertAfter(element);
                }
            },
            messages: {
                youtube: {
                    minlength: "Ingrese un código válido",
                },
            },
            submitHandler: function (form) {
                $('.loading').removeClass('d-none');
                // form.submit();
                confirmationProjectModal(form);
            }
        })
    }
}

function confirmationProjectModal(form) {
    // Obtenemos url origin
    let urlApi = window.location.origin;
    let $form = $(form), formAction, actualMessages;

    const messages = [
        {
            'title': 'Crear proyecto',
            'description': 'Se ha creado el proyecto.'
        },
        {
            'title': 'Editar proyecto',
            'description': 'Se ha editado el proyecto.'
        }
    ];

    let pathName = window.location.pathname;
    // Si estamos en edición
    if (pathName.includes("editar")) {
        actualMessages = messages[1];
        // Ocultamos boton crear nuevo
        $('.create-new').addClass('d-none');
    } else {
        actualMessages = messages[0];
    }

    // Modal de confirmación
    let modalBsProject = bootstrap.Modal.getOrCreateInstance(document.getElementById('modalConfirmationProject')),
        $modalConfirmationProject = $('#modalConfirmationProject');

    // Acción formulario
    formAction = $form.attr('action');

    let data = new FormData($form[0]);

    // Hacemos petición Ajax
    $.ajax({
        method: 'POST',
        url: `${urlApi}${formAction}`,
        // data: $form.serialize(),
        data: data,
        contentType: false,
        processData: false,
        success: function (res) {
            // Seteamos mensaje en el modal
            $modalConfirmationProject.find('.description').html(actualMessages["description"]);
            // Cambiamos icono del modal
            $modalConfirmationProject.find('.modal-alert__wrapper-icon').html(`<span class="icon-icon-check"></span>`);
        },
        error: function (jqXHR, estado, error) {
            // Seteamos mensaje en el modal
            $modalConfirmationProject.find('.description').html(`Ha ocurrido un error inesperado ${error}`);
            // Cambiamos icono del modal
            $modalConfirmationProject.find('.modal-alert__wrapper-icon').html(`<span class="icon-alert"></span>`);
        },
        complete: function (jqXHR, estado) {
            // Seteamos mensaje en el modal
            $modalConfirmationProject.find('.modal-title').html(actualMessages["title"]);
            // Ocultamos loader
            $('.loading').addClass('d-none');
            // Mostramos modal
            modalBsProject.show();
        },
    });

    // Escuchamos evento boton crear nuevo
    $('.create-new').on('click', function (event) {
        event.preventDefault();
        window.location.reload();
    });
}

function searchForSelectsProjectCreate(){
    // Array con todos los ids de selects a convertir en proyectos
    let selectsProjects = [
        '#id_tag_project', 
        '#id_provider_any_project', 
        '#id_category_project',
        '#id_related_statistical',
        '#id_theme_project',
        '#id_state_project',
        '#id_rraa_asociate'
    ];

    // Añade buscador a los selects normales y múltiples
    addSearchForSelects(selectsProjects);
}

/*==================== VALIDATE FORM CREATE DEMAND ====================*/

function validateCreateDemand() {

    $.extend($.validator.messages, {
        extension: "Tipo de archivo no válido.",
    });

    $.validator.addMethod('filesize', function (value, element, param) {
        return this.optional(element) || (element.files[0].size <= param * 1000000)
    }, 'No se puede subir archivos que pesen más de {0}MB');

    $('#demandCreateForm').validate({
        rules: {
            title: {
                required: true,
            },
            inventory: {
                required: true,
            },
            project: {
                required: true,
            },
            description: {
                required: true,
                maxlength: 300, // máx 300 caracteres
            },
            use: {
                required: true,
            },
            use_other: {
                required: true,
            },
            time: {
                required: true,
            },
            product: {
                required: true,
                maxlength: 300, // máx 300 caracteres
            },
            category: {
                required: true,
            },
            status: {
                required: true,
            },
            theme: {
                required: true,
            },
            topic: {
                required: true,
            },
            file_demand: {
                extension: "pdf|doc|docx|xls|xlsx|jpg|jpeg|png|",
                filesize: 5,
            },
        },
        errorClass: 'error-validacion', // Clase para las alertas de validación
        errorElement: 'p', // Elemento "html" para mostrar el error
        submitHandler: function (form) {
            $('.loading').removeClass('d-none');
            // form.submit();
            confirmationDemandModal(form);
        }
    });
}

function showHideDemandCreateConditional(){
    // Muestra o no, otros campos del formulario dependiendo de la opción del select
    showHideFields(false, ['id_use_other'], '#id_use');

    $('#id_use').on('change', function () {
        showHideFields(true, ['id_use_other'], '#id_use');
        validateCreateDemand();
    });
}

function searchForSelectsDemandCreate(){
    // Array con todos los ids de selects a convertir en crear solicitud
    let selectsDemandCreate = [
        '#id_inventory',
        '#id_project',
        '#id_category',
        '#id_theme',
        '#id_topic',
        '#id_key_words'
    ];

    // Añade buscador a los selects normales y múltiples
    addSearchForSelects(selectsDemandCreate);
}

function confirmationDemandModal(form) {
    // Obtenemos url origin
    let urlApi = window.location.origin;
    let $form = $(form), formAction, actualMessages;


    const messages = [
        {
            'title': 'Crear nueva solicitud',
            'description': 'Se ha creado la nueva solicitud correctamente.'
        },
        {
            'title': 'Editar solicitud',
            'description': 'Se ha editado la solicitud correctamente.'
        }
    ];

    let pathName = window.location.pathname;
    // Si estamos en edición
    if (pathName.includes("editar")) {
        actualMessages = messages[1];
        // Ocultamos boton crear nuevo
        $('.create-new').addClass('d-none');
    } else {
        actualMessages = messages[0];
    }

    // Modal de confirmación
    let modalBsDemand = bootstrap.Modal.getOrCreateInstance(document.getElementById('modalConfirmationDemand')),
        $modalConfirmationDemand = $('#modalConfirmationDemand');

    // Acción formulario
    formAction = $form.attr('action');

    let data = new FormData($form[0]);

    // Hacemos petición Ajax
    $.ajax({
        method: 'POST',
        url: `${urlApi}${formAction}`,
        // data: $form.serialize(),
        data: data,
        contentType: false,
        processData: false,
        success: function (res) {
            // Seteamos mensaje en el modal
            $modalConfirmationDemand.find('.description').html(actualMessages["description"]);
            // Cambiamos icono del modal
            $modalConfirmationDemand.find('.modal-alert__wrapper-icon').html(`<span class="icon-icon-check"></span>`);
        },
        error: function (jqXHR, estado, error) {
            // Seteamos mensaje en el modal
            $modalConfirmationDemand.find('.description').html(`Ha ocurrido un error inesperado ${error}`);
            // Cambiamos icono del modal
            $modalConfirmationDemand.find('.modal-alert__wrapper-icon').html(`<span class="icon-alert"></span>`);
        },
        complete: function (jqXHR, estado) {
            // Seteamos mensaje en el modal
            $modalConfirmationDemand.find('.modal-title').html(actualMessages["title"]);
            // Ocultamos loader
            $('.loading').addClass('d-none');
            // Mostramos modal
            modalBsDemand.show();
        },
    });

    // Escuchamos evento boton crear nuevo
    $('.create-new').on('click', function (event) {
        event.preventDefault();
        window.location.reload();
    });

}

function addCharacterCounter(fieldsArray){
    fieldsArray.forEach((fieldId) => {
        // Escuchamos evento input
        $(fieldId).on('input', function() {
            // Obtenemos el contenedor de nuestro contador
            let $counterWrapper = $(this).siblings('.counter');
            // Obtenemos el maximo número de caracteres permitidos
            const maxLength = $counterWrapper.attr('data-maxlength');
            // Contamos el número de caracteres actuales
            let currentLength = $(this).val().length;
            // Mostramos valores en el contador
            $counterWrapper.html(`${currentLength}/${maxLength}`);
        });
	});
}

function addCharacterCountersDemandCreate(){
    // array con selectores de los campos a añadirles contador de caracteres
    const fields = [
        '#id_description',
        '#id_product'
    ];
    // Añadimos contador de caracteres
    addCharacterCounter(fields);
}

function allCreateDemandFunctions(){
    searchForSelectsDemandCreate();
    validateCreateDemand()
    showHideDemandCreateConditional();
    addCharacterCountersDemandCreate();   
}

/*==================== VALIDATE FORM CREATE NEW DOCUMENT ====================*/

function validateCreateNewDocument() {
    if ($("#createNewDocument").length > 0) {

        // Modify message jquery validation
        $.extend($.validator.messages, {
            required: "Este campo es obligatorio.",
            extension: "Solo se permiten archivos pdf",
        });

        // Validate form
        $('form#createNewDocument').validate({
            rules: {
                title: {
                    required: true,
                },
                document: {
                    required: true,
                    extension: "pdf",
                },
                assigned_to: {
                    required: true,
                },
                copy_to: {
                    required: true,
                },
            },
            submitHandler: function (form) {
                $('.loading').removeClass('d-none');
                form.submit();
            }
        })
    }
}

/*==================== MOVE ACTIVITIES FOR ACTIVITY-MANAGMENT ====================*/
function moveActivitiesManagment() {
    if ($('.block-activity-management').length && !$('.provider-detail').length) {
        // Create los div parent of the item
        $('.block-activity-management-item.box-activities .activity-item').each(function () {
            let heighItem = jQuery(this).innerHeight();
            let dataName = jQuery(this).attr('data-name');

            jQuery('.block-activity-management-item-content').each(function (index) {
                jQuery(this).append(`<div class="parent-item" data-name="${dataName}" style="height: ${heighItem + 4}px;"></div>`)
            })
        })

        // Move item in block-start
        jQuery('.block-activity-management-item.box-activities .block-activity-management-item-content > .activity-item').each(function () {
            let dataName = jQuery(this).attr('data-name');
            jQuery(this).appendTo(jQuery('.block-activity-management-item.box-activities .block-activity-management-item-content .parent-item[data-name="' + dataName + '"]'))
        })

        let blockActivityManagment = $('.block-activity-management');

        blockActivityManagment.each(function (index) {
            let blockStart = $(this).find('.block-activity-management-item.box-start .block-activity-management-item-content');
            let blockProcess = $(this).find('.block-activity-management-item.box-process .block-activity-management-item-content');
            let blockRevision = $(this).find('.block-activity-management-item.box-revision .block-activity-management-item-content');
            let blockFinalized = $(this).find('.block-activity-management-item.box-finalized .block-activity-management-item-content');
            let managamentNumber = 'management-' + index;

            $(this).addClass(managamentNumber)

            if ($(this).find('.block-activity-management-item-content .box-ini')) {
                $('.block-activity-management.' + managamentNumber + ' .box-activities .block-activity-management-item-content .box-ini').each(function () {
                    let dataNameItem = $(this).attr('data-name');
                    $(this).appendTo(blockStart.find('.parent-item[data-name="' + dataNameItem + '"]'));
                })
            }
            if ($(this).find('.block-activity-management-item-content .box-pr')) {
                $('.block-activity-management.' + managamentNumber + ' .box-activities .block-activity-management-item-content .box-pr').each(function () {
                    let dataNameItem = $(this).attr('data-name');
                    $(this).appendTo(blockProcess.find('.parent-item[data-name="' + dataNameItem + '"]'));
                })
            }
            if ($(this).find('.block-activity-management-item-content .box-re')) {
                $('.block-activity-management.' + managamentNumber + ' .box-activities .block-activity-management-item-content .box-re').each(function () {
                    let dataNameItem = $(this).attr('data-name');
                    $(this).appendTo(blockRevision.find('.parent-item[data-name="' + dataNameItem + '"]'));
                })
            }
            if ($(this).find('.block-activity-management-item-content .box-fi')) {
                $('.block-activity-management.' + managamentNumber + ' .box-activities .block-activity-management-item-content .box-fi').each(function () {
                    let dataNameItem = $(this).attr('data-name');
                    $(this).appendTo(blockFinalized.find('.parent-item[data-name="' + dataNameItem + '"]'));
                })
            }
        })

        // Remove loader and overflow
        blockActivityManagment.removeClass('overflow-hidden');
        blockActivityManagment.find('.loading').addClass('d-none');

    }
}

/*==================== EVENT CLICK ACCORDION BLOCK-ACTIVITY-MANAGEMENT ====================*/
function eventClickAccordionBlockActivityManagement() {
    if ($('.profile-functionary .block-management-body').length || $('.provider-detail .providerRequests').length) {
        $('.accordion-secondary .accordion-header .accordion-button').on('click', function () {
            setTimeout(() => {
                processMoveItemActivityManagement('profile-functionary');
            }, 500);
        })
        $('.card-record-collapse .collapse__header .collapse__left').on('click', function () {
            $('.card-record-collapse > .collapse').each(function () {
                let acordionHeader = $(this).closest('.card-record-collapse').find('> .collapse__header');
                acordionHeader.find('.collapse__left').addClass('collapsed').attr('aria-expanded', 'false');
                $(this).removeClass('show');

            });
            $(this).closest('.card-record-collapse').find('> .collapse').addClass('show');

            setTimeout(() => {
                processMoveItemActivityManagement('provider-detail');
            }, 500);
        })

        function processMoveItemActivityManagement(pages) {
            let collapseOpen = '';

            if (pages == 'profile-functionary') {
                collapseOpen = $('.accordion-secondary .accordion-item .collapse.show');
            }
            if (pages == 'provider-detail') {
                collapseOpen = $('.card-record-collapse .collapse.show');
            }


            if (!collapseOpen.hasClass('orderly')) {
                collapseOpen.find('.block-activity-management-item.box-activities .activity-item').each(function () {
                    let heighItem = $(this).innerHeight();
                    let dataName = $(this).attr('data-name');

                    collapseOpen.find('.block-activity-management-item-content').each(function (index) {
                        $(this).append(`<div class="parent-item" data-name="${dataName}" style="height: ${heighItem + 4}px;"></div>`)
                    })
                })

                // Move item in block-start
                collapseOpen.find('.block-activity-management-item.box-activities .block-activity-management-item-content > .activity-item').each(function () {
                    let dataName = $(this).attr('data-name');
                    $(this).appendTo(collapseOpen.find('.block-activity-management-item.box-activities .block-activity-management-item-content .parent-item[data-name="' + dataName + '"]'))
                })

                collapseOpen.find('.block-activity-management').each(function (index) {
                    let blockStart = $(this).find('.block-activity-management-item.box-start .block-activity-management-item-content');
                    let blockProcess = $(this).find('.block-activity-management-item.box-process .block-activity-management-item-content');
                    let blockRevision = $(this).find('.block-activity-management-item.box-revision .block-activity-management-item-content');
                    let blockFinalized = $(this).find('.block-activity-management-item.box-finalized .block-activity-management-item-content');
                    let managamentNumber = 'management-' + index;

                    $(this).addClass(managamentNumber)

                    if ($(this).find('.block-activity-management-item-content .box-ini')) {
                        $('.block-activity-management.' + managamentNumber + ' .box-activities .block-activity-management-item-content .box-ini').each(function () {
                            let dataNameItem = $(this).attr('data-name');
                            $(this).appendTo(blockStart.find('.parent-item[data-name="' + dataNameItem + '"]'));
                        })
                    }
                    if ($(this).find('.block-activity-management-item-content .box-pr')) {
                        $('.block-activity-management.' + managamentNumber + ' .box-activities .block-activity-management-item-content .box-pr').each(function () {
                            let dataNameItem = $(this).attr('data-name');
                            $(this).appendTo(blockProcess.find('.parent-item[data-name="' + dataNameItem + '"]'));
                        })
                    }
                    if ($(this).find('.block-activity-management-item-content .box-re')) {
                        $('.block-activity-management.' + managamentNumber + ' .box-activities .block-activity-management-item-content .box-re').each(function () {
                            let dataNameItem = $(this).attr('data-name');
                            $(this).appendTo(blockRevision.find('.parent-item[data-name="' + dataNameItem + '"]'));
                        })
                    }
                    if ($(this).find('.block-activity-management-item-content .box-fi')) {
                        $('.block-activity-management.' + managamentNumber + ' .box-activities .block-activity-management-item-content .box-fi').each(function () {
                            let dataNameItem = $(this).attr('data-name');
                            $(this).appendTo(blockFinalized.find('.parent-item[data-name="' + dataNameItem + '"]'));
                        })
                    }
                })

                collapseOpen.find('.loading').css('display', 'none');
                collapseOpen.addClass('orderly');

            }
        }
    }
}

/*==================== ADD ATTRIBUTE TARGE:BLANK TO LINK EXTERNAL FOOTER ====================*/
function addAttributeTargetBlankFooter() {
    if ($('.footer').length) {
        $('.footer .footer-menu-region.help-menu .footer-menu-link').each(function () {
            if ($(this).attr('href').indexOf('http') > -1) {
                $(this).attr('target', '_blank');
            }
        })
        $('.footer .footer-menu-region.interest-menu .footer-menu-link').each(function () {
            if ($(this).attr('href').indexOf('http') > -1) {
                $(this).attr('target', '_blank');
            }
        })
    }
}

/*==================== SHOW PREVIEW OF FILE LOAD IN DETAILS-INVENTORY ====================*/

function showPreviewFileDetailsInventory() {
    if ($('.detail_inventory').length) {
        let myModalPreviewFile = new bootstrap.Modal(document.getElementById('modalPreviewFile'));

        $('.sample-data .data-actions .preview').on('click', function (e) {
            e.preventDefault();

            if (!$(this).hasClass('data-obtained')) {
                let urlLink = $(this).attr('href');
                $("#iframeFilePreview .table-responsive").load(urlLink, function (e) {
                    $('.sample-data .data-actions .preview').addClass('data-obtained');
                    myModalPreviewFile.show();
                });
                return false;
            }

            myModalPreviewFile.show();

        });
    }
}

/*==================== ADD PLACEHOLDER TO CREATE COMMENTS ====================*/
function addPlaceHolderCreateComments() {
    if ($('.detail_inventory .list-comments').length) {
        $('.create-comment form textarea').attr('placeholder', 'Realizar un comentario');
    }
}

/*==================== ORDER COMMENTS ====================*/
function orderComments() {
    if ($('.detail_inventory .list-comments').length) {
        let levelChildren = 1,
            screenMobile;
        if (screenWidth > 992) {
            $('.detail_inventory .list-comments-mobile').remove();
            screenMobile = false;
        } else {
            $('.detail_inventory .container-of-list-comment').remove();
            screenMobile = true;
        }

        // Function for show line of comment children
        function showLineCommentParent() {
            $('.comment-initial > .data-comment').each(function (index) {
                let containerCommentPrimary = $(this);

                // Heigh this element
                let containerParent = containerCommentPrimary.closest('.container-comment');
                let heightThisComment = containerParent.innerHeight();
                // Calculte the last ul comment
                let heightLastCommentChildren;
                heightLastCommentChildren = containerCommentPrimary.find('> .comment-children').last().innerHeight();

                // Set height line down comment
                containerParent.find('> .icon-comment .linedown').css('height', heightThisComment - heightLastCommentChildren);

                // Hiden tab-pane
                if (index != 0) {
                    containerCommentPrimary.closest('.tab-pane').removeClass('show active');
                }
            })

            let firstNav = $('body .container-of-list-comment .nav-link:first');
            let idfirstNav = firstNav.attr('id');
            firstNav.addClass('active').attr('aria-selected', true);
            $('body .container-of-list-comment .tab-content div[aria-labelledby="' + idfirstNav + '"]').addClass('active show').attr('aria-selected', true);

            // Call funtion for show line of comments

            // Cerrar el loader
            $('.loading').addClass('d-none');
            $('.list-comments').css('height', 'auto');
            $('.container-of-list-comment').css({ 'opacity': '1', 'pointer-events': 'auto' });
            $('.create-comment').slideDown();

        }

        // If is mobile create template of acordion
        if (!screenMobile) {
            let arrayOfDate = [],
                managamentNumber = 0,
                listCommentDesktop = $('.container-of-list-comment');

            /* Creating a new accordion item for each date. */
            $('.container-of-list-comment .date-comments p').each(function () {
                let date = $(this).text().trim();
                if (!arrayOfDate.includes(date)) {
                    managamentNumber++;
                    arrayOfDate.push(date);

                    let templateButton = `
                        <button class="nav-link" id="data-acordion-${managamentNumber}" data-bs-toggle="pill" data-bs-target="#acordion-${managamentNumber}" type="button" role="tab" aria-controls="acordion-${managamentNumber}" aria-selected="false">${date}</button>
                    `;
                    let templateTabPane = `
                        <div class="tab-pane fade style-scrooll active show" id="acordion-${managamentNumber}" role="tabpanel" aria-labelledby="data-acordion-${managamentNumber}" data-date="${date}" tabindex="0" aria-selected="false"></div>
                    `;

                    listCommentDesktop.find('.nav').prepend(templateButton);
                    listCommentDesktop.find('.tab-content').prepend(templateTabPane);
                }
            })

            listCommentDesktop.find('.date-comments').remove();
            listCommentDesktop.find('.nav').prepend(`<h3 class="subtitle">Actualizaciones</h3>`)

            /* Adding the comments to the accordion item. */
            listCommentDesktop.find('.container-comment.comment-initial').each(function () {
                let date = $(this).attr('data-date').trim();

                $(this).appendTo(listCommentDesktop.find(`.tab-content .tab-pane[data-date="${date}"]`))
            });

        }

        // Order comment with reply
        $('.comment-initial > .data-comment').each(function () {
            let containerCommentPrimary = $(this);
            let idCommentParent = parseInt($(this).attr('data-id-comment'));
            levelChildren = 0;

            $('.list-comments .comment-children').each(function () {
                let idCommentChildren = parseInt($(this).attr('data-parent'));

                if (idCommentParent === idCommentChildren) {
                    $(this).appendTo(containerCommentPrimary);
                } else {
                    idCommentChildren > levelChildren ? levelChildren = idCommentChildren : '';
                }
            })

            if (levelChildren > 1) {
                for (let i = 1; i < levelChildren; i++) {
                    $('.list-comments .comment-children').each(function () {
                        let parentComment = $(this);
                        let idParentComment = $(this).find('.data-comment').attr('data-id-comment');

                        $('.list-comments .comment-children').each(function () {
                            let idCommentChildren = $(this).attr('data-parent');

                            if (idParentComment === idCommentChildren) {
                                $(this).appendTo(parentComment);
                            }
                        })

                        // Heigh this element
                        let heightThisComment = parentComment.innerHeight();
                        // Calculte the last ul comment
                        let heightLastCommentChildren = parentComment.find('> .comment-children').last().innerHeight();

                        // Set height line down comment
                        parentComment.find('> .comment-children-container .icon-comment .linedown').css('height', heightThisComment - heightLastCommentChildren);
                    })

                }
            }


        })

        if (screenMobile) {
            let arrayOfDate = [],
                managamentNumber = 0,
                listCommentMobile = $('.list-comments-mobile');

            // Add who is the parent of the comment
            $('.list-comments .container-comment.comment-children').each(function () {
                let idCommentChildren = $(this).attr('data-parent');
                let userReply;

                if ($(this).parent('.comment-children').length) {
                    userReply = $(this).parent('.comment-children').find('> .comment-children-container .data-comment > .data-comment-header .data-comment-header-user').text().trim();
                } else {
                    userReply = $(this).parent('.data-comment').find('> .data-comment-header .data-comment-header-user').text().trim();
                }

                $(this).find('> .comment-children-container .data-comment .data-comment-header').prepend(`<p class="data-comment-header-reply">En respuesta a ${userReply}</p>`);

            })

            /* Creating a new accordion item for each date. */
            $('.list-comments-mobile .date-comments p').each(function () {
                let date = $(this).text().trim();
                if (!arrayOfDate.includes(date)) {
                    managamentNumber++;
                    arrayOfDate.push(date);

                    let template = `
                        <div class="accordion-item" data-date="${date}">
                            <h2 class="accordion-header" id="data-acordion-${managamentNumber}">
                                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#acordion-${managamentNumber}" aria-expanded="false" aria-controls="acordion-${managamentNumber}">${date}</button>
                            </h2>
                            <div id="acordion-${managamentNumber}" class="accordion-collapse collapse" aria-labelledby="data-acordion-${managamentNumber}" data-bs-parent="#accordionComments">
                                <div class="accordion-body style-scrooll"></div>
                            </div>
                        </div>
                    `;

                    listCommentMobile.find('.accordion').prepend(template);
                }
            })

            listCommentMobile.find('.date-comments').remove();

            /* Adding the comments to the accordion item. */
            listCommentMobile.find('.container-comment.comment-initial').each(function () {
                let date = $(this).attr('data-date').trim();

                $(this).appendTo(listCommentMobile.find(`.accordion-item[data-date="${date}"] .accordion-body`))
            });
        }


        setTimeout(() => {
            if (!screenMobile) {
                setTimeout(() => {
                    showLineCommentParent();
                }, 500);

            } else {
                // Cerrar el loader
                $('.loading').addClass('d-none');
                $('.list-comments').css('height', 'auto');
                $('.list-comments-mobile').slideDown();
                $('.create-comment').slideDown();
            }

        }, 1000);


    }
}

/*==================== LOAD MODAL FOR REQUEST COMMENT ====================*/
function loadModalRequestComment() {
    if ($('.detail_inventory .list-comments').length) {
        let replyComments = new bootstrap.Modal(document.getElementById('modalReplyComments'));
        $('body').on('click', '.container-comment .data-comment-body .reply-comment a', function (e) {
            e.preventDefault();
            let linkReplyComment = $(this).attr('href');
            let parentElementComment = $(this).closest('.data-comment');
            let modalBody = $('#modalReplyComments .modal-body');


            parentElementComment.find('> .data-comment-header').clone().appendTo(modalBody.find('.data-comment').text(''));
            parentElementComment.find('> .data-comment-body').clone().appendTo(modalBody.find('.data-comment'));

            modalBody.find("> .reply-comment").load(linkReplyComment, function (e) {
                $('#modalReplyComments .create-comment form textarea').attr('placeholder', 'Realizar un comentario');
                $('#modalReplyComments .modal-body > .reply-comment form').attr('action', linkReplyComment);
                replyComments.show();

                let replyComment = $("#modalReplyComments form");
                validateNoteList(replyComment);
            });
            return false;
        })
    }
}


/*==================== MEGA SEARCH MENU ====================*/
function megaSearchMenu() {

    // Traer info ajax
    function getMenuFilter(container, url) {
        $(container).load(url)
    }

    // Set Mega search
    function setMegaSearch(radio, $providerInput, $inventoryInput) {
        let radioValue = $(radio).val();
        if (radioValue === 'inventario') {
            // Ocultamos input proveedor
            $providerInput.hide();
            // Mostramos input inventario
            $inventoryInput.show();
            // Traemos info ajax
            getMenuFilter('.dropdownSearchMenu-load', '/menu-filtro-inventario/');
            changeTextSelect();
        } else if (radioValue === 'proveedor') {
            // Ocultamos input inventario
            $inventoryInput.hide();
            // Mostramos input proveedor
            if ($providerInput.hasClass('d-none')) {
                $providerInput.removeClass('d-none');
            }
            $providerInput.show();
            // Traemos info ajax
            getMenuFilter('.dropdownSearchMenu-load', '/menu-filtro-proveedor/');
            changeTextSelect();
        }
    }

    function removeDuplicateInputs() {
        // removemos los input ocultos para evitar parametros duplicados en URL
        let screenWidth = $(window).width();

        if (screenWidth < 992) {
            // Mobile
            let $inventoryInput = $('header .navbar .search-records .input-group input#id_title');
            let $providerInput = $('header .navbar .search-records .input-group input#id_name');
            $inventoryInput.remove();
            $providerInput.remove();
        } else {
            // Desktop
            let $inventoryInputMobile = $('header .navbar .search-records .input-group input#id_title_mobile');
            let $providerInputMobile = $('header .navbar .search-records .input-group input#id_name_mobile');
            $inventoryInputMobile.remove();
            $providerInputMobile.remove();
        }

    }

    function removeAndSend() {
        // removemos los input ocultos para evitar parametros duplicados en URL
        removeDuplicateInputs();
        // Obtenemos id del form
        let formId = $('.dropdownSearchMenu-load').find('form').attr('id');
        // Enviamos form
        $('#' + formId).trigger('submit');
    }

    function manageSearch($searchbyRadios, $inventoryInput, $providerInput, $submitBtn) {
        // Checkeamos por defecto RRAA(inventario)
        $searchbyRadios.closest('input[value="inventario"]').prop('checked', true);

        // Ocultamos input proveedor
        $providerInput.hide();

        // Traemos info ajax
        getMenuFilter('.dropdownSearchMenu-load', '/menu-filtro-inventario/');

        // Escuchamos cambios en esos radios
        $searchbyRadios.on('change', function () {
            setMegaSearch(this, $providerInput, $inventoryInput)
        });
        // Escuchamos click para submit
        $submitBtn.on('click', function (event) {
            event.preventDefault();
            removeAndSend();
        });
        // Escuchamos click en el submitBtn del form agregado por ajax
        $('body').on('click', '.dropdownSearchMenu-load form input[type="submit"]', function (event) {
            event.preventDefault();
            removeAndSend();
        });
    }

    // Para Mobile
    let $searchbyRadiosMobile = $('#dropdownSearchMobile input[name="buscarpor"]');
    let $inventoryInputMobile = $('header .navbar .search-records .input-group input#id_title_mobile');
    let $providerInputMobile = $('header .navbar .search-records .input-group input#id_name_mobile');
    let $submitBtnMobile = $('#btnSearchMobile');

    manageSearch($searchbyRadiosMobile, $inventoryInputMobile, $providerInputMobile, $submitBtnMobile);

    // Para Desktop
    let $searchbyRadiosDesk = $('#dropdownSearch input[name="order"]');
    let $inventoryInputDesk = $('header .navbar .search-records .input-group input#id_title');
    let $providerInputDesk = $('header .navbar .search-records .input-group input#id_name');
    let $submitBtnDesk = $('#btnSearchHeader');

    manageSearch($searchbyRadiosDesk, $inventoryInputDesk, $providerInputDesk, $submitBtnDesk);

}
/*==================== DELETE ACCESS RRAA ====================*/
function deleteAccessRraa() {
    $('body').on('click', '.groups-profile-main .access-rra-content .table-user-action .btn-delete', function () {
        // Obtenemos la url para borrar el acceso
        let actionUrl = $(this).attr('data-url');
        // Obtenemos el enlace para añadir la url
        $('#modalConfirmationDelete').find('a.btn-confirm-modal').attr('href', actionUrl);
    });
}

/*==================== CONTACT PROVIDER ====================*/
function contactProvider() {


    // verificamos que exista la sección dentro de perfil de proveedor
    if ($('.inventory-provider').length) {
        // Obtenemos url origin
        let urlApi = window.location.origin;

        // Modal de confirmación
        let modalConfirmationContact = new bootstrap.Modal(document.getElementById('modalConfirmationContact'));

        // Modal de respuesta del server
        let modalServerContact = new bootstrap.Modal(document.getElementById('modalServerContact'));


        // Escuchamos evento click en el boton para abrir modal
        $('body').on('click', '.confirm-contact', function (event) {
            event.preventDefault();
            // Obtenemos atributo data-action
            let urlAction = $(this).attr('data-action');
            //Obtenemos titulo RRAA
            let inventoryTitle = $(this).closest('.cards-activity-item').find('.cards-activity-item-body .item-description').text().trim();
            // Seteamos texto del modal
            $('#modalConfirmationContact').find('.description').html(`¿Está seguro de querer contactar al proveedor propietario del RRAA: <b>${inventoryTitle}</b>?`);
            // seteamos la data-action en el boton del modal
            $('#modalConfirmationContact').find('.contact-provider').attr('data-action', urlAction);
            // Mostramos modal
            modalConfirmationContact.show();
        });

        // Escuchamos evento click en el boton para contactar proveedor
        $('body').on('click', '#modalConfirmationContact .contact-provider', function (event) {
            event.preventDefault();
            // Obtenemos atributo data-action
            let urlAction = $(this).attr('data-action');
            // Obtenemos modal respuesta servidor
            let $modalServer = $('#modalServerContact');

            // Cerramos modal de confirmación
            modalConfirmationContact.hide();

            // Hacemos petición Ajax
            $.ajax({
                type: 'GET',
                url: `${urlApi}${urlAction}`,
                success: function (res) {
                    // console.log("Respuesta server: ",res);
                    if (res.success === "True") {
                        // Cambiamos icono del modal
                        $modalServer.find('.modal-alert__wrapper-icon').html(`<span class="icon-icon-check"></span>`);
                        // Seteamos mensaje en el modal
                        $modalServer.find('.description').html(`Se ha enviado la notificación de contacto al proveedor.`);
                    } else if (res.fail === "True") {
                        // Cambiamos icono del modal
                        $modalServer.find('.modal-alert__wrapper-icon').html(`<span class="icon-alert"></span>`);
                        // Seteamos mensaje en el modal
                        $modalServer.find('.description').html(`Ha ocurrido un error al contactar al proveedor.`);
                    } else {
                        // Seteamos mensaje en el modal
                        $modalServer.find('.description').html(`Ha ocurrido un problema inesperado.`);
                    }
                },
                error: function (jqXHR, estado, error) {
                    // console.log(`jqXHR: ${jqXHR}, estado: ${estado}, error: ${error}`);
                    // Cambiamos icono del modal
                    $modalServer.find('.modal-alert__wrapper-icon').html(`<span class="icon-close-icon"></span>`);
                    // Seteamos mensaje en el modal
                    $modalServer.find('.description').html(`Ha ocurrido un error al contactar al proveedor: ${error}`);
                },
                complete: function (jqXHR, estado) {
                    // console.log(estado);
                    // Mostramos modal respuesta servidor
                    modalServerContact.show();
                },
            });

        });
    }
}

/*==================== VALIDATE FILTER TYPE NUMBER FOR NUMBER NEGATIVE ====================*/
function validateFilterTypeNumber() {
    if ($('input[type="number"]').length) {
        // Validate form create RRAA
        if($('#createRraaForm').length) {
            $('input[type="number"]').each(function () {
                $(this).attr('min', 1);
                // $(this).val('1');
            })    
        }else {
            // Add attr min=0 for not accept negative number
            $('input[type="number"]').each(function () {
                $(this).attr('min', 1);
            })
        }
        
        $('input[type="number"]').on('keypress', function (event) {
            return (event.charCode != 8 && event.charCode == 0 || (event.charCode >= 48 && event.charCode <= 57))
        })

    }
}
/*==================== CHANGES SRC AT ICON IN MEGA PROCESS ====================*/
function changeSrcImagesBoxesActivity() {
    let country = $("body").attr("class");
    switch (country) {
        case "co":
            if ($("main").hasClass("demand-reception")) {
                $(".results-box-data-content .activity-badge img").attr("src", "/static/cepal/dist/assets/images/recepcion-mg-col.svg")
            }
            if ($("main").hasClass("demand-preparation")) {
                $(".results-box-data-content .activity-badge img").attr("src", "/static/cepal/dist/assets/images/preparacion-mg-col.svg")
            }
            if ($("main").hasClass("demand-relation")) {
                $(".results-box-data-content .activity-badge img").attr("src", "/static/cepal/dist/assets/images/relacion-mg-col.svg")
            }
            if ($("main").hasClass("demand-transfer")) {
                $(".results-box-data-content .activity-badge img").attr("src", "/static/cepal/dist/assets/images/transferencia-mg-col.svg")
            }
            break;
        case "pe":
            if ($("main").hasClass("demand-reception")) {
                $(".results-box-data-content .activity-badge img").attr("src", "/static/cepal/dist/assets/images/recepcion-mg-pe.svg")
            }
            if ($("main").hasClass("demand-preparation")) {
                $(".results-box-data-content .activity-badge img").attr("src", "/static/cepal/dist/assets/images/preparacion-mg-pe.svg")
            }
            if ($("main").hasClass("demand-relation")) {
                $(".results-box-data-content .activity-badge img").attr("src", "/static/cepal/dist/assets/images/relacion-mg-pe.svg")
            }
            if ($("main").hasClass("demand-transfer")) {
                $(".results-box-data-content .activity-badge img").attr("src", "/static/cepal/dist/assets/images/transferencia-mg-pe.svg")
            }
            break;
        case "bo":
            if ($("main").hasClass("demand-reception")) {
                $(".results-box-data-content .activity-badge img").attr("src", "/static/cepal/dist/assets/images/recepcion-mg-bo.svg")
            }
            if ($("main").hasClass("demand-preparation")) {
                $(".results-box-data-content .activity-badge img").attr("src", "/static/cepal/dist/assets/images/preparacion-mg-bo.svg")
            }
            if ($("main").hasClass("demand-relation")) {
                $(".results-box-data-content .activity-badge img").attr("src", "/static/cepal/dist/assets/images/relacion-mg-bo.svg")
            }
            if ($("main").hasClass("demand-transfer")) {
                $(".results-box-data-content .activity-badge img").attr("src", "/static/cepal/dist/assets/images/transferencia-mg-bo.svg")
            }
            break;
        case "cl":
            if ($("main").hasClass("demand-reception")) {
                $(".results-box-data-content .activity-badge img").attr("src", "/static/cepal/dist/assets/images/recepcion-mg-cl.svg")
            }
            if ($("main").hasClass("demand-preparation")) {
                $(".results-box-data-content .activity-badge img").attr("src", "/static/cepal/dist/assets/images/preparacion-mg-cl.svg")
            }
            if ($("main").hasClass("demand-relation")) {
                $(".results-box-data-content .activity-badge img").attr("src", "/static/cepal/dist/assets/images/relacion-mg-cl.svg")
            }
            if ($("main").hasClass("demand-transfer")) {
                $(".results-box-data-content .activity-badge img").attr("src", "/static/cepal/dist/assets/images/transferencia-mg-cl.svg")
            }
            break;
        default:
            break;
    }
}
/*==================== MODAL REGISTER RELOAD PAGES EVENT CLICK HERE ====================*/
function modalRegisterReloadPages() {
    if ($('#create-new-provider').length) {
        $('#create-new-provider .modal-body .reload-pages').on('click', function () {
            location.reload();
        });
    }
}

/*==================== CHANGE TEXT OF SELECT WHEN TEXT = "-------" ====================*/
function changeTextSelect() {
    setTimeout(() => {
        if ($('form select').length) {
            $('select').each(function () {
                let firtsOption = $(this).find('option:first');
                if (firtsOption.text().indexOf("----") == 0) {
                    firtsOption.text('Seleccione una opción');
                }
            })
        }

    }, 500);
}

/*====================  EVENT CLICK BTN LOGIN O MY BOARD ====================*/
function eventClickBtnLoginMyBoard() {
    if ($('#btnLoginHeader').length || $('#navbarTogglerMenu .navbar-nav').length) {
        $('#btnLoginHeader, #navbarTogglerMenu .navbar-nav .nav-link').on('click', function () {
            let urlBoton = $(this).attr('href');
            if (urlBoton == '/usuario/perfil/') {
                localStorage.removeItem('tabProfile');
            }
        });
    }
}
/*==================== SHOW FORM TO QUALITY TEST ====================*/
function showFormQualityTest(id) {
    // Mostramos loader
    $('.card-qualitytest-provider .loading').removeClass('d-none');
    // Carga preguntas desde url
    $('#form-qualitytest').load(`/test-calidad/${id}`, () => {
        // Ocultamos loader
        $('.card-qualitytest-provider .loading').addClass('d-none');
        // Removemos elementos con información/instrucciones
        $("#form-qualitytext").remove();

        if ($("body").find("#form-qualitytest form").length > 0) {
            // pregunta o paso actual
            let questionIndex = 0;
            // Botones
            let $btnContinue = $("#quality-btn-continue");
            let $btnVolver = $("#quality-btn-back");
            let $btnSend = $('#quality-btn-send');

            // array con los titulos de las preguntas
            const dataText = $('.form-qualitytest .all-questions .form-qualitytest-questionary-check .label-question').map(function () {
                // obtenemos texto de "Pregunta X" y eliminamos espacios al principio y al final
                return $(this).text().trim();
                // return $(this).text().replace(/\s/g, "");
            });
            let $arrayQuestions = $(".form-qualitytest .all-questions.main-questions .form-qualitytest-questionary");
            // Total preguntas o pasos
            let totalSteps = $arrayQuestions.length;

            function updateQuestionTexts(){
                // Actualizamos titulo pregunta actual
                $("#qualitytest-text").text(dataText[questionIndex]);
                // Actualizamos número pregunta|paso actual (flecha izq color primario)
                $("#qualitytest-number-current").text(questionIndex+1);
                // Actualizamos número pregunta|paso actual (circulo derecho)
                $("#qualitytest-numbers-current").text(questionIndex+1);
                // Mostramos total preguntas|pasos (circulo derecho)
                $("#qualitytest-numbers-total").text(totalSteps);
            }

            updateQuestionTexts();

            function enableBtnContinue(radiosName){
                // Verificamos que alguno de los radios de la pregunta actual este checkeado
                if ($(`input[name="${radiosName}"]:checked`).length > 0) {
                    // Habilitamos boton continuar
                    $btnContinue.removeAttr('disabled');
                    // Si nos encontramos en la ultima pregunta
                    if( questionIndex === totalSteps - 1 ){
                        // habilitamos boton guardar
                        $btnSend.removeAttr('disabled');
                    }
                }else{
                    // Deshabilitamos boton
                    $btnContinue.attr('disabled', true);
                }
            }

            // Obtenemos todos los radios y escuchamos cambios
            $(".form-qualitytest .all-questions .form-qualitytest-questionary-check .assessment-criteria .filter-radio label .radioinput").on('change', function () {
                // Obtenemos el atributo name del grupo de radios actual
                let radiosName = $(this).attr('name');
                enableBtnContinue(radiosName);
            });

            function hideShowQuestion(indexHide, indexShow){
                // ocultamos la pregunta|paso
                $($arrayQuestions[indexHide]).fadeOut("fast");
                // Mostramos la pregunta|paso
                $($arrayQuestions[indexShow]).fadeIn("slow");
            }

            // Escuchamos click en boton continuar
            $btnContinue.on('click', function (event) {
                event.preventDefault();
                // Si el indice actual es menor que la ultima pregunta
                if( questionIndex < totalSteps ){
                    hideShowQuestion(questionIndex, questionIndex + 1);
                    // Aumentamos indice
                    questionIndex++;
                    // Actualizamos textos
                    updateQuestionTexts();
                    if( questionIndex === totalSteps - 1 ){
                        // Ocultamos boton continuar
                        $btnContinue.hide();
                        // Mostramos boton enviar
                        $btnSend.show();
                    }
                    if(questionIndex > 0){
                        // Mostramos boton volver
                        $btnVolver.show();
                    }
                }
                // Deshabilitamos nuevamente el boton continuar
                let radiosName = $($arrayQuestions[questionIndex]).find('.radioinput').attr('name');
                enableBtnContinue(radiosName);
            });

            // Escuchamos click en boton volver
            $btnVolver.on('click', function (event) {
                event.preventDefault();
                // Si el indice actual es mayor a 0
                if( questionIndex  > 0 ){
                    hideShowQuestion(questionIndex, questionIndex - 1);
                    // disminuimos indice
                    questionIndex--;
                    // Actualizamos textos
                    updateQuestionTexts();
                    if( questionIndex === 0 ){
                        // Ocultamos boton volver
                        $('#quality-btn-back').hide();
                    }
                    if(questionIndex < totalSteps - 1 ){
                        // Mostramos boton continuar
                        $btnContinue.show();
                        // ocultamos y deshabilitamos boton guardar
                        $btnSend.hide();
                        $btnSend.attr('disabled', true);
                    }
                }
                // Habilitamos btn continuar
                let radiosName = $($arrayQuestions[questionIndex]).find('.radioinput').attr('name');
                enableBtnContinue(radiosName);
            });

            // Escuchamos click en boton enviar formulario
            $btnSend.on('click', function (event) {
                event.preventDefault();
                // Mostramos loader
                $('.card-qualitytest-provider .loading').removeClass('d-none');
                // Obtenemos url origin
                let urlApi = window.location.origin;
                // Hacemos petición Ajax
                $.ajax({
                    method: 'POST',
                    url: `${urlApi}/test-calidad/${id}`,
                    data: $('#form-qualitytest form').serialize(),
                    complete: function (jqXHR, estado) {
                        // console.log(estado);
                        location.reload();
                    },
                });
            });
        }
    });
}

function providerQualityTest(){
    // Insertamos opción por defecto
    $("#select-quality").prepend(`<option value='' selected disabled >Seleccione una opción</option>`);

    // Añadir buscador al select
    addSearchForSelects(['#select-quality']);

    $("#select-quality").on('change', function () {
        if( $(this).val() !== '' ){
            showFormQualityTest($(this).val());
        }
    });
}

/*==================== SHOW FORM TO REQUEST  ====================*/
function showRraaQuality(id) {

    jQuery(".card-qualityrraa-provider .quality-info").each(function (i, element) {
        if (jQuery(element).attr('data-demand') == id) {
            jQuery(this).addClass("active");
            jQuery(this).find('.demand-quality').val(id);
        } else {
            jQuery(this).removeClass("active")
        }
    })

}

/*==================== HIDE|DELETE NOTIFICATION ====================*/

function sortUnreadRead() {
    let $unread = [],
        $read = [],
        $allItems = [];

    $('.notifications-content-item').each(function () {
        if ($(this).hasClass('read')) {
            $read.push($(this));
        } else {
            $unread.push($(this));
        }
    });

    $allItems = $unread.concat($read);

    $allItems.forEach(function ($item) {
        $item.detach().appendTo('.notifications-content');
    });
}

function showAllNotifications() {
    $('.notifications-content-item').removeClass('d-none');
    // .each(function(){
    //     $(this).removeClass('d-none');
    // });
}

function showReadNotifications() {
    $('.notifications-content-item').addClass('d-none');
    $('.notifications-content-item.read').removeClass('d-none');
}

function showNoReadNotifications() {
    $('.notifications-content-item').removeClass('d-none');
    $('.notifications-content-item.read').addClass('d-none');
}

function notificationFilters() {
    // Escuchar evento filtros
    $('body').on('click', '.notifyfilter', function (event) {
        event.preventDefault();
        let $currentFilter = $(this);
        // Removemos clase activa
        $('.notifyfilter').removeClass('active');
        // Añadimos clase donde se hizo click
        $currentFilter.addClass('active');
        // Ejecutamos acción
        if ($currentFilter.hasClass('allnotify')) {
            showAllNotifications();
        } else if ($currentFilter.hasClass('newnotify')) {
            showNoReadNotifications();
        } else if ($currentFilter.hasClass('readnotify')) {
            showReadNotifications();
        }
    });
}

function notificationConfirmationModal() {
    const notifyMessages = [
        {
            "title": "Eliminar notificación",
            "description": "¿Está seguro de eliminar de forma permanente la notificación?",
        },
        {
            "title": "Marcar notificación como leída",
            "description": "¿Está seguro de marcar la notificación como leída?",
        },
        {
            "title": "Marcar notificación como no leída",
            "description": "¿Está seguro de marcar la notificación como no leída?",
        }
    ];

    // verificamos que exista el modal de notificaciones
    if ($('#modalConfirmationNotify').length > 0) {
        // Obtenemos url origin
        let urlApi = window.location.origin;
        let $deleteForm;
        let $notificationsCounter = $('.number-of-notifications');

        // Modal de confirmación
        let modalBsNotify = bootstrap.Modal.getOrCreateInstance(document.getElementById('modalConfirmationNotify'));

        let $modalConfirmationNotify = $('#modalConfirmationNotify');

        // Ordenar notificaciones
        sortUnreadRead();

        // Filtros
        notificationFilters();

        // Abrir modal eliminar notificación
        $('body').on('click', '.delete-notification', function (event) {
            event.preventDefault();
            let btnDeleteSelector = '.action-notification-delete';
            // Obtenemos atributo data-action
            let urlAction = $(this).attr('data-action');
            let notifyId = $(this).parents('.notifications-content-item').attr('data-notifyid');
            // Obtenemos formulario
            $deleteForm = $(this).parents('form');
            // Seteamos texto del modal
            $modalConfirmationNotify.find('.modal-title').html(notifyMessages[0]['title']);
            $modalConfirmationNotify.find('.description').html(notifyMessages[0]['description']);
            // seteamos la data-action en el boton del modal
            $modalConfirmationNotify.find(btnDeleteSelector).attr({
                'data-action': urlAction,
                'data-notifyid': notifyId,
            });
            // Mostramos boton eliminar y ocultamos el otro
            $modalConfirmationNotify.find(btnDeleteSelector).removeClass('d-none');
            $modalConfirmationNotify.find('.action-notification-hide').addClass('d-none');
            // Mostramos modal
            modalBsNotify.show();
        });

        // Eliminar notificacion
        $('body').on('click', '#modalConfirmationNotify .action-notification-delete', function (event) {
            event.preventDefault();
            // Obtenemos atributo data-action
            let urlAction = $(this).attr('data-action');
            let notifyId = $(this).attr('data-notifyid');

            // Mostramos loader
            $modalConfirmationNotify.find('.loading').removeClass('d-none');
            // $deleteForm.submit();

            // Hacemos petición Ajax
            $.ajax({
                method: 'POST',
                url: `${urlApi}${urlAction}`,
                data: $deleteForm.serialize(),
                success: function (res) {
                    // console.log("Respuesta server: ",res);
                    if (res.success === "True") {
                        // removemos la notificación del DOM
                        $(`.notifications-content-item[data-notifyid="${notifyId}"]`).remove();
                        // // Seteamos mensaje en el modal
                        $modalConfirmationNotify.find('.description').html(`Se ha eliminado la notificación.`);
                    } else if (res.fail === "True") {
                        // Seteamos mensaje en el modal
                        $modalConfirmationNotify.find('.description').html(`Ha ocurrido un error al eliminar.`);
                    } else {
                        // Seteamos mensaje en el modal
                        $modalConfirmationNotify.find('.description').html(`Ha ocurrido un problema inesperado.`);
                    }
                },
                error: function (jqXHR, estado, error) {
                    // Seteamos mensaje en el modal
                    $modalConfirmationNotify.find('.description').html(`Ha ocurrido un error inesperado: ${error}`);
                },
                complete: function (jqXHR, estado) {
                    // console.log(estado);
                    // Cerramos modal de confirmación
                    modalBsNotify.hide();
                    // Ocultamos loader
                    $modalConfirmationNotify.find('.loading').addClass('d-none');
                    // Cambiar número de notificaciones
                    $notificationsCounter.text(parseInt($notificationsCounter.text()) - 1);
                },
            });

        });

        // Abrir modal ocultar notificación
        $('body').on('click', 'button.hide-notification', function (event) {
            event.preventDefault();
            let btnHideSelector = '.action-notification-hide';
            // Obtenemos atributo data-action
            let urlAction = $(this).attr('data-action');
            let notifyId = $(this).parents('.notifications-content-item').attr('data-notifyid');
            // Seteamos texto del modal
            $modalConfirmationNotify.find('.modal-title').html(notifyMessages[1]['title']);
            $modalConfirmationNotify.find('.description').html(notifyMessages[1]['description']);
            // seteamos la data-action en el boton del modal
            $modalConfirmationNotify.find(btnHideSelector).attr({
                'data-action': urlAction,
                'data-notifyid': notifyId,
            });
            // Mostramos boton ocultar
            $modalConfirmationNotify.find(btnHideSelector).removeClass('d-none');
            $modalConfirmationNotify.find('.action-notification-delete').addClass('d-none');
            // Mostramos modal
            modalBsNotify.show();
        });

        // Ocultar/marcar como leída - notificacion
        $('body').on('click', '#modalConfirmationNotify .action-notification-hide', function (event) {
            event.preventDefault();
            // Obtenemos atributo data-action
            let urlAction = $(this).attr('data-action');
            let notifyId = $(this).attr('data-notifyid');

            // Mostramos loader
            $modalConfirmationNotify.find('.loading').removeClass('d-none');

            // Hacemos petición Ajax
            $.ajax({
                type: 'GET',
                url: `${urlApi}${urlAction}`,
                success: function (res) {
                    // console.log("Respuesta server: ",res);
                    if (res.success === "True") {
                        // Marcamos como leida
                        $(`.notifications-content-item[data-notifyid="${notifyId}"]`).addClass('read');
                        // removemos boton ocultar del item
                        $(`.notifications-content-item[data-notifyid="${notifyId}"] button.hide-notification`).remove();
                        // Seteamos mensaje en el modal
                        $modalConfirmationNotify.find('.description').html(`Se ha marcado la notificación como leída.`);
                    } else if (res.fail === "True") {
                        // Seteamos mensaje en el modal
                        $modalConfirmationNotify.find('.description').html(`Ha ocurrido un error al marcar como leída.`);
                    } else {
                        // Seteamos mensaje en el modal
                        $modalConfirmationNotify.find('.description').html(`Ha ocurrido un problema inesperado.`);
                    }
                },
                error: function (jqXHR, estado, error) {
                    // Seteamos mensaje en el modal
                    $modalConfirmationNotify.find('.description').html(`Ha ocurrido un error inesperado ${error}`);
                },
                complete: function (jqXHR, estado) {
                    // console.log(estado);
                    // Ordenamos las notificaciones
                    sortUnreadRead();

                    // Cerramos modal de confirmación
                    modalBsNotify.hide();
                    // Ocultamos loader
                    $modalConfirmationNotify.find('.loading').addClass('d-none');
                },
            });

        });

    }

}

function registerQuality() {
    let dataQuality = jQuery(".card-qualityrraa-provider .quality-info").map(function () {
        return jQuery(this).attr('data-demand');
    }
    ).get();
    showRraaQuality(dataQuality[0])
    $(".demand-quality").on('change', function () {

        if ($(this).val() != '' || $(this).val() != undefined) {
            showRraaQuality($(this).val());
        } else {
            showRraaQuality(dataQuality[0]);
        }
    });
}

/*==================== DELETE NOTE DEMAND DETAIL ====================*/

function noteConfirmationModal() {
    if ($('.card-type-notes-list').length > 0) {
        // Obtenemos url origin
        let urlApi = window.location.origin;
        let $deleteForm, formAction, $noteItem;

        // Modal de confirmación
        let modalBsNote = bootstrap.Modal.getOrCreateInstance(document.getElementById('modalConfirmationNote')),
            $modalConfirmationNote = $('#modalConfirmationNote');

        // Abrir modal eliminar nota
        $('body').on('click', '.delete-note', function (event) {
            event.preventDefault();
            // Obtenemos formulario
            $deleteForm = $(this).parents('form');
            // Acción formulario
            formAction = $deleteForm.attr('action');
            // item nota
            $noteItem = $(this).parents('.card-type-notes-list-item');
            // Seteamos mensaje en el modal
            $modalConfirmationNote.find('.description').html(`¿Está seguro de eliminar la nota?`);
            // Mostramos boton eliminar
            $('#modalConfirmationNote .action-note-delete').removeClass('d-none');
            // Mostramos modal
            modalBsNote.show();
        });

        // Eliminar notificacion
        $('body').on('click', '#modalConfirmationNote .action-note-delete', function (event) {
            event.preventDefault();

            // Mostramos loader
            $modalConfirmationNote.find('.loading').removeClass('d-none');
            // Ocultamos boton eliminar
            $('#modalConfirmationNote .action-note-delete').addClass('d-none');

            // Hacemos petición Ajax
            $.ajax({
                method: 'POST',
                url: `${urlApi}${formAction}`,
                data: $deleteForm.serialize(),
                success: function (res) {
                    // removemos item del DOM
                    $noteItem.remove();
                    // Seteamos mensaje en el modal
                    $modalConfirmationNote.find('.description').html(`Se ha eliminado la nota.`);
                },
                error: function (jqXHR, estado, error) {
                    // Seteamos mensaje en el modal
                    $modalConfirmationNote.find('.description').html(`Ha ocurrido un error inesperado: ${error}`);
                },
                complete: function (jqXHR, estado) {
                    // Ocultamos loader
                    $modalConfirmationNote.find('.loading').addClass('d-none');
                },
            });
        });
    }
}
function addOwnComment() {

    if ($(".detail-list-notes .block-notes .card-type-notes-list-item form").length > 0) {
        $(".detail-list-notes .block-notes .card-type-notes-list-item").addClass("own-comment");
    } else {
        $(".detail-list-notes .block-notes .card-type-notes-list-item").removeClass("own-comment");
    }
}

/*====================  VALIDATION FORM LOAD FILE ====================*/
function validateLoadFileDocumentBoxResult() {
    if ($("#loadDocumentBoxResult").length > 0 || $('#documentsmodal').length > 0) {

        $.validator.addMethod('filesize', function (value, element, param) {
            return this.optional(element) || (element.files[0].size <= param * 1000000)
        }, 'No se puede subir archivos que pesen más de {0}MB');

        $.validator.addMethod("notonlynumbers", function (value) {
            // Acepta letras y nuemros, pero no solo numeros
            if (/^[0-9]*[a-z ][a-zÀ-ú0-9 ]*$/i.test(value)) {
                return true;
            } else {
                return false;
            };
        }, "Solo se aceptan letras y números.");

        if ($("#loadDocumentBoxResult").length > 0) {
            let validator = $("#loadDocumentBoxResult .documentsmodal__form").validate({
                // Specify validation rules
                rules: {
                    assigned_to: {
                        required: true,
                    },
                    copy_to: {
                        required: true,
                    },
                    title: {
                        required: true,
                        minlength: 5,
                        maxlength: 70,
                        notonlynumbers: true
                    },
                    document: {
                        required: true,
                        extension: 'pdf',
                        filesize: 5 // 5MB in bytes
                    },
                },
                // Specify validation error messages
                messages: {
                    assigned_to: {
                        required: "Seleccione una opción",
                    },
                    copy_to: {
                        required: "Seleccione una opción",
                    },
                    title: {
                        required: "Ingrese el nombre del documento",
                        minlength: "El nombre es muy corto, minímo 5 caracteres",
                        maxlength: "El nombre es muy largo, máximo 70 caracteres",
                    },
                    document: {
                        required: "Seleccione un archivo pdf",
                        extension: 'Por favor seleccione un archivo PDF válido',
                    }
                },
                submitHandler: function (form) {
                    form.submit();
                },
                errorClass: 'error-validacion', // Clase para las alertas de validación
                errorElement: 'p', // Elemento "html" para mostrar el error
            });
        }

        if ($('#documentsmodal').length > 0) {
            let validator = $("#documentsmodal .documentsmodal__form").validate({
                // Specify validation rules
                rules: {
                    name: {
                        required: true,
                        minlength: 5,
                        maxlength: 70,
                        notonlynumbers: true
                    },
                    stage_document: {
                        required: true,
                    },
                    documents: {
                        required: true,
                        extension: 'pdf',
                        filesize: 5 // 5MB in bytes
                    },
                },
                // Specify validation error messages
                messages: {
                    name: {
                        required: "Ingrese el nombre del documento",
                        minlength: "El nombre es muy corto, minímo 5 caracteres",
                        maxlength: "El nombre es muy largo, máximo 70 caracteres",
                    },
                    stage_document: {
                        required: "Seleccione una opción",
                    },
                    documents: {
                        required: "Seleccione un archivo pdf",
                        extension: 'Por favor seleccione un archivo PDF válido',
                    }
                },
                submitHandler: function (form) {
                    form.submit();
                },
                errorClass: 'error-validacion', // Clase para las alertas de validación
                errorElement: 'p', // Elemento "html" para mostrar el error
            });
        }
    }
}

function searchForSelectsDemandDocuments(){
    // Array con todos los ids de selects a convertir en crear solicitud
    let selectsDemandDocuments = [
        '#id_assigned_to',
        '#id_copy_to'
    ];

    let $modalDocuments = $('#id_assigned_to').parents('.documentsmodal');

    // Añade buscador a los selects normales y múltiples
    selectsDemandDocuments.forEach(function(selectSelector){
        $(selectSelector).select2({
            language: 'es',
            placeholder: 'Buscar y seleccionar',
            width: '100%',
            dropdownParent: $modalDocuments //para solucionar error dentro de modal
        });
    });
}

/*====================  SHOW MODAL FOR DELETE FILE IN MP ====================*/
function showDeleteFileModal() {
    if ($('.form-stpes .list-of-documents .list-of-documents-item').length > 0) {
        $('body').on('click', '.list-of-documents .list-of-documents-item .list-of-documents-item-delete a', function (e) {
            e.preventDefault();

            let itemFile = $(this).closest('.list-of-documents-item');
            let nameFile = itemFile.find('.list-of-documents-item-content-namedocument').text().trim();
            let urlFile = itemFile.find('.list-of-documents-item-delete a').attr('href');
            let modalDeleteFile = $('#deleteDocumentMP');
            let modalDeleteFileLoad = new bootstrap.Modal(document.querySelector('#deleteDocumentMP'));

            modalDeleteFile.find('.modal-body .description span').text(nameFile);
            modalDeleteFileLoad.show();

            modalDeleteFile.find('.container-button .btn-acept-modal').on('click', function () {
                window.location.href = `${window.location.origin}${urlFile}`;
            });



        })
    }
}


/*====================  ADD VALIDATE FOR NOTELIST ====================*/
function validateIfExistFormForComment() {
    if ($(".detail-list-notes .block-notes .block-form-notes form").length) {
        let formNoteList = $(".detail-list-notes .block-notes .block-form-notes form");

        validateNoteList(formNoteList);

    }

    if ($('.comments-update .create-comment').length) {
        let formCommentary = $(".create-comment form");

        validateNoteList(formCommentary);
    }
}

function validateNoteList(formForValidate) {
    $.extend($.validator.messages, {
        required: "Este campo es obligatorio.",
    });

    formForValidate.validate({
        submitHandler: function (form) {
            formForValidate.find('input[type="submit"]').val('Enviando...').attr('disabled', true);
            form.submit();
        }
    })
}

function validateMiniumYearAndMaxYear() {
    $("#id_created_date__gt").on('change', function (e) {
        let dateMin = +$(this).val();
        $("#id_created_date__lt").val(dateMin + 1);
        $("#id_created_date__lt").attr("min", dateMin + 1);
    });
}

/*====================  INTERVALO OF TIME FOR MP RELATIONS ====================*/
function intervalTimeForMP() {
    if($('.demand-relation__process #formStep5').length) {
        let formStepFive = $('#formStep5'),
            timeInterval;
        
        function updateDateFormat() {
            let deadLine = dayjs(formStepFive.find('#date_agreed').val());
            let dateNewInterval = deadLine.add(timeInterval, 'day');
            let dateNewIntervalFormat = dateNewInterval.format('YYYY-MM-DD');

            formStepFive.find('#date_agreement').val(dateNewIntervalFormat).attr('min', dateNewIntervalFormat);
            formStepFive.find('#date_agreement').trigger('change');
        }

        $('#formStep5 #time').on('change', function(e) {
            e.preventDefault();
            let time = $(this).val()
            if(time <= 0) {
                $(this).val(1);
            }

            timeInterval = formStepFive.find('#time').val();
            timeInterval = String(parseInt(timeInterval) + 1);
            
            updateDateFormat();
        });

        $('#formStep5 #date_agreed').on('change', function(e) {
            e.preventDefault();
            timeInterval = formStepFive.find('#time').val();
            timeInterval = String(parseInt(timeInterval) + 1);
            
            updateDateFormat();
        });

    }
}

/*====================  VALIDATE DATE OF ACCESS Y LIMIT FOR CREATE ACCESS ====================*/
function validateDateAccess() {
    if($('.create-user .create-user__form').length) {
        $('.create-user__form #id_date_access').on('change', function(e) {
            e.preventDefault();

            let deadLine = dayjs($(this).val());
            let dateNewInterval = deadLine.add(1, 'day');
            let dateNewIntervalFormat = dateNewInterval.format('YYYY-MM-DD');

            $('.create-user__form #id_date_limit').val(dateNewIntervalFormat).attr('min', dateNewIntervalFormat);
        });

        $('.create-user__form').validate({
            errorClass: 'error-validacion', // Clase para las alertas de validación
            errorElement: 'p', // Elemento "html" para mostrar el error
        });
    }
}

/*==================== ADD SEARCH TO SELECTS ====================*/
function addSearchForSelects(selectsSelectorsArray){
    // Añade buscador a los selects normales y múltiples
    // Recibe un array con el(los) selector(es) de el(los) select(s).
    selectsSelectorsArray.forEach(function(selectSelector){
        $(selectSelector).select2({
            language: 'es',
            placeholder: 'Buscar y seleccionar',
            width: '100%'
        });
    });
}

/*==================== PROVIDER DETAIL DOCUMENTS ====================*/
function loadFilterProvDetail(){
    // Obtenemos los parametros de la URL
    let params = new URLSearchParams(document.location.search);

    // Iteramos entre cada searchparam
    for(const [key, value] of params){
        // Si el valor es diferente a nada 
        if( value !== ''){ 
            // obtenemos el campo del form
            let $fieldElement = $(`.provider-detail .filterModal__form [name=${key}]`);
            // verificamos que el campo del form exista
            if($fieldElement.length > 0){
                // Si es select
                if( $fieldElement.is('select') ){
                    // Asignamos "value" al select
                    $fieldElement.val(value).prop('selected', true);
                    // Se selecciona la "option"
                    $fieldElement.find('option[value=' + value + ']').attr('selected', true);
                }else{
                    // es input
                    $fieldElement.val(value);
                }
            }
        }
    }
}

function allFilterProvDetailFunctions(){
    if( $('.provider-detail .filterModal__form').length > 0 ){
        loadFilterProvDetail();
    }
}

/*==================== DOCUMENT READY ====================*/
document.addEventListener('DOMContentLoaded', function () {
    allPageSliders();
    allPageVideoModals();
    eventsDropdownSearchMenu();
    windowEvents();
    eventButtonSliderActivity();
    eventInputRangePorcentege();
    eventInputRangePorcentegeAll('input-range-secondary');
    eventClickMenuHeadUnit('ready');
    identifySteps();
    // animateOnScroll();
    // initTransitions();
    activeUserRol();
    validateRecoveryPass();
    formFiltrosProviders();
    validateLoginForm();
    eventClickButtonFilter();
    showTagFilterResult();
    removeTagFilterResult();
    clearInputFilter();
    setActiveTab();
    showModalFilterMobile();
    copyEmailParticipante();
    createMultiList();
    boxResultAccordion();
    sendFilterOrderBy();
    allReceptionFunctions();
    allNegotiationFunctions();
    allTransferFunctions();
    allCreateRRAAfunctions();
    createMultiSelectCheck();
    validateCreateUser();
    progressbarScroll();
    smoothScroll();
    changeFooterCopy();
    addLinkPoliticaNewsletter();
    changeProjectsDescription();
    providerCreateMultistepForm();
    deleteProjectListProject();
    customUploadFile();
    takePhotoCamera();
    validateCreateProject();
    allCreateDemandFunctions();
    validateCreateNewDocument();
    moveActivitiesManagment();
    addAttributeTargetBlankFooter();
    showPreviewFileDetailsInventory();
    megaSearchMenu();
    deleteAccessRraa();
    addPlaceHolderCreateComments();
    followDemandInventory();
    eventClickAccordionBlockActivityManagement();
    contactProvider();
    allPreparationFunctions();
    validateFilterTypeNumber();
    modalRegisterReloadPages();
    eventClickBtnLoginMyBoard();
    notificationConfirmationModal();
    noteConfirmationModal();
    // deleteDemandMPLocalStorage();
    allEvaluationFunctions();
    intervalTimeForMP();
    validateDateAccess();
    searchForSelectsDemandDocuments();
    allFilterProvDetailFunctions();

});

/*==================== DOCUMENT ONLOAD PAGES ====================*/
jQuery(window).on("load", function () {
    orderComments();
    loadModalRequestComment();
    eventClickMenuHeadUnit('load');
    toggleShowHideFilterTags()
    changeSrcImagesBoxesActivity();
    changeTextSelect();
    providerQualityTest();  
    registerQuality();
    addOwnComment();
    validateLoadFileDocumentBoxResult();
    showDeleteFileModal();
    validateIfExistFormForComment();
    validateMiniumYearAndMaxYear();
    addStyleScrollFormDatalist();
});
