# Generated by Django 5.0 on 2024-01-02 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('center', '0004_alter_centre_code_c'),
    ]

    operations = [
        migrations.AlterField(
            model_name='centre',
            name='code_c',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
