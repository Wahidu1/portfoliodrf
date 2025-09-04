from django.db.models.signals import post_migrate
from django.dispatch import receiver
from apps.users.models import Settings

@receiver(post_migrate)
def create_default_settings(sender, **kwargs):
    """
    Ensure default settings are created after migrations.
    """
    defaults = [
        {"key": "facebook", "value": "https://facebook.com/yourpage"},
        {"key": "twitter", "value": "https://twitter.com/yourprofile"},
        {"key": "linkedin", "value": "https://linkedin.com/in/yourprofile"},
        {"key": "github", "value": "https://github.com/yourusername"},
        {"key": "email", "value": "Vb5r0@example.com"},
        {"key": "about", "value": "I’m Wahid, a passionate backend developer specializing in Django & DRF. I love creating clean, scalable, and efficient systems that power web applications. I focus on performance, maintainability, and smooth user experiences."},
        {"key": "header", "value": "Backend Developer specializing in Django & DRF. I craft clean APIs and scalable systems with a focus on performance and simplicity."},
        {"key": "highlightText", "value": "['Django', 'DRF', 'Python', 'Flask', 'FastAPI', 'React']"},
        {"key": "website_url", "value": "https://example.com"},
        {"key": "website_name", "value": "My Portfolio"},
        {"key": "website_logo", "value": "/static/default_logo.png"},
    ]
    for item in defaults:
        Settings.objects.update_or_create(
            key=item["key"],
            defaults={"value": item["value"]}
        )
