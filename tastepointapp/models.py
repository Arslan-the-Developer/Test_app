from django.db import models
from django.conf import settings

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=50)
    product_price = models.IntegerField()
    prodcut_category = models.CharField(max_length=50)
    product_description = models.TextField(max_length=200)
    product_image = models.ImageField(upload_to="images")

    def __str__(self):
        return self.product_name
    


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class CartProduct(models.Model):    
    cart = models.ForeignKey(Cart, related_name='products', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_quantity = models.IntegerField()

    def __str__(self):
        return self.product.product_name
    
class BillingInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    billing_address = models.TextField(max_length=1400)
    billing_zip_code = models.CharField(max_length=100)
    billing_city = models.CharField(max_length=200,default="No City")

    def __str__(self):
        return self.user.username + "'s Order to Ship to " + self.billing_city