"""Fill the site with sample squad, fixtures and news so you can preview it.

Usage:  python manage.py seed_demo
Safe to run again (it skips if data already exists).  Replace the sample data
with your real players/matches from the admin panel (/admin/).
"""
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from MBA.models import Announcement, Match, Player


class Command(BaseCommand):
    help = "Create sample players, matches and news for previewing the site."

    def handle(self, *args, **options):
        if Player.objects.exists() or Match.objects.exists() or Announcement.objects.exists():
            self.stdout.write("Data already present - nothing added.")
            return
        now = timezone.now()
        players = [
            ("Sample Keeper", "GK", 1, False), ("Sample Defender A", "DF", 4, True),
            ("Sample Defender B", "DF", 5, False), ("Sample Midfielder A", "MF", 8, False),
            ("Sample Midfielder B", "MF", 10, False), ("Sample Forward A", "FW", 9, False),
            ("Sample Forward B", "FW", 11, False),
        ]
        for name, pos, num, cap in players:
            Player.objects.create(name=name, position=pos, jersey_number=num, is_captain=cap,
                                  bio="Sample entry - edit or delete in the admin panel.")
        Match.objects.create(opponent="Sample FC", date=now + timedelta(days=6), venue="Home Ground",
                             competition="Friendly", is_home=True)
        Match.objects.create(opponent="Demo United", date=now + timedelta(days=13), venue="City Stadium",
                             competition="League", is_home=False)
        Match.objects.create(opponent="Test Town", date=now - timedelta(days=7), venue="Home Ground",
                             competition="Friendly", is_home=True, our_score=3, opponent_score=1)
        Match.objects.create(opponent="Preview Rangers", date=now - timedelta(days=14), venue="Away",
                             competition="League", is_home=False, our_score=1, opponent_score=1)
        Announcement.objects.create(title="Welcome to the new RFC website",
                                    body="Fixtures, results, squad and club news now live in one place. "
                                         "Register to join the community and chat with our assistant.")
        Announcement.objects.create(title="Trials open soon",
                                    body="Interested in playing for Ramos Football Club? Send us a message "
                                         "from the Contact page.")
        self.stdout.write(self.style.SUCCESS("Sample data added."))
