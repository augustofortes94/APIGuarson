from django.urls import path
from .views import WeaponView

urlpatterns=[
    path('weapons/', WeaponView.as_view(), name='weapons_list'),
    path('weapons/<int:id>', WeaponView.as_view(), name='weapon_get_id'),
    path('weapons/<str:command>', WeaponView.as_view(), name='weapon_get_command'),
]