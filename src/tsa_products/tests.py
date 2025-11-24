from django.test import TestCase  # noqa F401
from tsa_products.models import Category
from django.core.exceptions import ValidationError


# Create your tests here.

class CategoryTestCase(TestCase):
    
    def test_success_create_category(self):
        initial_number_of_categories = Category.objects.count()
        
        test_category = Category.objects.create(
            title="test",
            image= "test",
            base_price=0.0,
            max_amount_of_lettering_items= -1,
            height= 0.0,
            width=0.0
        )

        number_of_categories = Category.objects.count()

        self.assertEqual(
            initial_number_of_categories+1,
            number_of_categories
        )
    
    def test_failure_create_category_without_title(self):
        test_category = Category(
            title=None,                 
            image="test",
            base_price=0.0,
            max_amount_of_lettering_items=-1,
            height=0.0,
            width=0.0,
        )

        with self.assertRaises(ValidationError):
            test_category.full_clean()

        