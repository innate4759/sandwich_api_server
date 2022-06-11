from typing import Union

from django.shortcuts import get_object_or_404
from django.db import transaction
from django.core.exceptions import ValidationError
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .serializers import *


class SandwichPagination(PageNumberPagination):
    page_size = 10


class SandwichViewSet(viewsets.ModelViewSet):
    queryset = Sandwich.objects.all()
    serializer_class = SandwichSerializer
    pagination_class = SandwichPagination

    def __init__(self):
        self.current_ingredient_name = ''

    @swagger_auto_schema(responses={200: openapi.Response(description='SandwichVO', schema=SandwichVOSerializer)})
    def get_sandwiches(self, request):
        sandwiches = Sandwich.objects.filter(is_deleted=False)
        return Response(SandwichVOSerializer(sandwiches, many=True).data)

    @swagger_auto_schema(responses={200: openapi.Response(description='SandwichVO', schema=SandwichVOSerializer)})
    def create_sandwich(self, request):
        bread_params = request.data.get('bread')
        topping_params = request.data.get('topping')
        cheese_params = request.data.get('cheese')
        sauce_params = request.data.get('sauce')

        if not bread_params or not topping_params or not cheese_params or not sauce_params:
            return Response({'detail': 'Cannot be made without selection of bread, toppings, cheese, and sauce'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        
        if len(bread_params) >= 2:
            return Response({'detail': 'You cannot choose more than 2 breads'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        if len(topping_params) >= 3:
            return Response({'detail': 'You cannot choose more than 3 toppings'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        if len(cheese_params) >= 2:
            return Response({'detail': 'You cannot choose more than 2 cheeses'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        if len(sauce_params) >= 3:
            return Response({'detail': 'You cannot choose more than 3 sauces'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

        try:
            with transaction.atomic():
                sandwich = Sandwich.objects.create()

                for pk in bread_params:
                    bread = get_object_or_404(Bread, pk=pk, is_deleted=False)
                    self.check_ingredient_stock(bread)
                    bread.qty -= 1
                    bread.save()
                    sandwich.bread.add(bread)

                for pk in topping_params:
                    topping = get_object_or_404(Topping, pk=pk, is_deleted=False)
                    self.check_ingredient_stock(topping)
                    topping.qty -= 1
                    topping.save()
                    sandwich.topping.add(topping)

                for pk in cheese_params:
                    cheese = get_object_or_404(Cheese, pk=pk, is_deleted=False)
                    self.check_ingredient_stock(cheese)
                    cheese.qty -= 1
                    cheese.save()
                    sandwich.cheese.add(cheese)

                for pk in sauce_params:
                    sauce = get_object_or_404(Sauce, pk=pk, is_deleted=False)
                    self.check_ingredient_stock(sauce)
                    sauce.qty -= 1
                    sauce.save()
                    sandwich.sauce.add(sauce)

                sandwich.save()
        except ValidationError:
            return Response({'detail': f'{self.current_ingredient_name} cannot be selected because stock is 0'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

        return Response(SandwichSerializer(sandwich).data)

    def delete_sandwich(self, request, pk):
        with transaction.atomic():
            sandwich = get_object_or_404(Sandwich, pk=pk)
            sandwich.is_deleted = True
            sandwich.save()

            for bread in sandwich.bread.all():
                bread.qty -= 1
                bread.save()
            for topping in sandwich.topping.all():
                topping.qty -= 1
                topping.save()
            for cheese in sandwich.cheese.all():
                cheese.qty -= 1
                cheese.savw()
            for sauce in sandwich.sauce.all():
                sauce -= 1
                sauce.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def check_ingredient_stock(self, ingredient: Union[Bread, Topping, Cheese, Sauce]):
        self.current_ingredient_name = ingredient.name
        if ingredient.qty < 1:
            raise ValidationError('')


class BreadViewSet(viewsets.ModelViewSet):
    queryset = Bread.objects.all()
    serializer_class = BreadSerialize

    def get_breads(self, request):
        breads = Bread.objects.filter(is_deleted=False)
        return Response(BreadSerialize(breads, many=True).data)

    def delete_bread(self, request, pk):
        bread = get_object_or_404(Bread, pk=pk)
        bread.is_deleted = True
        bread.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ToppingViewSet(viewsets.ModelViewSet):
    queryset = Topping.objects.all()
    serializer_class = ToppingSerialize

    def get_toppings(self, request):
        toppings = Topping.objects.filter(is_deleted=False)
        return Response(ToppingSerialize(toppings, many=True).data)
    
    def delete_topping(self, request, pk):
        topping = get_object_or_404(Topping, pk=pk)
        topping.is_deleted = True
        topping.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class CheeseViewSet(viewsets.ModelViewSet):
    queryset = Cheese.objects.all()
    serializer_class = CheeseSerialize

    def get_cheeses(self, request):
        cheeses = Cheese.objects.filter(is_deleted=False)
        return Response(CheeseSerialize(cheeses, many=True).data)
    
    def delete_cheese(self, request, pk):
        cheese = get_object_or_404(Cheese, pk=pk)
        cheese.is_deleted = True
        cheese.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class SauceViewSet(viewsets.ModelViewSet):
    queryset = Sauce.objects.all()
    serializer_class = SauceSerialize

    def get_sauces(self, request):
        sauces = Sauce.objects.filter(is_deleted=False)
        return Response(SauceSerialize(sauces, many=True).data)
    
    def delete_sauce(self, request, pk):
        sauce = get_object_or_404(Sauce, pk=pk)
        sauce.is_deleted = True
        sauce.save()
        return Response(status=status.HTTP_204_NO_CONTENT)