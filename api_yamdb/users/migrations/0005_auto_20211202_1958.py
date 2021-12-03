# Generated by Django 2.2.16 on 2021-12-02 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20211202_1938'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='code_confirmation',
            new_name='confirmation_code',
        ),
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('USER', 'Аутентифицированный пользователь'), ('MODERATOR', 'Модератор'), ('ADMIN', 'Администратор'), ('SUPERUSER', 'Суперюзер Django')], default='user', max_length=35),
        ),
    ]