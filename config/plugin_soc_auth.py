from social_core.backends.vk import VKOAuth2

class CustomVKOAuth2(VKOAuth2):
    def get_user_details(self, response):
        details = super().get_user_details(response)
        details['username'] = None  # Устанавливаем username в None, чтобы избежать попыток создания пользователя с пустым username
        return details