from django.db import models
from django.utils import timezone
from django.utils.text import slugify
import uuid
import os

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(default='', editable=False, max_length=200)
    price = models.FloatField(default=100)
    stock = models.IntegerField(default=1)

    image = models.ImageField(default='default.jpg', upload_to='para_pics', max_length=500)
    prod_type = models.CharField(max_length=100, default='default')
    source = models.CharField(max_length=100, default='default')
    picture_path = models.CharField(max_length=500, default='default')
    date_posted = models.DateTimeField(default=timezone.now)

    uid = models.CharField(default='', editable=False, max_length=100)


    def save(self, *args, **kwargs):

        if self.uid == '':
            self.uid = uuid.uuid4().hex

        if self.name == 'test':
            self.name = 'produit ' + self.uid[:6]

        if self.slug in 'test':
            self.slug = slugify(self.name)

        if self.uid not in self.image.url:
            new_path = f'para_pics/{self.uid}.jpeg'
            print(self.picture_path)
            os.rename(self.picture_path, 'media/' + new_path)
            self.image = new_path

        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.price}"