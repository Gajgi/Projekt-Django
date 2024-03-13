from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db import models
from django.shortcuts import redirect, get_object_or_404, render
from django.views import View



#Model Membership reprezentuje wędkarza,ktory jest czlonkiem koła wędkarskiego
class Membership(models.Model):  # Wędkarz
    date = models.DateField()  # data rozpoczęcia członkostwa
    fee = models.DecimalField(max_digits=7, decimal_places=2) #składka
    angler= models.ForeignKey(User, on_delete=models.CASCADE)# członek koła

#Model Fish reprezentuje rybę, której wędkarze mogą łowić.
class Fish(models.Model):  # Ryba
    name = models.CharField(max_length=100)  # nazwa
    max_weight = models.FloatField()  # maksymalna waga

#Model Catch reprezentuje połów-rybę złowioną przez wędkarza.
class Catch(models.Model):  # Połów
    angler = models.ForeignKey(User, on_delete=models.CASCADE)  # wędkarz
    fish = models.ForeignKey(Fish, on_delete=models.CASCADE)  # ryba
    weight = models.FloatField()  # waga
    date = models.DateField()  # data połowu

#Model Competition reprezentuje zawody wędkarskie organizowane przez kolo
class Competition(models.Model):  # Zawody
    name = models.CharField(max_length=100)  # nazwa
    date = models.DateField()  # data
    description = models.TextField()  # opis
    available_places = models.IntegerField()  # dostępne miejsca
    first_place = models.ForeignKey(User, related_name='first_place_competitions', on_delete=models.SET_NULL, null=True)
    second_place = models.ForeignKey(User, related_name='second_place_competitions', on_delete=models.SET_NULL,null=True)
    third_place = models.ForeignKey(User, related_name='third_place_competitions', on_delete=models.SET_NULL, null=True)

#Model WaterBody reprezentuje ciało wodne, na którym wędkarze mogą łowić
class WaterBody(models.Model):  # Ciało wodne
    name = models.CharField(max_length=100)  # nazwa
    location = models.CharField(max_length=200)  # lokalizacja
    fish_species = models.ManyToManyField(Fish)  # gatunki ryb

#Model InformationForAnglers zawiera informacje przeznaczone do udostępnienia wędkarzom.
class InformationForAnglers(models.Model):  # Informacje dla wędkarzy
    title = models.CharField(max_length=200)  # tytuł
    content = models.TextField()  # zawartość
    PZW_fees = models.DecimalField(max_digits=7, decimal_places=2)  # składki PZW
    documents_for_anglers = models.TextField()  # materiały dla wędkarzy
    fishing_grounds = models.TextField()  # łowiska
    catch_register = models.TextField()  # rejestr połowu ryb
    angling_rules = models.TextField()  # zasady wędkowania

#Model Contact zawiera informacje kontaktowe do klubu wędkarskiego
class Contact(models.Model):  # Kontakt
    address = models.CharField(max_length=200)  # adres
    phone_number = models.CharField(max_length=15)  # numer telefonu
    email = models.EmailField()  # e-mail








