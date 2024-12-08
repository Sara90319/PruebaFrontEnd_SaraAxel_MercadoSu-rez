from rest_framework import serializers
from .models import Moves, MovesPokemons, Pokemons

class MovesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moves
        fields = ['id', 'name', 'type', 'power', 'accuracy']  

class PokemonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pokemons
        fields = ['id', 'name']

class PokemonsDescSerializer(serializers.ModelSerializer):
    moves = serializers.SerializerMethodField()  #
    class Meta:
        model = Pokemons
        fields = ['id', 'name', 'type_1', 'type_2', 'description', 'height', 'weight', 'moves']
    def get_moves(self, obj):
        
        moves = Moves.objects.filter(movespokemons__pokemon=obj)
        return MovesSerializer(moves, many=True).data