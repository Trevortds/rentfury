from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, get_user_model, logout
from .forms import ContactForm



def home_page(request):
    context = {
        "title": "Our Equipment Rental Website!",
        "content": "welcome to the homepage!",
    }
    if request.user.is_authenticated:
        context["premium_content"] = "Woohoo, you're a very special user!"
    return render(request, "index.html", context)


def about_page(request):
    context = {
        "title": "About Page!",
        "content": "this is an about page"
    }
    return render(request, "index.html", context)



def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        "title": "Contact Us",
        "content": """
        This is our contact page, please fill out the form below to email us about any issues you have.
         We will respond by email shortly
         """,
        "form": contact_form
    }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
    if request.method == "POST":
        print("its a post!")
        print(request.POST)
        print("name is {}".format(request.POST["fullname"]))
    return render(request, "contact/view.html", context)


