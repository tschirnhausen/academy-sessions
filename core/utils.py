from django.utils.crypto import get_random_string

# User token generator

def token_generator():
    return get_random_string(32)
