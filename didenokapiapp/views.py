from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ShopUnit
from .serializers import ShopUnitSerializer, ShopUnitCreateSerializer
import numpy
from rest_framework.exceptions import ValidationError


class ShopUnitView(APIView):
    def get_object(self, request, pk):
        try:
            return ShopUnit.objects.get(pk=pk)
        except ShopUnit.DoesNotExist:
            raise Http404

        # data = ShopUnit.objects.get(id=pk)
        # serializer = ShopUnitSerializer(data, many=True)
        # return Response(serializer.data)


class ShopUnitCreateView(APIView):
    def post(self, request):
        inst = ShopUnitCreateSerializer(instance=request.data)
        if inst.instance['type'] == 'OFFER':
            if 'price' in inst.instance and inst.instance['price'] >= 0:
                if 'parentId' in inst.instance:
                    unit = ShopUnit(
                        name=inst.instance['name'],
                        type=inst.instance['type'],
                        price=int(inst.instance['price']),
                        parentId=inst.instance['parentId'],
                        date=datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                    )
                    unit.save()

                    ShopUnit.objects.filter(
                        id=inst.instance['parentId']).update(
                        children=list(ShopUnit.objects.filter(
                            parentId=inst.instance['parentId']).values()), price=numpy.average(
                                ShopUnit.objects.filter(
                                parentId=inst.instance['parentId']).values_list('price')))
                    if ShopUnit.objects.filter(id=ShopUnit.objects.filter(
                        id=inst.instance['parentId']).values_list('parentId', flat=True)[0]).values_list(
                        'parentId', flat=True):
                        ShopUnit.objects.filter(id=ShopUnit.objects.filter(
                            id=inst.instance['parentId']).values_list('parentId', flat=True)[0]).update(children=list(ShopUnit.objects.filter(
                            parentId=ShopUnit.objects.filter(id=inst.instance['parentId']).values_list('parentId', flat=True)[0]).values()), price=numpy.average(ShopUnit.objects.filter(
                            parentId=ShopUnit.objects.filter(id=inst.instance['parentId']).values_list('parentId', flat=True)[0]).values_list('price', flat=True)))

                else:
                    unit = ShopUnit(
                        name=inst.instance['name'],
                        type=inst.instance['type'],
                        price=int(inst.instance['price']),
                        date=datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                    )
                    unit.save()
            else:
                raise ValidationError

        else:
            if 'parentId' in inst.instance:
                unit = ShopUnit(
                    name=inst.instance['name'],
                    type=inst.instance['type'],
                    parentId=inst.instance['parentId'],
                    date=datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                )
                unit.save()
            else:
                unit = ShopUnit(
                    name=inst.instance['name'],
                    type=inst.instance['type'],
                    date=datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                )
                unit.save()

        return Response(status=201)
# Create your views here.


class EventDetail(APIView):

    """
    Retrieve, update or delete a event instance.
    """

    def get_object(self, pk):
        try:
            return Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        event = self.get_object(pk)
        serializer = ShopUnitCreateSerializer(event)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ShopUnitCreateSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def put(self, request, pk, format=None):
    #     event = self.get_object(pk)
    #     serializer = EventSerializer(event, data=request.DATA)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        event = self.get_object(pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
