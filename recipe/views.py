from django.shortcuts import render

from recipe.models import RecipeProduct, Product, Recipe
from django.http import HttpResponse

# Create your views here.


def add_product_to_recipe(request):
    if request.method == "GET":
        recipe_id = request.GET.get("recipe_id", None)
        product_id = request.GET.get("product_id", None)
        if recipe_id is None or product_id is None:
            return HttpResponse("product_id or recipe_id are not passed", status=400)
        weight = request.GET.get("weight")
        if weight is None:
            return HttpResponse("weight are not passed", status=400)
        if int(weight) <= 0:
            return HttpResponse("Weight must be greater than 0", status=400)
        query = RecipeProduct.objects.get_or_create(
            recipe_id=Recipe.objects.get(id=recipe_id),
            product_id=Product.objects.get(id=product_id),
        )
        query[0].weight = weight
        query[0].save()
    return HttpResponse("ok", status=200)


def cook_recipe(request):
    if request.method == "GET":
        recipe_id = request.GET.get("recipe_id")
        if recipe_id is None:
            return HttpResponse("recipe_id are not passed", status=400)
        recipe_products = RecipeProduct.objects.select_related("product_id").filter(
            recipe_id__id=recipe_id
        )
        for product in recipe_products:
            product = product.product_id
            product.times_cook += 1
            product.save()
    return HttpResponse(status=200)


def show_recipes_without_product(request):
    if request.method == "GET":
        product_id = request.GET.get("product_id")
        if product_id is None:
            return HttpResponse("product_id are not passed", status=400)
        recipe_ids = RecipeProduct.objects.filter(
            product_id=product_id, weight__gt=10
        ).values_list("recipe_id_id", flat=True)
        queryset = Recipe.objects.exclude(id__in=list(recipe_ids)).distinct()
        return render(request, "recipe_table.html", {"recipes": queryset})
