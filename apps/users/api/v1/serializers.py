import json
import random
from datetime import timedelta

from dateutil.relativedelta import relativedelta
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from django.utils import timezone
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError as DRFValidationError

from apps.core.utils import (send_support_email, generate_unique_token)

from apps.users.models import MyAchievement, MySkill, MyUser, SettingFiles, Settings, BlogComment, BlogPost, ContactMessage, FrequentlyAskedQuestion, MyExperience, MyWork, Technology, Testimonial

class MySkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = MySkill
        fields = ( 'id', 'name', 'icon', 'percentage', 'order')
        read_only = ('id',)


class MyAchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyAchievement
        fields = ( 'id', 'title', 'organization', 'image', 'date', 'order')
        read_only = ('id',)


class MyWorkSerializer(serializers.ModelSerializer):
    technologies = serializers.SerializerMethodField()
    class Meta:
        model = MyWork
        fields = ( 'id', 'title', 'subtext', 'description', 'image', 'technologies', 'github_link', 'live_link', 'order')
        read_only = ('id',)
    def get_technologies(self, obj):
        return [t.name for t in obj.technologies.all()]

class MyExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyExperience
        fields = ( 'id', 'title', 'company', 'description', 'start_date', 'end_date', 'order')
        read_only = ('id',)

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ( 'id', 'name', 'email', 'message')
        read_only = ('id',)

class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ( 'id', 'title', 'slug', 'excerpt', 'content', 'image', 'published_at')
        read_only = ('id',)

class SettingsFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SettingFiles
        fields = ( 'id', 'name', 'file')
        read_only = ('id',)
