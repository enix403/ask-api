from django.db import DataError

# Robust filter and exist implementations. Ensures that queryset.exists() for
# an invalid value returns `False`, rather than raising an error.

def qs_exists(queryset):
    try:
        return queryset.exists()
    except (TypeError, ValueError, DataError):
        return False


def qs_filter(queryset, **kwargs):
    try:
        return queryset.filter(**kwargs)
    except (TypeError, ValueError, DataError):
        return queryset.none()
