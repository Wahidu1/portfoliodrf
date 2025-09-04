from django.core.management.base import BaseCommand
from apps.users.models import Technology, MyWork

class Command(BaseCommand):
    help = "Add default portfolio works and technologies"

    def handle(self, *args, **kwargs):
        # Define technologies
        tech_data = [
            {"name": "Django", "icon": "fa-django"},
            {"name": "DRF", "icon": "fa-code"},
            {"name": "React", "icon": "fa-react"},
            {"name": "PostgreSQL", "icon": "fa-database"},
        ]

        tech_objects = {}
        for tech in tech_data:
            obj, created = Technology.objects.update_or_create(
                name=tech["name"],
                defaults=tech
            )
            tech_objects[obj.name] = obj
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added technology: {obj.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Updated technology: {obj.name}"))

        # Define works/projects
        works_data = [
            {
                "title": "Portfolio Website",
                "subtext": "Personal portfolio built with Django and React",
                "description": "A website to showcase my projects and skills.",
                "technologies": ["Django", "React"],
                "github_link": "https://github.com/username/portfolio",
                "live_link": "https://portfolio.example.com",
                "order": 1,
            },
            {
                "title": "Task Manager API",
                "subtext": "REST API built with Django REST Framework",
                "description": "An API to manage tasks, users, and projects.",
                "technologies": ["Django", "DRF", "PostgreSQL"],
                "github_link": "https://github.com/username/task-manager",
                "live_link": "",
                "order": 2,
            },
        ]

        for work in works_data:
            obj, created = MyWork.objects.update_or_create(
                title=work["title"],
                defaults={
                    "subtext": work["subtext"],
                    "description": work["description"],
                    "github_link": work["github_link"],
                    "live_link": work["live_link"],
                    "order": work["order"],
                }
            )
            # Set many-to-many technologies
            tech_list = [tech_objects[name] for name in work["technologies"] if name in tech_objects]
            obj.technologies.set(tech_list)
            obj.save()

            if created:
                self.stdout.write(self.style.SUCCESS(f"Added work: {obj.title}"))
            else:
                self.stdout.write(self.style.WARNING(f"Updated work: {obj.title}"))
