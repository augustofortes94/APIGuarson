import json
from .serializers import CommandSerializer, LobbySerializer, WeaponW1Serializer, WeaponW2Serializer
from .models import Command, Lobby, WeaponW1, WeaponW2
from django.db.models import Q
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
        try:    # Get by command
            command = Command.objects.filter(Q(name__istartswith=request.GET.get('command'))).values()[0]
            if command['warzone_version'] == request.GET.get('warzone_version') or command['warzone_version'] is None:
                serializer = CommandSerializer(command)
                return Response({'message': "Success", 'command': serializer.data}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            try:    # Get all commands by category
                data = {}
                categories = Command.objects.filter(Q(warzone_version=request.GET.get('warzone_version')) | Q(warzone_version=None)).order_by('category').values('category').distinct()  # get the different categories
                for category in categories:
                    commands = Command.objects.filter(Q(category=category['category']) & (Q(warzone_version=request.GET.get('warzone_version')) | Q(warzone_version=None))).order_by('name')
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
                                parameter2=command['parameter2'],
                                warzone_version=command['warzone_version']
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


class WeaponW1Api(APIView):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            if request.GET.get('id'):
                weapons = WeaponW1.objects.filter(id=request.GET.get('id'))
            elif request.GET.get('command'):
                command = Command.objects.filter(name__icontains=request.GET.get('command'))[0]
                weapons = WeaponW1.objects.select_related().filter(command=command)
            else:   # Get all
                weapons = WeaponW1.objects.all()
            serializer = WeaponW1Serializer(weapons, many=True)
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
                                category=weapons['category'],
                                warzone_version='w1'
                            )
                WeaponW1.objects.create(
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
        command = Command.objects.filter(name__icontains=request.data['command'])[0]
        weapon = WeaponW1.objects.select_related().get(command=command)
        weapon.category = request.data['category']
        weapon.name = request.data['name']
        weapon.muzzle = request.data['muzzle']
        weapon.barrel = request.data['barrel']
        weapon.laser = request.data['laser']
        weapon.optic = request.data['optic']
        weapon.stock = request.data['stock']
        weapon.underbarrel = request.data['underbarrel']
        weapon.magazine = request.data['magazine']
        weapon.ammunition = request.data['ammunition']
        weapon.reargrip = request.data['reargrip']
        weapon.perk = request.data['perk']
        weapon.perk2 = request.data['perk2']
        weapon.alternative = request.data['alternative']
        weapon.alternative2 = request.data['alternative2']
        weapon.save()
        serializer = WeaponW1Serializer(weapon)
        return Response({'message': "Success", 'weapons': serializer.data}, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, id, *args, **kwargs):
        try:
            weapon = WeaponW1.objects.get(id=id)
        except:
            return Response({'message': "Error: weapon not found..."}, status=status.HTTP_404_NOT_FOUND)
        
        WeaponW1.objects.filter(id=id).delete()
        Command.objects.filter(id=weapon.command.id).delete()
        serializer = WeaponW1Serializer(weapon)
        return Response({'message': "Success", 'weapons': serializer.data}, status=status.HTTP_202_ACCEPTED)


class WeaponW2Api(APIView):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            if request.GET.get('id'):
                weapons = WeaponW2.objects.filter(id=request.GET.get('id'))
            elif request.GET.get('command'):
                command = Command.objects.filter(name__icontains=request.GET.get('command'))[0]
                weapons = WeaponW2.objects.select_related().filter(command=command)
            else:   # Get all
                weapons = WeaponW2.objects.all()
            serializer = WeaponW2Serializer(weapons, many=True)
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
                                category=weapons['category'],
                                warzone_version='w2'
                            )
                WeaponW2.objects.create(
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
                    guard=weapons['guard'],
                    comb=weapons['comb'],
                    receiver=weapons['receiver'],
                    alternative=weapons['alternative'],
                    alternative2=weapons['alternative2']
                )
                success[weapons['command']] = 'Added'
            except:
                error[weapons['command']] = 'Error: not added'
        return Response({'message': "Success", 'Weapons added': success, 'Weapons not added': error}, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        command = Command.objects.filter(name__icontains=request.data['command'])[0]
        weapon = WeaponW2.objects.select_related().get(command=command)
        weapon.category = request.data['category']
        weapon.name = request.data['name']
        weapon.muzzle = request.data['muzzle']
        weapon.barrel = request.data['barrel']
        weapon.laser = request.data['laser']
        weapon.optic = request.data['optic']
        weapon.stock = request.data['stock']
        weapon.underbarrel = request.data['underbarrel']
        weapon.magazine = request.data['magazine']
        weapon.ammunition = request.data['ammunition']
        weapon.reargrip = request.data['reargrip']
        weapon.guard = request.data['guard']
        weapon.comb = request.data['comb']
        weapon.receiver = request.data['receiver']
        weapon.alternative = request.data['alternative']
        weapon.alternative2 = request.data['alternative2']
        weapon.save()
        serializer = WeaponW2Serializer(weapon)
        return Response({'message': "Success", 'weapons': serializer.data}, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, id, *args, **kwargs):
        try:
            weapon = WeaponW2.objects.get(id=id)
        except:
            return Response({'message': "Error: weapon not found..."}, status=status.HTTP_404_NOT_FOUND)
        
        WeaponW2.objects.filter(id=id).delete()
        Command.objects.filter(id=weapon.command.id).delete()
        serializer = WeaponW2Serializer(weapon)
        return Response({'message': "Success", 'weapons': serializer.data}, status=status.HTTP_202_ACCEPTED)
