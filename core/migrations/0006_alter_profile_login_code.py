# Generated by Django 4.0.2 on 2022-02-23 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_profile_login_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='login_code',
            field=models.CharField(blank=True, default='PW0DDK', max_length=200, null=True),
        ),
    ]