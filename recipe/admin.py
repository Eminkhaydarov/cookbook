from django.contrib import admin
from recipe.models import Product, RecipeProduct, Recipe


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "times_cook",
    )
    list_display_links = ("id", "name")
    search_fields = ("name",)


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    list_display_links = ("id", "name")
    search_fields = ("name",)


class RecipeProductAdmin(admin.ModelAdmin):
    list_display = ("id", "recipe_id", "product_id", "weight")


admin.site.register(Product, ProductAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeProduct, RecipeProductAdmin)
