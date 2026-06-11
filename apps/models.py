from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


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
    stock = models.TextField(max_length=210)
    description = models.TextField()
    tags = models.CharField(max_length=500, blank=True)
    is_new = models.BooleanField(default=False)

    @property
    def discount_percentage(self):
        if self.mainprice == 0:
            return 0

        return round(
            ((self.mainprice - self.price) / self.mainprice) * 100
        )

    def __str__(self):
        return self.name


class CustomerModel(models.Model):
    email = models.EmailField(max_length=254, unique=True)
    name = models.TextField(max_length=250)
    city = models.TextField(max_length=250)
    password = models.TextField(null=False)
    is_seller = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(CustomerModel, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    is_shipped = models.BooleanField(default=False)


# class UserManager(BaseUserManager):
#     def create_user(self, email, name, city, password=None):
#         if not email:
#             raise ValueError("Email is required")
#         user = self.model(
#             email=self.normalize_email(email),
#             name=name,
#             city=city
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, name, city, password=None):
#         user = self.create_user(
#             email=email,
#             name=name,
#             city=city,
#             password=password
#         )
#         user.is_superuser = True
#         user.is_staff = True
#         user.is_active = True
#         user.is_seller = True
#         user.save(using=self._db)
#         return user


# class User(AbstractBaseUser):
#     email = models.EmailField(max_length=254, unique=True)
#     name = models.TextField(max_length=250)
#     city = models.TextField(max_length=250)

#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#     is_seller = models.BooleanField(default=False)

#     objects = UserManager()

#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = ['name', 'city']

#     def __str__(self):
#         return self.email

#     def has_perm(self, perm, obj=None):
#         return self.is_superuser

#     def has_module_perms(self, app_label):
#         return self.is_superuser

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, name, city, password=None, is_seller=False):
        if not email:
            raise ValueError("Email required")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            city=city,
            is_seller=is_seller
        )

        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name="Fenil", city="Surat", password=None):
        user = self.create_user(
            email=email,
            name=name,
            city=city,
            password=password,
            is_seller=True
        )

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "city"]

    def __str__(self):
        return self.email
    
    
class Cart(models.Model):
    customer_id = models.IntegerField()

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.name


class contectmassage(models.Model):
    user = models.ForeignKey(CustomerModel, on_delete=models.CASCADE)
    subject = models.CharField(max_length=250)
    message = models.TextField()
   
    is_resolved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name
