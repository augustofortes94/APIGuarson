from dataclasses import fields
from .models import Weapon, Lobby, Command
from rest_framework import serializers


class CommandSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Command
        fields = ('command', 'text')


class WeaponSerializer(serializers.ModelSerializer):
    command_id = CommandSimpleSerializer(many=True, read_only=True)
    
    class Meta:
        model = Weapon
        fields = ['id', 'name', 'command_id', 'category', 'muzzle', 'barrel', 'laser', 'optic', 'stock', 'underbarrel', 'magazine', 'ammunition', 'reargrip', 'perk', 'perk2', 'alternative', 'alternative2']


class WeaponCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Weapon
        fields = ['command']


class LobbySerializer(serializers.ModelSerializer):
    map = serializers.CharField(required=False)

    class Meta:
        model = Lobby
        fields = ['id', 'mode', 'name', 'map']
