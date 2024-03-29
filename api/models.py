from django.db import models
from django.db.models.functions import Cast, Concat
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Command(models.Model):
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    text = models.CharField(max_length=500, null=True, blank=True, default=None)
    parameter1 = models.CharField(max_length=50, null=True, blank=True, default=None)
    parameter2 = models.CharField(max_length=50, null=True, blank=True, default=None)
    warzone_version = models.CharField(max_length=2, null=True, blank=True, default=None)
    identity_name_version = models.CharField(max_length=100, blank=True, null=True, unique=True)
    updated_on = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.updated_on = timezone.now()
        if self.warzone_version is None:
            self.identity_name_version = self.name + '_None'
        else:
            self.identity_name_version = self.name + '_' + self.warzone_version
        return super(Command, self).save(*args, **kwargs)

@receiver(pre_save, sender=Command)
def update_identity_name_version(sender, instance, **kwargs):
    if not instance.identity_name_version:
        # If the identity has not been set, create it from name and version
        instance.identity_name_version = f"{instance.name}_{instance.warzone_version}"


class WeaponW1(models.Model):
    command = models.ForeignKey(Command, on_delete=models.CASCADE, related_name="commands_w1")
    category = models.CharField(max_length=50)
    name = models.CharField(max_length=50, unique=True)
    muzzle = models.CharField(max_length=100, null=True, blank=True, default=None)
    barrel = models.CharField(max_length=100, null=True, blank=True, default=None)
    laser = models.CharField(max_length=100, null=True, blank=True, default=None)
    optic = models.CharField(max_length=100, null=True, blank=True, default=None)
    stock = models.CharField(max_length=100, null=True, blank=True, default=None)
    underbarrel = models.CharField(max_length=100, null=True, blank=True, default=None)
    magazine = models.CharField(max_length=100, null=True, blank=True, default=None)
    ammunition = models.CharField(max_length=100, null=True, blank=True, default=None)
    reargrip = models.CharField(max_length=100, null=True, blank=True, default=None)
    perk = models.CharField(max_length=100, null=True, blank=True, default=None)
    perk2 = models.CharField(max_length=100, null=True, blank=True, default=None)
    alternative = models.CharField(max_length=512, null=True, blank=True, default=None)
    alternative2 = models.CharField(max_length=512, null=True, blank=True, default=None)
    updated_on = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.updated_on = timezone.now()
        return super(WeaponW1, self).save(*args, **kwargs)


class WeaponW2(models.Model):
    command = models.ForeignKey(Command, on_delete=models.CASCADE, related_name="commands_w2")
    category = models.CharField(max_length=50)
    name = models.CharField(max_length=50, unique=True)
    muzzle = models.CharField(max_length=100, null=True, blank=True, default=None)
    barrel = models.CharField(max_length=100, null=True, blank=True, default=None)
    laser = models.CharField(max_length=100, null=True, blank=True, default=None)
    optic = models.CharField(max_length=100, null=True, blank=True, default=None)
    stock = models.CharField(max_length=100, null=True, blank=True, default=None)
    underbarrel = models.CharField(max_length=100, null=True, blank=True, default=None)
    magazine = models.CharField(max_length=100, null=True, blank=True, default=None)
    ammunition = models.CharField(max_length=100, null=True, blank=True, default=None)
    reargrip = models.CharField(max_length=100, null=True, blank=True, default=None)
    guard = models.CharField(max_length=100, null=True, blank=True, default=None)
    comb = models.CharField(max_length=100, null=True, blank=True, default=None)
    receiver = models.CharField(max_length=100, null=True, blank=True, default=None)
    alternative = models.CharField(max_length=512, null=True, blank=True, default=None)
    alternative2 = models.CharField(max_length=512, null=True, blank=True, default=None)
    updated_on = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.updated_on = timezone.now()
        return super(WeaponW2, self).save(*args, **kwargs)


class Lobby(models.Model):
    mode = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50, unique=True)
    map = models.CharField(max_length=50, null=True, blank=True, default=None)
    updated_on = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.updated_on = timezone.now()
        return super(Lobby, self).save(*args, **kwargs)
