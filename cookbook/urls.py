"""
URL configuration for cookbook project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from recipe.views import (
    add_product_to_recipe,
    cook_recipe,
    show_recipes_without_product,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("add_product_to_recipe", add_product_to_recipe),
    path("cook_recipe", cook_recipe, name="cook-recipe"),
    path(
        "show_recipes_without_product",
        show_recipes_without_product,
        name="show_recipes_without_product",
    ),
]
