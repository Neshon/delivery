from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.template.loader import render_to_string


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created and instance.email:
        body = render_to_string(
            'welcome_email_template.html',
            {
                'name': instance.get_full_name()
            }
        )
        if settings.DEBUG == 1:
            print(body)
        else:
            send_mail('Welcome to Delivery', body,
                      from_email=settings.EMAIL_HOST_USER,
                      recipient_list=[instance.email],
                      fail_silently=False)