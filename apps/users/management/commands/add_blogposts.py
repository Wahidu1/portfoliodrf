from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.users.models import BlogPost

class Command(BaseCommand):
    help = "Add default blog posts"

    def handle(self, *args, **kwargs):
        blogposts_data = [
            {
                "title": "Getting Started with Django",
                "excerpt": "A beginner's guide to Django web framework.",
                "content": "Django is a powerful Python web framework...",
                "status": BlogPost.Status.PUBLISHED,
            },
            {
                "title": "Django REST Framework Tips",
                "excerpt": "Improve your APIs with these DRF tips.",
                "content": "DRF makes it easy to build REST APIs in Django...",
                "status": BlogPost.Status.PUBLISHED,
            },
            {
                "title": "Understanding Django Models",
                "excerpt": "Deep dive into Django ORM and models.",
                "content": "Models are the heart of Django's ORM...",
                "status": BlogPost.Status.DRAFT,
            },
        ]

        for post in blogposts_data:
            obj, created = BlogPost.objects.update_or_create(
                title=post["title"],
                defaults={
                    "excerpt": post["excerpt"],
                    "content": post["content"],
                    "status": post["status"],
                    "published_at": timezone.now() if post["status"] == BlogPost.Status.PUBLISHED else None
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added blog post: {obj.title}"))
            else:
                self.stdout.write(self.style.WARNING(f"Updated blog post: {obj.title}"))
