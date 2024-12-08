from rest_framework import viewsets
from rest_framework.decorators import action
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from .models import Moves, MovesPokemons, Pokemons
from .serializers import MovesSerializer, PokemonsSerializer, PokemonsDescSerializer

# Vista para el modelo Moves
class MovesViewSet(viewsets.ModelViewSet):
    queryset = Moves.objects.all()
    serializer_class = MovesSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# Vista para el modelo Pokemons
class PokemonsViewSet(viewsets.ModelViewSet):
    queryset = Pokemons.objects.all()
    serializer_class = PokemonsSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PokemonsActViewSet(viewsets.ModelViewSet):
    queryset = Pokemons.objects.all()
    serializer_class = PokemonsDescSerializer

    @action(detail=True, methods=['patch'], url_path='update_type')
    def update_type(self, request, pk=None):
        """Actualizar tipos del Pokémon"""
        pokemon = self.get_object()  
        pokemon.type_1 = request.data.get('type_1', pokemon.type_1)  
        pokemon.type_2 = request.data.get('type_2', pokemon.type_2)  
        pokemon.save()  
        return Response(
            {"message": f"Tipos del Pokémon con ID {pokemon.id} actualizados correctamente"},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=['patch'], url_path='update_stats')
    def update_stats(self, request, pk=None):
        """Actualizar altura y peso del Pokémon"""
        try:
            pokemon = self.get_object()
            height = request.data.get('height')
            weight = request.data.get('weight')

            if height is not None:
                pokemon.height = height
            if weight is not None:
                pokemon.weight = weight

            pokemon.save()
            return Response(
                {"message": f"Estadísticas del Pokémon con ID {pokemon.id} actualizadas correctamente"},
                status=status.HTTP_200_OK,
            )
        except Pokemons.DoesNotExist:
            return Response({"error": "Pokémon no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=True, methods=['patch'], url_path='update_moves')
    def update_moves(self, request, pk=None):
        """Actualizar movimientos del Pokémon"""
        try:
            pokemon = self.get_object()
            add_moves = request.data.get('add_moves', [])
            remove_moves = request.data.get('remove_moves', [])
            update_moves = request.data.get('update_moves', {})

           
            for move_id in add_moves:
                move = Moves.objects.get(id=move_id)
                MovesPokemons.objects.create(pokemon=pokemon, move=move)

            
            for move_id in remove_moves:
                MovesPokemons.objects.filter(pokemon=pokemon, move_id=move_id).delete()

            
            for move_id, move_data in update_moves.items():
                move = Moves.objects.get(id=move_id)
                if 'name' in move_data:
                    move.name = move_data['name']
                if 'type' in move_data:
                    move.type = move_data['type']
                if 'power' in move_data:
                    move.power = move_data['power']
                if 'accuracy' in move_data:
                    move.accuracy = move_data['accuracy']
                move.save()

            return Response({"message": f"Movimientos actualizados correctamente, Id pokemon: {pokemon.id} "}, status=status.HTTP_200_OK)
        except Pokemons.DoesNotExist:
            return Response({"error": "Pokémon no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Moves.DoesNotExist:
            return Response({"error": "Movimiento no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['patch'], url_path='crear_pokemon')
    def create_or_replace_pokemon(self, request):
        """Crear o reemplazar un Pokémon según su ID"""
        pokemon_id = request.data.get('id')  
        if not pokemon_id:
            return Response({"error": "El ID del Pokémon es obligatorio"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():  
            try:
                
                existing_pokemon = Pokemons.objects.get(id=pokemon_id)

                
                MovesPokemons.objects.filter(pokemon=existing_pokemon).delete()

               
                existing_pokemon.delete()
            except Pokemons.DoesNotExist:
                pass 

           
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(id=pokemon_id)  
                return Response(
                    {
                        "message": f"Pokémon con ID {pokemon_id} creado o reemplazado correctamente",
                        "pokemon": serializer.data,
                    },
                    status=status.HTTP_201_CREATED,
                )

    @action(detail=False, methods=['patch'], url_path='eliminar_pokemon')
    def delete_pokemon(self, request):
        """Eliminar un Pokémon por su ID"""
        pokemon_id = request.data.get('id')  
        if not pokemon_id:
            return Response({"error": "El ID del Pokémon es obligatorio"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            
            pokemon = Pokemons.objects.get(id=pokemon_id)

            
            MovesPokemons.objects.filter(pokemon=pokemon).delete()

           
            pokemon.delete()

            return Response(
                {"message": f"Pokémon con ID {pokemon_id} eliminado correctamente"},
                status=status.HTTP_200_OK,
            )
        except Pokemons.DoesNotExist:
            return Response({"error": "Pokémon no encontrado"}, status=status.HTTP_404_NOT_FOUND)
