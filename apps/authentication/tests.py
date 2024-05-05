"""
File use for test cases
"""
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.authentication.models import User
from apps.common.constants import RANDOM_KEY


class BaseTestClass(APITestCase):
    """
    Base test class for API test cases with initial data loading.
    """

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Load initial data for the TestCase.

        Comments:
        This method is a class method used to set up initial data for the test case.
        It is automatically executed before any test methods in the test class.
        In this specific implementation:
            The test user's 'is_active' flag is set to True and saved to the database.
            A RefreshToken is generated for the test user, and the associated access token is
            used to create the 'headers' dictionary for API authentication.
        """
        cls.user = User.objects.create(
            first_name="test",
            last_name="user",
            email="test@yopmail.com"
        )
        cls.user.is_active = True
        cls.user.save()
        refresh = RefreshToken.for_user(cls.user)
        cls.headers = {"HTTP_AUTHORIZATION": f"Bearer {refresh.access_token}"}

    @staticmethod
    def get_headers(user):
        """Returns headers of user."""
        refresh = RefreshToken.for_user(user)
        print(refresh.access_token)
        return {"HTTP_AUTHORIZATION": f"Bearer {refresh.access_token}"}


class SignUpTest(BaseTestClass):
    """
    Sign up user test cases
    """
    def setUp(self):
        """
        Set up test data
        """
        self.url = reverse("authentication:signup-list")
        self.data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test.user@yopmail.com',
            'password': RANDOM_KEY['valid_key']
        }

    def test_signup_with_valid_data(self):
        """
        Test user signup with valid data
        """
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signup_with_invalid_email(self):
        """
        Test user signup with missing required data
        """
        data = self.data.copy()
        del data['email']
        data['email'] = 'testusergmail.com'
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_with_required_first_name(self):
        """
        Test user signup with required first_name
        """
        data = self.data.copy()
        del data['first_name']
        data['first_name'] = ''
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_with_required_last_name(self):
        """
        Test user signup with required last_name
        """
        data = self.data.copy()
        del data['last_name']
        data['last_name'] = ''
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_with_missing_first_name(self):
        """
        Test user signup with missing first_name
        """
        data = self.data.copy()
        del data['first_name']
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_with_missing_last_name(self):
        """
        Test user signup with missing last_name
        """
        data = self.data.copy()
        del data['last_name']
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_with_invalid_password_length(self):
        """
        Test user signup with invalid password length
        """
        data = self.data.copy()
        data['password'] = RANDOM_KEY['short_key']
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data['password'] = RANDOM_KEY['long_key']
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginUserTest(APITestCase):
    """
    Login to the user
    """
    def setUp(self):
        """
        Set up test data
        """
        name = "TestUser@123"
        self.email = "testuser@gmail.com"
        self.username = name
        self.password = name
        user = User.objects.create(
            first_name="Test", last_name="Test",
            email=self.email.lower(),
            is_active=True
        )
        user.set_password(self.password)
        user.save()
        self.user = user
        self.url = reverse("authentication:login-list")
        self.data = {
            'email': self.email,
            'password': self.password
        }

    def test_login_with_valid_creds(self):
        """
        Test login with valid credentials
        """
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_with_invalid_creds(self):
        """
        Test login with invalid credentials
        """
        data = self.data.copy()
        data.update({'email': 'test@gmail.com', 'password': RANDOM_KEY['small_key']})
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_invalid_email(self):
        """
        Test login with invalid email
        """
        data = self.data.copy()
        data.update({'email': 'test@gmail.com'})
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_invalid_password(self):
        """
        Test login with invalid password
        """
        data = self.data.copy()
        data.update({'password': RANDOM_KEY['small_key']})
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LogoutTest(BaseTestClass):
    """
    Test cases for logout
    """
    def setUp(self):
        """
        Set up test data
        """
        super().setUp()
        self.url = reverse("authentication:logout-list")
        refresh_token = RefreshToken.for_user(self.user)
        self.header = {
            'HTTP_AUTHORIZATION': f'Bearer {refresh_token.access_token}',
            'Content-Type': "Application/json"
        }

    def test_logout_with_valid_token(self):
        """
        Test logout with valid token
        """
        response = self.client.post(self.url, **self.header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_with_invalid_token(self):
        """
        Test logout with valid token
        """
        header = self.header.update({'HTTP_AUTHORIZATION': 'shgdjgwdjwjw'})
        response = self.client.post(self.url, header)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
