from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse, Http404, HttpResponse

# Create your views here.
import stripe
from django.utils.http import is_safe_url
from django.views.decorators.csrf import ensure_csrf_cookie

# TODO put these in environment
from billing.models import BillingProfile, Card


STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", "sk_test_qv0vYPHZYXdty8jw31ELn9oS00C76oYLNj")
STRIPE_PUB_KEY = getattr(settings, "STRIPE_PUB_KEY", 'pk_test_D5cmBFDplcJVrEG6HOsknjQj00e3oKBgrt')
stripe.api_key = STRIPE_SECRET_KEY

# TODO use https://django-background-tasks.readthedocs.io/en/latest/ to enable recurring payments, possibly new module?
# more info on making payments here: https://stripe.com/docs/payments/save-and-reuse


@ensure_csrf_cookie
def payment_method_view(request):

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if not billing_profile:
        # TODO put a real error here that the billingprofile didn't load, or else make a new one
        print("Error trying to save address")
        return redirect("cart")

    print(stripe.PaymentMethod.list(
        customer=billing_profile.customer_id,
        type="card",
    ))

    intent = stripe.SetupIntent.create(
        customer=billing_profile.customer_id,
        usage='off_session',
    )

    next_url = None
    next_ = request.GET.get("next")
    if is_safe_url(next_, request.get_host()):
        next_url = next_

    context = {
        "publish_key": STRIPE_PUB_KEY,
        "client_secret": intent.client_secret,
        "next_url": next_url,
    }
    return render(request, "billing/payment-method.html", context=context)

@ensure_csrf_cookie
def payment_view(request):
    intent = stripe.PaymentIntent.create(
        amount=1099,
        currency='usd',
        # Verify your integration in this guide by including this parameter
        metadata={'integration_check': 'accept_a_payment',
                  # "order_id": "order_id_goes_here",
                  },
        setup_future_usage='off_session',
        # statement_descriptor="22 character Description to appear on cc statement goes here",
    )
    next_url = None
    next_ = request.GET.get("next")
    if is_safe_url(next_, request.get_host()):
        next_url = next_

    context = {
        "publish_key": STRIPE_PUB_KEY,
        "client_secret": intent.client_secret,
        "next_url": next_url,
    }
    return render(request, "billing/payment.html", context=context)


def payment_method_createview(request):
    if request.method == "POST" and request.is_ajax():
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if not billing_profile:
            return HttpResponse({"message": "cannot find this user"}, 401)

        customer = stripe.Customer.retrieve(billing_profile.customer_id)
        print(request.POST)
        card_response = stripe.PaymentMethod.retrieve(request.POST.get("setupIntent[payment_method]"))
        print("card response")
        print(card_response)
        new_card = Card.objects.add_new(billing_profile=billing_profile, stripe_card_response=card_response)
        print("new card")
        print(new_card)
        return JsonResponse({"message": "Card successfully added!"})
    return HttpResponse("error", status_code=401)


