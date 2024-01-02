# Generated by Django 5.0 on 2024-01-02 22:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('center', '0006_alter_employe_salaire_jour'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientC',
            fields=[
                ('code_cl', models.AutoField(primary_key=True, serialize=False)),
                ('nom_cl', models.CharField(max_length=50)),
                ('prenom_cl', models.CharField(max_length=50)),
                ('adresse_cl', models.CharField(max_length=100)),
                ('telephone_cl', models.CharField(max_length=50)),
                ('credit', models.FloatField(default=0.0)),
                ('centre', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='center.centre')),
            ],
        ),
    ]
