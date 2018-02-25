from django.contrib.auth.models import User # For authentication
from ldap3 import Server, Connection, ALL

class Backend:
    def authenticate(self, request, username=None, password=None):
        # Check the username/password and return a user.
        try:
            print("hello {}".format(username))
            user = User.objects.get(username = username)
            print("Connected")

            if password == "tdlog":
                return user
            else:
                return None

        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(id = user_id)
        except User.DoesNotExist:
            return None
