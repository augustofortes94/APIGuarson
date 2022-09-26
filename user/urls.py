from django.urls import path, include
from .views import RegisterUser

app_name = 'user'

urlpatterns = [
    # USERS
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', RegisterUser.register, name='register'),
    path('edit/<int:id>', RegisterUser.userEdit, name='user_edit'),
    path('list', RegisterUser.userList, name='user_list'),
    path('delete/<int:id>', RegisterUser.userDelete, name='user_delete'),
]
