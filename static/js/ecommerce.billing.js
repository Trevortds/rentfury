$(document).ready(function () {


var stripeFormModule = $(".stripe-payment-form")
var stripeModuleToken = stripeFormModule.attr("data-token")
var stripeModuleNextUrl = stripeFormModule.attr("data-next-url")
var stripeModuleSecret = stripeFormModule.attr("data-secret")
var stripeModuleEndpoint = stripeFormModule.attr("data-endpoint")
var stripeModuleBtnTitle = stripeFormModule.attr("data-btn-title") || "Submit"
var stripeTemplate = $.templates("#stripeTemplate")
var stripeTemplateDataContext = {
    publishKey: stripeModuleToken,
    nextUrl: stripeModuleNextUrl,
    clientSecret: stripeModuleSecret,
    billingPaymentMethodEndpoint: stripeModuleEndpoint,
    btnTitle: stripeModuleBtnTitle
}
var stripeTemplateHtml = stripeTemplate.render(stripeTemplateDataContext)
stripeFormModule.html(stripeTemplateHtml)

// Set your publishable key: remember to change this to your live publishable key in production
// See your keys here: https://dashboard.stripe.com/account/apikeys
var setupForm = $(".setup-form");
if (setupForm.length > 1) {
    alert("only one setup form per page");
    setupForm.css("display", 'none');
}
else if (setupForm.length === 1) {
    var pubKey = setupForm.attr('data-token');
    var clientSecret = setupForm.attr('data-secret');
    var nextUrl = setupForm.attr('data-next-url')
    console.log(pubKey)


    var stripe = Stripe(pubKey);
    var elements = stripe.elements();


    // Set up Stripe.js and Elements to use in checkout form
    var style = {
        base: {
            color: "#32325d",
        }
    };

    var cardElement = elements.create("card");
    cardElement.mount("#card-element");

    cardElement.addEventListener('change', ({error}) => {
        const displayError = document.getElementById('card-errors');
        if (error) {
            displayError.textContent = error.message;
        } else {
            displayError.textContent = '';
        }
    });


    var cardholderName = document.getElementById('cardholder-name');
    var cardButton = document.getElementById('card-button');
    var cardElementDocument = document.getElementById('card-element')
    var form = document.getElementById('setup-form');
    //{#var clientSecret = cardButton.dataset.secret;#}


    form.addEventListener('submit', function (ev) {
        ev.preventDefault();
        console.log(clientSecret);
        console.log(cardElement);
        stripe.confirmCardSetup(
            clientSecret,
            {
                payment_method: {
                    card: cardElement,
                    billing_details: {
                        name: "Empty Name",
                    },
                },
            }
        ).then(function (result) {
            console.log(result)
            if (result.error) {
                console.log(result.error);
                console.log(result.error.message)
                // Display error.message in your UI.
            } else {
                console.log(result);
                console.log(result.setupIntent);
                // The setup has succeeded. Display a success message.
                stripeCardAddSuccessHandler(result, nextUrl)
            }
        });
    });

    function redirectToNext(nextUrl, timeOffset) {
        if (nextUrl) {
            setTimeout(function () {
                console.log(nextUrl)
                window.location.href = nextUrl
            }, timeOffset);
        }
    }

    function stripeCardAddSuccessHandler(result, nextUrl) {
        // The payment has been processed!
        if (result.setupIntent.status === 'succeeded') {
            console.log(result);
            console.log(result.setupIntent);
            console.log(result.setupIntent.status);
            var paymentMethodEndpoint = document.getElementById('billing_payment_endpoint').value
            var data = {
                'setupIntent': result.setupIntent
            }
            $.ajax({
                data: data,
                url: paymentMethodEndpoint,
                method: "POST",
                success: function (data) {
                    console.log(data);
                    cardElement.clear();
                    var successMsg = data.message || "Success! card added";
                    if (nextUrl) {
                        successMsg = successMsg + "<br/><i class='fa fa-spin fa-spinner'></i> Redirecting..."
                    }
                    if ($.alert) {
                        $.alert(successMsg);
                    } else {
                        alert(successMsg);
                    }
                    redirectToNext(nextUrl, 1500);
                },
                error: function (error) {
                    console.log(error);
                }
            });
        }
    }
}
})