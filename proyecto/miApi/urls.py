from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()

router.register(r'moves', views.MovesViewSet, basename='moves')
router.register(r'pokemons', views.PokemonsViewSet, basename='pokemons')
router.register(r'pokemonsAct', views.PokemonsActViewSet, basename='pokemonsAct')


urlpatterns = [
    path('', include(router.urls)),  
]