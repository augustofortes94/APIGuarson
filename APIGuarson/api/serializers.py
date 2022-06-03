from dataclasses import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Weapon

class WeaponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weapon
        fields = ['id', 'command', 'category', 'name', 'muzzle', 'barrel', 'laser', 'optic', 'stock', 'underbarrel', 'magazine', 'ammunition', 'reargrip', 'perk', 'perk2', 'alternative', 'alternative2']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance