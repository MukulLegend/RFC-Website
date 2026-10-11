from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    contact_no = models.CharField(max_length=15)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class Register(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    contact_no = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.user.username if self.user else "No User"


class Player(models.Model):
    POSITIONS = [
        ("GK", "Goalkeeper"),
        ("DF", "Defender"),
        ("MF", "Midfielder"),
        ("FW", "Forward"),
    ]
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=2, choices=POSITIONS)
    jersey_number = models.PositiveSmallIntegerField(null=True, blank=True)
    is_captain = models.BooleanField(default=False)
    bio = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True, help_text="Untick to hide from the squad page")

    class Meta:
        ordering = ["jersey_number", "name"]

    def __str__(self):
        return f"{self.name} ({self.get_position_display()})"

    @property
    def initials(self):
        return "".join(part[0] for part in self.name.split()[:2]).upper()


class Match(models.Model):
    opponent = models.CharField(max_length=100)
    date = models.DateTimeField()
    venue = models.CharField(max_length=150, blank=True)
    competition = models.CharField(max_length=100, blank=True, help_text="e.g. Friendly, League, Cup")
    is_home = models.BooleanField(default=True)
    our_score = models.PositiveSmallIntegerField(null=True, blank=True)
    opponent_score = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        ordering = ["date"]
        verbose_name_plural = "matches"

    def __str__(self):
        return f"RFC vs {self.opponent} - {self.date:%d %b %Y}"

    @property
    def is_played(self):
        return self.our_score is not None and self.opponent_score is not None

    @property
    def result(self):
        if not self.is_played:
            return ""
        if self.our_score > self.opponent_score:
            return "W"
        if self.our_score < self.opponent_score:
            return "L"
        return "D"


class Announcement(models.Model):
    title = models.CharField(max_length=150)
    body = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
