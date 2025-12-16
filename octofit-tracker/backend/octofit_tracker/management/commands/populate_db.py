from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings
from djongo import models

from octofit_tracker import models as app_models

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Delete existing data
        User = get_user_model()
        User.objects.all().delete()
        app_models.Team.objects.all().delete()
        app_models.Activity.objects.all().delete()
        app_models.Leaderboard.objects.all().delete()
        app_models.Workout.objects.all().delete()

        # Create Teams
        marvel = app_models.Team.objects.create(name='Marvel')
        dc = app_models.Team.objects.create(name='DC')

        # Create Users (Superheroes)
        users = [
            {'email': 'tony@stark.com', 'username': 'IronMan', 'team': marvel},
            {'email': 'steve@rogers.com', 'username': 'CaptainAmerica', 'team': marvel},
            {'email': 'bruce@wayne.com', 'username': 'Batman', 'team': dc},
            {'email': 'clark@kent.com', 'username': 'Superman', 'team': dc},
        ]
        user_objs = []
        for u in users:
            user = User.objects.create_user(email=u['email'], username=u['username'], password='password', team=u['team'])
            user_objs.append(user)

        # Create Activities
        activities = [
            {'user': user_objs[0], 'type': 'Run', 'duration': 30},
            {'user': user_objs[1], 'type': 'Swim', 'duration': 45},
            {'user': user_objs[2], 'type': 'Bike', 'duration': 60},
            {'user': user_objs[3], 'type': 'Yoga', 'duration': 50},
        ]
        for a in activities:
            app_models.Activity.objects.create(user=a['user'], type=a['type'], duration=a['duration'])

        # Create Workouts
        workouts = [
            {'name': 'Morning Cardio', 'description': 'Cardio for all'},
            {'name': 'Strength Training', 'description': 'Strength for all'},
        ]
        for w in workouts:
            app_models.Workout.objects.create(**w)

        # Create Leaderboard
        app_models.Leaderboard.objects.create(team=marvel, points=100)
        app_models.Leaderboard.objects.create(team=dc, points=90)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
