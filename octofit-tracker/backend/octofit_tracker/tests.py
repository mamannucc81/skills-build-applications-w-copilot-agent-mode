"""
Tests for OctoFit Tracker models and views.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from .models import (
    UserProfile, Activity, Team, Leaderboard,
    WorkoutSuggestion, Achievement
)


class UserProfileTestCase(TestCase):
    """Test cases for UserProfile model."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            fitness_level='beginner',
            bio='Test bio'
        )
    
    def test_profile_creation(self):
        """Test that a user profile is created successfully."""
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertEqual(self.profile.fitness_level, 'beginner')
        self.assertEqual(self.profile.total_points, 0)
    
    def test_profile_string(self):
        """Test the string representation of UserProfile."""
        self.assertEqual(str(self.profile), 'Profile of testuser')


class ActivityTestCase(TestCase):
    """Test cases for Activity model."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.user = User.objects.create_user(
            username='athlete',
            email='athlete@example.com',
            password='testpass123'
        )
        self.profile = UserProfile.objects.create(user=self.user)
        self.activity = Activity.objects.create(
            user=self.user,
            activity_type='running',
            duration_minutes=30,
            distance_km=5.0,
            calories_burned=300,
            intensity='medium'
        )
    
    def test_activity_creation(self):
        """Test that an activity is created successfully."""
        self.assertEqual(self.activity.user.username, 'athlete')
        self.assertEqual(self.activity.activity_type, 'running')
        self.assertEqual(self.activity.duration_minutes, 30)
    
    def test_calculate_points(self):
        """Test point calculation for activities."""
        points = self.activity.calculate_points()
        self.assertGreater(points, 0)
        self.assertIsInstance(points, int)
    
    def test_activity_string(self):
        """Test the string representation of Activity."""
        expected = f"athlete - running on {self.activity.logged_at.date()}"
        self.assertEqual(str(self.activity), expected)


class TeamTestCase(TestCase):
    """Test cases for Team model."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
        self.profile1 = UserProfile.objects.create(user=self.user1, total_points=100)
        self.profile2 = UserProfile.objects.create(user=self.user2, total_points=50)
        self.team = Team.objects.create(
            name='Test Team',
            description='Test team description',
            creator=self.user1
        )
        self.team.members.add(self.user1, self.user2)
    
    def test_team_creation(self):
        """Test that a team is created successfully."""
        self.assertEqual(self.team.name, 'Test Team')
        self.assertEqual(self.team.creator.username, 'user1')
    
    def test_team_member_count(self):
        """Test team member count."""
        self.assertEqual(self.team.members.count(), 2)
    
    def test_calculate_team_points(self):
        """Test team points calculation."""
        team_points = self.team.calculate_team_points()
        self.assertEqual(team_points, 150)  # 100 + 50


class LeaderboardTestCase(TestCase):
    """Test cases for Leaderboard model."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.user = User.objects.create_user(username='leader', password='pass123')
        self.profile = UserProfile.objects.create(user=self.user, total_points=500)
        self.leaderboard = Leaderboard.objects.create(
            leaderboard_type='global',
            user=self.user,
            rank=1,
            points=500
        )
    
    def test_leaderboard_creation(self):
        """Test that a leaderboard entry is created successfully."""
        self.assertEqual(self.leaderboard.rank, 1)
        self.assertEqual(self.leaderboard.points, 500)
        self.assertEqual(self.leaderboard.leaderboard_type, 'global')
    
    def test_leaderboard_string(self):
        """Test the string representation of Leaderboard."""
        expected = '1. leader - 500 points'
        self.assertEqual(str(self.leaderboard), expected)


class WorkoutSuggestionTestCase(TestCase):
    """Test cases for WorkoutSuggestion model."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.user = User.objects.create_user(username='trainer', password='pass123')
        self.suggestion = WorkoutSuggestion.objects.create(
            user=self.user,
            title='Morning Run',
            description='A good morning run to start the day',
            activity_type='running',
            difficulty_level='beginner',
            estimated_duration_minutes=30,
            recommended_frequency='3x_per_week'
        )
    
    def test_suggestion_creation(self):
        """Test that a workout suggestion is created successfully."""
        self.assertEqual(self.suggestion.title, 'Morning Run')
        self.assertEqual(self.suggestion.activity_type, 'running')
        self.assertEqual(self.suggestion.difficulty_level, 'beginner')


class AchievementTestCase(TestCase):
    """Test cases for Achievement model."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.user = User.objects.create_user(username='achiever', password='pass123')
        self.achievement = Achievement.objects.create(
            user=self.user,
            title='First Run',
            description='Completed your first running activity',
            badge_icon_url='http://example.com/first-run.png',
            points_reward=50,
            criteria='Complete 1 running activity'
        )
    
    def test_achievement_creation(self):
        """Test that an achievement is created successfully."""
        self.assertEqual(self.achievement.title, 'First Run')
        self.assertEqual(self.achievement.points_reward, 50)


class UserProfileAPITestCase(APITestCase):
    """API tests for UserProfile endpoints."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='apiuser',
            email='api@example.com',
            password='apipass123'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            fitness_level='intermediate'
        )
    
    def test_list_profiles(self):
        """Test listing all profiles."""
        response = self.client.get('/api/profiles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_retrieve_profile(self):
        """Test retrieving a specific profile."""
        response = self.client.get(f'/api/profiles/{self.profile.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['username'], 'apiuser')


class ActivityAPITestCase(APITestCase):
    """API tests for Activity endpoints."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='active',
            email='active@example.com',
            password='activepass'
        )
        UserProfile.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user)
    
    def test_create_activity(self):
        """Test creating a new activity."""
        data = {
            'activity_type': 'running',
            'duration_minutes': 45,
            'distance_km': 7.0,
            'calories_burned': 450,
            'intensity': 'high'
        }
        response = self.client.post('/api/activities/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Activity.objects.count(), 1)
    
    def test_my_activities_endpoint(self):
        """Test retrieving current user's activities."""
        Activity.objects.create(
            user=self.user,
            activity_type='running',
            duration_minutes=30,
            intensity='medium'
        )
        response = self.client.get('/api/activities/my_activities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class TeamAPITestCase(APITestCase):
    """API tests for Team endpoints."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='teamleader',
            email='leader@example.com',
            password='leaderpass'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_create_team(self):
        """Test creating a new team."""
        data = {
            'name': 'Running Club',
            'description': 'For running enthusiasts'
        }
        response = self.client.post('/api/teams/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), 1)
