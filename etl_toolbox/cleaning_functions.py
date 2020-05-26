import re


def fingerprint(x):
    """Returns a lowercase, alphanumeric representation of x"""
    return re.sub(r'[^0-9a-z]', '', str(x).lower())


def clean_whitespace(x):
    """
    Returns x with:
     - all whitespace characters replaced with standard ASCII space (32)
     - consecutive whitespace condensed
     - leading/trailing whitespace removed

    Example input: ''' 123   abc 456
                                def\t\t 789\t'''
    Example output: '123 abc 456 def 789'

    Expects: str
    Returns: str

    Note: Does not remove unicode formatting characters without White_Space property:
     - \u180E \u200B \u200C \u200D \u2060 \uFEFF
    """

    pass
