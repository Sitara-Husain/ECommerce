"""
Constants used in application
"""
API_TITLE = 'E-Commerce API Document'
API_VERSION = 'v1'
API_DESCRIPTION = 'API for E-Commerce'

REGEX_VALID = {
    "password": "^[A-Za-z0-9~'`!@#$%^&*()_+,.-]*$",
    "email": '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
}

RANDOM_KEY = {
    'valid_key': 'Test@123',
    'long_key': 'thispasswordiswaytoolong',
    'strong_key': '}p[@M~NX@@{Ud+=z~1',
    'short_key': 'short',
    'small_key': 'test@123',
}
