from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
    return 'products/{0}'.format(filename)


class Trainer(models.Model):
    name = models.CharField(max_length=255)
    expertise = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    pid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet='abcdefgh12345')
    title = models.CharField(max_length=100, default="san")
    image = models.ImageField(upload_to=user_directory_path, default="product.jpg")
    description = models.TextField(null=True, blank=True, default="No description available")

    class Meta:
        verbose_name_plural = "Products"

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='product-images', default="product.jpg")

    class Meta:
        verbose_name_plural = "Product Images"
