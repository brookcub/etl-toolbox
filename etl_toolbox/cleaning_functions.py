import re


def fingerprint(x):
    """Returns a lowercase, alphanumeric representation of x"""
    return re.sub(r'[^0-9a-z]', '', str(x).lower())
