from django.db import models


class Product(models.Model):
    SPECIFIC_OF_ALLERGEN = (
        ('0', 'Рыба и морепродукты'),
        ('1', 'Мясо'),
        ('2', 'Зерновые'),
        ('3', 'Продукты пчеловодства'),
        ('4', 'Орехи и бобовые'),
        ('5', 'Молочные продукты'),
    )
    name = models.CharField(
        'наименование',
        max_length=300,
    )
    specific = models.CharField(
        'аллерген',
        max_length=2,
        choices=SPECIFIC_OF_ALLERGEN,
        null=True,
        blank=True,
        db_index=True
    )
    caloric = models.PositiveSmallIntegerField(
        'калории',
    )

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ['name']

    def __str__(self):
        return self.name


class Receipt(models.Model):
    name = models.CharField(
        'наименование',
        max_length=300,
    )

    def calories(self):
        calories = 0
        for product in self.products.all():
            calories += product.calories()
        return calories

    calories.short_description = 'калории'

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'
        ordering = ['name']

    def __str__(self):
        return self.name


class ProductInReceipt(models.Model):
    receipt = models.ForeignKey(
        Receipt,
        verbose_name='рецепт',
        on_delete=models.CASCADE,
        related_name='products'
    )
    product = models.ForeignKey(
        Product,
        verbose_name='продукт',
        on_delete=models.CASCADE,
        related_name='receipts'
    )
    amount = models.PositiveSmallIntegerField(
        'граммы',
    )

    def calories(self):
        return round(self.amount * self.product.caloric / 100, 2)

    calories.short_description = 'калории'

    def allergen(self):
        return self.product.get_specific_display()

    allergen.short_description = 'алерген'

    class Meta:
        verbose_name = 'продукт в рецепте'
        verbose_name_plural = 'продукты в рецепте'
        ordering = ['product']

    def __str__(self):
        return f'{self.receipt}____{self.product}'
