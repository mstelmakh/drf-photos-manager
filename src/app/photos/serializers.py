from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from photos.models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = (
            'id',
            'title',
            'album_id',
            'width',
            'height',
            'color',
            'URL',
        )
        read_only_fields = ('id', 'width', 'height', 'color', )

    def validate_album_id(self, value):
        if value <= 0:
            raise ValidationError("Invalid album ID.")
        return value
