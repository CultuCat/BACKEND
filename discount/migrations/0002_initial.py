# Generated by Django 4.2.6 on 2023-11-19 08:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('discount', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='discount',
            name='userDiscount',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.perfil'),
        ),
    ]
