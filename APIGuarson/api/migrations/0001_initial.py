# Generated by Django 4.0.3 on 2022-04-11 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Weapon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('command', models.CharField(max_length=50)),
                ('category', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('muzzle', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('barrel', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('laser', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('optic', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('stock', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('underbarrel', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('magazine', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('ammunition', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('reargrip', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('perk', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('perk2', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('alternative', models.CharField(blank=True, default=None, max_length=512, null=True)),
            ],
        ),
    ]