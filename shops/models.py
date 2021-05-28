from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from core.compress import compress


class Banner(models.Model):
    title = models.CharField(max_length=50)
    link = models.URLField(max_length=240)
    image = models.ImageField(upload_to="banners/")
    block = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id', ]


class Category(models.Model):
    title = models.CharField(max_length=90)
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title


class Shop(models.Model):
    name = models.CharField(max_length=120)
    address = models.CharField(max_length=100, default="")
    owner = models.OneToOneField("users.User",  on_delete=models.CASCADE)
    category = models.ForeignKey(
        "shops.Category", related_name="shops", on_delete=models.DO_NOTHING, null=True)
    pan_number = models.CharField(max_length=90, default="")
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to='shops/', null=True)
    slug = models.SlugField()
    block = models.BooleanField(default=False)
    hide = models.BooleanField(default=False)
    is_trusted = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    limited = models.BooleanField(default=True)
    date_added = models.DateField(default=timezone.now, null=True)

    class Meta:
        verbose_name_plural = "Shops"
        ordering = ("-id",)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        try:
            shop = Shop.objects.get(pk=self.pk)
        except Shop.DoesNotExist:
            self.slug = slugify(self.name)
        if self.image:
            self.image = compress(self.image)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("shops:shop-detail", kwargs={"name": self.slug})
