from django.db import models
from django.contrib.auth.models import User
# Create your models here.

def create_admins():
    name = 'controlPanel/admin.txt'
    with open(name) as f:
        for username in f.readlines():
            username = username.strip()
            user = None
            try:
                user = User.objects.get(username = username)
            except User.DoesNotExist:
                user = User(username = username, password = "my password")

            user.is_superuser = True
            user.is_staff = True
            user.save()
