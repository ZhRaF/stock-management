# Generated by Django 5.0 on 2024-01-04 18:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_store', '0007_alter_achat_type_paiement_a'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achat',
            name='stock',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='achat', to='main_store.stock'),
        ),
    ]
