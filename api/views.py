import json
from .serializers import CommandSerializer, LobbySerializer, WeaponSerializer
from .models import Command, Lobby, Weapon_w1
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class CommandApi(APIView):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

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

    def post(self, request, *args, **kwargs):
        error = {}
        success = {}
        for command in request.data:
            try:
                Command.objects.create(
                                name=command['name'],
                                category=command['category'],
                                text=command['text'],
                                parameter1=command['parameter1'],
                                parameter2=command['parameter2']
                            )
                success[command['name']] = 'Added'
            except:
                error[command['name']] = 'Error: not added'
        return Response({'message': "Success", 'Commands added': success, 'Commands not added': error}, status=status.HTTP_200_OK)


class ModeLobbyApi(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    queryset = Lobby.objects.all()
    serializer_class = LobbySerializer
    lookup_field = 'mode'   # Search by mode and not for id

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        try:
            mode = Lobby.objects.filter(mode=self.get_object().mode).values()
            return Response({'message': "Success", 'mode': mode}, status=status.HTTP_202_ACCEPTED)
        except:
            return Response({'message': "Error: mode not found"}, status=status.HTTP_404_NOT_FOUND)

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

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class WeaponApi(APIView):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            if request.GET.get('id'):
                weapons = Weapon_w1.objects.get(id=request.GET.get('id'))
            elif request.GET.get('command'):
                command = Command.objects.filter(name__icontains=request.GET.get('command'))[0]
                weapons = Weapon_w1.objects.select_related().filter(command=command)
            else:           # GET ALL
                weapons = Weapon_w1.objects.all()
            serializer = WeaponSerializer(weapons, many=True)
            return Response({'message': "Success", 'weapons': serializer.data}, status=status.HTTP_202_ACCEPTED)
        except:
            return Response({'message': "Error: weapon not found..."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        error = {}
        success = {}
        for weapons in request.data:
            try:
                command = Command.objects.create(
                                name=weapons['command'],
                                category=weapons['category']
                            )
                Weapon_w1.objects.create(
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
                success[weapons['command']] = 'Added'
            except:
                error[weapons['command']] = 'Error: not added'
        return Response({'message': "Success", 'Weapons added': success, 'Weapons not added': error}, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        data = json.loads(request.body)
        command = Command.objects.filter(name__icontains=data['command'])[0]
        weapon = Weapon_w1.objects.select_related().get(command=command)
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

    def delete(self, request, id, *args, **kwargs):
        try:
            weapon = Weapon_w1.objects.get(id=id)
        except:
            return Response({'message': "Error: weapon not found..."}, status=status.HTTP_404_NOT_FOUND)
        
        Weapon_w1.objects.filter(id=id).delete()
        Command.objects.filter(id=weapon.command.id).delete()
        serializer = WeaponSerializer(weapon)
        return Response({'message': "Success", 'weapons': serializer.data}, status=status.HTTP_202_ACCEPTED)
