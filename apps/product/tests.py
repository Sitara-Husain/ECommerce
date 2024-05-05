"""
Product test cases
"""
from django.urls import reverse
from rest_framework import status

from apps.authentication.tests import BaseTestClass
from apps.product.models import Product


class ProductAPITestCase(BaseTestClass):
    """
    Test cases for Product API endpoints.
    """

    def setUp(self):
        """
        Set up initial data for each test case.
        """
        self.product_data = {
            "title": "Test Product",
            "description": "Test Description",
            "price": 10.5
        }
        self.product = Product.objects.create(**self.product_data)
        self.url = reverse('product:products-list')

    def test_create_product(self):
        """
        Test creating a new product.
        """
        product_data = self.product_data.copy()
        product_data.update({'title': 'New Product'})
        response = self.client.post(self.url, product_data, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_create_product(self):
        """
        Test creating a product with invalid data.
        """
        invalid_data = {
            "price": "10.5"
        }
        response = self.client.post(self.url, invalid_data, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_product(self):
        """
        Test retrieving a product.
        """
        response = self.client.get(f"{self.url}/{self.product.id}", **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_nonexistent_product(self):
        """
        Test retrieving a non-existent product.
        """
        response = self.client.get(f"{self.url}/10", **self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_product(self):
        """
        Test updating an existing product.
        """
        updated_data = {
            "title": "Updated Title",
            "description": "Updated Description",
            "price": 20.5
        }
        response = self.client.put(f"{self.url}/{self.product.id}", updated_data, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.title, updated_data["title"])

    def test_nonexistent_product(self):
        """
        Test updating a product with non-existing id.
        """
        updated_data = {
            "price": "invalid_price"
        }
        response = self.client.put(f"{self.url}/10", updated_data, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_update_product(self):
        """
        Test updating a product with invalid data.
        """
        invalid_data = {
            "description": "Updated Description",
            "price": "invalid_price"
        }
        response = self.client.put(f"{self.url}/{self.product.id}", invalid_data, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_product(self):
        """
        Test deleting an existing product.
        """
        response = self.client.delete(f"{self.url}/{self.product.id}", **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_nonexistent_product(self):
        """
        Test deleting a non-existent product.
        """
        response = self.client.delete(f"{self.url}/10", **self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

