# Generated by Django 3.2.25 on 2025-05-09 14:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0002_auto_20250509_1842'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='first_name',
            new_name='username',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='last_name',
        ),
    ]
