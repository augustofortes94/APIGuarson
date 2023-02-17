from .views import CommandApi, WeaponApi
from django.urls import path, include
from . import views
from rest_framework import routers
#from user.views import ApiLogin

app_name = 'api'

router = routers.DefaultRouter()
router.register('mode', views.ModeLobbyApi)

urlpatterns = [
    # API
    path('', include(router.urls), name='api_mode_lobby'),  # include api for lobby modes
    path('commands/', CommandApi.as_view(), name='api_commands'),
    #path('login/', ApiLogin.as_view(), name='api_login'),
    path('weapons/', WeaponApi.as_view(), name='api_weapon_list'),
    path('weapons/<int:id>', WeaponApi.as_view(), name='api_delete_by_id'),
]
