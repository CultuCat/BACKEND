# Generated by Django 4.2.6 on 2023-11-19 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spaces', '0001_initial'),
        ('user', '0002_perfil_tags_preferits'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='espais_preferits',
            field=models.ManyToManyField(blank=True, related_name='perfils', to='spaces.space', verbose_name='Espais preferits'),
        ),
    ]