from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from .models import User


@csrf_exempt
def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        error = None
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            error = "Username or password not correct"
            return render(request, "login.html", {"error": error})
    return render(request, "login.html")


@csrf_exempt
def logout_user(request):
    logout(request)
    return redirect("login")


def register(request):
    error = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password == confirm_password:
            user = User.objects.filter(username=username)
            if len(user)>0:
                error = "User already existed"
                return render(request, "register.html", {"error": error})
            user = User(
                username=username,
                password=make_password(password),
            )
            user.save()
            return redirect("login")

        error = "Password and confirm password are different"
        return render(request, "register.html", {"error": error})

    return render(request, "register.html")

# Create your views here.
