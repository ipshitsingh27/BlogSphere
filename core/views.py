from django.shortcuts import render
from django.db.models import Q
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

    # search query from URL like: /?q=django
    query = request.GET.get("q", "").strip()

    posts = Post.objects.all().order_by("-id")
    selected_category = None

    # ✅ Category filter
    if cat_id:
        try:
            selected_category = Category.objects.get(id=cat_id)
            posts = posts.filter(category_id=cat_id).order_by("-id")
        except Category.DoesNotExist:
            selected_category = None

    # ✅ Search filter (works together with category filter)
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        ).order_by("-id")

    return render(request, "core/home.html", {
        "categories": categories,
        "posts": posts,
        "selected_category": selected_category,
        "q": query,
    })
