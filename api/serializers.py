from .models import Command, Lobby, WeaponW1, WeaponW2
from rest_framework import serializers


class CommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Command
        fields = ['name', 'category', 'text', 'parameter1', 'parameter2', 'warzone_version']


class CommandSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Command
        fields = ('command')


class LobbySerializer(serializers.ModelSerializer):
    map = serializers.CharField(required=False)

    class Meta:
        model = Lobby
        fields = ['id', 'mode', 'name', 'map']


class WeaponW1Serializer(serializers.ModelSerializer):
    command = serializers.CharField(source='command.name', read_only=True)
    warzone = serializers.CharField(source='command.warzone_version', read_only=True)

    class Meta:
        model = WeaponW1
        fields = ['id', 'warzone', 'name', 'command', 'category', 'muzzle', 'barrel', 'laser', 'optic', 'stock', 'underbarrel', 'magazine', 'ammunition', 'reargrip', 'perk', 'perk2', 'alternative', 'alternative2']


class WeaponW2Serializer(serializers.ModelSerializer):
    command = serializers.CharField(source='command.name', read_only=True)
    warzone = serializers.CharField(source='command.warzone_version', read_only=True)

    class Meta:
        model = WeaponW2
        fields = ['id', 'warzone', 'name', 'command', 'category', 'muzzle', 'barrel', 'laser', 'optic', 'stock', 'underbarrel', 'magazine', 'ammunition', 'reargrip', 'guard', 'comb', 'receiver', 'alternative', 'alternative2']
