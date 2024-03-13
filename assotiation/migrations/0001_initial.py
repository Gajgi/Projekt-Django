# Generated by Django 5.0.3 on 2024-03-13 12:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200)),
                ('phone_number', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Fish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('max_weight', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='InformationForAnglers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('PZW_fees', models.DecimalField(decimal_places=2, max_digits=7)),
                ('documents_for_anglers', models.TextField()),
                ('fishing_grounds', models.TextField()),
                ('catch_register', models.TextField()),
                ('angling_rules', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('description', models.TextField()),
                ('available_places', models.IntegerField()),
                ('first_place', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='first_place_competitions', to=settings.AUTH_USER_MODEL)),
                ('second_place', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='second_place_competitions', to=settings.AUTH_USER_MODEL)),
                ('third_place', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='third_place_competitions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Catch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.FloatField()),
                ('date', models.DateField()),
                ('angler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('fish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assotiation.fish')),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('fee', models.DecimalField(decimal_places=2, max_digits=7)),
                ('angler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WaterBody',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=200)),
                ('fish_species', models.ManyToManyField(to='assotiation.fish')),
            ],
        ),
    ]
