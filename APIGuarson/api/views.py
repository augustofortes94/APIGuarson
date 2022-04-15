import json
from unicodedata import name
import django
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from django.views import View
from pymysql import NULL
from .models import Weapon

import json

# Create your views here.

class HomeView(View):
    def homeview():
        pass

class WeaponView(View):

    def weaponAdd(request):
        return render(request, 'crud_weapons/weapon_add.html')

    def weaponDetail(request, command):
        weapon=Weapon.objects.filter(command=command).first()
        return render(request, 'crud_weapons/weapon_detail.html', {"weapon": weapon})

    def weaponEdit(request, command):
        weapon=Weapon.objects.filter(command=command).first()
        return render(request, 'crud_weapons/weapon_edit.html', {"weapon": weapon})

    def weaponList(request):
        weapons=list(Weapon.objects.values())
        return render(request, 'crud_weapons/weapons_list.html', {"weapons": weapons})
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0, command=NULL):
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
                alternative=data['alternative']
            )
            return JsonResponse({'message':"Success"})
    
    def put(self, request, id):
        data = json.loads(request.body)
        weapons=list(Weapon.objects.filter(id=id).values())
        if len(weapons) > 0:
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
            weapon.save()
            return JsonResponse({'message':"Success"})
        else:
            return JsonResponse({'message':"Error: weapon not found..."})
    
    @login_required
    def delete(self, request, id):
        weapons=list(Weapon.objects.filter(id=id).values())
        if len(weapons) > 0:
            Weapon.objects.filter(id=id).delete()
            return JsonResponse({'message':"Success",'weapons':weapons})
        else:
            return JsonResponse({'message':"Error: weapon not found..."})