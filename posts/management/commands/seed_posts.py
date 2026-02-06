from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from posts.models import Post, Category


class Command(BaseCommand):
    help = "Create sample categories and posts for testing"

    def handle(self, *args, **options):
        User = get_user_model()

        # 1) Ensure a user exists (we'll use admin/superuser if present)
        user = User.objects.filter(is_superuser=True).first()
        if not user:
            user = User.objects.first()

        if not user:
            self.stdout.write(self.style.ERROR("No users found. Create a superuser first."))
            return

        # 2) Create categories (if not already)
        category_names = ["Tech", "Health", "Travel", "Finance", "College Life"]
        categories = []
        for name in category_names:
            cat, _ = Category.objects.get_or_create(name=name)
            categories.append(cat)

        # 3) Create posts
        sample_posts = [
            ("How I stay productive in college", "Simple habits that helped me study better and feel less stressed."),
            ("Beginner guide to Django", "Django is a Python framework that helps you build websites faster."),
            ("My favorite night drive playlist", "A mix of calm + boost songs that feel perfect on the highway."),
            ("Budgeting for students", "Track your money weekly and avoid small expenses that add up."),
            ("Travel tips for first trip", "Carry light, plan your route, and keep copies of important documents."),
        ]

        created = 0
        for i in range(1, 16):  # 15 posts
            title, content = sample_posts[(i - 1) % len(sample_posts)]
            post_title = f"{title} #{i}"

            obj, was_created = Post.objects.get_or_create(
                title=post_title,
                defaults={
                    "content": content,
                    "author": user,
                    "category": categories[(i - 1) % len(categories)],
                    "is_published": True,
                },
            )
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(f"Done! Created {created} new posts."))
