import os

import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "podcast.settings")
django.setup()

from cli import app  # noqa # type: ignore


app()
