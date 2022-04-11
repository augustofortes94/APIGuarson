from django.urls import path
from .views import WeaponView
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('login/', auth_views.LoginView.as_view(template_name='login/login.html'), name='login'),
    path('weapons/', WeaponView.as_view(), name='weapons_list'),
    path('weapons/<int:id>', WeaponView.as_view(), name='weapon_get_id'),
    path('weapons/<str:command>', WeaponView.as_view(), name='weapon_get_command'),
]