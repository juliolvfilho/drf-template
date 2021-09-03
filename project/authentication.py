from firebase_admin import auth
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import TokenAuthentication


class FirebaseAuthentication(TokenAuthentication):

    keyword = settings.FIREBASE_AUTH_HEADER_PREFIX

    def authenticate_credentials(self, key):
        # Attempt to verify JWT from Authorization header with Firebase
        # and return the decoded token
        try:
            token = auth.verify_id_token(key)
        except:  # noqa: E722
            raise AuthenticationFailed()

        return (token, key)
