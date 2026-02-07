from django.urls import path
from . import views

urlpatterns = [
    path("write/", views.create_post, name="create_post"),
    path("my-posts/", views.my_posts, name="my_posts"),

    # ✅ Edit post (fixes /posts/edit/<id>/ 404)
    path("edit/<int:id>/", views.edit_post, name="edit_post"),

    # Post detail
    path("<int:id>/", views.post_detail, name="post_detail"),

    # Delete post
    path("delete/<int:id>/", views.delete_post, name="delete_post"),
]
