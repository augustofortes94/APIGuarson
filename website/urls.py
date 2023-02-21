from .views import CommandView, HomeView, ModeLobbyView, WeaponW1View, WeaponW2View
from django.urls import path

app_name = 'api'

urlpatterns = [
    path('', HomeView.home_view, name='home_view'),
    path('home/', HomeView.home_view, name='home_view'),

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
    path('w1/', WeaponW1View.weaponList, name='weapons_w1_list'),
    path('w1/weapon/list', WeaponW1View.weaponList, name='weapons_w1_list'),
    path('w1/weapon/add', WeaponW1View.weaponAdd, name='weapon_w1_add'),
    path('w1/weapon/addform', WeaponW1View.weaponAddForm, name='weapon_w1_addform'),
    path('w1/weapon/delete/<int:id>', WeaponW1View.weaponDelete, name='weapon_w1_delete_by_id'),
    path('w1/weapon/edition/<int:id>', WeaponW1View.weaponEdition, name='weapon_w1_editition'),
    path('w1/weapon/edit/<str:command>', WeaponW1View.weaponEdit, name='weapon_w1_edit'),
    path('w1/weapon/<str:command>', WeaponW1View.weaponDetail, name='weapon_w1_by_command'),

    path('w2/', WeaponW2View.weaponList, name='weapons_w2_list'),
    path('w2/weapon/list', WeaponW2View.weaponList, name='weapons_w2_list'),
    path('w2/weapon/add', WeaponW2View.weaponAdd, name='weapon_w2_add'),
    path('w2/weapon/addform', WeaponW2View.weaponAddForm, name='weapon_w2_addform'),
    path('w2/weapon/delete/<int:id>', WeaponW2View.weaponDelete, name='weapon_w2_delete_by_id'),
    path('w2/weapon/edition/<int:id>', WeaponW2View.weaponEdition, name='weapon_w2_editition'),
    path('w2/weapon/edit/<str:command>', WeaponW2View.weaponEdit, name='weapon_w2_edit'),
    path('w2/weapon/<str:command>', WeaponW2View.weaponDetail, name='weapon_w2_by_command'),
]
