from pyexpat import model
from .models import Weapon, Lobby
from rest_framework import serializers


class WeaponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weapon
        fields = ['id', 'command', 'category', 'name', 'muzzle', 'barrel', 'laser', 'optic', 'stock', 'underbarrel', 'magazine', 'ammunition', 'reargrip', 'perk', 'perk2', 'alternative', 'alternative2']


class LobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Lobby
        fields = ['id', 'mode', 'name', 'map']
