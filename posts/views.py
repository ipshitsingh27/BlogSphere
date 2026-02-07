from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Category
from interactions.models import Comment, Rating
from django.db.models import Avg


def post_detail(request, id):
    post = get_object_or_404(Post, id=id, is_published=True)

    comments = Comment.objects.filter(post=post).order_by("-created_at")
    ratings = Rating.objects.filter(post=post)

    avg_rating = None
    if ratings.exists():
        avg_rating = round(sum(r.stars for r in ratings) / ratings.count(), 1)

    # ✅ Comment submit
    if request.method == "POST" and "comment_submit" in request.POST:
        if request.user.is_authenticated:
            name = request.user.username
            user = request.user
        else:
            name = request.POST.get("name")
            user = None

        text = request.POST.get("text")

        if name and text:
            Comment.objects.create(post=post, user=user, name=name, text=text)

        return redirect(request.path)

    # ✅ Rating submit (update if same name already rated)
    if request.method == "POST" and "rating_submit" in request.POST:
        if request.user.is_authenticated:
            name = request.user.username
            user = request.user
        else:
            name = request.POST.get("name")
            user = None

        stars = request.POST.get("stars")

        if name and stars:
            Rating.objects.update_or_create(
                post=post,
                name=name,
                defaults={"stars": int(stars), "user": user},
            )

        return redirect(request.path)

    context = {
        "post": post,
        "comments": comments,
        "avg_rating": avg_rating,
    }
    return render(request, "posts/detail.html", context)


@login_required
def create_post(request):
    categories = Category.objects.all()

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        category_id = request.POST.get("category")

        if title and content and category_id:
            category = Category.objects.get(id=category_id)

            Post.objects.create(
                title=title,
                content=content,
                author=request.user,
                category=category,
                is_published=True,
            )
            return redirect("/")

        return render(
            request,
            "posts/create_post.html",
            {"categories": categories, "error": "Please fill all fields."},
        )

    return render(request, "posts/create_post.html", {"categories": categories})


@login_required
def edit_post(request, id):
    post = get_object_or_404(Post, id=id)

    # ✅ only owner can edit
    if post.author != request.user:
        return redirect("/")

    categories = Category.objects.all()

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        category_id = request.POST.get("category")

        if title and content and category_id:
            post.title = title
            post.content = content
            post.category_id = category_id
            post.save()
            return redirect(f"/posts/{post.id}/")

        return render(
            request,
            "posts/edit_post.html",
            {"post": post, "categories": categories, "error": "Please fill all fields."},
        )

    return render(request, "posts/edit_post.html", {"post": post, "categories": categories})


@login_required
def my_posts(request):
    posts = Post.objects.filter(author=request.user).order_by("-id")
    return render(request, "posts/my_posts.html", {"posts": posts})


@login_required
def delete_post(request, id):
    post = get_object_or_404(Post, id=id)

    if post.author != request.user:
        return redirect("/")

    if request.method == "POST":
        post.delete()
        return redirect("/posts/my-posts/")

    return render(request, "posts/confirm_delete.html", {"post": post})


@login_required
def delete_comment(request, id):
    comment = get_object_or_404(Comment, id=id)

    if comment.user == request.user or comment.name == request.user.username:
        post_id = comment.post.id
        if request.method == "POST":
            comment.delete()
        return redirect(f"/posts/{post_id}/")

    return redirect(f"/posts/{comment.post.id}/")
