from django.urls import path

from apps.users.api.v1.views import *


urlpatterns = [
    path('skills/', MySkillView.as_view()),
    path('works/', MyWorkView.as_view()),
    path('works/<int:id>/', MyWorkView.as_view()),
    path('achievements/', MyAchievementsView.as_view()),
    path('experiences/', MyExperienceView.as_view()),
    path('contact/', ContactMessageView.as_view()),
    path('blog/', BlogPostView.as_view()),
    path('blog/<slug:slug>/', BlogPostView.as_view()),
    path('settings/', SettingsView.as_view()),
    path('settings/files/', SettingsFilesView.as_view()),
]
