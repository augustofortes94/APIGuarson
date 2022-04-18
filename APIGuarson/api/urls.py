from xml.etree.ElementInclude import include
from django.urls import path, include
from .views import HomeView, RegisterUser, WeaponView
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('', HomeView.homeview),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/weapons/', WeaponView.as_view(), name='weapons_list'),
    path('api/weapons/<int:id>', WeaponView.as_view(), name='weapon_get_id'),
    path('api/weapons/<str:command>', WeaponView.as_view(), name='weapon_get_command'),
    path('weapon/list', WeaponView.weaponList, name='weapons_list'),
    path('weapon/add', WeaponView.weaponAdd),
    path('weapon/addform', WeaponView.weaponAddForm),
    path('weapon/delete/<int:id>', WeaponView.weaponDelete),
    path('weapon/edition/<int:id>', WeaponView.weaponEdition),
    path('weapon/edit/<str:command>', WeaponView.weaponEdit),
    path('weapon/<str:command>', WeaponView.weaponDetail),
]