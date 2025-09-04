from django.core.management.base import BaseCommand
from apps.users.models import MyAchievement
from datetime import date

class Command(BaseCommand):
    help = "Add default achievements"

    def handle(self, *args, **kwargs):
        achievements_data = [
            {
                "title": "Certified Django Developer",
                "organization": "Django Software Foundation",
                "date": date(2023, 5, 10),
                "order": 1,
                "image": None,  # Optional: add image path if available
            },
            {
                "title": "REST API Expert",
                "organization": "My Portfolio",
                "date": date(2023, 7, 15),
                "order": 2,
                "image": None,
            },
            {
                "title": "Open Source Contributor",
                "organization": "GitHub",
                "date": date(2023, 8, 20),
                "order": 3,
                "image": None,
            },
        ]

        for achievement in achievements_data:
            obj, created = MyAchievement.objects.update_or_create(
                title=achievement["title"],
                defaults={
                    "organization": achievement["organization"],
                    "date": achievement["date"],
                    "order": achievement["order"],
                    "image": achievement["image"],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added achievement: {obj.title}"))
            else:
                self.stdout.write(self.style.WARNING(f"Updated achievement: {obj.title}"))
