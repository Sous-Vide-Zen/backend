from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from django.db import transaction
from django.utils.module_loading import import_string
from mozilla_django_oidc.auth import OIDCAuthenticationBackend


User = get_user_model()


class CustomOIDCAuthenticationBackend(OIDCAuthenticationBackend):
    def get_username(self, claims):
        username_algo = self.get_settings("OIDC_USERNAME_ALGO", None)
        if username_algo:
            if isinstance(username_algo, str):
                username_algo = import_string(username_algo)
            return username_algo(claims.get("email"))
        if not claims.get("email"):
            raise AuthenticationFailed("Email is required")

        return claims.get("email")

    def filter_users_by_claims(self, claims):
        email = self.get_username(claims)
        if not email:
            return self.UserModel.objects.none()
        users = self.UserModel.objects.filter(email__iexact=email)
        return users

    @transaction.atomic
    def create_user(self, claims):
        email = self.get_username(claims)
        user = self.UserModel.objects.create_user(email=email)
        return user

    def update_user(self, user, claims):
        changed = False
        email = self.get_username(claims)
        if user.email != email:
            user.email = email
            changed = True
        if changed:
            user.save()
            user.refresh_from_db()

        return user
