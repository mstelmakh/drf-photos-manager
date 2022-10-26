from hexfield.validators import color_hex_validator
from django.db import models


class HexField(models.CharField):

    default_validators = []

    def __init__(self, *args, **kwargs):
        self.default_validators = [color_hex_validator]
        kwargs.setdefault("max_length", 18)
        super().__init__(*args, **kwargs)
