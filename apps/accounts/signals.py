from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_save, sender=User)
def superuser_email_verified(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        EmailAddress.objects.update_or_create(
            user=instance,
            email=instance.email,
            defaults={'verified': True, 'primary': True}
        )