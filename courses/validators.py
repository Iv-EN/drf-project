import re

from rest_framework.exceptions import ValidationError


class VideoLinkValidator:
    """Валидация ссылки на видео."""

    video_link_pattern = re.compile(
        r"^(?:https?:\/\/)?"
        r"(?:www\.)?"
        r"(?:youtube\.com\/(?:embed\/|v\/|watch\?v=|.*[?&]v=))"
        r"([\w-]{11})"
    )

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if value is None:
            return
        if not isinstance(value, str) or not self.video_link_pattern.match(
            value
        ):
            raise ValidationError(
                f"{self.field} ссылка разрешена только на видео YouTube."
            )
        return value
