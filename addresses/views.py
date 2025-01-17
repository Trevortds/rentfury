from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
# Create your views here.
from addresses.forms import AddressForm
from billing.models import BillingProfile
from .models import Address


def checkout_address_create_view(request):
    form = AddressForm(request.POST or None)
    context = {
        "form": form
    }
    next_ = request.GET.get("next")
    next_post = request.POST.get("next")
    redirect_path = next_ or next_post or None
    if form.is_valid():
        print(request.POST)
        instance = form.save(commit=False)
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if billing_profile is not None:
            address_type = request.POST.get("address_type", 'shipping')
            instance.billing_profile = billing_profile
            instance.address_type = request.POST.get('address_type', 'shipping')
            instance.save()

            request.session[address_type + "_address_id"] = instance.id
            print(request.session[address_type + "_address_id"])
        else:
            # TODO put a real error here that the address didn't save
            print("Error trying to save address")
            return redirect("cart:checkout")

        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect("cart:checkout")
    return redirect("cart:checkout")

def checkout_address_reuse_view(request):
    if request.user.is_authenticated:
        context= {}
        next_ = request.GET.get("next")
        next_post = request.POST.get("next")
        redirect_path = next_ or next_post or None
        if request.method == "POST":
            print(request.POST)
            address_type = request.POST.get("address_type", 'shipping')
            reused_address_id = request.POST.get("reused_address", None)
            billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
            if reused_address_id:
                qs =  Address.objects.filter(billing_profile=billing_profile, id=reused_address_id)
                if qs.exists():
                    request.session[address_type + "_address_id"] = reused_address_id
                print(request.session[address_type + "_address_id"])
                if is_safe_url(redirect_path, request.get_host()):
                    return redirect(redirect_path)
    return redirect("cart:checkout")
