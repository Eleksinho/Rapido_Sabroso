# Generated by Django 5.1 on 2024-10-05 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rapidoysabrosoWEB', '0002_categoria_producto_marca_producto_categoria'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='imagen_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]