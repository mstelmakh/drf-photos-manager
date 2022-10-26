from django.db import models
from django.db.models.query import Q

from photos.services import save_analyzed_photo
from hexfield.fields import HexField


class Photo(models.Model):
    title = models.CharField(max_length=255)
    album_id = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    color = HexField(verbose_name="Dominant color")
    URL = models.CharField(max_length=200)

    @save_analyzed_photo
    def save(self, *args, **kwargs) -> None:
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}. {self.title}"

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="negative_album_id",
                check=Q(album_id__gte=1)
            )
        ]
