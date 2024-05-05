"""
User Sign up related serializer
"""
import re
from rest_framework_simplejwt.tokens import RefreshToken

# python import

# django import
from rest_framework import serializers
from apps.authentication.models import User, CustomUserAccessToken
from apps.common.constants import REGEX_VALID
from apps.common.msg.validation_msg import CHAR_LIMIT_SIZE, VALIDATION, ERROR_MESSAGE


def signup_email_validation(value):
    """
    TO validate email
    :param value:
    :return: error or value
    """
    if User.objects.filter(email=value.lower()).exists():
        raise serializers.ValidationError(ERROR_MESSAGE['email']['exists'])
    return value


def password_validation(value):
    """
    To validate password
    :param value: value
    :return: error or value
    """
    value = value.strip()
    if re.match(REGEX_VALID['password'], value):
        return value
    return serializers.ValidationError(VALIDATION['password']['pattern'])


class SignUpSerializer(serializers.ModelSerializer):
    """
    Validate signup data and creating a new user.
    create: validate request data for auth-user-instance creation
    Return auth-user-instance object
    Return modified serializer (add new keys-values required for processing, and those keys are not
    required for processing, remove from serializer data) data of auth-user-instance
    """
    first_name = serializers.CharField(
        required=True, max_length=CHAR_LIMIT_SIZE['first_name_max'],
        error_messages=VALIDATION['first_name']
    )
    last_name = serializers.CharField(
        required=True, max_length=CHAR_LIMIT_SIZE['last_name_max'],
        error_messages=VALIDATION['last_name']
    )
    email = serializers.EmailField(
        required=True,
        validators=[signup_email_validation],
        error_messages=VALIDATION['email']
    )
    password = serializers.CharField(
        required=True, min_length=CHAR_LIMIT_SIZE['pass_min'],
        max_length=CHAR_LIMIT_SIZE['pass_max'],
        validators=[password_validation],
        error_messages=VALIDATION['password']
    )

    def create(self, validated_data):
        """
        to add a new user
        :return: instance
        """
        password = validated_data.pop('password')
        instance = super(
            SignUpSerializer, self
        ).create(validated_data)
        instance.set_password(password)
        instance.is_active = True
        instance.save()
        return instance

    class Meta:
        """
        Meta class for SignUpSerializer
        """
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'password'
        )


class LoginValidation(serializers.ModelSerializer):
    """
    To validate login
    """

    def validate(self, attrs):
        """
        Validate password those associated with user(email)
        :param attrs:
        :return: attrs or error_message
        """
        password = attrs.get("password")
        email = attrs.get("email")
        user = User.objects.filter(email__iexact=email).first()
        raise_data = {}
        if user is None or not user.check_password(password):
            raise_data = {
                'invalid': ERROR_MESSAGE['invalid_login']
            }
        # Check if raise_data
        if raise_data:
            raise serializers.ValidationError(raise_data)
        attrs.update({"user": user})
        return attrs


class GenerateToken(serializers.ModelSerializer):
    """
    Class used for generating and return tokens
    """
    tokens = serializers.SerializerMethodField()

    @staticmethod
    def get_tokens(user):
        """
        To get user tokens
        :param user: user instance
        :return: token dict
        """
        user_obj = user
        # Generate token
        refresh = RefreshToken.for_user(user_obj)
        if refresh:
            access_token = refresh.access_token
            CustomUserAccessToken.objects.update_or_create(
                user=user_obj,
                token=str(access_token),
                defaults={'jti': refresh.payload['jti'], 'exp': refresh.payload['exp']}
            )
        return {
            'refresh': str(refresh),
            'access': str(access_token),
        }


class LoginSerializer(LoginValidation, GenerateToken):
    """
    Used to verify the login credentials and return the login response
    """
    email = serializers.EmailField(
        error_messages=VALIDATION["email"],
        required=True
    )
    password = serializers.CharField(
        required=True,
        error_messages=VALIDATION['password']
    )

    def to_representation(self, instance):
        """
        Convert the model instance to a Python representation for serialization.
        """
        rep = super().to_representation(instance)
        rep.pop('password', None)
        return rep

    class Meta:
        """
        meta class for LoginSerializer
        """
        model = User
        fields = ('email', 'password', 'tokens')


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer to get user details
    """

    class Meta:
        """
        Define fields for this serializer
        """
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'email', 'is_active'
        )
