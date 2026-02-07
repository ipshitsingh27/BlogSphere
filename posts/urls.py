from django.urls import path
from . import views

urlpatterns = [
    path("write/", views.create_post, name="create_post"),
    path("my-posts/", views.my_posts, name="my_posts"),
    path("delete/<int:id>/", views.delete_post, name="delete_post"),

    # post detail
    path("<int:id>/", views.post_detail, name="post_detail"),

    # comment delete
    path("comment/delete/<int:id>/", views.delete_comment, name="delete_comment"),
]
