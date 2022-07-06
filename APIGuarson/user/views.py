import jwt
import datetime
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class ApiLogin(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = User.objects.filter(username=username).first()
        if user is None:
            return Response({'message': "Error: user not found..."}, status=status.HTTP_404_NOT_FOUND)

        else:
            if not user.check_password(password):
                return Response({'message': "incorrect password..."}, status=status.HTTP_401_UNAUTHORIZED)

            payload = {
                    'id': user.id,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                    'iat': datetime.datetime.utcnow()
                    }
            token = jwt.encode(payload, 'secret', algorithm='HS256')

            response = Response()
            response.set_cookie(key='jwt', value=token, httponly=True)
            response.data = {'message': "Succes"}
            return response


class RegisterUser(CreateView):
    def register(request):
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Account created for {username}, please Login')
                return redirect('/weapon/list')
        else:
            form = UserRegisterForm()
        return render(request, 'registration/register.html', {'form': form})

    @login_required
    @user_passes_test(lambda u: u.is_superuser)
    def userEdit(request, id):
        user = User.objects.get(id=id)
        if len(request.POST) == 2:
            user.is_staff = False
        else:
            user.is_staff = True
        user.save()
        return redirect('/user/list')

    @login_required
    @user_passes_test(lambda u: u.is_superuser)
    def userList(request):
        users = list(User.objects.all().order_by('username'))
        return render(request, 'registration/user_list.html', {"users": users})

    @login_required
    @user_passes_test(lambda u: u.is_superuser)
    def userDelete(request, id):
        user = User.objects.get(id=id)
        if user.is_superuser:
            messages.warning(request, 'No es posible eliminar al superusuario')
        else:
            User.objects.filter(id=id).delete()
        return redirect('/user/list')
