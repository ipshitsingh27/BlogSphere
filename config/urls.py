from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from accounts.views import signup

urlpatterns = [
    path("admin/", admin.site.urls),

    # ✅ Signup (keep it ABOVE other includes)
    path("signup/", signup, name="signup"),

    # Auth (login/logout)
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    # Apps
    path("", include("core.urls")),
    path("posts/", include("posts.urls")),
]
