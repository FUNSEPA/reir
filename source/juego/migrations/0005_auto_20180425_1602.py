# Generated by Django 2.0.4 on 2018-04-25 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('juego', '0004_punteo_porcentaje'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='indicador',
            options={'verbose_name': 'Indicador', 'verbose_name_plural': 'Indicadores'},
        ),
        migrations.AddField(
            model_name='punteo',
            name='justificacion',
            field=models.TextField(blank=True, null=True),
        ),
    ]
