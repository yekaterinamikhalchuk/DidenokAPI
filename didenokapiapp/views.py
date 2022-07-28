from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ShopUnit
from .serializers import ShopUnitSerializer, ShopUnitCreateSerializer
import numpy
from rest_framework.exceptions import ValidationError


class ShopUnitView(APIView):
    def get(self, request):
        data = ShopUnit.objects.all()
        serializer = ShopUnitSerializer(data, many=True)
        return Response(serializer.data)


class ShopUnitCreateView(APIView):
    def post(self, request):
        inst = ShopUnitCreateSerializer(instance=request.data)
        if inst.instance['type'] == 'OFFER':
            if 'price' in inst.instance and inst.instance['price'] >= 0:
                if 'parentId' in inst.instance:
                    unit = ShopUnit(
                        name=inst.instance['name'],
                        type=inst.instance['type'],
                        price=inst.instance['price'],
                        parentId=inst.instance['parentId'],
                        date=datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                    )
                    unit.save()
                    ShopUnit.objects.filter(
                        id=inst.instance['parentId']).update(
                        children=list(ShopUnit.objects.filter(
                            parentId=inst.instance['parentId']).values()), price=int(
                            numpy.average(ShopUnit.objects.filter(
                                parentId=inst.instance['parentId']).values_list('price'))))
                else:
                    unit = ShopUnit(
                        name=inst.instance['name'],
                        type=inst.instance['type'],
                        price=inst.instance['price'],
                        date=datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                    )
                    unit.save()
            else:
                raise ValidationError

        else:
            if 'parentId' in inst.instance and ShopUnit.objects.filter(
                    type="CATEGORY").get(id=inst.instance['parentId']):
                unit = ShopUnit(
                    name=inst.instance['name'],
                    type=inst.instance['type'],
                    parentId=inst.instance['parentId'],
                    date=datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                )
                unit.save()
                ShopUnit.objects.filter(
                    id=inst.instance['parentId']).update(
                    children=list(ShopUnit.objects.filter(
                        parentId=inst.instance['parentId']).values()), price=int(
                        numpy.average(ShopUnit.objects.filter(
                            parentId=inst.instance['parentId']).filter(type="OFFER").values_list('price'))))
            else:
                unit = ShopUnit(
                    name=inst.instance['name'],
                    type=inst.instance['type'],
                    date=datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                )
                unit.save()

            if ShopUnit.objects.filter(parentId=unit.id):

                ShopUnit.objects.filter(
                    id=unit.id).update(
                    price=int(numpy.average(ShopUnit.objects.filter(
                        parentId=unit.id).filter(type="OFFER").values_list('price'))),
                    children=list(ShopUnit.objects.filter(
                        parentId=unit.id).values()))

        return Response(status=201)
# Create your views here.
