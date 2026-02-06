from django.shortcuts import render
from posts.models import Post
from django.db.models import Q


def home(request):
    query = request.GET.get("q")

    posts = Post.objects.filter(is_published=True)

    # If user searched something
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )

    posts = posts.order_by("-created_at")

    return render(request, "core/home.html", {
        "posts": posts,
        "query": query
    })
