import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Application


@receiver(post_delete, sender=Application)
def delete_cv_file(sender, instance, **kwargs):
    """
    Hapus file CV dari media/cvs ketika Application dihapus
    """
    if instance.cv:
        cv_path = instance.cv.path
        if os.path.isfile(cv_path):
            os.remove(cv_path)
