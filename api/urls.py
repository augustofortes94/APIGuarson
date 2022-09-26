from .views import CommandApi, CommandView, ModeLobbyView, WeaponApi, WeaponView
from django.urls import path, include
from . import views
from rest_framework import routers
#from user.views import ApiLogin

app_name = 'api'

router = routers.DefaultRouter()
router.register('mode', views.ModeLobbyApi)

urlpatterns = [
    path('', WeaponView.weaponList, name='weapons_list'),

    # API
    path('api/', include(router.urls), name='api_mode_lobby'),  # include api for lobby modes
    path('api/commands/', CommandApi.as_view(), name='api_commands'),
    #path('api/login/', ApiLogin.as_view(), name='api_login'),
    path('api/weapons/', WeaponApi.as_view(), name='api_weapon_list'),
    path('api/weapons/<int:id>', WeaponApi.as_view(), name='api_delete_by_id'),

    # COMMANDS
    path('command/list/', CommandView.commandList, name='commands_list'),
    path('command/addform', CommandView.commandAddForm, name='commands_addform'),
    path('command/add', CommandView.commandAdd, name='commands_add'),
    path('command/delete/<int:id>', CommandView.commandDelete, name='command_delete_by_id'),
    path('command/edit/<int:id>', CommandView.commandEdit, name='commands_edit'),
    path('command/edition/<int:id>', CommandView.commandEdition, name='commands_edition'),

    # MODE MAPS
    path('mode/list/', ModeLobbyView.modesList, name='map_modes_list'),
    path('mode/add', ModeLobbyView.modeAdd, name='mode_add'),
    path('mode/addform', ModeLobbyView.modeAddForm, name='mode_addform'),
    path('mode/delete/<int:id>', ModeLobbyView.modeDelete, name='mode_delete_by_id'),

    # WEAPONS
    path('weapon/list', WeaponView.weaponList, name='weapons_list'),
    path('weapon/add', WeaponView.weaponAdd, name='weapon_add'),
    path('weapon/addform', WeaponView.weaponAddForm, name='weapon_addform'),
    path('weapon/delete/<int:id>', WeaponView.weaponDelete, name='weapon_delete_by_id'),
    path('weapon/edition/<int:id>', WeaponView.weaponEdition, name='weapon_editition'),
    path('weapon/edit/<str:command>', WeaponView.weaponEdit, name='weapon_edit'),
    path('weapon/<str:command>', WeaponView.weaponDetail, name='weapon_by_command'),
]
