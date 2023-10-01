import json
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from users.models import User


class Product(models.Model):
    SPECIFIC_OF_ALLERGEN = (
        ('10', 'Рыба и морепродукты'),
        ('2', 'Мясо'),
        ('3', 'Зерновые'),
        ('4', 'Продукты пчеловодства'),
        ('5', 'Орехи и бобовые'),
        ('6', 'Молочные продукты'),
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
    classic = models.BooleanField(
        'классик',
        default=False,
    )
    lowcarb = models.BooleanField(
        'низкоуглеводная',
        default=False,
    )
    vegan = models.BooleanField(
        'вегетарианская',
        default=False,
    )
    keto = models.BooleanField(
        'кето',
        default=False,
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
    description = models.TextField(
        'описание',
        blank=True,
        null=True,
    )
    breakfast = models.BooleanField(
        'завтрак',
        default=False,
    )
    dinner = models.BooleanField(
        'обед',
        default=False,
    )
    supper = models.BooleanField(
        'ужин',
        default=False,
    )
    dessert = models.BooleanField(
        'десерт',
        default=False,
    )

    def calories(self):
        calories = 0
        for product in self.products.all():
            product_calories = product.calories()
            if product_calories:
                calories += product_calories
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
        null=True,
        blank=True,
    )

    def calories(self):
        if self.amount:
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


class Order(models.Model):
    PERIOD = (
        (1, '1 месяц'),
        (3, '3 месяца'),
        (6, '6 месяцев'),
        (12, '12 месяцев'),
    )
    user = models.ForeignKey(
        User,
        verbose_name='клиент',
        on_delete=models.CASCADE,
        related_name='orders'
    )
    classic = models.BooleanField(
        'классик',
        default=False,
    )
    lowcarb = models.BooleanField(
        'низкоуглеводная',
        default=False,
    )
    vegan = models.BooleanField(
        'вегетарианская',
        default=False,
    )
    keto = models.BooleanField(
        'кето',
        default=False,
    )
    period = models.IntegerField(
        'период',
        choices=PERIOD,
        null=True,
        blank=True,
        db_index=True
    )
    allergic = models.CharField(
        verbose_name='аллергии',
        max_length=200,
        null=True,
        blank=True
    )
    breakfast = models.BooleanField(
        'завтрак',
        default=False,
    )
    dinner = models.BooleanField(
        'обед',
        default=False,
    )
    supper = models.BooleanField(
        'ужин',
        default=False,
    )
    dessert = models.BooleanField(
        'десерт',
        default=False,
    )
    paid = models.BooleanField(
        'оплачен',
        default=False,
    )
    person = models.PositiveSmallIntegerField(
        'количество персон',
        default=1
    )
    discount = models.PositiveSmallIntegerField(
        'процент скидки',
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0,
    )

    def cost(self):
        price = Price.objects.last()
        attrs_price = price.__dict__
        del attrs_price['id'], attrs_price['_state']
        amount = 0
        for attr in attrs_price:
            attr_order = getattr(self, attr, None)
            if attr_order:
                amount += self.period * 30 * attrs_price[attr]

        return amount * self.person * (1 - self.discount / 100)

    def diet(self):
        dietic = []
        if self.classic:
            dietic.append('класссика')
        if self.lowcarb:
            dietic.append('низкоуглеводная')
        if self.vegan:
            dietic.append('вегетарианская')
        if self.keto:
            dietic.append('кето')
        return dietic

    cost.short_description = 'стоимость'

    def set_allergic(self, x):
        self.allergic = json.dumps(x)

    def get_allergic(self):
        return json.loads(self.allergic)

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        name = '__'.join(self.diet())
        return f'{name}__{self.period} мес.'


class Price(models.Model):
    breakfast = models.FloatField('цена завтрака')
    dinner = models.FloatField('цена обеда')
    supper = models.FloatField('цена ужина')
    dessert = models.FloatField('цена дессерта')

    class Meta:
        verbose_name = 'прайс'
        verbose_name_plural = 'прайсы'

    def __str__(self):
        return f'прайс_{self.id}'


class Promo(models.Model):
    promokod = models.CharField(
        'промокод',
        max_length=300
    )
    discount = models.PositiveSmallIntegerField(
        'процент скидки',
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    class Meta:
        verbose_name = 'промокод'
        verbose_name_plural = 'промокоды'

    def __str__(self):
        return f'промокод: {self.promokod}, процент скидки: {self.discount}'
