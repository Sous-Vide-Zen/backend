from django.conf import settings
from django.db import models


class Follow(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name="Подписчик",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name="Автор",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        ordering = ("-created_at",)
        constraints = [
            models.UniqueConstraint(fields=["user", "author"], name="unique_following"),
            models.CheckConstraint(
                check=~models.Q(user=models.F("author")),
                name="same_follower_constraint",
            ),
        ]

    def __str__(self):
        return f"{self.user} подписан на {self.author}"
