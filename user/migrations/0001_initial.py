# Generated by Django 4.2.6 on 2023-11-19 08:40

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('imatge', models.CharField(default='https://www.calfruitos.com/es/fotos/pr_223_20190304145434.png')),
                ('bio', models.CharField(blank=True, default="Hey there, I'm using CultuCat", max_length=200, null=True, verbose_name='Bio')),
                ('puntuacio', models.IntegerField(default=0, verbose_name='Puntuacio')),
                ('isBlocked', models.BooleanField(default=False, verbose_name='Està bloquejat a la aplicacio')),
                ('wantsToTalk', models.BooleanField(default=True, verbose_name='La resta dels usuaris poden parlar amb ell')),
                ('isVisible', models.BooleanField(default=True, verbose_name='La resta dels usuaris el poden trobar')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
