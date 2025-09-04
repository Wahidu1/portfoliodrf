from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.users.managers import MyUserManager


class MyUser(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(max_length=60, unique=True, verbose_name="Email")
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False, verbose_name="Verified")
    name = models.CharField(max_length=250, verbose_name="Name")
    name_ar = models.CharField(
        max_length=250, verbose_name="Arabic Name", null=True, blank=True)
    date_joined = models.DateTimeField(
        verbose_name="Date Joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="Last Login", auto_now=True)
    is_active = models.BooleanField(default=True, verbose_name="Active")
    is_superuser = models.BooleanField(default=False, verbose_name="Superuser")
    is_admin = models.BooleanField(default=False, verbose_name="Admin")
    is_staff = models.BooleanField(default=False, verbose_name="Staff")
    is_two_step = models.BooleanField(
        default=False, verbose_name="Two-Step Verification")

    token_valid = models.BooleanField(
        default=False, verbose_name="Token Valid")

    USERNAME_FIELD = "email"

    objects = MyUserManager()

    def __str__(self) -> str:
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

class MySkill(BaseModel):
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='skills/', blank=True, null=True)
    percentage = models.PositiveIntegerField(default=0)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Skill"
        verbose_name_plural = "Skills"
        ordering = ["order"]

class Technology(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=100, blank=True, null=True)  # For Font Awesome icons

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Technology"
        verbose_name_plural = "Technologies"
        ordering = ["name"]

class MyWork(BaseModel):
    title = models.CharField(max_length=100)
    subtext = models.TextField()
    description = models.TextField()
    image = models.ImageField(upload_to='works/', blank=True, null=True)
    technologies = models.ManyToManyField(Technology, related_name='works')
    github_link = models.URLField(blank=True, null=True)
    live_link = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Work"
        verbose_name_plural = "Works"
        ordering = ["order"]

class MyAchievement(BaseModel):
    title = models.CharField(max_length=100)
    organization = models.CharField(max_length=100)
    image = models.ImageField(upload_to='achievements/', blank=True, null=True)
    date = models.DateField()
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Achievement"
        verbose_name_plural = "Achievements"
        ordering = ["order"]

class MyExperience(BaseModel):
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Experience"
        verbose_name_plural = "Experiences"
        ordering = ["order"]

class ContactMessage(BaseModel):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self) -> str:
        return f"{self.name} - {self.email}"

    class Meta:
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
        ordering = ["-created_at"]


class Testimonial(BaseModel):
    client_name = models.CharField(max_length=100)
    feedback = models.TextField()
    rating = models.PositiveIntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    client_photo = models.ImageField(
        upload_to='testimonials/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.client_name} ({self.rating}★)"

    class Meta:
        ordering = ["order"]
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"








class Settings(BaseModel):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()

    def __str__(self):
        return f"{self.key} - {self.value}"

    class Meta:
        verbose_name = "Settings"
        verbose_name_plural = "Settings"


class FrequentlyAskedQuestion(BaseModel):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.question

    class Meta:
        ordering = ["order"]
        verbose_name = "Frequently Asked Question"
        verbose_name_plural = "Frequently Asked Questions"

class BlogPost(BaseModel):
    # SUGGESTION: Using `models.TextChoices` is the modern and recommended way
    # to handle choices. It's cleaner and more readable than a simple tuple.
    class Status(models.TextChoices):
        DRAFT = "draft", _("Draft")
        PUBLISHED = "published", _("Published")

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, max_length=255) # Increased max_length
    excerpt = models.TextField(blank=True, null=True)
    content = models.TextField()
    image = models.ImageField(upload_to='blog/', blank=True, null=True)
    published_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.DRAFT)

    class Meta:
        # SUGGESTION: Order blog posts by publication date by default.
        ordering = ["-published_at"]

    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        # If post is being published and has no published_at date, set it.
        if self.status == self.Status.PUBLISHED and self.published_at is None:
            self.published_at = timezone.now()

        super().save(*args, **kwargs)


class BlogComment(BaseModel):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.email}"


class SettingFiles(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    file = models.FileField(upload_to='settings_files/')

    def __str__(self):
        return self.name
