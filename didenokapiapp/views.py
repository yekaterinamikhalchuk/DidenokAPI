from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ShopUnit
from .serializers import ShopUnitSerializer, ShopUnitCreateSerializer
import numpy


class ShopUnitView(APIView):
    def get(self, request):
        data = ShopUnit.objects.all()
        serializer = ShopUnitSerializer(data, many=True)
        return Response(serializer.data)


class ShopUnitCreateView(APIView):
    def post(self, request):
        inst = ShopUnitCreateSerializer(instance=request.data)
        if inst.instance['type'] == 'OFFER':
            unit = ShopUnit(
            id = inst.instance['id'],
            name = inst.instance['name'],
            type = inst.instance['type'],
            price = inst.instance['price'],
            parentId = inst.instance['parentId'],
            date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            )
            unit.save()
        else:
            unit = ShopUnit(
            id = inst.instance['id'],
            name = inst.instance['name'],
            type = inst.instance['type'],
            price = int(numpy.average(ShopUnit.objects.filter(parentId=inst.instance['id']).values_list('price'))),
            children = list(ShopUnit.objects.filter(parentId=inst.instance['id']).values()),
            date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            )
            unit.save()
        
        return Response(status=201)
# Create your views here.
