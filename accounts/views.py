from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import UserCreationForm


# Signup view
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
    else:
        form = UserCreationForm()

    return render(request, "accounts/signup.html", {"form": form})


# Custom Logout view (FIXES WHITE SCREEN)
@require_POST
def logout_user(request):
    logout(request)
    return redirect("/")
