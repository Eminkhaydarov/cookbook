from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=255)
    times_cook = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class RecipeProduct(models.Model):
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    weight = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ["recipe_id", "product_id"]
