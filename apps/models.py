from django.db import models

# Create your models here.


class Product(models.Model):

    CATEGORY_CHOICES = (
        ('Dress', 'Dress'),
        ('Footwear', 'Footwear'),
        ('Heals', 'Heals'),
        ('Jwelery', 'Jwelery'),
        ('Pent', 'Pent'),
        ('Saree', 'Saree'),
        ('Shert', 'Shert'),
        ('Shoes', 'Shoes'),

    )

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )

    name = models.CharField(max_length=200)
    mainprice = models.IntegerField(default=None)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product/')
    description = models.TextField()

    @property
    def discount_percentage(self):
        if self.mainprice == 0:
            return 0

        return round(
            ((self.mainprice - self.price) / self.mainprice) * 100
        )

    def __str__(self):
        return self.name
