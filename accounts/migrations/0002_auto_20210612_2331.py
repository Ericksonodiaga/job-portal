# Generated by Django 3.2.4 on 2021-06-12 20:31

import accounts.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='cv',
            field=models.FileField(default='media/default.pdf', upload_to='cv/', validators=[accounts.validators.validate_file_extension]),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(default='', max_length=25, validators=[accounts.validators.validate_phone_number]),
        ),
        migrations.CreateModel(
            name='OTPModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp_code', models.CharField(max_length=8, unique=True)),
                ('expiry', models.DateTimeField()),
                ('UUID', models.CharField(max_length=50, unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
