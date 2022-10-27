from django.db import models
from django.db.models.query import Q

from photos.services import save_analyzed_photo
from hexfield.fields import HexField


class Photo(models.Model):
    """Model used to store photo state."""
    title = models.CharField(max_length=255)

    # Since we don't have album model
    # this is just a placeholder for album_id
    album_id = models.IntegerField()

    width = models.IntegerField()
    height = models.IntegerField()
    color = HexField(verbose_name="Dominant color")

    # Not sure about the type of the field.
    # Task says we should store photo's url.
    # I assume it means that we don't need to store the image itself.
    # Otherwise we could use ImageField and store image as a media file.
    URL = models.CharField(max_length=200)

    @save_analyzed_photo
    def save(self, *args, **kwargs) -> None:
        # I used decorator to change the model's fields
        # like width, height and color on every photo create/update,
        # so that I dont need to override serializer create()
        # and update() methods independently.
        # Plus, serializer's create/update methods doesn't effect objects
        # added through django shell or admin panel.
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}. {self.title}"

    class Meta:
        # Since album_id is an IntegerField
        # we need to make sure it can't be a negative number.
        constraints = [
            models.CheckConstraint(
                name="negative_album_id",
                check=Q(album_id__gte=1)
            )
        ]
