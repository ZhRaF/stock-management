# Generated by Django 5.0 on 2024-01-04 23:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_store', '0007_alter_achat_type_paiement_a'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transfert',
            name='id',
        ),
        migrations.AddField(
            model_name='transfert',
            name='montant_t',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transfert',
            name='num_t',
            field=models.AutoField(default=0, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transfert',
            name='produit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_store.stock'),
        ),
    ]
