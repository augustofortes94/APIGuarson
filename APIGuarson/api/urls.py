from xml.etree.ElementInclude import include
from django.urls import path, include
from .views import ApiLogin, HomeView, RegisterUser, WeaponView
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('', HomeView.homeview),

    #USERS
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', RegisterUser.register, name='register'),
    path('user/list', RegisterUser.userList, name='user_list'),
    path('user/delete/<int:id>', RegisterUser.userDelete, name='user_delete'),

    #API
    path('api/login/', ApiLogin.as_view(), name='api_login'),
    path('api/weapons/', WeaponView.as_view(), name='api_list'),
    path('api/weapons/<int:id>', WeaponView.as_view(), name='api_get_by_id'),
    path('api/weapons/<str:command>', WeaponView.as_view(), name='api_get_by_command'),

    #WEAPONS
    path('weapon/list', WeaponView.weaponList, name='weapons_list'),
    path('weapon/add', WeaponView.weaponAdd, name='weapon_add'),
    path('weapon/addform', WeaponView.weaponAddForm, name='weapon_addform'),
    path('weapon/delete/<int:id>', WeaponView.weaponDelete, name='weapon_delete_by_id'),
    path('weapon/edition/<int:id>', WeaponView.weaponEdition, name='weapon_editition'),
    path('weapon/edit/<str:command>', WeaponView.weaponEdit, name='weapon_edit'),
    path('weapon/<str:command>', WeaponView.weaponDetail, name='weapon_by_command'),
]