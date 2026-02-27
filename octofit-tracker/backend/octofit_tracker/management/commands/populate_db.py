from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from octofit_tracker.models import UserProfile, Activity, Team, Leaderboard, WorkoutSuggestion, Achievement
from django.utils import timezone
from datetime import timedelta
import random

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Deleting old data...'))
        Activity.objects.all().delete()
        Team.objects.all().delete()
        Leaderboard.objects.all().delete()
        WorkoutSuggestion.objects.all().delete()
        Achievement.objects.all().delete()
        UserProfile.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()

        self.stdout.write(self.style.SUCCESS('Old data deleted.'))

        # Super heroes sample data
        users_data = [
            {'username': 'ironman', 'email': 'ironman@marvel.com', 'first_name': 'Tony', 'last_name': 'Stark'},
            {'username': 'spiderman', 'email': 'spiderman@marvel.com', 'first_name': 'Peter', 'last_name': 'Parker'},
            {'username': 'captainmarvel', 'email': 'captainmarvel@marvel.com', 'first_name': 'Carol', 'last_name': 'Danvers'},
            {'username': 'batman', 'email': 'batman@dc.com', 'first_name': 'Bruce', 'last_name': 'Wayne'},
            {'username': 'wonderwoman', 'email': 'wonderwoman@dc.com', 'first_name': 'Diana', 'last_name': 'Prince'},
            {'username': 'flash', 'email': 'flash@dc.com', 'first_name': 'Barry', 'last_name': 'Allen'},
        ]

        marvel_team = Team.objects.create(name='Team Marvel', description='Marvel superheroes', creator=None)
        dc_team = Team.objects.create(name='Team DC', description='DC superheroes', creator=None)

        created_users = []
        for user_data in users_data:
            user, created = User.objects.get_or_create(username=user_data['username'], defaults=user_data)
            user.set_password('password123')
            user.save()
            profile = UserProfile.objects.create(user=user, fitness_level=random.choice(['beginner', 'intermediate', 'advanced']))
            created_users.append(user)
            if 'marvel' in user.email:
                marvel_team.members.add(user)
            else:
                dc_team.members.add(user)

        marvel_team.creator = created_users[0]
        dc_team.creator = created_users[3]
        marvel_team.save()
        dc_team.save()

        # Activities
        activity_types = ['running', 'walking', 'cycling', 'swimming', 'strength_training', 'yoga', 'sports']
        intensities = ['low', 'medium', 'high']
        base_date = timezone.now() - timedelta(days=30)
        for user in created_users:
            for j in range(random.randint(3, 7)):
                activity_date = base_date + timedelta(days=random.randint(0, 29), hours=random.randint(6, 20))
                activity = Activity.objects.create(
                    user=user,
                    activity_type=random.choice(activity_types),
                    duration_minutes=random.randint(20, 120),
                    distance_km=round(random.uniform(2.0, 15.0), 2),
                    calories_burned=random.randint(150, 800),
                    intensity=random.choice(intensities),
                    notes=f'Activity for {user.username}',
                    logged_at=activity_date
                )
                user.profile.total_points += activity.calculate_points()
                user.profile.total_workouts += 1
            user.profile.save()

        # Leaderboard
        sorted_users = sorted(created_users, key=lambda u: u.profile.total_points, reverse=True)
        for rank, user in enumerate(sorted_users, 1):
            Leaderboard.objects.create(
                leaderboard_type='global',
                user=user,
                rank=rank,
                points=user.profile.total_points,
                period_start=timezone.now() - timedelta(days=7)
            )

        # Workout Suggestions
        suggestions_data = [
            {'title': 'Hero Run', 'description': 'Run like a superhero', 'activity_type': 'running', 'difficulty_level': 'beginner'},
            {'title': 'Power Yoga', 'description': 'Yoga for strength', 'activity_type': 'yoga', 'difficulty_level': 'intermediate'},
            {'title': 'Strength Circuit', 'description': 'Super strength training', 'activity_type': 'strength_training', 'difficulty_level': 'advanced'},
        ]
        for user in created_users:
            for suggestion_data in random.sample(suggestions_data, k=2):
                WorkoutSuggestion.objects.create(
                    user=user,
                    estimated_duration_minutes=random.choice([30, 45, 60]),
                    recommended_frequency=random.choice(['daily', '3x_per_week', 'weekly']),
                    reason='Superhero training',
                    **suggestion_data
                )

        # Achievements
        achievement_data = [
            {'title': 'First Mission', 'description': 'Complete your first activity', 'points_reward': 50, 'criteria': '1 activity'},
            {'title': 'League Member', 'description': 'Join a superhero team', 'points_reward': 100, 'criteria': 'Join team'},
        ]
        for user in created_users:
            for achievement in achievement_data:
                Achievement.objects.create(
                    user=user,
                    badge_icon_url='http://example.com/badge.png',
                    **achievement
                )

        self.stdout.write(self.style.SUCCESS('Test data populated successfully!'))
