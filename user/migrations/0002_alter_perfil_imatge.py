# Generated by Django 4.2.6 on 2023-11-11 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='imatge',
            field=models.CharField(default='https://www.calfruitos.com/es/fotos/pr_223_20190304145434.png'),
        ),
    ]
