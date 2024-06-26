# Generated by Django 5.0 on 2023-12-29 14:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Centre',
            fields=[
                ('Code_c', models.AutoField(primary_key=True, serialize=False)),
                ('designation_c', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='VenteCentre',
            fields=[
                ('num_vc', models.AutoField(primary_key=True, serialize=False)),
                ('qte_vc', models.IntegerField()),
                ('date_vc', models.DateField()),
                ('montant_vc', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Employe',
            fields=[
                ('code_e', models.AutoField(primary_key=True, serialize=False)),
                ('nom_e', models.CharField(max_length=50)),
                ('prenom_e', models.CharField(max_length=50)),
                ('adresse_e', models.CharField(max_length=100)),
                ('telephone_e', models.CharField(max_length=50)),
                ('salaire_jour', models.FloatField(max_length=50)),
                ('centre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='center.centre')),
            ],
        ),
        migrations.CreateModel(
            name='produits_centre',
            fields=[
                ('Code_pc', models.AutoField(primary_key=True, serialize=False)),
                ('designation_pc', models.CharField(max_length=50)),
                ('centre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='center.centre')),
            ],
        ),
    ]
