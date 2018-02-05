from django.contrib.auth.models import User # For authentication

class Backend:
    def authenticate(self, request, username=None, password=None):
        # Check the username/password and return a user.
        try:
            user = User.objects.get(username = username)

        except User.DoesNotExist:
            return None

    def get_user(ldap):
        return User.get(username = ldp)
