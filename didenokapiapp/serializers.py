from rest_framework import serializers
from .models import ShopUnit


class ShopUnitSerializer(serializers.ModelSerializer):
    
    class Meta:

        model = ShopUnit
        fields = '__all__'


class ShopUnitCreateSerializer(serializers.Serializer):

    class Meta:

        model = ShopUnit
        fields = ('id', 'name', 'parentId', 'price', 'type')