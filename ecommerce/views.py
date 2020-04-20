from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, get_user_model, logout
from .forms import ContactForm, LoginForm, RegisterForm




def home_page(request):
    context = {
        "title": "Hello, Trevor!",
        "content": "welcome to the homepage!",
    }
    if request.user.is_authenticated:
        context["premium_content"] = "Fuck Yeah!"
    return render(request, "index.html", context)


def about_page(request):
    context = {
        "title": "About Page!",
        "content": "this is an about page"
    }
    return render(request, "index.html", context)

def logout_page(request):
    logout(request)
    return redirect("/")


def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        "title": "Contact Page!",
        "content": "this certainly is a contact page!",
        "form": contact_form
    }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
    if request.method == "POST":
        print("its a post!")
        print(request.POST)
        print("name is {}".format(request.POST["fullname"]))
    return render(request, "contact/view.html", context)


def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }
    print("user logged in?")
    print(request.user.is_authenticated)
    if form.is_valid():
        print(form.cleaned_data)
        user = authenticate(request, username=form.cleaned_data["username"], password=form.cleaned_data["password"])
        print(request.user.is_authenticated)
        print(user)
        if user is not None:
            login(request, user)
            # context["form"] = LoginForm()
            # redirect to a success page
            return redirect("/")
        else:
            # invalid login error message
            print("Failed login")

    return render(request, "auth/login.html", context)


User = get_user_model()


def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form": form,
    }
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        new_user = User.objects.create_user(username, email, password)
        print(new_user)
        login(request, new_user)
        return redirect("/")
    return render(request, "auth/register.html", context)

