# Generated by Django 5.0.6 on 2024-07-03 09:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gameshopapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='manufacturer',
            new_name='developer',
        ),
    ]
