from django.core.exceptions import ValidationError
from django.test import TestCase

from tsa_products.models import Category

# Create your tests here.


class CategoryTestCase(TestCase):

    @classmethod
    def setUpTestData(self):
        # Creates testing data for the test cases.
        self.test_title = "test"
        self.test_image = "test-path"
        self.test_base_price = 0.0
        self.test_max_amount_of_lettering_items = -1
        self.test_height = 0.0
        self.test_width = 0.0

    def setUp(self):
        # Ensures there are categories in the db before a test case is running.
        Category.objects.all().delete()

    def test_successful_category_creation(self):
        # Tests the creation of a category
        category = Category.objects.create(
            title=self.test_title,
            image=self.test_image,
            base_price=self.test_base_price,
            max_amount_of_lettering_items=self.test_max_amount_of_lettering_items,
            height=self.test_height,
            width=self.test_width,
        )
        # Runs model validation for given data.
        category.full_clean()
        self.assertEqual(Category.objects.count(), 1)

    def test_failure_category_creation_without_title(self):
        # Test the failure of category creation without a title
        with self.assertRaises(ValidationError):
            category = Category(
                image=self.test_image,
            )
            category.full_clean()
            category.save()
        self.assertEqual(Category.objects.count(), 0)
        self.assertRaisesMessage(ValidationError, "Missing Property 'title'. This field cannot be blank.")

    def test_failure_category_creation_without_image_path(self):
        # Test the failure of category creation without an image-path
        with self.assertRaises(ValidationError):
            category = Category(
                title=self.test_title,
            )
            category.full_clean()
            category.save()
        self.assertEqual(Category.objects.count(), 0)
        self.assertRaisesMessage(ValidationError, "Missing Property 'image'. This field cannot be blank.")
