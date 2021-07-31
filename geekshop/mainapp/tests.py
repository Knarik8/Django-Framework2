from django.test import TestCase
from django.test.client import Client
from mainapp.models import Product, ProductCategory
from django.core.management import call_command

class TestMainappSmoke(TestCase):
    status_code_success = 200

    def setUp(self):
       cat_1 = ProductCategory.objects.create(
           name = 'cat 1'
       )
       for i in range(100):
           Product.objects.create(
               category=cat_1,
               name= f'prod {i}'
           )
       self.client = Client()

    def get_products_item(self):
        return Product.objects.all()

    def test_main_app_urls(self):
       response = self.client.get('/')
       self.assertEqual(response.status_code, self.status_code_success)

    def test_products_urls(self):
        for product_item in self.get_products_item():
            response = self.client.get(f'/products/product/{product_item.pk}/')
            self.assertEqual(response.status_code, self.status_code_success)
   #
   #     response = self.client.get('/contact/')
   #     self.assertEqual(response.status_code, 200)
   #
   #     response = self.client.get('/products/')
   #     self.assertEqual(response.status_code, 200)
   #
   #     response = self.client.get('/products/category/0/')
   #     self.assertEqual(response.status_code, 200)
   #
   #     for category in ProductCategory.objects.all():
   #         response = self.client.get(f'/products/category/{category.pk}/')
   #         self.assertEqual(response.status_code, 200)
   #
   #     for product in Product.objects.all():
   #         response = self.client.get(f'/products/product/{product.pk}/')
   #         self.assertEqual(response.status_code, 200)
   #
   # def tearDown(self):
   #      call_command('sqlsequencereset', 'mainapp', 'authapp', 'ordersapp',\
   #                   'basketapp')
