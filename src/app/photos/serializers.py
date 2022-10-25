from rest_framework import serializers

from photos.models import Photo

from photos.services import get_size, get_dominant_color


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

    def create(self, validated_data):
        photo_size = get_size(validated_data["URL"])
        validated_data['width'], validated_data['height'] = photo_size
        validated_data['color'] = get_dominant_color(validated_data["URL"])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        photo_size = get_size(validated_data["URL"])
        instance.width, instance.height = photo_size
        instance.color = get_dominant_color(validated_data["URL"])

        instance = super().update(instance, validated_data)
        return instance
