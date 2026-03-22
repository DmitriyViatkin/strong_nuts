from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_password_recovery_email(email, reset_url):
    send_mail(
        subject='Відновлення пароля',
        message=f'Для відновлення пароля перейдіть за посиланням:\n{reset_url}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
    return f'Email відправлено на {email}'


@shared_task
def send_registration_email(email, first_name):
    send_mail(
        subject='Ласкаво просимо!',
        message=f'Вітаємо {first_name}!\n\nВи успішно зареєструвались.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
    return f'Вітальний email відправлено на {email}'


@shared_task
def send_order_confirmation_email(email, order_id, total):
    send_mail(
        subject=f'Замовлення #{order_id} підтверджено',
        message=f'Ваше замовлення #{order_id} на суму {total} грн прийнято в обробку.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
    return f'Email про замовлення відправлено на {email}'