from django.test import TestCase

# Create your tests here.
from django.test import TestCase, RequestFactory
from django.urls import reverse

from .models import Recipe, Product, RecipeProduct


class AddProductToRecipeTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.recipe = Recipe.objects.create(name="test")
        self.product = Product.objects.create(name="test")
        self.url = "/add_product_to_recipe"

    def test_add_product_to_recipe_missing_ids(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.content.decode(), "product_id or recipe_id are not passed"
        )
        query = RecipeProduct.objects.filter(
            product_id=self.product.id, weight=100, recipe_id=self.recipe
        )
        self.assertEqual(query.count(), 0)

    def test_add_product_to_recipe_missing_weight(self):
        response = self.client.get(
            self.url, data={"recipe_id": self.recipe.id, "product_id": self.product.id}
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), "weight are not passed")
        query = RecipeProduct.objects.filter(
            product_id=self.product.id, weight=100, recipe_id=self.recipe
        )
        self.assertEqual(query.count(), 0)

    def test_add_product_to_recipe_invalid_weight(self):
        response = self.client.get(
            self.url,
            data={
                "recipe_id": self.recipe.id,
                "product_id": self.product.id,
                "weight": -100,
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), "Weight must be greater than 0")
        query = RecipeProduct.objects.filter(
            product_id=self.product.id, weight=100, recipe_id=self.recipe
        )
        self.assertEqual(query.count(), 0)

    def test_add_product_to_recipe_success(self):
        response = self.client.get(
            self.url,
            data={
                "recipe_id": self.recipe.id,
                "product_id": self.product.id,
                "weight": 100,
            },
        )

        query = RecipeProduct.objects.get(
            product_id=self.product.id, weight=100, recipe_id=self.recipe
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(query.weight, 100)
        self.assertEqual(query.recipe_id.id, self.recipe.id)
        self.assertEqual(query.product_id.id, self.product.id)


class CookRecipeTest(TestCase):
    def setUp(self):
        self.recipe = Recipe.objects.create(name="test")
        self.product = Product.objects.create(name="test")
        RecipeProduct.objects.create(product_id=self.product, recipe_id=self.recipe)

    def test_cook_recipe_successful(self):
        response = self.client.get(
            reverse("cook-recipe"), {"recipe_id": self.recipe.id}
        )
        self.assertEqual(response.status_code, 200)
        self.product.refresh_from_db()
        self.assertEqual(self.product.times_cook, 1)

    def test_cook_recipe_missing_recipe_id(self):
        response = self.client.get(reverse("cook-recipe"))
        self.assertEqual(response.status_code, 400)
        self.assertIn("recipe_id are not passed", response.content.decode())

    def test_cook_recipe_recipe_product_does_not_exist(self):
        response = self.client.get(reverse("cook-recipe"), {"recipe_id": 999})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(RecipeProduct.objects.filter(recipe_id=999).count(), 0)


class RecipeViewTests(TestCase):
    def setUp(self):
        self.recipe_1 = Recipe.objects.create(name="Recipe 1")
        self.recipe_2 = Recipe.objects.create(name="Recipe 2")
        self.recipe_3 = Recipe.objects.create(name="Recipe 3")
        self.recipe_4 = Recipe.objects.create(name="Recipe 4")

        self.product_1 = Product.objects.create(name="Product 1")
        self.product_2 = Product.objects.create(name="Product 2")
        self.product_3 = Product.objects.create(name="Product 3")
        self.product_4 = Product.objects.create(name="Product 4")

        self.recipe_product_1 = RecipeProduct.objects.create(
            recipe_id=self.recipe_1, product_id=self.product_1, weight=50
        )
        self.recipe_product_4 = RecipeProduct.objects.create(
            recipe_id=self.recipe_2, product_id=self.product_2, weight=50
        )
        self.recipe_product_2 = RecipeProduct.objects.create(
            recipe_id=self.recipe_2, product_id=self.product_1, weight=50
        )
        self.recipe_product_3 = RecipeProduct.objects.create(
            recipe_id=self.recipe_3, product_id=self.product_1, weight=50
        )
        self.recipe_product_5 = RecipeProduct.objects.create(
            recipe_id=self.recipe_3, product_id=self.product_3, weight=5
        )
        self.recipe_product_5 = RecipeProduct.objects.create(
            recipe_id=self.recipe_4, product_id=self.product_3, weight=50
        )

    def test_show_recipes_without_product(self):
        url = reverse("show_recipes_without_product")
        params = {"product_id": self.product_1.id}
        response = self.client.get(url, params)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipe_table.html")
        expected_recipe_ids = [4]
        returned_recipe_ids = [recipe.id for recipe in response.context["recipes"]]
        self.assertEqual(returned_recipe_ids, expected_recipe_ids)

        params = {"product_id": self.product_3.id}
        response = self.client.get(url, params)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipe_table.html")
        expected_recipe_ids = 4
        returned_recipe_ids = [recipe.id for recipe in response.context["recipes"]]
        self.assertNotIn(container=returned_recipe_ids, member=expected_recipe_ids)

    def test_show_recipes_without_product_missing_product_id(self):
        url = reverse("show_recipes_without_product")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 400)

        self.assertEqual(response.content.decode(), "product_id are not passed")
