# Generated by Django 5.0 on 2024-01-02 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('center', '0003_rename_code_c_centre_code_c'),
    ]

    operations = [
        migrations.AlterField(
            model_name='centre',
            name='code_c',
            field=models.AutoField(default=1, editable=False, primary_key=True, serialize=False),
        ),
    ]
