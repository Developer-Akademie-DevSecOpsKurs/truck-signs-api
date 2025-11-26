from django.test import TestCase
from django.core.exceptions import ValidationError
from tsa_products.models import ProductVariation, Product, ProductColor, LetteringItemVariation, Category

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

    def test_success_get_all_lettering_items_method(self):
        """Test get_all_lettering_items method returns all related items."""
        test_product_variation = ProductVariation.objects.create(product=self.test_product)
        item1 = LetteringItemVariation.objects.create(product_variation=test_product_variation)
        item2 = LetteringItemVariation.objects.create(product_variation=test_product_variation)
        items = test_product_variation.get_all_lettering_items()
        self.assertQuerySetEqual(
            items.order_by("id"),
            [item1, item2],
            ordered=True,
        )
