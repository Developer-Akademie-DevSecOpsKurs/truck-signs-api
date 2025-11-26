from django.test import TestCase

from tsa_products.models import ProductColor


class ProductColorTestCase(TestCase):
    @classmethod
    def setUpTestData(self):
        self.test_color_in_hex = "#000000"
        self.test_color_nickname = "add nickname"

    def setUp(self):
        # Deletes all ProductColor objects from the database to ensure a clean state before each test.
        ProductColor.objects.all().delete()

    def test_successful_product_color_creation(self):
        """Tests the creation of a product color."""
        product_color = ProductColor.objects.create(
            color_in_hex=self.test_color_in_hex, color_nickname=self.test_color_nickname
        )
        product_color.full_clean()
        self.assertEqual(ProductColor.objects.count(), 1)
