from django.db import models
from hexfield.fields import HexField


class Photo(models.Model):
    title = models.CharField(max_length=255)
    album_id = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    color = HexField(verbose_name="Dominant color")
    URL = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.id}. {self.title}"
