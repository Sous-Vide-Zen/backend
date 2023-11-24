from djoser import email


class CustomActivationEmail(email.ActivationEmail):
    template_name = "activation.html"


class CustomPasswordResetEmail(email.PasswordResetEmail):
    template_name = "password_reset.html"
