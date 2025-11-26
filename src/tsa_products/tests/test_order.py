from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from tsa_products.models import Category, Order, Product, ProductVariation


class OrderTestCase(TestCase):
    @classmethod
    def setUpTestData(self):
        self.test_ordered_date = timezone.now()
        self.test_user_email = "test-email"
        self.test_user_first_name = "test-name"
        self.test_user_last_name = "test-surname"
        self.test_address1 = "Address line 1"
        self.test_address2 = "Address line 2"
        self.test_ordered = False
        self.test_product = ProductVariation.objects.create(
            product=Product.objects.create(
                category=Category.objects.create(title="test", image="test-path"), title="test-title"
            )
        )
        self.test_comment = "test-comment"

    def setUp(self):
        # Deletes all Order objects from the database to ensure a clean state before each test.
        Order.objects.all().delete()

    def test_successful_order_creation(self):
        """Tests the creation of an order."""
        order = Order.objects.create(
            ordered_date=self.test_ordered_date,
            user_email=self.test_user_email,
            user_first_name=self.test_user_first_name,
            user_last_name=self.test_user_last_name,
            address1=self.test_address1,
            address2=self.test_address2,
            ordered=self.test_ordered,
            product=self.test_product,
            comment=self.test_comment,
        )
        order.full_clean()
        self.assertEqual(Order.objects.count(), 1)

    def test_failure_order_creation_without_user_email(self):
        """Test the failure of order creation without a user_email."""
        with self.assertRaisesMessage(ValidationError, "{'user_email': ['This field cannot be blank.']}"):
            order = Order(user_first_name=self.test_user_first_name)
            order.full_clean()
            order.save()
        self.assertEqual(Order.objects.count(), 0)
