from .views import CommandApi, WeaponW1Api
from django.urls import path, include
from . import views
from rest_framework import routers

app_name = 'api'

router = routers.DefaultRouter()
router.register('mode', views.ModeLobbyApi)

urlpatterns = [
    # API
    path('', include(router.urls), name='api_mode_lobby'),  # include api for lobby modes
    path('commands/', CommandApi.as_view(), name='api_commands'),
    path('w1/weapons/', WeaponW1Api.as_view(), name='api_weapon_list'),
    path('w1/weapons/<int:id>', WeaponW1Api.as_view(), name='api_delete_by_id'),
]
