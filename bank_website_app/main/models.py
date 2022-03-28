from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django.dispatch import receiver
from django.db.models.signals import post_save
from localflavor.generic.models import IBANField
from localflavor.generic.countries.sepa import IBAN_SEPA_COUNTRIES


# Create your models here.


class IBAN(models.Model):
    iban = IBANField(include_countries=IBAN_SEPA_COUNTRIES)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    iban = models.TextField(IBANField, null=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

        @receiver(post_save, sender=User)
        def save_user_profile(sender, instance, **kwargs):
            instance.profile.save()
