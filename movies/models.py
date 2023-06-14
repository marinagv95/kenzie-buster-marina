from django.db import models
from django.db import models
from django.utils import timezone
from decimal import Decimal


class RatingChoices(models.TextChoices):
    G = "G"
    PG = "PG"
    PG_13 = "PG-13"
    R = "R"
    NC_17 = "NC-17"


class Movie(models.Model):
    title = models.CharField(max_length=127)
    duration = models.CharField(max_length=10, null=True, default=None)
    rating = models.CharField(
        max_length=20,
        choices=RatingChoices.choices,
        default=RatingChoices.G,
        null=True,
    )
    synopsis = models.TextField(
        default=None,
        null=True,
    )

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="movies"
    )

