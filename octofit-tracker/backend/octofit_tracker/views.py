"""
Views and ViewSets for the OctoFit Tracker API.
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta

from .models import (
    UserProfile, Activity, Team, Leaderboard,
    WorkoutSuggestion, Achievement
)
from .serializers import (
    UserSerializer, UserProfileSerializer, ActivitySerializer,
    TeamSerializer, LeaderboardSerializer, WorkoutSuggestionSerializer,
    AchievementSerializer
)


class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for User Profile management."""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', 'user__email']
    
    def get_queryset(self):
        """Filter profiles based on user."""
        queryset = UserProfile.objects.all()
        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = queryset.filter(user__username=username)
        return queryset
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user's profile."""
        if not request.user.is_authenticated:
            return Response(
                {'detail': 'User not authenticated'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        try:
            profile = request.user.profile
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response(
                {'detail': 'User profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def add_points(self, request, pk=None):
        """Add points to a user profile."""
        profile = self.get_object()
        points = request.data.get('points', 0)
        profile.total_points += points
        profile.save()
        serializer = self.get_serializer(profile)
        return Response(serializer.data)


class ActivityViewSet(viewsets.ModelViewSet):
    """ViewSet for Activity management."""
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__username', 'activity_type']
    ordering_fields = ['logged_at', 'created_at', 'duration_minutes']
    ordering = ['-logged_at']
    
    def get_queryset(self):
        """Filter activities based on user and date."""
        queryset = Activity.objects.all()
        username = self.request.query_params.get('username', None)
        activity_type = self.request.query_params.get('activity_type', None)
        date_from = self.request.query_params.get('date_from', None)
        
        if username is not None:
            queryset = queryset.filter(user__username=username)
        if activity_type is not None:
            queryset = queryset.filter(activity_type=activity_type)
        if date_from is not None:
            queryset = queryset.filter(logged_at__gte=date_from)
        
        return queryset
    
    def perform_create(self, serializer):
        """Create activity and add points to user profile."""
        activity = serializer.save()
        user_profile = activity.user.profile
        points = activity.calculate_points()
        user_profile.total_points += points
        user_profile.total_workouts += 1
        user_profile.save()
    
    @action(detail=False, methods=['get'])
    def my_activities(self, request):
        """Get current user's activities."""
        if not request.user.is_authenticated:
            return Response(
                {'detail': 'User not authenticated'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        activities = Activity.objects.filter(user=request.user)
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get activity statistics for current user."""
        if not request.user.is_authenticated:
            return Response(
                {'detail': 'User not authenticated'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        activities = Activity.objects.filter(user=request.user)
        
        stats = {
            'total_activities': activities.count(),
            'total_duration': activities.aggregate(Sum('duration_minutes'))['duration_minutes__sum'] or 0,
            'total_distance': activities.aggregate(Sum('distance_km'))['distance_km__sum'] or 0,
            'total_calories': activities.aggregate(Sum('calories_burned'))['calories_burned__sum'] or 0,
            'activity_types': {}
        }
        
        for activity_type, _ in Activity.ACTIVITY_TYPES:
            count = activities.filter(activity_type=activity_type).count()
            if count > 0:
                stats['activity_types'][activity_type] = count
        
        return Response(stats)


class TeamViewSet(viewsets.ModelViewSet):
    """ViewSet for Team management."""
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']
    
    def get_queryset(self):
        """Filter teams based on user membership."""
        queryset = Team.objects.all()
        my_teams = self.request.query_params.get('my_teams', None)
        if my_teams is not None and self.request.user.is_authenticated:
            queryset = queryset.filter(members=self.request.user)
        return queryset
    
    def perform_create(self, serializer):
        """Create team with current user as creator."""
        team = serializer.save(creator=self.request.user)
        team.members.add(self.request.user)
    
    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        """Add a member to the team."""
        team = self.get_object()
        user_id = request.data.get('user_id', None)
        
        if user_id is None:
            return Response(
                {'detail': 'user_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(id=user_id)
            team.members.add(user)
            serializer = self.get_serializer(team)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(
                {'detail': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def remove_member(self, request, pk=None):
        """Remove a member from the team."""
        team = self.get_object()
        user_id = request.data.get('user_id', None)
        
        if user_id is None:
            return Response(
                {'detail': 'user_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(id=user_id)
            team.members.remove(user)
            serializer = self.get_serializer(team)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(
                {'detail': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class LeaderboardViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Leaderboard (read-only)."""
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['leaderboard_type', 'user__username', 'team__name']
    ordering = ['rank']
    
    def get_queryset(self):
        """Filter leaderboard by type."""
        queryset = Leaderboard.objects.all()
        leaderboard_type = self.request.query_params.get('type', None)
        
        if leaderboard_type is not None:
            queryset = queryset.filter(leaderboard_type=leaderboard_type)
        
        return queryset


class WorkoutSuggestionViewSet(viewsets.ModelViewSet):
    """ViewSet for Workout Suggestions."""
    queryset = WorkoutSuggestion.objects.all()
    serializer_class = WorkoutSuggestionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        """Filter suggestions based on user."""
        queryset = WorkoutSuggestion.objects.all()
        username = self.request.query_params.get('username', None)
        
        if username is not None:
            queryset = queryset.filter(user__username=username)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def my_suggestions(self, request):
        """Get current user's workout suggestions."""
        if not request.user.is_authenticated:
            return Response(
                {'detail': 'User not authenticated'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        suggestions = WorkoutSuggestion.objects.filter(user=request.user)
        serializer = self.get_serializer(suggestions, many=True)
        return Response(serializer.data)


class AchievementViewSet(viewsets.ModelViewSet):
    """ViewSet for Achievement badges."""
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        """Filter achievements based on user."""
        queryset = Achievement.objects.all()
        username = self.request.query_params.get('username', None)
        
        if username is not None:
            queryset = queryset.filter(user__username=username)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def my_achievements(self, request):
        """Get current user's achievements."""
        if not request.user.is_authenticated:
            return Response(
                {'detail': 'User not authenticated'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        achievements = Achievement.objects.filter(user=request.user)
        serializer = self.get_serializer(achievements, many=True)
        return Response(serializer.data)
