from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


# ----------------------------------------------------------------------------
# -------------------------- Product LIsting ---------------------------------
# ----------------------------------------------------------------------------

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

    @property
    def discount_percentage(self):
        if self.mainprice == 0:
            return 0

        return round(
            ((self.mainprice - self.price) / self.mainprice) * 100
        )

    def __str__(self):
        return self.name


# ----------------------------------------------------------------------------
# ------------------------------  Admin Model  -------------------------------
# ----------------------------------------------------------------------------

class UserManager(BaseUserManager):
    def create_user(self , email , name , city , password = None):
        if not email:
            raise ValueError("Email is required")
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            city=city
        )
        user.set_password(password)
        user.save(using=self._db)
        return user  
    
    def create_superuser(self, email, name, city, password=None):
        user = self.create_user(
            email=email,
            name=name,
            city=city,
            password=password
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.is_seller = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email  = models.EmailField( max_length=254 , unique=True)
    name = models.TextField(max_length=250)
    city = models.TextField(max_length=250)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['name', 'city']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
    
