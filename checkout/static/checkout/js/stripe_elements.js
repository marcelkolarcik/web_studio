/*script to handle checkout process*/

var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();
var style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};

var card = elements.create('card', {style: style, hidePostalCode: true});
card.mount('#card-element');

// Handle realtime validation errors on the card element
card.addEventListener('change', function (event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});

/*checking project ID validity
*
* if it already used, we disable purchase button
*
* if it's not existent we disable purchase button
*
* if it exists and appointment didn't take place
* for testing purposes we will display success
* message and allow purchase
*
* but in production, consultation would have to
* take place, to ensure, that we know what the project
* is and whether we will do it */

$('#project_number').on('input', function () {
    console.log($(this).val())
    var project_number = $(this).val();

    $.ajax({
        url: '/validate_project_number/',
        data: {
            'project_number': project_number,
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
        },
        dataType: 'json',
        success: function (data) {
            if (data.is_taken) {

                $('#submit-button').attr('disabled', true);
                $('#project_number_error').text(data.msg)
                $('#consultation').removeClass('d-none')
                $('#project_no_consultation_error').text('')
            } else if (data.no_consultation) {
                $('#submit-button').attr('disabled', false);
                $('#project_number_error').text('')
                $('#project_no_consultation_error').text(data.msg)
                $('#consultation').addClass('d-none')
            } else {
                $('#submit-button').attr('disabled', false);
                $('#project_number_error').text('')
                $('#consultation').addClass('d-none')
            }

        }
    });
})

// Handle form submit
var form = document.getElementById('payment-form');

form.addEventListener('submit', function (ev) {
    ev.preventDefault();


    card.update({'disabled': true});
    $('#submit-button').attr('disabled', true);
    $('#payment-form').fadeToggle(100);
    $('#loading-overlay').fadeToggle(100);


    // From using {% csrf_token %} in the form
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var postData = {
        'csrfmiddlewaretoken': csrfToken,
        'client_secret': clientSecret,
        'project_number': $.trim(form.project_number.value),


    };
    var url = '/checkout/cache_checkout_data/';
    $.post(url, postData).done(function () {


        stripe.confirmCardPayment(clientSecret, {
            payment_method: {

                card: card,
                billing_details: {
                    name: $.trim(form.name.value),
                    email: $.trim(form.email.value),
                    address: {
                        line1: $.trim(form.street1.value),
                        line2: $.trim(form.post_code.value),
                        city: $.trim(form.city.value),
                        country: $.trim(form.country.value),


                    },


                },

            }


        }).then(function (result) {
            if (result.error) {
                var errorDiv = document.getElementById('card-errors');
                var html = `
                    <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                    </span>
                    <span>${result.error.message}</span>`;
                $(errorDiv).html(html);
                $('#payment-form').fadeToggle(100);
                $('#loading-overlay').fadeToggle(100);
                card.update({'disabled': false});
                $('#submit-button').attr('disabled', false);
            } else {
                if (result.paymentIntent.status === 'succeeded') {

                    //console.log(form)
                    form.submit();
                }
            }
        });

    });
});