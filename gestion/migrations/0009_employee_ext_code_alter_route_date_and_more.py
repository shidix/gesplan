# Generated by Django 5.1.2 on 2024-11-29 11:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0008_employeetype_alter_route_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='ext_code',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='External code'),
        ),
        migrations.AlterField(
            model_name='route',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 11, 30, 11, 43, 41, 957548, tzinfo=datetime.timezone.utc), verbose_name='Fecha de la ruta'),
        ),
        migrations.AlterField(
            model_name='wasteinfacility',
            name='last_modification',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 11, 29, 11, 43, 41, 914761, tzinfo=datetime.timezone.utc), null=True, verbose_name='Última modificación'),
        ),
    ]
