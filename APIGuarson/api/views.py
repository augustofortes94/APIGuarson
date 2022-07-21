import json
from .serializers import LobbySerializer, WeaponCategorySerializer, WeaponSerializer
from .models import Lobby, Weapon
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from user.decorators import api_login_required


class ModeLobbyApi(viewsets.ModelViewSet):
    queryset = Lobby.objects.all()
    serializer_class = LobbySerializer
    lookup_field = 'mode'   # Search by mode and not for id

    @api_login_required
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @api_login_required
    def retrieve(self, request, *args, **kwargs):
        try:
            mode = Lobby.objects.filter(mode=self.get_object().mode).values()
            return Response({'message': "Success", 'mode': mode}, status=status.HTTP_202_ACCEPTED)
        except:
            return Response({'message': "Error: mode not found"}, status=status.HTTP_404_NOT_FOUND)

    @api_login_required
    def create(self, request, *args, **kwargs):
        error = {}
        for modes in request.data:
            try:
                Lobby.objects.create(
                    mode=modes['mode'],
                    name=modes['name'],
                    map=modes['map']
                )
            except:
                error[modes['mode']] = 'Error: not added'
        return Response({'message': "Success", 'modes not added': error}, status=status.HTTP_200_OK)

    @api_login_required
    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    @api_login_required
    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ModeLobbyView(ListView):
    @login_required
    @user_passes_test(lambda u: u.is_superuser)
    def modesList(request):
        modes = Lobby.objects.all().order_by('name')
        paginator = Paginator(modes, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'crud_modes/modes_list.html', {'page_obj': page_obj})
    
    @login_required
    @user_passes_test(lambda u: u.is_superuser)
    def modeAddForm(request):
        return render(request, 'crud_modes/modes_add.html')

    @login_required
    @user_passes_test(lambda u: u.is_superuser)
    def modeAdd(request):
        print(request.POST)
        print(type(request))
        try:
            Lobby.objects.get(mode=request.POST['mode'])
            Lobby.objects.get(name=request.POST['name'])
            messages.warning(request, 'El modo o nombre ya existen')
        except:
            Lobby.objects.create(
                mode=request.POST['mode'],
                name=request.POST['name'],
                map=request.POST['map']
            )
            messages.success(request, request.POST['name'] + ' ha sido creado')
        return redirect('/mode/list')

    @login_required
    @user_passes_test(lambda u: u.is_superuser)
    def modeDelete(request, id):
        mode = Lobby.objects.get(id=id)
        Lobby.objects.filter(id=id).delete()
        messages.success(request,  mode.name + ' ha sido eliminada')
        return redirect('/mode/list')


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
        try:
            Weapon.objects.get(command=data['command'])
            messages.warning(request, data['command'] + ' ya existe')
        except:
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
    def get(self, request, *args, **kwargs):
        if request.GET.get('id'):
            weapons = list(Weapon.objects.filter(id=request.GET.get('id')).values())
        elif request.GET.get('command'):
            weapons = list(Weapon.objects.filter(command__icontains=request.GET.get('command')).values())
        else:           # GET ALL
            weapons = list(Weapon.objects.values())
            
        serializer = WeaponSerializer(weapons, many=True)
        if weapons:
            return Response({'message': "Success", 'weapons': serializer.data}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'message': "Error: weapon not found..."}, status=status.HTTP_404_NOT_FOUND)

    @api_login_required
    def post(self, request, *args, **kwargs):
        error = {}
        for weapons in request.data:
            try:
                Weapon.objects.create(
                    command=weapons['command'],
                    category=weapons['category'],
                    name=weapons['name'],
                    muzzle=weapons['muzzle'],
                    barrel=weapons['barrel'],
                    laser=weapons['laser'],
                    optic=weapons['optic'],
                    stock=weapons['stock'],
                    underbarrel=weapons['underbarrel'],
                    magazine=weapons['magazine'],
                    ammunition=weapons['ammunition'],
                    reargrip=weapons['reargrip'],
                    perk=weapons['perk'],
                    perk2=weapons['perk2'],
                    alternative=weapons['alternative'],
                    alternative2=weapons['alternative2']
                )
            except:
                error[weapons['command']] = 'Error: not added'
        return Response({'message': "Success", 'weapons not added': error}, status=status.HTTP_200_OK)

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
        try:
            weapon = Weapon.objects.get(id=id)
        except:
            return Response({'message': "Error: weapon not found..."}, status=status.HTTP_404_NOT_FOUND)
        
        Weapon.objects.filter(id=id).delete()
        serializer = WeaponSerializer(weapon)
        return Response({'message': "Success", 'weapons': serializer.data}, status=status.HTTP_202_ACCEPTED)


class WeaponCategoryApi(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @api_login_required
    def get(self, request, *args, **kwargs):        
        data = {}
        categories = Weapon.objects.order_by('category').values('category').distinct()  # get the different categories
        
        for category in categories:
            commands = Weapon.objects.filter(category=category['category']).order_by('command')
            serializer = WeaponCategorySerializer(commands, many=True)
            data[category['category']] = serializer.data
        return Response({'message': "Success", 'categories': data}, status=status.HTTP_202_ACCEPTED)
