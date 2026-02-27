"""
Models for the OctoFit Tracker application.
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime


class UserProfile(models.Model):
    """Extended user profile for fitness tracking."""
    
    ACTIVITY_LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True, default='')
    profile_picture_url = models.URLField(blank=True, default='')
    fitness_level = models.CharField(
        max_length=20,
        choices=ACTIVITY_LEVEL_CHOICES,
        default='beginner'
    )
    total_points = models.IntegerField(default=0)
    total_workouts = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Profile of {self.user.username}"
    
    class Meta:
        db_table = 'user_profile'


class Activity(models.Model):
    """Activity logging for users."""
    
    ACTIVITY_TYPES = [
        ('running', 'Running'),
        ('walking', 'Walking'),
        ('cycling', 'Cycling'),
        ('swimming', 'Swimming'),
        ('strength_training', 'Strength Training'),
        ('yoga', 'Yoga'),
        ('sports', 'Sports'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    duration_minutes = models.IntegerField()  # Duration in minutes
    distance_km = models.FloatField(default=0.0)  # Distance in kilometers
    calories_burned = models.IntegerField(default=0)
    intensity = models.CharField(
        max_length=10,
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        default='medium'
    )
    notes = models.TextField(blank=True, default='')
    logged_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.activity_type} on {self.logged_at.date()}"
    
    def calculate_points(self):
        """Calculate points based on activity type, duration, and intensity."""
        base_points = {
            'running': 10,
            'walking': 5,
            'cycling': 8,
            'swimming': 12,
            'strength_training': 10,
            'yoga': 6,
            'sports': 10,
            'other': 5,
        }
        
        intensity_multiplier = {
            'low': 1.0,
            'medium': 1.5,
            'high': 2.0,
        }
        
        base = base_points.get(self.activity_type, 5)
        duration_factor = self.duration_minutes / 30  # 30 minutes = 1x
        intensity_factor = intensity_multiplier.get(self.intensity, 1.0)
        
        points = int(base * duration_factor * intensity_factor)
        return max(points, 1)
    
    class Meta:
        db_table = 'activity'
        ordering = ['-logged_at']


class Team(models.Model):
    """Team model for group fitness challenges."""
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_teams')
    members = models.ManyToManyField(User, related_name='teams', blank=True)
    team_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def calculate_team_points(self):
        """Calculate total team points from all members."""
        total = 0
        for member in self.members.all():
            member_profile = member.profile
            total += member_profile.total_points
        return total
    
    class Meta:
        db_table = 'team'


class Leaderboard(models.Model):
    """Leaderboard for tracking rankings."""
    
    LEADERBOARD_TYPES = [
        ('global', 'Global'),
        ('team', 'Team'),
        ('monthly', 'Monthly'),
        ('weekly', 'Weekly'),
    ]
    
    leaderboard_type = models.CharField(max_length=20, choices=LEADERBOARD_TYPES, default='global')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leaderboard_entries', null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='leaderboard_entries', null=True, blank=True)
    rank = models.IntegerField()
    points = models.IntegerField()
    period_start = models.DateTimeField(default=timezone.now)
    period_end = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if self.user:
            return f"{self.rank}. {self.user.username} - {self.points} points"
        elif self.team:
            return f"{self.rank}. {self.team.name} - {self.points} points"
        return f"Rank {self.rank}"
    
    class Meta:
        db_table = 'leaderboard'
        ordering = ['rank']
        unique_together = ('leaderboard_type', 'user', 'team', 'period_start')


class WorkoutSuggestion(models.Model):
    """Personalized workout suggestions for users."""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workout_suggestions')
    title = models.CharField(max_length=200)
    description = models.TextField()
    activity_type = models.CharField(
        max_length=20,
        choices=Activity.ACTIVITY_TYPES,
        default='running'
    )
    difficulty_level = models.CharField(
        max_length=20,
        choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')],
        default='beginner'
    )
    estimated_duration_minutes = models.IntegerField()
    recommended_frequency = models.CharField(
        max_length=20,
        choices=[('daily', 'Daily'), ('3x_per_week', '3x Per Week'), ('2x_per_week', '2x Per Week'), ('weekly', 'Weekly')],
        default='3x_per_week'
    )
    reason = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} for {self.user.username}"
    
    class Meta:
        db_table = 'workout_suggestion'


class Achievement(models.Model):
    """Achievement badges for users."""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=100)
    description = models.TextField()
    badge_icon_url = models.URLField(default='')
    criteria = models.CharField(max_length=200, default='')
    points_reward = models.IntegerField(default=0)
    earned_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"
    
    class Meta:
        db_table = 'achievement'
