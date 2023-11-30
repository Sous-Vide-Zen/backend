from django.db import models


class EmojyChoice(models.TextChoices):
    LIKE = "Like"
    DISLIKE = "Dislike"
    ANGRY_FACE = "Angry_Face"
    HEART = "Heart"
    FIRE = "Fire"
