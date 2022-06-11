from rest_framework import serializers

from .models import Sandwich, Bread, Topping, Cheese, Sauce


class BreadSerialize(serializers.ModelSerializer):
    class Meta:
        model = Bread
        fields = [
            'id',
            'name',
            'qty',
            'price'
        ]


class ToppingSerialize(serializers.ModelSerializer):
    class Meta:
        model = Topping
        fields = [
            'id',
            'name',
            'qty',
            'price'
        ]


class CheeseSerialize(serializers.ModelSerializer):
    class Meta:
        model = Cheese
        fields = [
            'id',
            'name',
            'qty',
            'price'
        ]


class SauceSerialize(serializers.ModelSerializer):
    class Meta:
        model = Sauce
        fields = [
            'id',
            'name',
            'qty',
            'price'
        ]


class SandwichSerializer(serializers.ModelSerializer):
    bread = serializers.PrimaryKeyRelatedField(queryset=Bread.objects.filter(is_deleted=False), many=True)
    topping = serializers.PrimaryKeyRelatedField(queryset=Topping.objects.filter(is_deleted=False), many=True)
    cheese = serializers.PrimaryKeyRelatedField(queryset=Cheese.objects.filter(is_deleted=False), many=True)
    sauce = serializers.PrimaryKeyRelatedField(queryset=Sauce.objects.filter(is_deleted=False), many=True)

    class Meta:
        model = Sandwich
        fields = [
            'id',
            'bread',
            'topping',
            'cheese',
            'sauce'
        ]
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['bread'] = BreadSerialize(instance.bread, many=True).data
        ret['topping'] = ToppingSerialize(instance.topping, many=True).data
        ret['cheese'] = CheeseSerialize(instance.cheese, many=True).data
        ret['sauce'] = SauceSerialize(instance.sauce, many=True).data
        return ret


class SandwichVOSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField(read_only=True)
    bread = BreadSerialize(many=True, read_only=True)
    topping = ToppingSerialize(many=True, read_only=True)
    cheese = CheeseSerialize(many=True, read_only=True)
    sauce = SauceSerialize(many=True, read_only=True)

    class Meta:
        model = Sandwich
        fields = [
            'id',
            'bread',
            'topping',
            'cheese',
            'sauce',
            'total_price'
        ]

    def get_total_price(self, obj) -> int:
        ret = 0
        for bread in obj.bread.all():
            ret += bread.price
        for topping in obj.topping.all():
            ret += topping.price
        for cheese in obj.cheese.all():
            ret += cheese.price
        for sauce in obj.sauce.all():
            ret += sauce.price
        return ret
