"""
URL configuration for octofit_tracker.
"""

import os
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.views import APIView
from rest_framework.response import Response

from .views import (
    UserProfileViewSet, ActivityViewSet, TeamViewSet,
    LeaderboardViewSet, WorkoutSuggestionViewSet,
    AchievementViewSet
)

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet, basename='userprofile')
router.register(r'activities', ActivityViewSet, basename='activity')
router.register(r'teams', TeamViewSet, basename='team')
router.register(r'leaderboards', LeaderboardViewSet, basename='leaderboard')
router.register(r'workout-suggestions', WorkoutSuggestionViewSet, basename='workoutsuggestion')
router.register(r'achievements', AchievementViewSet, basename='achievement')


class APIRoot(APIView):
    """API root endpoint."""
    def get(self, request):
        return Response({
            'message': 'Welcome to OctoFit Tracker API',
            'version': '1.0.0',
            'endpoints': {
                'profiles': request.build_absolute_uri('/api/profiles/'),
                'activities': request.build_absolute_uri('/api/activities/'),
                'teams': request.build_absolute_uri('/api/teams/'),
                'leaderboards': request.build_absolute_uri('/api/leaderboards/'),
                'workout-suggestions': request.build_absolute_uri('/api/workout-suggestions/'),
                'achievements': request.build_absolute_uri('/api/achievements/'),
                'admin': request.build_absolute_uri('/admin/'),
            }
        })


api_root = APIRoot.as_view()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_root, name='api-root'),
    path('api/', include(router.urls)),
    path('', api_root, name='root'),  # Redirige '/' a la API root
]
