"""
Validation messages used in project
"""
CHAR_LIMIT_SIZE = {
    'first_name_max': 50,
    'last_name_max': 50,
    'max_username': 50,
    'min_username': 6,
    'pass_min': 6,
    'pass_max': 15,
    'title': 255,
    'description': 5000,
}

VALIDATION = {
    'first_name': {
        "blank": "FIRST_NAME_BLANK",
        "invalid": "FIRST_NAME_INVALID",
        "min_length": "FIRST_NAME_MIN_LENGTH",
        "max_length": "FIRST_NAME_MAX_LENGTH",
        "required": "FIRST_NAME_REQUIRED"
    },
    'last_name': {
        "blank": "LAST_NAME_BLANK",
        "invalid": "LAST_NAME_INVALID",
        "min_length": "LAST_NAME_MIN_LENGTH",
        "max_length": "LAST_NAME_MAX_LENGTH",
        "required": "LAST_NAME_REQUIRED"
    },
    'username': {
        "blank": "USERNAME_BLANK",
        "invalid": "USERNAME_INVALID",
        "min_length": "USERNAME_MIN_LENGTH",
        "max_length": "USERNAME_MAX_LENGTH",
        "required": "USERNAME_REQUIRED"
    },
    'email': {
        "blank": "EMAIL_BLANK",
        "invalid": "EMAIL_INVALID",
        "min_length": "EMAIL_MIN_LENGTH",
        "max_length": "EMAIL_MAX_LENGTH",
        "required": "EMAIL_REQUIRED"
    },
    'password': {
        "blank": "PASSWORD_BLANK",
        "min_length": "PASSWORD_MAX_LENGTH",
        "max_length": "PASSWORD_MAX_LENGTH",
        "pattern": "PASSWORD_PATTERN",
        "required": "PASSWORD_REQUIRED"
    },
    "title": {
        "blank": "Title is a required field",
        "invalid": "Title is invalid. Please try again.",
        "required": "Title is a required field. Please fill it in.",
        "max_length": "Please ensure that the title does not exceed 255 characters in length.",
        "already_exists": "Product title already exists."
    },
    'description': {
        "blank": "Description field can't be blank.",
        "invalid": "Description contains invalid characters. Please try again.",
        "max_length": "Description is invalid. Please try again.",
        "required": "Description is a required field."
    },
    'price': {
        "blank": "Price field can't be blank.",
        "invalid": "Price contains invalid characters. Please try again.",
        "max_length": "Price is invalid. Please try again.",
        "required": "Price is a required field."
    },
}

ERROR_MESSAGE = {
    'email': {
        'exists': 'EMAIL_ALREADY_EXISTS',
        'invalid': 'EMAIL_INVALID',
        'not_verified': 'EMAIL_NOT_VERIFIED',
    },
    'password': {
        'invalid': 'INVALID_PASSWORD',
    },
    'user': {
        'inactive': 'ACCOUNT_DEACTIVATED'
    },
    'verification_otp': {
        'invalid': 'EMAIL_VERIFICATION_OTP_INVALID',
        'verified': 'EMAIL_ALREADY_VERIFIED'
    },
    'invalid_login': 'Invalid login'
}

# To define success key
SUCCESS_KEY = {
    "register": "Account created successfully! Welcome to our platform.",
    "logout": "You have been successfully logged out. See you again soon!",
    "product": {
        'created': 'Product created successfully',
        'updated': 'Product updated successfully',
        'deleted': 'Product deleted successfully',
    }
}
