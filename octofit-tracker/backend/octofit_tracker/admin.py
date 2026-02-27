"""
Django admin configuration for OctoFit Tracker models.
"""

from django.contrib import admin
from .models import (
    UserProfile, Activity, Team, Leaderboard,
    WorkoutSuggestion, Achievement
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin interface for UserProfile."""
    list_display = ('user', 'fitness_level', 'total_points', 'total_workouts', 'created_at')
    list_filter = ('fitness_level', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Profile Information', {
            'fields': ('bio', 'profile_picture_url', 'fitness_level')
        }),
        ('Statistics', {
            'fields': ('total_points', 'total_workouts')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """Admin interface for Activity."""
    list_display = ('user', 'activity_type', 'duration_minutes', 'intensity', 'logged_at')
    list_filter = ('activity_type', 'intensity', 'logged_at')
    search_fields = ('user__username', 'notes')
    readonly_fields = ('created_at', 'id')
    date_hierarchy = 'logged_at'
    fieldsets = (
        ('User & Type', {
            'fields': ('id', 'user', 'activity_type')
        }),
        ('Activity Details', {
            'fields': ('duration_minutes', 'distance_km', 'calories_burned', 'intensity', 'notes')
        }),
        ('Timestamps', {
            'fields': ('logged_at', 'created_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Admin interface for Team."""
    list_display = ('name', 'creator', 'member_count', 'team_points', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description', 'creator__username')
    readonly_fields = ('created_at', 'updated_at', 'team_points', 'id')
    filter_horizontal = ('members',)
    fieldsets = (
        ('Team Information', {
            'fields': ('id', 'name', 'description')
        }),
        ('Management', {
            'fields': ('creator', 'members')
        }),
        ('Statistics', {
            'fields': ('team_points',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def member_count(self, obj):
        """Display member count."""
        return obj.members.count()
    member_count.short_description = 'Members'
    
    def team_points(self, obj):
        """Display team points."""
        return obj.calculate_team_points()
    team_points.short_description = 'Total Points'


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    """Admin interface for Leaderboard."""
    list_display = ('rank', 'leaderboard_type', 'user_or_team', 'points', 'period_start')
    list_filter = ('leaderboard_type', 'period_start')
    search_fields = ('user__username', 'team__name')
    readonly_fields = ('created_at', 'updated_at', 'id')
    fieldsets = (
        ('Ranking', {
            'fields': ('id', 'rank', 'points')
        }),
        ('Type', {
            'fields': ('leaderboard_type',)
        }),
        ('Entity', {
            'fields': ('user', 'team')
        }),
        ('Period', {
            'fields': ('period_start', 'period_end'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def user_or_team(self, obj):
        """Display user or team name."""
        if obj.user:
            return obj.user.username
        elif obj.team:
            return obj.team.name
        return 'N/A'
    user_or_team.short_description = 'User / Team'


@admin.register(WorkoutSuggestion)
class WorkoutSuggestionAdmin(admin.ModelAdmin):
    """Admin interface for WorkoutSuggestion."""
    list_display = ('title', 'user', 'activity_type', 'difficulty_level', 'created_at')
    list_filter = ('activity_type', 'difficulty_level', 'created_at')
    search_fields = ('title', 'description', 'user__username')
    readonly_fields = ('created_at', 'updated_at', 'id')
    fieldsets = (
        ('Suggestion Details', {
            'fields': ('id', 'user', 'title', 'description', 'reason')
        }),
        ('Workout Parameters', {
            'fields': ('activity_type', 'difficulty_level', 'estimated_duration_minutes', 'recommended_frequency')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    """Admin interface for Achievement."""
    list_display = ('title', 'user', 'points_reward', 'earned_at')
    list_filter = ('earned_at',)
    search_fields = ('title', 'description', 'user__username')
    readonly_fields = ('earned_at', 'id')
    fieldsets = (
        ('Achievement Details', {
            'fields': ('id', 'user', 'title', 'description')
        }),
        ('Reward', {
            'fields': ('points_reward', 'badge_icon_url', 'criteria')
        }),
        ('Timestamp', {
            'fields': ('earned_at',),
            'classes': ('collapse',)
        }),
    )
