from django.db import models


class EmojyChoice(models.TextChoices):
    LIKE = "\U0001F44D"
    DISLIKE = "\U0001F44E"
    ANGRY_FACE = "\U0001F621"
    HEART = "\u2764"
    FIRE = "\U0001F525"
