from django.db import models


class Weapon(models.Model):
    command = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
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
