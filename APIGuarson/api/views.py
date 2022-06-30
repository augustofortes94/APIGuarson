import json
from .serializers import WeaponSerializer
from .models import Weapon
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from pymysql import NULL
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from user.decorators import api_login_required


class HomeView(View):
    @login_required
    def homeview(request):
        return redirect('/weapon/list')


class WeaponView(ListView):
    @login_required
    @user_passes_test(lambda u: u.is_staff)
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
    @user_passes_test(lambda u: u.is_staff)
    def edit(request, data, id):
        weapon = Weapon.objects.get(id=id)
        weapon.command = data['command']
        weapon.category = data['category']
        weapon.name = data['name']
        weapon.muzzle = data['muzzle']
        weapon.barrel = data['barrel']
        weapon.laser = data['laser']
        weapon.optic = data['optic']
        weapon.stock = data['stock']
        weapon.underbarrel = data['underbarrel']
        weapon.magazine = data['magazine']
        weapon.ammunition = data['ammunition']
        weapon.reargrip = data['reargrip']
        weapon.perk = data['perk']
        weapon.perk2 = data['perk2']
        weapon.alternative = data['alternative']
        weapon.alternative2 = data['alternative2']
        weapon.save()

    @login_required
    @user_passes_test(lambda u: u.is_staff)
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
        if len(list(Weapon.objects.filter(command=data['command']).values())) > 0:
            messages.warning(request, data['command'] + ' ya existe')
        else:
            WeaponView.add(request, data)
            messages.success(request, data['name'] + ' ha sido creada')
        return redirect('/weapon/list')

    @login_required
    @user_passes_test(lambda u: u.is_staff)
    def weaponAddForm(request):
        return render(request, 'crud_weapons/weapon_add.html')

    @login_required
    @user_passes_test(lambda u: u.is_superuser)
    def weaponDelete(request, id):
        weapon = Weapon.objects.get(id=id)
        Weapon.objects.filter(id=id).delete()
        messages.success(request,  weapon.name + ' ha sido eliminada')
        return redirect('/weapon/list')

    def weaponDetail(request, command):
        weapon = Weapon.objects.filter(command=command).first()
        return render(request, 'crud_weapons/weapon_detail.html', {"weapon": weapon})

    @login_required
    @user_passes_test(lambda u: u.is_staff)
    def weaponEdit(request, command):
        weapon = Weapon.objects.filter(command=command).first()
        return render(request, 'crud_weapons/weapon_edit.html', {"weapon": weapon})

    @login_required
    @user_passes_test(lambda u: u.is_staff)
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
        if request.method == "POST":
            weapons = Weapon.objects.filter(name__icontains=request.POST['searched']).order_by('command')
        else:
            weapons = Weapon.objects.all().order_by('command')

        paginator = Paginator(weapons, 12)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'crud_weapons/weapons_list.html', {'page_obj': page_obj})


class WeaponApi(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @api_login_required
    def get(self, request, id=0, command=NULL, *args, **kwargs):
        if id > 0:      # GET BY ID
            weapons = list(Weapon.objects.filter(id=id).values())
        elif command is not NULL:
            weapons = list(Weapon.objects.filter(command=command).values())
        else:           # GET ALL
            weapons = list(Weapon.objects.values())

        if len(weapons) > 0:
            return Response({'message': "Success", 'weapons': weapons}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'message': "Error: weapon not found..."}, status=status.HTTP_404_NOT_FOUND)

    @api_login_required
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        if len(list(Weapon.objects.filter(command=data['command']).values())) > 0:
            return Response({'message': "Error: this weapon already exist"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            weapon = Weapon.objects.create(
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
            serializer = WeaponSerializer(data=vars(weapon))
            serializer.is_valid(raise_exception=True)
            return Response({'message': "Success", 'weapons': serializer.data}, status=status.HTTP_201_CREATED)

    @api_login_required
    def put(self, request, *args, **kwargs):
        data = json.loads(request.body)
        weapons = list(Weapon.objects.filter(command=data['command']).values())
        if len(weapons) > 0:
            weapon = Weapon.objects.get(command=data['command'])
            weapon.command = data['command']
            weapon.category = data['category']
            weapon.name = data['name']
            weapon.muzzle = data['muzzle']
            weapon.barrel = data['barrel']
            weapon.laser = data['laser']
            weapon.optic = data['optic']
            weapon.stock = data['stock']
            weapon.underbarrel = data['underbarrel']
            weapon.magazine = data['magazine']
            weapon.ammunition = data['ammunition']
            weapon.reargrip = data['reargrip']
            weapon.perk = data['perk']
            weapon.perk2 = data['perk2']
            weapon.alternative = data['alternative']
            weapon.alternative2 = data['alternative2']
            weapon.save()
            serializer = WeaponSerializer(data=vars(weapon))
            serializer.is_valid(raise_exception=True)
            return Response({'message': "Success", 'weapons': serializer.data}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'message': "Error: weapon not found..."}, status=status.HTTP_404_NOT_FOUND)

    @api_login_required
    def delete(self, request, id, *args, **kwargs):
        weapons = list(Weapon.objects.filter(id=id).values())
        if len(weapons) > 0:
            Weapon.objects.filter(id=id).delete()
            return Response({'message': "Success", 'weapons': weapons}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'message': "Error: weapon not found..."}, status=status.HTTP_404_NOT_FOUND)
