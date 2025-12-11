import os
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import CustomUser, SeekerProfile, CompanyProfile


# ==========================================
# AUTO CREATE SEEKER & COMPANY PROFILE
# ==========================================
@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == "seeker":
            SeekerProfile.objects.create(user=instance)
        elif instance.role == "company":
            CompanyProfile.objects.create(user=instance)


# ==========================================
# DELETE LOGO FILE WHEN COMPANYPROFILE DELETED
# ==========================================
@receiver(post_delete, sender=CompanyProfile)
def delete_company_logo_on_delete(sender, instance, **kwargs):
    """Menghapus file logo jika profil perusahaan dihapus."""
    if instance.logo:
        if os.path.isfile(instance.logo.path):
            os.remove(instance.logo.path)


# ==========================================
# DELETE OLD LOGO WHEN UPDATING NEW LOGO
# ==========================================
@receiver(pre_save, sender=CompanyProfile)
def delete_old_company_logo_on_update(sender, instance, **kwargs):
    """
    Saat logo perusahaan diganti, hapus file lama
    agar tidak menumpuk di folder media.
    """
    if not instance.pk:
        return  # skip untuk create

    try:
        old_logo = CompanyProfile.objects.get(pk=instance.pk).logo
    except CompanyProfile.DoesNotExist:
        return

    new_logo = instance.logo

    # jika logonya berubah → hapus file lama
    if old_logo and old_logo != new_logo:
        if os.path.isfile(old_logo.path):
            os.remove(old_logo.path)
