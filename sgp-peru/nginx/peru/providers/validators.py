from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class SizeValidator:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def __call__(self, value):
        error = False
        if self.width is not None and value.width != self.width:
            error = True
        if self.height is not None and value.height != self.height:
            error = True
        if error:
            raise ValidationError(
                [f'El tamaño de la imagen debe ser de: {self.width} x {self.height} pixeles.']
            )
