# Generated by Django 5.0.2 on 2024-03-10 17:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='user_type',
            new_name='account_type',
        ),
    ]
