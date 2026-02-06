from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),

    # Login
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),

    # Logout → redirect to home after logout
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),

    # Apps
    path("", include("core.urls")),
    path("posts/", include("posts.urls")),
    path("accounts/", include("accounts.urls")),
]
