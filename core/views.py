from django.shortcuts import render
from posts.models import Post

# Handle Category model name in your project (sometimes it's Categorys)
try:
    from posts.models import Category
except ImportError:
    from posts.models import Categorys as Category


def home(request):
    categories = Category.objects.all().order_by("name")

    # filter by category from URL like: /?cat=1
    cat_id = request.GET.get("cat")

    posts = Post.objects.all().order_by("-id")
    selected_category = None

    if cat_id:
        try:
            selected_category = Category.objects.get(id=cat_id)
            # IMPORTANT: assumes Post has field named "category"
            posts = posts.filter(category_id=cat_id).order_by("-id")
        except Category.DoesNotExist:
            selected_category = None

    return render(request, "core/home.html", {
        "categories": categories,
        "posts": posts,
        "selected_category": selected_category,
    })
