from django.urls import path
from .views import WeaponView
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('', WeaponView.weaponList),
    path('weapon/list', WeaponView.weaponList),
    path('weapon/add', WeaponView.weaponAdd),
    path('weapon/edit/<str:command>', WeaponView.weaponEdit),
    path('weapon/<str:command>', WeaponView.weaponDetail),
    path('login/', auth_views.LoginView.as_view(template_name='login/login.html'), name='login'),
    path('api/weapons/', WeaponView.as_view(), name='weapons_list'),
    path('api/weapons/<int:id>', WeaponView.as_view(), name='weapon_get_id'),
    path('api/weapons/<str:command>', WeaponView.as_view(), name='weapon_get_command'),
]