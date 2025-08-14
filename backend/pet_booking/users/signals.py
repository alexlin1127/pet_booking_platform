from django_rest_passwordreset.signals import reset_password_token_created
from django.dispatch import receiver
from django.core.mail import send_mail

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    send_mail(
        "密碼重設",
        f"你的密碼重設驗證碼：{reset_password_token.key}",
        None,
        [reset_password_token.user.email]
    )
