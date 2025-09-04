from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from apps.users.models import Settings

@shared_task
def send_support_email_task(name, email, subject="Contact Message", message="Thanks for reaching out!", from_email=None):
    """
    Send an email to the provided email address when a new contact message is submitted.
    """
    if from_email is None:
        from_email = settings.DEFAULT_FROM_EMAIL
    def get_setting(key, default=None):
        """Helper to get a setting value by key."""
        setting = Settings.objects.filter(key=key).first()
        return setting.value if setting else default

    website_url = get_setting("website_url", "https://default.url")
    website_name = get_setting("website_name", "My Website")
    website_logo = get_setting("website_logo", "/static/default_logo.png")

    context = {
        'website_url': website_url,
        'website_name': website_name,
        'logo': website_logo,
        'name': name,
        'email': email,
        'from_email': from_email,
        'message': message,
        'year': timezone.now().year,
    }


    email_subject = f"📩 New Contact Message: {subject}"
    html_content = render_to_string("email/contact_support.html", context)
    text_content = render_to_string("email/contact_support.txt", context)

    msg = EmailMultiAlternatives(
        subject=email_subject,
        body=text_content,
        from_email=from_email,
        to=[email],  # send to the email parameter
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
