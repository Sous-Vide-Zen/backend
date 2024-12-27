from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from django.db import transaction
from mozilla_django_oidc.auth import OIDCAuthenticationBackend


User = get_user_model()


class CustomOIDCAuthenticationBackend(OIDCAuthenticationBackend):
    """
    Аутентификация, через OIDC + создание и обновление пользователя в БД.
    В claims получаем данные пользователя из keycloak token и сверяем с данными в БД.
    """

    def get_username(self, claims):
        email = claims.get("email")
        if not email:
            raise AuthenticationFailed("Email is required")
        return email

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
        email = self.get_username(claims)
        if user.email != email:
            user.email = email
            user.save(update_fields=["email"])

        return user
