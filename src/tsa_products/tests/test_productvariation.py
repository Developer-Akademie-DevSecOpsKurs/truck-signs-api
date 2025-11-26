from django.core.exceptions import ValidationError
from django.test import TestCase

from tsa_products.models import Category, LetteringItemVariation, Product, ProductColor, ProductVariation


class ProductVariationTestCase(TestCase):
    @classmethod
    def setUpTestData(self):
        self.test_product = Product.objects.create(
            category=Category.objects.create(title="test", image="test-path"), title="test-title"
        )
        self.test_product_color = ProductColor.objects.create(color_nickname="test-color-name")
        self.test_amount = 1

    def setUp(self):
        # Deletes all ProductVariation objects from the database to ensure a clean state before each test.
        ProductVariation.objects.all().delete()

    def test_successful_product_variation_creation(self):
        """Tests the creation of a product variation."""
        product_variation = ProductVariation.objects.create(
            product=self.test_product, product_color=self.test_product_color, amount=self.test_amount
        )
        product_variation.full_clean()
        self.assertEqual(ProductVariation.objects.count(), 1)

    def test_failure_product_variation_creation_without_product(self):
        """Test the failure of product variation creation without a product."""
        with self.assertRaisesMessage(ValidationError, "{'product': ['This field cannot be blank.']}"):
            product_variation = ProductVariation(amount=self.test_amount)
            product_variation.full_clean()
            product_variation.save()
        self.assertEqual(ProductVariation.objects.count(), 0)

    def test_success_get_all_lettering_items_sorted_by_id(self):
        """Test get_all_lettering_items method returns all related items."""
        # Arrange: setup necessary variables and data for the test
        test_product_variation = ProductVariation.objects.create(product=self.test_product)
        item1 = LetteringItemVariation.objects.create(product_variation=test_product_variation)
        item2 = LetteringItemVariation.objects.create(product_variation=test_product_variation)

        # Act: execute the (inter)action that should be tested
        #      -> retrieve all items sorted by their id
        all_items = test_product_variation.get_all_lettering_items()
        sorted_items = all_items.order_by("id")

        # Assert: Check if the actual result of the actions match the expectations
        self.assertQuerySetEqual(
            all_items.order_by("id"),
            [item1, item2],
            ordered=True,
        )
