from .models import Weapon, Lobby, Command
from rest_framework import serializers


class CommandSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Command
        fields = ('command')


class WeaponSerializer(serializers.ModelSerializer):
    command = serializers.CharField(source='command.name', read_only=True)

    class Meta:
        model = Weapon
        fields = ['id', 'name', 'command', 'category', 'muzzle', 'barrel', 'laser', 'optic', 'stock', 'underbarrel', 'magazine', 'ammunition', 'reargrip', 'perk', 'perk2', 'alternative', 'alternative2']


class WeaponCategorySerializer(serializers.ModelSerializer):
    command = serializers.CharField(source='command.name', read_only=True)
    
    class Meta:
        model = Weapon
        fields = ['command']


class CommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Command
        fields = ['name', 'text', 'parameter1', 'parameter2']


class LobbySerializer(serializers.ModelSerializer):
    map = serializers.CharField(required=False)

    class Meta:
        model = Lobby
        fields = ['id', 'mode', 'name', 'map']
