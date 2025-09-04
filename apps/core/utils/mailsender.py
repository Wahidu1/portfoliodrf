from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone

def send_support_email(name, email, subject="Contact Message", message="Thanks for reaching out!", from_email=None):
    """
    Send an email to the provided email address when a new contact message is submitted.
    """
    if from_email is None:
        from_email = settings.DEFAULT_FROM_EMAIL

    context = {
        'website_url': settings.WEBSITE_URL,
        'website_name': settings.WEBSITE_NAME,
        'name': name,
        'email': email,
        'from_email': from_email,
        'message': message,
        'year': timezone.now().year,
        "logo": settings.WEBSITE_LOGO
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
