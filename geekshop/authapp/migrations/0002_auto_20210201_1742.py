# Generated by Django 2.2 on 2021-02-01 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopuser',
            name='age',
            field=models.PositiveIntegerField(null=True, verbose_name='возраст'),
        ),
        migrations.AddField(
            model_name='shopuser',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='avatars'),
        ),
    ]