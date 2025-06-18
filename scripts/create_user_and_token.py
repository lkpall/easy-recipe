import os
import sys

import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model  # noqa: E402

User = get_user_model()

username = "testuser"
password = "testpassword"

user = User.objects.filter(username=username).first()

if not user:
    user = User.objects.create_user(
        username=username, email="test@email.com", password=password
    )
