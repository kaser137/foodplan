# Generated by Django 4.2.5 on 2023-09-27 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, verbose_name='наименование')),
                ('specific', models.CharField(blank=True, choices=[('0', 'Рыба и морепродукты'), ('1', 'Мясо'), ('2', 'Зерновые'), ('3', 'Продукты пчеловодства'), ('4', 'Орехи и бобовые'), ('5', 'Молочные продукты')], db_index=True, max_length=2, null=True, verbose_name='вид')),
                ('caloric', models.PositiveSmallIntegerField(verbose_name='калории')),
            ],
            options={
                'verbose_name': 'продукт',
                'verbose_name_plural': 'продукты',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, verbose_name='наименование')),
                ('foods', models.ManyToManyField(related_name='receipts', to='foodplan_site.food', verbose_name='продукты')),
            ],
            options={
                'verbose_name': 'рецепт',
                'verbose_name_plural': 'рецепты',
                'ordering': ['name'],
            },
        ),
    ]
