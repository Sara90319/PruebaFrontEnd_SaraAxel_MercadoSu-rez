from django.db import models

class Moves(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    power = models.IntegerField(blank=True, null=True)
    accuracy = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'moves'

class MovesPokemons(models.Model):
    move = models.ForeignKey(Moves, models.DO_NOTHING, blank=True, null=True)
    pokemon = models.ForeignKey('Pokemons', models.DO_NOTHING, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'moves_pokemons'

class Pokemons(models.Model):
    id = models.AutoField(primary_key=True)  
    type_1 = models.CharField(max_length=255, blank=True, null=True)
    type_2 = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    mega_evolves = models.IntegerField(blank=True, null=True)
    evolves = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'pokemons'

