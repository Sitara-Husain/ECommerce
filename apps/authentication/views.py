"""

"""
from datetime import datetime

from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.authentication.models import User
from apps.authentication.serializers import SignUpSerializer, LoginSerializer, UserSerializer
from apps.common.jwt import delete_tokens_for_user
from apps.common.msg import SUCCESS_KEY
from apps.common.utils import CustomResponse
from apps.common.viewsets import CustomModelViewSet, CustomModelCreateViewSet


class SignUpViewSet(CustomModelViewSet):
    """
    A view-set for user signup.
    This view-set allows users to sign up by sending a POST request with their registration details,
    such as email and password, to the API endpoint. The endpoint then creates a new user account in
    the database and returns a response.
    Supported HTTP methods: POST
    Attributes:
       The list of allowed HTTP methods for this view-set, which
            includes only POST in this case.
       The serializer class used to validate and deserialize
            the request data and create a new user account in the database.
    """
    http_method_names = ('post',)
    serializer_class = SignUpSerializer

    def create(self, request, *args, **kwargs):
        """
        Creates a new user with the specified details.
        :param request: WSGI request.
        :return: The created user object, or an error object if the creation fails.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(
                status.HTTP_201_CREATED, SUCCESS_KEY['register']
            ).success_response()
        return CustomResponse(status.HTTP_400_BAD_REQUEST, serializer.errors).error_response()


class LoginViewSet(CustomModelCreateViewSet):
    """
    A ViewSet for user login functionality.

    This class provides endpoints for user login. It includes methods for user authentication,
    token generation, and returning user information upon successful login.

    Attributes:
        serializer_class: The serializer class for login data.
        serializer_class_user: The serializer class for user data.
        http_method_names: Allowed HTTP methods for this view.
        queryset: The queryset of User objects.

    Methods:
        login_response: Generates and returns user information along with a token.
        create: Handles the POST request for user login.
    """
    serializer_class = LoginSerializer
    serializer_class_user = UserSerializer
    http_method_names = ('post',)
    queryset = User.objects

    def login_response(self, user: object, token: str):
        """
        To get user login response
        :param token: user tokens
        :param user: user object
        :return: user info
        """
        user.last_login = datetime.now()
        user.save()
        user_info = self.serializer_class_user(user).data
        user_info['tokens'] = token
        return user_info

    def create(self, request, *args, **kwargs):
        """
        Login with email and password.
        Note - for user login please remove group fields from body request
        :param request: post request object
        :param args: arguments
        :param kwargs: key arguments
        :return: json response
        """
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            user_obj = serializer.validated_data.get('user')
            serializer = self.serializer_class(user_obj).data
            user_info = self.login_response(user_obj, serializer['tokens'])
            return CustomResponse(
                status=status.HTTP_200_OK, detail=None
            ).success_response(data=user_info)
        return CustomResponse(
            status=status.HTTP_400_BAD_REQUEST, detail=serializer.errors
        ).error_response()


class LogoutViewSet(CustomModelCreateViewSet):
    """
    A ViewSet for user logout functionality.

    This class provides endpoints for user logout. Upon logout, all associated tokens
    are added to a blacklist, ensuring they cannot be used for further authentication.

    Attributes:
        http_method_names: Allowed HTTP methods for this view.
        permission_classes: The permission classes required for accessing this view.
        serializer_class: The serializer class for logout data (None as there's no data to serialize).

    Methods:
        create: Handles the POST request for user logout.
    """
    http_method_names = ('post',)
    permission_classes = [IsAuthenticated, ]
    serializer_class = None

    def create(self, request, *args, **kwargs):
        """
        adding all token in black list model
        Outstanding token have refresh token
        whenever user login refresh token is stored in this
        """
        delete_tokens_for_user(self, request)
        return CustomResponse(
            status.HTTP_200_OK, detail=SUCCESS_KEY['logout']
        ).success_response()
