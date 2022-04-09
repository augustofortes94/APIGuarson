import json
from unicodedata import name
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from django.views import View
from .models import Weapon

import json

# Create your views here.

class WeaponView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        weapons=list(Weapon.objects.values())
        if len(weapons) > 0:
            return JsonResponse({'message':"Success",'weapons':weapons})
        else:
            return JsonResponse({'message':"Error: weapons not found..."})

    def post(self, request):
        data = json.loads(request.body)

        Weapon.objects.create(name=data['name'],
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
    
    def put(self, request):
        pass
    
    def delete(self, request):
        pass