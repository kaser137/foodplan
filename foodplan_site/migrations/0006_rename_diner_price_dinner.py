# Generated by Django 4.2.5 on 2023-10-01 20:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodplan_site', '0005_rename_diner_order_dinner_order_discount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='price',
            old_name='diner',
            new_name='dinner',
        ),
    ]