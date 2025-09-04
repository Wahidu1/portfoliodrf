from django.core.management.base import BaseCommand
from apps.users.models import MyExperience
from datetime import date

class Command(BaseCommand):
    help = "Add default experiences"

    def handle(self, *args, **kwargs):
        experiences_data = [
            {
                "title": "Backend Developer",
                "company": "Tech Solutions Ltd.",
                "description": "Worked on Django and DRF projects, building REST APIs and backend services.",
                "start_date": date(2022, 1, 15),
                "end_date": date(2023, 6, 30),
                "order": 1,
            },
            {
                "title": "Full Stack Developer Intern",
                "company": "Startup Hub",
                "description": "Developed web applications using Django, React, and PostgreSQL.",
                "start_date": date(2021, 6, 1),
                "end_date": date(2021, 12, 31),
                "order": 2,
            },
            {
                "title": "Software Engineer",
                "company": "Innovatech",
                "description": "Contributed to backend APIs, optimized database queries, and implemented authentication systems.",
                "start_date": date(2023, 7, 1),
                "end_date": None,
                "order": 3,
            },
        ]

        for exp in experiences_data:
            obj, created = MyExperience.objects.update_or_create(
                title=exp["title"],
                company=exp["company"],
                defaults={
                    "description": exp["description"],
                    "start_date": exp["start_date"],
                    "end_date": exp["end_date"],
                    "order": exp["order"],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added experience: {obj.title} at {obj.company}"))
            else:
                self.stdout.write(self.style.WARNING(f"Updated experience: {obj.title} at {obj.company}"))
