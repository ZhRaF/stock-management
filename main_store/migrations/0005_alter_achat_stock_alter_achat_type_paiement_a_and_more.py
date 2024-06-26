# Generated by Django 5.0 on 2024-01-03 12:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_store', '0004_alter_achat_type_paiement_a'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achat',
            name='stock',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='main_store.stock'),
        ),
        migrations.AlterField(
            model_name='achat',
            name='type_Paiement_A',
            field=models.CharField(choices=[('Entier', 'Entier'), ('Partiel', 'Partiel')], default='Entier', max_length=20),
        ),
        migrations.AlterField(
            model_name='vente',
            name='type_paiement_v',
            field=models.CharField(choices=[('Entier', 'Entier'), ('Partiel', 'Partiel')], default='Entier', max_length=20),
        ),
    ]
