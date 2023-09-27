# Generated by Django 4.2.5 on 2023-09-27 11:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodplan_site', '0002_alter_food_specific_delete_receipt'),
    ]

    operations = [
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, verbose_name='наименование')),
            ],
            options={
                'verbose_name': 'рецепт',
                'verbose_name_plural': 'рецепты',
                'ordering': ['name'],
            },
        ),
        migrations.RenameModel(
            old_name='Food',
            new_name='Product',
        ),
        migrations.CreateModel(
            name='ProductInReceipt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(verbose_name='граммы')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receipts', to='foodplan_site.product', verbose_name='продукт')),
                ('receipt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='foodplan_site.receipt', verbose_name='рецепт')),
            ],
        ),
    ]
