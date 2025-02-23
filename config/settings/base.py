import os
from pathlib import Path

import environ
from split_settings.tools import include

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "account.User"


env = environ.Env(DEFAULT=(bool, False))
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


include(
    "components/apps.py",
    "components/db.py",
    "components/i18n.py",
    "components/media.py",
    "components/security.py",
    "third_party/*.py",
)
