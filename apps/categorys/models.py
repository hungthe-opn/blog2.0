from django.db import models


# Create your models here.


class CategoryModel(models.Model):
    name = models.CharField(max_length=250)
    image = models.ImageField(max_length=100, null=True, blank=True)
    slug = models.SlugField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'
