from pathlib import Path
from django.conf import settings

# An everyday static path maanger :)
class AppPaths:

    _profile_pics = None

    @classmethod
    def _create_missing_dir(cls, path):
        path.mkdir(parents=True, exist_ok=True) 
        return path

    @classmethod
    def profile_pics(cls) -> Path:
        if cls._profile_pics is None:
            p = Path(settings.MEDIA_ROOT) / 'w'
            cls._profile_pics = cls._create_missing_dir(p)

        return cls._profile_pics

