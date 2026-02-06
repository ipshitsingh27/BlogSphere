from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from core.views import home

urlpatterns = [
    path("admin/", admin.site.urls),

    # Home
    path("", home, name="home"),

    # Posts
    path("posts/", include("posts.urls")),

    # ✅ Accounts (main)
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="accounts_login",
    ),
    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(),
        name="accounts_logout",
    ),

    # ✅ Also support old URLs (so navbar /login/ /logout/ buttons won't 404)
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),

    # Signup + custom logout route inside accounts app
    path("accounts/", include("accounts.urls")),
]
