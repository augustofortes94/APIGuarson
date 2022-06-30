from .views import HomeView, WeaponApi, WeaponView
from django.urls import path
from user.views import ApiLogin

app_name = 'api'

urlpatterns = [
    path('', HomeView.homeview, name='home'),

    # API
    path('api/login/', ApiLogin.as_view(), name='api_login'),
    path('api/weapons/', WeaponApi.as_view(), name='api_list'),
    path('api/weapons/<int:id>', WeaponApi.as_view(), name='api_get_by_id'),
    path('api/weapons/<str:command>', WeaponApi.as_view(), name='api_get_by_command'),

    # WEAPONS
    path('weapon/list', WeaponView.weaponList, name='weapons_list'),
    path('weapon/add', WeaponView.weaponAdd, name='weapon_add'),
    path('weapon/addform', WeaponView.weaponAddForm, name='weapon_addform'),
    path('weapon/delete/<int:id>', WeaponView.weaponDelete, name='weapon_delete_by_id'),
    path('weapon/edition/<int:id>', WeaponView.weaponEdition, name='weapon_editition'),
    path('weapon/edit/<str:command>', WeaponView.weaponEdit, name='weapon_edit'),
    path('weapon/<str:command>', WeaponView.weaponDetail, name='weapon_by_command'),
]
