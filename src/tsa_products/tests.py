from django.core.exceptions import ValidationError
from django.test import TestCase

from tsa_products.models import Category, LetteringItemCategory, ProductColor, Product

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

class LetteringItemCategoryTestCase(TestCase):

    @classmethod
    def setUpTestData(self):
        # Creates testing data for the test cases.
        self.test_title = "test"
        self.test_price = 0.0

    def setUp(self):
        # Ensures there are categories in the db before a test case is running.
        LetteringItemCategory.objects.all().delete()

    def test_successful_lettering_item_category_creation(self):
        # Tests the creation of a lettering item category
        lettering_item_category = LetteringItemCategory.objects.create(
            title=self.test_title,
            price=self.test_price
        )
        # Runs model validation for given data.
        lettering_item_category.full_clean()
        self.assertEqual(LetteringItemCategory.objects.count(), 1)

    def test_failure_lettering_category_creation_without_title(self):
        # Test the failure of lettering item category creation without a title
        with self.assertRaises(ValidationError):
            lettering_item_category = LetteringItemCategory(
                price=self.test_price,
            )
            lettering_item_category.full_clean()
            lettering_item_category.save()
        self.assertEqual(LetteringItemCategory.objects.count(), 0)
        self.assertRaisesMessage(ValidationError, "Missing Property 'title'. This field cannot be blank.")

class ProductColorTestCase(TestCase):

    @classmethod
    def setUpTestData(self):
        # Creates testing data for the test cases.
        self.test_color_in_hex = "#000000"
        self.test_color_nickname = "add nickname"

    def setUp(self):
        # Ensures there are categories in the db before a test case is running.
        ProductColor.objects.all().delete()

    def test_successful_product_color_creation(self):
        # Tests the creation of a product color
        product_color = ProductColor.objects.create(
            color_in_hex=self.test_color_in_hex,
            color_nickname=self.test_color_nickname
        )
        # Runs model validation for given data.
        product_color.full_clean()
        self.assertEqual(ProductColor.objects.count(), 1)

class ProductTestCase(TestCase):

    @classmethod
    def setUpTestData(self):
        # Creates testing data for the test cases.
        self.test_category = Category.objects.create(title="test", image="test-path")
        self.test_title = "test-title"

    def setUp(self):
        # Ensures there are categories in the db before a test case is running.
        Product.objects.all().delete()

    def test_successful_product_creation(self):
        # Tests the creation of a product
        product = Product.objects.create(
            category=self.test_category,
            title=self.test_title
        )
        # Runs model validation for given data.
        product.full_clean()
        self.assertEqual(Product.objects.count(), 1)

    def test_failure_product_creation_without_category(self):
        # Test the failure of product creation without a category
        with self.assertRaises(ValidationError):
            product = Product(
                title=self.test_title
            )
            product.full_clean()
            product.save()
        self.assertEqual(Product.objects.count(), 0)
        self.assertRaisesMessage(ValidationError, "Missing Property 'category'. This field cannot be blank.")

    def test_failure_product_creation_without_title(self):
        # Test the failure of product creation without a title
        with self.assertRaises(ValidationError):
            product = Product(
                category=self.test_category
            )
            product.full_clean()
            product.save()
        self.assertEqual(Product.objects.count(), 0)
        self.assertRaisesMessage(ValidationError, "Missing Property 'title'. This field cannot be blank.")
