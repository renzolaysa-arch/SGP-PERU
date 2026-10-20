// import '../../node_modules/jquery-validation/dist/jquery.validate.js';
// const jqueryValidator = require('jquery-validation');


function toogleDataSeries(e) {
    if (typeof (e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
        e.dataSeries.visible = false;
    } else {
        e.dataSeries.visible = true;
    }
    e.chart.render();
}

$(document).ready(function () {

    validateRegisterForm();
    validateRecoveryForm();

    if (sessionStorage.getItem('modal') !== null) {
        if ($('#reset-password').length > 0) {

            openSuccesModal()
        }
    }

    $(".modal.success__register .modal-content .modal-body .container-button a").on('click', function (e) {
        $('#create-new-provider').removeClass("success__register");
        sessionStorage.removeItem('modalRegister');
    })

});
function makesvg(percentage, inner_text = "") {
    let abs_percentage = percentage.toString();
    let percentage_str = percentage.toString();
    let classes = "";
    if (percentage < 0) {
        classes = "danger-stroke circle-chart__circle--negative";
    }
    else if (percentage > 0 && percentage <= 70) {
        classes = "warning-stroke";
    } else {
        classes = "success-stroke";
    }
    let svg = '<svg class="circle-chart" viewbox="0 0 33.83098862 33.83098862" xmlns="http://www.w3.org/2000/svg">' +
        '<circle class="circle-chart__background" cx="16.9" cy="16.9" r="15.9" />' + '<circle class="circle-chart__circle ' + classes + '"'
        + 'stroke-dasharray="' + abs_percentage + ',100"  cx="16.9" cy="16.9" r="15.9" />' + '<g class="circle-chart__info">' +
        '<text class="circle-chart__percent" x="16.5" y="15.5">' + percentage_str + '</text>';
        // '<text class="circle-chart__percent" x="17.9" y="15.5">' + percentage_str + '%</text>';
    if (inner_text) {
        svg += '<text class="circle-chart__subline" x="16.91549431" y="22">' + inner_text + '</text>'
    }
    svg += ' </g></svg>';
    return svg
}



const circlechart = (elems) => {
    elems.each(function (index, elem) {
        console.log($(elem));
        let percentage = $(elem).data("percentage");
        let inner_text = $(elem).text();
        $(elem).html(makesvg(percentage, inner_text));
    });
    return elems;
};



jQuery(window).on("load", function (e) {



    let url = window.location.href;
    if (url.includes("unit=")) {
        $('#create-new-provider').addClass('unit-central');
    } else {
        $('#create-new-provider').addClass('not-aproved');
    }

    let circles = jQuery(".circlechart");
    circlechart(circles)

    let $circlechartCol = jQuery(".circle-withoutPercentage");

    $circlechartCol.each(function(){
        let circleChartText = jQuery(this).find('.circle-chart g text').text().replace(/%/g, "");
        jQuery(this).find('.circle-chart g text').text(circleChartText);
    });


    // jQuery(".circle-withoutPercentage").text();
    // jQuery(".circle-withoutPercentage .circle-chart g text").text(jQuery(".circle-withoutPercentage .circle-chart g text").text().replace(/%/g, ""))

    const dataDay = [];
    const dataQuantity = [];
    const dataChart = jQuery("#dataChart > div").map(function () {
        return jQuery(this).attr("data-day")

    })
    const dataChartQuantity = jQuery("#dataChart > div").map(function () {
        return jQuery(this).attr("data-quantity")
    })
    let i = 0;
    for(i; i< dataChart.length; i++){
        dataDay.push(dataChart[i])   
        dataQuantity.push(dataChartQuantity[i])   
   }
   

    if (jQuery("#grafica").length > 0) {
        new Chartist.Line('#grafica', {
            labels: dataDay,
            series: [
                dataQuantity
            ]
        }, {
            fullWidth: true,
            low: 0,
            showArea: true,
            divisor: 5,
            chartPadding: {
                right: 40
            }
        });
    }


    if (sessionStorage.getItem('modalRegister') !== null) {
        if (!$(".errorlist").length > 0) {
            $('#create-new-provider').addClass('success__register');
            $('#create-new-provider').modal('show');

        } else {
            sessionStorage.removeItem('modalRegister');
        }
    }
    if (sessionStorage.getItem('recorySuccess') !== null) {
        $('#recovery-form').addClass('success__recovery')
        $('#recovery-form').modal('show')
    }

    if ($('.filter-primary-filtermobile').length) {
        $('.btn-filter-mobile').on('click', function (e) {
            e.preventDefault();
            let screenWidth = $(window).width();
            if (screenWidth < 768) {
                $('#modalFilterMobile').modal('show');
            }
        });
    }

    // Load documents for box result
    if ($('#accordionActivityManagement').length) {
        let sizeFile,
            typeFile,
            previewFile,
            reader = new FileReader(),
            counter = 1;

        $('.form-stpes .show-modal-file').on('click', function (e) {
            e.preventDefault();

            let idFormLoadFile = $(this).closest('.form-stpes').attr('id');
            $('#loadDocumentBoxResult #loadFile').attr('data-content-file', idFormLoadFile);

            sizeFile = $('#' + idFormLoadFile + ' .load-files-description-size span').text();
            typeFile = $('#' + idFormLoadFile + ' .load-files-description-type span').text();
        })
    }

});

/*====================  OPEN MODAL FORGOT PASSWORD ====================*/
function openModal(url, url2) {
    sessionStorage.setItem('modal', url2);
    $('#reset-password').load(url, function () {
        $(this).modal('show')

        // Escuchar click boton "Enviar"
        $('body').on('click', '.btn-user-login.btn-reset', function(event){
            // Prevenimos envio formulario normal
            event.preventDefault();
            // Obtenemos form
            const $recoveryPassform = $(this).parents('form');
            // Obtenemos metodo
            const formMethod = $recoveryPassform.attr('method');
            // Obtenemos action
            const formAction = $recoveryPassform.attr('action');
            // Hacemos petición Ajax
            $.ajax({
                method: formMethod,
                url: formAction,
                data: $recoveryPassform.serialize(),
                success: function (res, estado, jqXHR) {
                    // openSuccesModal
                    let url = sessionStorage.getItem('modal');
                    $('#reset-password').addClass("modal__success");
                    $('#reset-password').load(url, function () {
                        $('#reset-password').modal('show');
                    });
                },
                error: function (jqXHR, estado, error) {
                    // console.log("jqXHR: ", jqXHR);
                    // console.log("estado: ", estado);
                    // console.log("error ", error);
                    // Verificamos que sea el error de que no existe el correo
                    if(estado === 'error' && jqXHR.status === 404){
                        // Si no existe mensaje de error
                        if( $('#reset-password form .email-error').length <= 0 ){
                            // Seteamos mensaje en el modal
                            $('#reset-password form .imput-email').after(`<div class="email-error">El correo ingresado no se encuentra registrado. Intente nuevamente.</div>`);
                        }
                    }else if(estado === 'error' && jqXHR.status === 503){
                        // Error servidor
                        // Seteamos mensaje en el modal
                        const plantillaErrorServer = `<div class="modal-dialog modal-md modal-dialog-centered" role="document">
                                <div class="modal-content">
                                    <div class="modal-header">
                                        <h2 class="modal-title">Error del Servidor</h2>
                                        <button id = "password-done" type="button" className="btn btn-close-modal" data-bs-dismiss="modal" aria-label="Close"></button>
                                        <p>Ha ocurrido un error inesperado en el servidor al intentar enviar el correo de recuperación (código de error 503).</p>
                                    </div>
                                </div>
                            </div>`;


                        $('#reset-password').html(plantillaErrorServer);
                    }else{
                        // Otro error del servidor
                        // Seteamos mensaje en el modal
                        const plantillaErrorServer = `<div class="modal-dialog modal-md modal-dialog-centered" role="document">
                                <div class="modal-content">
                                    <div class="modal-header">
                                        <h2 class="modal-title">Error del Servidor</h2>
                                        <button id = "password-done" type="button" className="btn btn-close-modal" data-bs-dismiss="modal" aria-label="Close"></button>
                                        <p>Ha ocurrido un error inesperado en el servidor (código de error 500).</p>
                                    </div>
                                </div>
                            </div>`;


                        $('#reset-password').html(plantillaErrorServer);
                    }

                    
                },
                complete: function (jqXHR, estado) {
                    
                },
            });

        });
    });

}

/*==================== OPEN SUCCES MODAL TO SEND EMAIL ====================*/

function openSuccesModal() {
    let search = '?send=true';
    let parameter = window.location.search;
    if (search === parameter) {
        let url = sessionStorage.getItem('modal');
        $('#reset-password').addClass("modal__success");
        $('#reset-password').load(url, function () {
            $('#reset-password').modal('show')
        });

    }
}



/*==================== CLEAR SESSIONSTORAGE ====================*/
function closeModal(event) {

    sessionStorage.removeItem('modal');
    sessionStorage.removeItem('modalRegister');
    $('#reset-password').removeClass("modal__success");
    $('#create-new-provider').removeClass("success__register");

}



/*====================  VALIDATION FORM REGISTER ====================*/
function validateRegisterForm() {



    if ($("form#register-form").length > 0) {
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

        const capctchaValiation = () => {
            let response = grecaptcha.getResponse();
            if (response.length == 0) {
                // console.log("error")
                $(".register-screen .container-fluid .row .card-container form.register-form .captcha-container #label-captcha").addClass("active");
                return false;
            } else {
                // console.log("success")
                return true;
            }
        }

        $("form#register-form").validate({
            // Specify validation rules
            rules: {
                // The key name on the left side is the name attribute
                // of an input field. Validation rules are defined
                // on the right side
                name: {
                    required: true,
                    letterwithbasicpunc: true,
                    maxlength: 30,
                    // onlyLetters: true
                },
                last_name: {
                    required: true,
                    letterwithbasicpunc: true,
                    maxlength: 30,
                    // onlyLetters: true
                },
                document_type: { valueNotEquals: "default" },
                identification_number: {
                    required: true,
                    alphaNum: true,
                    minlength: 5,
                },
                email: {
                    required: true,
                    emailValidate: true
                },
                password: {
                    required: true,
                    minlength: 8,
                    validate_password: true

                },
                password_confirm: {
                    required: true,
                    minlength: 8,
                    equalTo: "#id_password",
                    validate_password: true

                },
                terms_conditions: "required",

            },
            // Specify validation error messages
            messages: {
                document_type: { valueNotEquals: "seleccione un tipo de identificación" },
                name: {
                    required: "Este campo es requerido",
                    maxlength: "Máximo 30 caracteres",
                },
                last_name: {
                    required: "Este campo es requerido",
                    maxlength: "Máximo 30 caracteres",
                },
                identification_number: {
                    required: "Ingrese su número de identificación",
                    alphaNum: "Ingrese un número de indentifación válido",
                    minlength: "Minímo 5 caracteres",
                },
                password: {
                    required: "Ingrese su contraseña",
                    minlength: "Minímo 8 caracteres",
                },
                email: "Ingrese un correo electrónico válido",
                password_confirm: {
                    required: "Ingrese su contraseña",
                    minlength: "Minímo 8 caracteres",
                    equalTo: "Debe ser la misma contraseña",
                },
                terms_conditions: "Debe aceptar los términos y condiciones",
            },
            errorPlacement: function(error, element) {
                error.insertAfter( element.closest('div.content-field') );
            },
            highlight: function(element, errorClass, validClass) {
                $(element).closest('div.input-container').addClass('errorInput');
                $(element).addClass('error')
            },
            unhighlight: function(element, errorClass, validClass) {
                $(element).closest('div.input-container').removeClass('errorInput');
                $(element).removeClass('error')
            },
            // Make sure the form is submitted to the destination defined
            // in the "action" attribute of the form when valid
            submitHandler: function (form) {
                if (capctchaValiation()) {
                    sessionStorage.removeItem('modalRegister');
                    form.submit();
                }
            }
        });

        // hidden and show password
        $("#register-form .icon-password").on("click", function () {
            let iconEye = $("#register-form .icon-password");

            iconEye.each(function() {
                if ($(this).hasClass("icon-eye-blocked")) {
                    $(this).removeClass("icon-eye-blocked").addClass("icon-eye");
                    $(this).closest('.input-container').find('input').attr("type", "text");
                } else if($(this).hasClass("icon-eye")) {
                    $(this).removeClass("icon-eye").addClass("icon-eye-blocked");
                    $(this).closest('.input-container').find('input').attr("type", "password");
                }
            })
        });
    }
}
/*====================  VALIDATION FORM NEW USER PASSWORD ====================*/
function validateRecoveryForm() {



    if ($("form#recovery-form").length > 0) {
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

        $("form#recovery-form").validate({
            // Specify validation rules
            rules: {

                new_password1: {
                    required: true,
                    minlength: 8,
                    validate_password: true

                },
                new_password2: {
                    required: true,
                    minlength: 8,
                    equalTo: "#id_new_password1",
                    validate_password: true
                },

            },
            // Specify validation error messages
            messages: {
                new_password1: {
                    required: "Ingrese su contraseña",
                    minlength: "Minímo 8 caracteres"
                },
                new_password2: {
                    required: "Ingrese su contraseña",
                    minlength: "Minímo 8 caracteres",
                    equalTo: "Debe ser la misma contraseña"
                }

            },
            // Make sure the form is submitted to the destination defined
            // in the "action" attribute of the form when valid
            submitHandler: function (form) {
                sessionStorage.setItem('modalChangePass', 'recorySuccess');
                form.submit();
            }
        });
    }
}