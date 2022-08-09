import json
from .serializers import CommandSerializer, LobbySerializer, WeaponSerializer
from .models import Command, Lobby, Weapon
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from user.decorators import api_login_required


class CommandApi(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @api_login_required
    def get(self, request, *args, **kwargs):
        try:    # get by command
            command = Command.objects.filter(name__istartswith=request.GET.get('command')).values()[0]
            serializer = CommandSerializer(command)
            return Response({'message': "Success", 'command': serializer.data}, status=status.HTTP_202_ACCEPTED)
        except:
            try:
                data = {}
                categories = Command.objects.order_by('category').values('category').distinct()  # get the different categories
                
                for category in categories:
                    commands = Command.objects.filter(category=category['category']).order_by('name')
                    serializer = CommandSerializer(commands, many=True)
                    data[category['category']] = serializer.data
                return Response({'message': "Success", 'categories': data}, status=status.HTTP_202_ACCEPTED)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)


class CommandView(ListView):
    @login_required
    @user_passes_test(lambda u: u.is_superuser)
    def commandList(request):
        categories = Command.objects.filter(Q(category='Bonus') | Q(category='Lobbys') | Q(category='Streamers')).order_by('category', 'name')
        paginator = Paginator(categories, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'crud_commands/commands_list.html', {'page_obj': page_obj})

    @login_required
    @user_passes_test(lambda u: u.is_superuser)
    def commandAddForm(request):
        return render(request, 'crud_commands/commands_add.html')

    @login_required
    @user_passes_test(lambda u: u.is_superuser)
    def commandAdd(request):
        try:
            Command.objects.get(name=request.POST['name'])
            messages.warning(request, 'El comando ya existe')
        except:
            data = {}
            for key in request.POST:
                if key == 'csrfmiddlewaretoken':
                    pass
                elif request.POST[key] == 'None' or request.POST[key] == "":
                    data[key] = None
                else:
                    data[key] = request.POST[key]
            Command.objects.create(
                name=data['name'],
                category=data['category'],
                text=data['text'],
                parameter1=data['parameter1'],
                parameter2=data['parameter2']
            )
            messages.success(request, data['name'] + ' ha sido creado')
        return redirect('/command/list')

    @login_required
    @user_passes_test(lambda u: u.is_superuser)
    def commandDelete(request, id):
        command = Command.objects.get(id=id)
        Command.objects.filter(id=id).delete()
        messages.success(request,  command.name + ' ha sido eliminado')
        return redirect('/command/list')

    @login_required
    @user_passes_test(lambda u: u.is_superuser)
    def commandEdit(request, id):
        command = Command.objects.get(id=id)
        return render(request, 'crud_commands/commands_edit.html', {"command": command})

    @login_required
    @user_passes_test(lambda u: u.is_superuser)
    def commandEdition(request, id):
        data = {}
        for key in request.POST:
            if key == 'csrfmiddlewaretoken':
                pass
            elif request.POST[key] == 'None' or request.POST[key] == "":
                data[key] = None
            else:
                data[key] = request.POST[key]
        data = json.loads(json.dumps(data))
        command = Command.objects.get(id=id)
        command.name = data['name']
        command.category = data['category']
        command.text = data['text']
        command.parameter1 = data['parameter1']
        command.parameter2 = data['parameter2']
        command.save()
        messages.success(request, data['name'] + ' ha sido modificado')
        return redirect('/command/list')


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
        command = Command.objects.create(
                    command=data['command'],
                    category=data['category']
                    )
        Weapon.objects.create(
            command=command,
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
        command = Command.objects.get(id=weapon.command.id)
        command.name = data['command']
        command.category = data['category']

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
        command.save()

    @login_required
    @user_passes_test(lambda u: u.is_staff)
    def weaponAdd(request):
        try:
            Weapon.objects.get(command=request.POST['command'])
            messages.warning(request, request.POST['command'] + ' ya existe')
        except:
            data = {}
            for key in request.POST:
                if key == 'csrfmiddlewaretoken':
                    pass
                elif request.POST[key] == 'None' or request.POST[key] == "":
                    data[key] = None
                else:
                    data[key] = request.POST[key]
            data = json.loads(json.dumps(data))
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
        Command.objects.filter(id=weapon.command.id).delete()
        messages.success(request,  weapon.name + ' ha sido eliminada')
        return redirect('/weapon/list')

    def weaponDetail(request, command):
        command = Command.objects.filter(name__icontains=command)[0]
        weapon = Weapon.objects.filter(command=command).first()
        return render(request, 'crud_weapons/weapon_detail.html', {"weapon": weapon})

    @login_required
    @user_passes_test(lambda u: u.is_staff)
    def weaponEdit(request, command):
        command = Command.objects.filter(name__icontains=command)[0]
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
            weapons = Weapon.objects.filter(name__icontains=request.POST['searched']).order_by('command__name')
        else:
            weapons = Weapon.objects.all().order_by('command__name')

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
        try:
            if request.GET.get('id'):
                weapons = Weapon.objects.get(id=request.GET.get('id'))
            elif request.GET.get('command'):
                command = Command.objects.get(name__icontains=request.GET.get('command'))[0]
                weapons = Weapon.objects.select_related().filter(command=command)
            else:           # GET ALL
                weapons = Weapon.objects.all()
            serializer = WeaponSerializer(weapons, many=True)
            if weapons:
                return Response({'message': "Success", 'weapons': serializer.data}, status=status.HTTP_202_ACCEPTED)
        except:
            return Response({'message': "Error: weapon not found..."}, status=status.HTTP_404_NOT_FOUND)

    @api_login_required
    def post(self, request, *args, **kwargs):
        error = {}
        for weapons in request.data:
            try:
                command = Command.objects.create(
                                name=weapons['command'],
                                category=weapons['category']
                            )
                Weapon.objects.create(
                    command=command,
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
        command = Command.objects.filter(name__icontains=data['command'])[0]
        weapon = Weapon.objects.select_related().get(command=command)
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
        serializer = WeaponSerializer(data=weapon)
        serializer.is_valid(raise_exception=True)
        return Response({'message': "Success", 'weapons': serializer.data}, status=status.HTTP_202_ACCEPTED)

    @api_login_required
    def delete(self, request, id, *args, **kwargs):
        try:
            weapon = Weapon.objects.get(id=id)
        except:
            return Response({'message': "Error: weapon not found..."}, status=status.HTTP_404_NOT_FOUND)
        
        Weapon.objects.filter(id=id).delete()
        Command.objects.filter(id=weapon.command.id).delete()
        serializer = WeaponSerializer(weapon)
        return Response({'message': "Success", 'weapons': serializer.data}, status=status.HTTP_202_ACCEPTED)
