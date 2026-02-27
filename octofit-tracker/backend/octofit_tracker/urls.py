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
        codespace_name = os.environ.get('CODESPACE_NAME')
        if codespace_name:
            base_url = f"https://{codespace_name}-8000.app.github.dev"
        else:
            base_url = request.build_absolute_uri('').rstrip('/')
        return Response({
            'message': 'Welcome to OctoFit Tracker API',
            'version': '1.0.0',
            'endpoints': {
                'profiles': f"{base_url}/api/profiles/",
                'activities': f"{base_url}/api/activities/",
                'teams': f"{base_url}/api/teams/",
                'leaderboards': f"{base_url}/api/leaderboards/",
                'workout-suggestions': f"{base_url}/api/workout-suggestions/",
                'achievements': f"{base_url}/api/achievements/",
                'admin': f"{base_url}/admin/",
            }
        })


api_root = APIRoot.as_view()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_root, name='api-root'),
    path('api/', include(router.urls)),
    path('', api_root, name='root'),  # Redirige '/' a la API root
]
