from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from shops.models import Category
from django.core.exceptions import ValidationError
from core.compress import compress


class Product(models.Model):
    shop = models.ForeignKey(
        "shops.Shop", related_name="products", on_delete=models.CASCADE)
    name = models.CharField(max_length=90)
    slug = models.SlugField(blank=True)
    price = models.PositiveIntegerField()
    discounted_price = models.PositiveIntegerField(blank=True, null=True)
    sub_title = models.TextField(blank=True, max_length=300)
    description = models.TextField(blank=True, max_length=3000)
    main_image = models.ImageField(
        upload_to="products/")
    image1 = models.ImageField(upload_to="products/", blank=True)
    image2 = models.ImageField(upload_to="products/", blank=True)
    image3 = models.ImageField(upload_to="products/", blank=True)
    image4 = models.ImageField(upload_to="products/", blank=True)
    in_stock = models.BooleanField(default=True)
    sku = models.CharField(blank=True, max_length=50)
    brand = models.CharField(max_length=60, blank=True)
    category = models.ForeignKey(
        "shops.Category",  related_name="products", on_delete=models.DO_NOTHING)
    date_added = models.DateField(default=timezone.now)
    date_edited = models.DateField(auto_now=True)
    featured = models.BooleanField(default=False)
    block = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("products:detail", kwargs={"pk": self.pk, "slug": self.slug})

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.discounted_price:
            if self.discounted_price > self.price:
                self.discounted_price = None
        try:
            product = Product.objects.get(pk=self.pk)
        except Product.DoesNotExist:
            self.slug = slugify(self.name)

        self.main_image = compress(self.main_image)

        if self.image1:
            self.image1 = compress(self.image1)

        if self.image2:
            self.image2 = compress(self.image2)

        if self.image3:
            self.image3 = compress(self.image3)

        if self.image4:
            self.image4 = compress(self.image4)

        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['-pk', ]
