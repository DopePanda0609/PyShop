from django.db import models


CATEGORY_CHOICES = [
    ('vegetables-fruits', 'Vegetables & Fruits'),
    ('dairy-bread', 'Dairy & Bread'),
    ('snacks-drinks', 'Snacks & Drinks'),
    ('meat-fish', 'Meat & Fish'),
    ('cleaning', 'Cleaning'),
    ('bath-body', 'Bath & Body'),
    ('paper-goods', 'Paper Goods'),
    ('pet-care', 'Pet Care'),
]


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    stock = models.IntegerField()
    image_url = models.CharField(max_length=2083)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='dairy-bread')

    def __str__(self):
        return self.name


class Offer(models.Model):
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=255)
    discount = models.FloatField()
