# Generated by Django 5.0 on 2024-01-04 19:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_store', '0008_alter_achat_stock'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vente',
            old_name='type_paiement_v',
            new_name='type_Paiement_v',
        ),
        migrations.RemoveField(
            model_name='transfert',
            name='produit',
        ),
        migrations.RemoveField(
            model_name='vente',
            name='produit',
        ),
        migrations.AddField(
            model_name='transfert',
            name='stock',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='main_store.stock'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vente',
            name='prix_unitaireVT',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='vente',
            name='stock',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='main_store.stock'),
        ),
    ]