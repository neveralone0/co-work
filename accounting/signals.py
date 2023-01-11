from django.db.models.signals import post_save
from django.dispatch import receiver
from accounting.models import InternProxy, InternProfile
from helpers.helpers import INTERN


@receiver(post_save, sender=InternProxy)
def create_intern_profile(sender, instance, created, **kwargs):
    if created:
        InternProfile.objects.create(user=instance)
