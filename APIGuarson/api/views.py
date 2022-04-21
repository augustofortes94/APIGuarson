import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from django.views import View
from pymysql import NULL
from .models import Weapon
from .forms import UserRegisterForm
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
import jwt, datetime

import json

# Create your views here.

class ApiLogin(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = User.objects.filter(username=username).first()
        if user is None:
            return JsonResponse({'message':"Error: user not found..."})

        else:
            if not user.check_password(password):
                return JsonResponse({'message':"Error: incorrect password..."})
            
            payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
            }
            token = jwt.encode(payload, 'secret', algorithm='HS256')

            response = Response()
            response.set_cookie(key='jwt', value=token, httponly=True)
            response.data = {'jwt': token}
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
        return render(request, 'registration/register.html', {'form':form})

    @login_required
    def userList(request):
        if request.user.is_superuser == True:
            users=list(User.objects.values())
            return render(request, 'registration/user_list.html', {"users":users})
        else:
            messages.warning(request, 'Solo el superusuario puede acceder a esta vista')
            return redirect('/weapon/list')

    @login_required
    def userDelete(request, id):
        user=User.objects.get(id=id)
        if user.is_superuser == True:
            messages.warning(request, 'No es posible eliminar al superusuario')
        else:
            User.objects.filter(id=id).delete()
        return redirect('/user/list')

class HomeView(View):
    @login_required
    def homeview(request):
        return redirect('/weapon/list')

class WeaponView(View):
    @login_required
    def add(request, data):
        Weapon.objects.create(
            command=data['command'],
            category=data['category'],
            name=data['name'],
            muzzle=data['muzzle'],
            barrel=data['barrel'],
            laser=data['laser'],
            optic=data['optic'],
            stock=data['stock'],
            underbarrel=data['underbarrel'],
            magazine=data['magazine'],
            ammunition=data['ammunition'],
            reargrip=data['reargrip'],
            perk=data['perk'],
            perk2=data['perk2'],
            alternative=data['alternative'],
            alternative2=data['alternative2']
        )
    
    @login_required
    def edit(request, data, id):
        weapon=Weapon.objects.get(id=id)
        weapon.command= data['command']
        weapon.category=data['category']
        weapon.name= data['name']
        weapon.muzzle= data['muzzle']
        weapon.barrel= data['barrel']
        weapon.laser= data['laser']
        weapon.optic= data['optic']
        weapon.stock= data['stock']
        weapon.underbarrel= data['underbarrel']
        weapon.magazine= data['magazine']
        weapon.ammunition= data['ammunition']
        weapon.reargrip= data['reargrip']
        weapon.perk= data['perk']
        weapon.perk2= data['perk2']
        weapon.alternative= data['alternative']
        weapon.alternative2= data['alternative2']
        weapon.save()

    @login_required
    def weaponAdd(request):
        data = {}
        for key in request.POST:
            if key == 'csrfmiddlewaretoken':
                pass
            elif request.POST[key] == 'None' or request.POST[key] == "":
                data[key] = None
            else:
                data[key] = request.POST[key]
        data = json.loads(json.dumps(data))
        print(request.POST)
        WeaponView.add(request, data)
        messages.success(request, data['name'] + ' ha sido creada')
        return redirect('/weapon/list')

    @login_required
    def weaponAddForm(request):
        return render(request, 'crud_weapons/weapon_add.html')

    @login_required
    def weaponDelete(request, id):
        if request.user.is_superuser == True:
            weapon=Weapon.objects.get(id=id)
            Weapon.objects.filter(id=id).delete()
            messages.success(request,  weapon.name + ' ha sido eliminada')
        else:
            messages.warning(request,  'Solo el superusuario puede eliminar')
        return redirect('/weapon/list')

    def weaponDetail(request, command):
        weapon=Weapon.objects.filter(command=command).first()
        return render(request, 'crud_weapons/weapon_detail.html', {"weapon": weapon})

    @login_required
    def weaponEdit(request, command):
        weapon=Weapon.objects.filter(command=command).first()
        return render(request, 'crud_weapons/weapon_edit.html', {"weapon": weapon})

    @login_required
    def weaponEdition(request, id):
        data = {}
        for key in request.POST:
            if key == 'csrfmiddlewaretoken':
                pass
            elif request.POST[key] == 'None' or request.POST[key] == "":
                data[key] = None
            else:
                data[key] = request.POST[key]
        data = json.loads(json.dumps(data))
        WeaponView.edit(request, data, id)
        messages.success(request, data['name'] + ' ha sido modificada')
        return redirect('/weapon/list')

    def weaponList(request):
        weapons=list(Weapon.objects.values())
        return render(request, 'crud_weapons/weapons_list.html', {"weapons": weapons})

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def userVerifier(request):
        token = request.COOKIES.get('jwt')
        if token == None:
            return False
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])     #if the token can be decoded, it is a valid token
        except Exception: #jwt.ExpiredSignatureError:
            return False    #if the token is expired or something else, refuse

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def get(self, request, id=0, command=NULL):
        if not WeaponView.userVerifier(request):
            return JsonResponse({'message':"Error: Unauthenticated..."})
        else:
            if id > 0:      ##GET BY ID
                weapons=list(Weapon.objects.filter(id=id).values())
            elif command is not NULL:
                weapons=list(Weapon.objects.filter(command=command).values())
            else:           ##GET ALL
                weapons=list(Weapon.objects.values())

            if len(weapons) > 0:
                return JsonResponse({'message':"Success",'weapons':weapons})
            else:
                return JsonResponse({'message':"Error: weapon not found..."})

    def post(self, request):
        data = json.loads(request.body)
        if len(list(Weapon.objects.filter(command=data['command']).values())) > 0:
            return JsonResponse({'message':"Error: this weapon already exist"})
        else:
            WeaponView.add(request, data)
            return JsonResponse({'message':"Success"})
    
    def put(self, request, id):
        data = json.loads(request.body)
        weapons=list(Weapon.objects.filter(id=id).values())
        if len(weapons) > 0:
            WeaponView.edit(request, data, id)
            return JsonResponse({'message':"Success"})
        else:
            return JsonResponse({'message':"Error: weapon not found..."})
    
    def delete(request, self, id):
        weapons=list(Weapon.objects.filter(id=id).values())
        if len(weapons) > 0:
            Weapon.objects.filter(id=id).delete()
            return JsonResponse({'message':"Success",'weapons':weapons})
        else:
            return JsonResponse({'message':"Error: weapon not found..."})