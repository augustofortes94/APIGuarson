from django.urls import path
from .views import WeaponView

urlpatterns=[
    path('weapons/', WeaponView.as_view(), name='weapons_list')
]