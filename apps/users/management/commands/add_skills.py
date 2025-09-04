from django.core.management.base import BaseCommand
from apps.users.models import MySkill


class Command(BaseCommand):
    help = "Add default skills for a Django & DRF developer"

    def handle(self, *args, **kwargs):
        skills = [
            {"name": "Python", "icon_name": "fa-python", "percentage": 90, "order": 1},
            {"name": "Django", "icon_name": "fa-django", "percentage": 85, "order": 2},
            {"name": "Django REST Framework", "icon_name": "fa-code", "percentage": 80, "order": 3},
            {"name": "PostgreSQL", "icon_name": "fa-database", "percentage": 75, "order": 4},
            {"name": "Git", "icon_name": "fa-git-alt", "percentage": 70, "order": 5},
            {"name": "Docker", "icon_name": "fa-docker", "percentage": 65, "order": 6},
        ]

        for skill in skills:
            obj, created = MySkill.objects.update_or_create(
                name=skill["name"],
                defaults=skill
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added skill: {obj.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Updated skill: {obj.name}"))
