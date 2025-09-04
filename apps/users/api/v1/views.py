"""
User application view
"""

import logging
import random
from collections import defaultdict
from typing import Any, Dict

from drf_spectacular.utils import extend_schema
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError, transaction
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response


from apps.core.utils import (format_response, generate_random_token,
                             send_support_email)

from apps.users.api.v1.serializers import (ContactMessageSerializer, MySkillSerializer,
                                           MyWorkSerializer, MyAchievementSerializer,
                                           MyExperienceSerializer, BlogPostSerializer, SettingsFilesSerializer)
from apps.users.models import MyExperience, MySkill, MyWork, MyAchievement, BlogPost, SettingFiles, Settings
from apps.users.tasks import send_support_email_task

# Create your views here.

logger = logging.getLogger(__name__)


class MySkillView(APIView):
    def get(self, request):
        skills = MySkill.objects.all()
        serializer = MySkillSerializer(skills, many=True, context={'request': request})
        data = {
            "success": True,
            "message": "Operation successful",
            "results": serializer.data
        }
        return Response(data, status=200)


class MyWorkView(APIView):
    def get(self, request, id=None):

        if id:
            work = get_object_or_404(MyWork, id=id)
            serializer = MyWorkSerializer(work, context={'request': request})
            data = {
                "success": True,
                "message": "Operation successful",
                "results": serializer.data
            }
            return Response(data, status=200)

        works = MyWork.objects.all()
        serializer = MyWorkSerializer(works, many=True, context={'request': request})
        data = {
            "success": True,
            "message": "Operation successful",
            "results": serializer.data
        }
        return Response(data, status=200)

class MyAchievementsView(APIView):
    def get(self, request):
        achievements = MyAchievement.objects.all()
        serializer = MyAchievementSerializer(achievements, many=True, context={'request': request})
        data = {
            "success": True,
            "message": "Operation successful",
            "results": serializer.data
        }
        return Response(data, status=200)

class MyExperienceView(APIView):
    def get(self, request):
        experiences = MyExperience.objects.all()
        serializer = MyExperienceSerializer(experiences, many=True, context={'request': request})
        data = {
            "success": True,
            "message": "Operation successful",
            "results": serializer.data
        }
        return Response(data, status=200)


class ContactMessageView(APIView):

    @extend_schema(
        request=ContactMessageSerializer,  # <--- explicitly set request body
        responses={200: ContactMessageSerializer}
    )
    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name'] # type: ignore
            email = serializer.validated_data['email'] # type: ignore
            message = serializer.validated_data['message'] # type: ignore
            try:
                send_support_email_task.delay(name, email, message)
            except Exception as e:
                print(e)
                logger.error(e)
            serializer.save()
            return Response({
                "success": True,
                "message": "Operation successful",
                "results": serializer.data
            }, status=200)
        return Response({
            "success": False,
            "message": "Operation failed",
            "results": serializer.errors
        }, status=400)

class BlogPostView(APIView):
    def get(self, request, slug=None):
        if slug:
            post = get_object_or_404(BlogPost, slug=slug)
            serializer = BlogPostSerializer(post, context={'request': request})
            data = {
                "success": True,
                "message": "Operation successful",
                "results": serializer.data
            }
            return Response(data, status=200)
        posts = BlogPost.objects.filter(status=BlogPost.Status.PUBLISHED).order_by('-published_at')
        serializer = BlogPostSerializer(posts, many=True, context={'request': request})
        data = {
            "success": True,
            "message": "Operation successful",
            "results": serializer.data
        }
        return Response(data, status=200)


class SettingsView(APIView):
    def get(self, request):
        settings = Settings.objects.all()
        data = []
        for setting in settings:
            data.append({
                "key": setting.key,
                "value": setting.value
            })
        return Response({
            "success": True,
            "message": "Operation successful",
            "results": data
            }, status=200)

class SettingsFilesView(APIView):

    def get(self, request):
        settings = SettingFiles.objects.all()
        data = SettingsFilesSerializer(settings, many=True, context={'request': request}).data
        return Response({
            "success": True,
            "message": "Operation successful",
            "results": data
            }, status=200)
