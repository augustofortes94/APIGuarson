import json
from api.models import Command, Lobby, Weapon_w1
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views.generic import ListView


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


class HomeView(ListView):
    def home_view(request):
        return render(request, 'home/home.html')


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
            messages.warning(request, 'El modo ya existen')
        except:
            try:
                Lobby.objects.get(name=request.POST['name'])
                messages.warning(request, 'El nombre ya existen')
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
                    name=data['command'],
                    category=data['category']
                    )
        Weapon_w1.objects.create(
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
        weapon = Weapon_w1.objects.get(id=id)
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
            Weapon_w1.objects.get(command__name=request.POST['command'])
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
        weapon = Weapon_w1.objects.get(id=id)
        Weapon_w1.objects.filter(id=id).delete()
        Command.objects.filter(id=weapon.command.id).delete()
        messages.success(request,  weapon.name + ' ha sido eliminada')
        return redirect('/weapon/list')

    def weaponDetail(request, command):
        command = Command.objects.filter(name=command)[0]
        weapon = Weapon_w1.objects.filter(command=command).first()
        return render(request, 'crud_weapons/weapon_detail.html', {"weapon": weapon})

    @login_required
    @user_passes_test(lambda u: u.is_staff)
    def weaponEdit(request, command):
        command = Command.objects.filter(name__icontains=command)[0]
        weapon = Weapon_w1.objects.filter(command=command).first()
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
            weapons = Weapon_w1.objects.filter(name__icontains=request.POST['searched']).order_by('command__name')
        else:
            weapons = Weapon_w1.objects.all().order_by('command__name')

        paginator = Paginator(weapons, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'crud_weapons/weapons_list.html', {'page_obj': page_obj})
