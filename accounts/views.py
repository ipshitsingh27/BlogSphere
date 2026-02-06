from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomSignupForm


def signup(request):
    # ✅ If user is already logged in, don't show signup page
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # ✅ auto login after signup
            return redirect("/")  # ✅ go home after signup
    else:
        form = CustomSignupForm()

    return render(request, "accounts/signup.html", {"form": form})
