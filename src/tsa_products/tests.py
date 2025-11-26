from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from tsa_products.models import (
    Category,
    Comment,
    LetteringItemCategory,
    LetteringItemVariation,
    Order,
    Product,
    ProductColor,
    ProductVariation,
)

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
        # Tests the creation of a category.
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
        # Test the failure of category creation without a title.
        with self.assertRaisesMessage(ValidationError, "{'title': ['This field cannot be blank.']}"):
            category = Category(
                image=self.test_image,
            )
            category.full_clean()
            category.save()
        self.assertEqual(Category.objects.count(), 0)

    def test_failure_category_creation_without_image_path(self):
        # Test the failure of category creation without an image-path.
        with self.assertRaisesMessage(ValidationError, "{'image': ['This field cannot be blank.']}"):
            category = Category(
                title=self.test_title,
            )
            category.full_clean()
            category.save()
        self.assertEqual(Category.objects.count(), 0)


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
        # Tests the creation of a lettering item category.
        lettering_item_category = LetteringItemCategory.objects.create(title=self.test_title, price=self.test_price)
        # Runs model validation for given data.
        lettering_item_category.full_clean()
        self.assertEqual(LetteringItemCategory.objects.count(), 1)

    def test_failure_lettering_category_creation_without_title(self):
        # Test the failure of lettering item category creation without a title.
        with self.assertRaisesMessage(ValidationError, "{'title': ['This field cannot be blank.']}"):
            lettering_item_category = LetteringItemCategory(
                price=self.test_price,
            )
            lettering_item_category.full_clean()
            lettering_item_category.save()
        self.assertEqual(LetteringItemCategory.objects.count(), 0)


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
        # Tests the creation of a product color.
        product_color = ProductColor.objects.create(
            color_in_hex=self.test_color_in_hex, color_nickname=self.test_color_nickname
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
        self.test_image = "test-path"
        self.test_detail_image = "test-detail-path"
        self.test_is_uploaded = False

    def setUp(self):
        # Ensures there are categories in the db before a test case is running.
        Product.objects.all().delete()

    def test_successful_product_creation(self):
        # Tests the creation of a product
        product = Product.objects.create(
            category=self.test_category,
            title=self.test_title,
            image=self.test_image,
            detail_image=self.test_detail_image,
            is_uploaded=self.test_is_uploaded,
        )
        # Runs model validation for given data.
        product.full_clean()
        self.assertEqual(Product.objects.count(), 1)

    def test_failure_product_creation_without_category(self):
        # Test the failure of product creation without a category.
        with self.assertRaisesMessage(ValidationError, "{'category': ['This field cannot be null.']}"):
            product = Product(title=self.test_title)
            product.full_clean()
            product.save()
        self.assertEqual(Product.objects.count(), 0)

    def test_failure_product_creation_without_title(self):
        # Test the failure of product creation without a title.
        with self.assertRaisesMessage(ValidationError, "{'title': ['This field cannot be blank.']}"):
            product = Product(category=self.test_category)
            product.full_clean()
            product.save()
        self.assertEqual(Product.objects.count(), 0)


class ProductVariationTestCase(TestCase):

    @classmethod
    def setUpTestData(self):
        # Creates testing data for the test cases.
        self.test_product = Product.objects.create(
            category=Category.objects.create(title="test", image="test-path"), title="test-title"
        )
        self.test_product_color = ProductColor.objects.create(color_nickname="test-color-name")
        self.test_amount = 1

    def setUp(self):
        # Ensures there are categories in the db before a test case is running.
        ProductVariation.objects.all().delete()

    def test_successful_product_variation_creation(self):
        # Tests the creation of a product variation.
        product_variation = ProductVariation.objects.create(
            product=self.test_product, product_color=self.test_product_color, amount=self.test_amount
        )
        # Runs model validation for given data.
        product_variation.full_clean()
        self.assertEqual(ProductVariation.objects.count(), 1)

    def test_failure_product_variation_creation_without_product(self):
        # Test the failure of product variation creation without a product.
        with self.assertRaisesMessage(ValidationError, "{'product': ['This field cannot be blank.']}"):
            product_variation = ProductVariation(amount=self.test_amount)
            product_variation.full_clean()
            product_variation.save()
        self.assertEqual(ProductVariation.objects.count(), 0)

    def test_success_get_all_lettering_items_method(self):
        test_product_variation = ProductVariation.objects.create(product=self.test_product)
        item1 = LetteringItemVariation.objects.create(product_variation=test_product_variation)
        item2 = LetteringItemVariation.objects.create(product_variation=test_product_variation)

        items = test_product_variation.get_all_lettering_items()
        self.assertQuerySetEqual(
            items.order_by("id"),
            [item1, item2],
            ordered=True,
        )


class LetteringItemVariationTestCase(TestCase):

    @classmethod
    def setUpTestData(self):
        # Creates testing data for the test cases.
        self.test_lettering_item_category = LetteringItemCategory.objects.create(title="test")
        self.test_lettering = "test"
        self.test_product_variation = ProductVariation.objects.create(
            product=Product.objects.create(
                category=Category.objects.create(title="test", image="test-path"), title="test-title"
            )
        )

    def setUp(self):
        # Ensures there are categories in the db before a test case is running.
        LetteringItemVariation.objects.all().delete()

    def test_successful_lettering_item_variation_creation(self):
        # Tests the creation of a lettering item variation.
        lettering_item_variation = LetteringItemVariation.objects.create(
            lettering_item_category=self.test_lettering_item_category,
            lettering=self.test_lettering,
            product_variation=self.test_product_variation,
        )
        # Runs model validation for given data.
        lettering_item_variation.full_clean()
        self.assertEqual(LetteringItemVariation.objects.count(), 1)

    def test_failure_lettering_item_variation_creation_without_lettering(self):
        # Test the failure of lettering item variation creation without a lettering.
        with self.assertRaisesMessage(ValidationError, "{'lettering': ['This field cannot be blank.']}"):
            lettering_item_variation = LetteringItemVariation(product_variation=self.test_product_variation)
            lettering_item_variation.full_clean()
            lettering_item_variation.save()
        self.assertEqual(LetteringItemVariation.objects.count(), 0)


class OrderTestCase(TestCase):

    @classmethod
    def setUpTestData(self):
        # Creates testing data for the test cases.
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
        # Ensures there are categories in the db before a test case is running.
        Order.objects.all().delete()

    def test_successful_order_creation(self):
        # Tests the creation of an order.
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
        # Runs model validation for given data.
        order.full_clean()
        self.assertEqual(Order.objects.count(), 1)

    def test_failure_order_creation_without_user_email(self):
        # Test the failure of order creation without an user_email.
        with self.assertRaisesMessage(ValidationError, "{'user_email': ['This field cannot be blank.']}"):
            order = Order(user_first_name=self.test_user_first_name)
            order.full_clean()
            order.save()
        self.assertEqual(Order.objects.count(), 0)


class CommentTestCase(TestCase):

    @classmethod
    def setUpTestData(self):
        # Creates testing data for the test cases.
        self.test_user_email = "test-email"
        self.test_image = "test-path"
        self.test_text = "test-text"
        self.test_visible = False

    def setUp(self):
        # Ensures there are categories in the db before a test case is running.
        Comment.objects.all().delete()

    def test_successful_comment_creation(self):
        # Tests the creation of a comment.
        comment = Comment.objects.create(
            user_email=self.test_user_email, image=self.test_image, text=self.test_text, visible=self.test_visible
        )
        # Runs model validation for given data.
        comment.full_clean()
        self.assertEqual(Comment.objects.count(), 1)

    def test_failure_comment_creation_without_user_email(self):
        # Test the failure of comment creation without an user mail address.
        with self.assertRaisesMessage(ValidationError, "{'user_email': ['This field cannot be blank.']}"):
            comment = Comment(image=self.test_image)
            comment.full_clean()
            comment.save()
        self.assertEqual(Comment.objects.count(), 0)

    def test_failure_comment_creation_without_image(self):
        # Test the failure of comment creation without an image-path.
        with self.assertRaisesMessage(ValidationError, "{'image': ['This field cannot be blank.']}"):
            comment = Comment(user_email=self.test_user_email)
            comment.full_clean()
            comment.save()
        self.assertEqual(Comment.objects.count(), 0)
