# Generated by Django 5.0 on 2024-01-07 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_store', '0009_rename_type_paiement_v_vente_type_paiement_v_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vente',
            name='type_Paiement_v',
            field=models.CharField(choices=[('Entier', 'Entier'), ('Partiel', 'Partiel')], max_length=20),
        ),
    ]