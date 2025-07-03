# kel5_app/signals.py

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    # Fungsi ini hanya akan membuat Profile jika User baru dibuat
    if created:
        Profile.objects.create(user=instance)

# Fungsi save_profile yang sebelumnya ada di sini, sudah dihapus.