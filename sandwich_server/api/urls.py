from django.urls import path

from .views import *

app_name = "api"
urlpatterns = [
    path(
        "sandwiches",
        SandwichViewSet.as_view({"get": "get_sandwiches", "post": "create_sandwich"}),
        name=app_name
    ),
    path(
        "sandwiches/<int:pk>",
        SandwichViewSet.as_view({"get": "retrieve", "delete": "delete_sandwich"}),
        name=app_name
    ),
    
    path(
        "breads",
        BreadViewSet.as_view({"get": "get_breads", "post": "create"}),
        name=app_name
    ),
    path(
        "breads/<int:pk>",
        BreadViewSet.as_view({"get": "retrieve", "put": "update", "delete": "delete_bread"}),
        name=app_name
    ),
    
    path(
        "toppings",
        ToppingViewSet.as_view({"get": "get_toppings", "post": "create"}),
        name=app_name
    ),
    path(
        "toppings/<int:pk>",
        ToppingViewSet.as_view({"get": "retrieve", "put": "update", "delete": "delete_topping"}),
        name=app_name
    ),
    
    path(
        "cheeses",
        CheeseViewSet.as_view({"get": "get_cheeses", "post": "create"}),
        name=app_name
    ),
    path(
        "cheeses/<int:pk>",
        CheeseViewSet.as_view({"get": "retrieve", "put": "update", "delete": "delete_cheese"}),
        name=app_name
    ),
    
    path(
        "sauces",
        SauceViewSet.as_view({"get": "get_sauces", "post": "create"}),
        name=app_name
    ),
    path(
        "sauces/<int:pk>",
        SauceViewSet.as_view({"get": "retrieve", "put": "update", "delete": "delete_sauce"}),
        name=app_name
    ),
]