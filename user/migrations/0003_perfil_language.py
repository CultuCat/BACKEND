# Generated by Django 4.2.6 on 2023-11-30 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_perfil_wantsnotifications'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='language',
            field=models.CharField(choices=[('en', 'ENGLISH'), ('es', 'SPANISH'), ('cat', 'CATALAN')], default='cat', max_length=3),
        ),
    ]
