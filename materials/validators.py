from rest_framework.serializers import ValidationError
import re

forbidden_words = []


def validate_url(value):
    """Валидатор проверяющий поле ссылки на видео."""

    print(value)
    if value:
        reg = re.compile("^(https?://)?(www\.)?youtube\.com/.+$")
        if not bool(reg.match(value)):
            raise ValidationError(
                "Использована запрещённая ссылка. Разрешены только ссылки на youtube.com."
            )
