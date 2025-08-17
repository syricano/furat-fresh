from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _


class UserProfile(models.Model):
    """Default delivery info and order history"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("User"))
    first_name = models.CharField(_("First name"), max_length=80, null=True, blank=True)
    last_name = models.CharField(_("Last name"), max_length=80, null=True, blank=True)
    phone_number = models.CharField(_("Phone number"), max_length=20, null=True, blank=True)
    email = models.EmailField(_("Email"), max_length=254, null=True, blank=True)

    postcode = models.CharField(_("Postcode"), max_length=20, null=True, blank=True)
    town_or_city = models.CharField(_("Town or city"), max_length=40, null=True, blank=True)
    street_address1 = models.CharField(_("Street address 1"), max_length=80, null=True, blank=True)
    street_address2 = models.CharField(_("Street address 2"), max_length=80, null=True, blank=True)
    county = models.CharField(_("County"), max_length=80, null=True, blank=True)
    country = CountryField(verbose_name=_("Country"), blank_label=_("Country *"), null=True, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    # Existing users: ensure profile saves on user save
    instance.userprofile.save()
