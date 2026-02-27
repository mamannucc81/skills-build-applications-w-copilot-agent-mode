"""
Serializers for the OctoFit Tracker API.
Converts ObjectId fields to strings for API responses.
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    UserProfile, Activity, Team, Leaderboard,
    WorkoutSuggestion, Achievement
)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile model."""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'bio', 'profile_picture_url',
            'fitness_level', 'total_points', 'total_workouts',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for Activity model with ObjectId conversion to string."""
    user_id = serializers.IntegerField(source='user.id')
    username = serializers.CharField(source='user.username', read_only=True)
    points = serializers.SerializerMethodField()
    
    class Meta:
        model = Activity
        fields = [
            'id', 'user_id', 'username', 'activity_type',
            'duration_minutes', 'distance_km', 'calories_burned',
            'intensity', 'notes', 'logged_at', 'created_at', 'points'
        ]
        read_only_fields = ['id', 'created_at', 'points']
    
    def get_points(self, obj):
        """Calculate and return points for the activity."""
        return obj.calculate_points()


class TeamSerializer(serializers.ModelSerializer):
    """Serializer for Team model with ObjectId conversion to string."""
    creator_id = serializers.IntegerField(source='creator.id', read_only=True)
    creator_name = serializers.CharField(source='creator.username', read_only=True)
    members = UserSerializer(many=True, read_only=True)
    member_count = serializers.SerializerMethodField()
    team_points = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = [
            'id', 'name', 'description', 'creator_id', 'creator_name',
            'members', 'member_count', 'team_points',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'team_points']
    
    def get_member_count(self, obj):
        """Return the count of team members."""
        return obj.members.count()
    
    def get_team_points(self, obj):
        """Calculate and return total team points."""
        return obj.calculate_team_points()


class LeaderboardSerializer(serializers.ModelSerializer):
    """Serializer for Leaderboard model with ObjectId conversion to string."""
    user = UserSerializer(read_only=True)
    team = TeamSerializer(read_only=True)
    
    class Meta:
        model = Leaderboard
        fields = [
            'id', 'leaderboard_type', 'user', 'team', 'rank',
            'points', 'period_start', 'period_end',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class WorkoutSuggestionSerializer(serializers.ModelSerializer):
    """Serializer for WorkoutSuggestion model with ObjectId conversion to string."""
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = WorkoutSuggestion
        fields = [
            'id', 'user_id', 'username', 'title', 'description',
            'activity_type', 'difficulty_level', 'estimated_duration_minutes',
            'recommended_frequency', 'reason',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AchievementSerializer(serializers.ModelSerializer):
    """Serializer for Achievement model with ObjectId conversion to string."""
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Achievement
        fields = [
            'id', 'user_id', 'username', 'title', 'description',
            'badge_icon_url', 'criteria', 'points_reward', 'earned_at'
        ]
        read_only_fields = ['id', 'earned_at']
