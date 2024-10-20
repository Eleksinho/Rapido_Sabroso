# Generated by Django 5.1.2 on 2024-10-16 18:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rapidoysabrosoWEB', '0008_producto_logo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255, unique=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='logos/')),
            ],
        ),
        migrations.RemoveField(
            model_name='producto',
            name='logo',
        ),
        migrations.AlterField(
            model_name='producto',
            name='marca',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rapidoysabrosoWEB.marca'),
        ),
    ]
