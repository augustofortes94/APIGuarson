from .models import Command, Lobby, Weapon_w1
from rest_framework import serializers


class CommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Command
        fields = ['name', 'category', 'text', 'parameter1', 'parameter2']


class CommandSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Command
        fields = ('command')


class LobbySerializer(serializers.ModelSerializer):
    map = serializers.CharField(required=False)

    class Meta:
        model = Lobby
        fields = ['id', 'mode', 'name', 'map']


class WeaponSerializer(serializers.ModelSerializer):
    command = serializers.CharField(source='command.name', read_only=True)

    class Meta:
        model = Weapon_w1
        fields = ['id', 'name', 'command', 'category', 'muzzle', 'barrel', 'laser', 'optic', 'stock', 'underbarrel', 'magazine', 'ammunition', 'reargrip', 'perk', 'perk2', 'alternative', 'alternative2']
