import uuid

from django.db import models


class Podcast(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False,
        null=False,
        unique=True,
        db_index=True,
    )
    title = models.CharField(max_length=500)
    subtitle = models.CharField(max_length=500, blank=True)
    hosted_by = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    image = models.ImageField(upload_to="podcasts/", blank=True)
    # list of links with name and url (spotify, apple music, etc)
    links = models.JSONField(blank=True, default=list)

    def __str__(self):
        return self.title


class Episode(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False,
        null=False,
        unique=True,
        db_index=True,
    )
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    notes = models.TextField(blank=True)
    total_time = models.PositiveSmallIntegerField(default=0)
    audio = models.FileField(upload_to="episodes/", blank=True)
    image = models.ImageField(upload_to="episodes/", blank=True)
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.podcast.title} - {self.title}"
