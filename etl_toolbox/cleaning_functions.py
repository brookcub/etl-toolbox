import ast
import collections.abc
import re


def fingerprint(x, special_characters=''):
    """
    Returns a lowercase, alphanumeric representation of x

    Example input: '(Aa_Bb_Cc)'
    Example output: 'aabbcc'

    Expects: anything that can be meaningfully cast to a str
    Returns: str

    Optional parameters:
        special_characters (str): special characters to allow in the fingerprint
    """
    remove_regex = r'[^0-9a-z{}]'.format(re.escape(special_characters))

    return re.sub(remove_regex, '', str(x).lower())


NULL_INDICATORS = [
    '',
    'blocked',
    'empty',
    'invalid',
    'na',
    'nan',
    'nbsp',
    'none',
    'notavailable',
    'notset',
    'np',
    'null',
    'removed',
    'unavailable',
    'unidentified',
    'unknown'
]

FALSEY_INDICATORS = [
    'false',
    '0'
]


def clean_null(x, falsey_is_null=False, special_characters=''):
    """
    Returns None if x is null-indicating, else returns x

    x is considered null-indicating if any of the following are true:
     - x is None
     - len(x) == 0
     - fingerprint(x) in NULL_INDICATORS
     - falsey_is_null == True and !x
     - falsey_is_null == True and fingerprint(x) in FALSEY_INDICATORS
     - x is an iterable consisting of all null-indicating values
     - x evaluates as a Python literal that is null-indicating

    Example input: 'Unknown'
    Example output: None

    Expects: any
    Returns: None or x

    Optional parameters:
        falsey_is_null (bool):
            True = all falsey values will be considered null-indicating
            False = not all falsey values will be considered null-indicating
            default is False

        special_characters (str):
            special characters to allow in the fingerprint
    """

    if x is None:
        return None

    # Check if x is a Sized object with length 0
    if isinstance(x, collections.abc.Sized) and len(x) == 0:
        return None

    # Check if fingerprint of x is in NULL_INDICATORS
    x_fingerprint = fingerprint(x, special_characters)
    if x_fingerprint in NULL_INDICATORS:
        return None

    # Optional falsey_is_null checks
    if falsey_is_null:
        if not x:
            return None
        if x_fingerprint in FALSEY_INDICATORS:
            return None

    # Check if x is an iterable consisting of all null-indicating values
    #     Strings are excluded to improve performance. They will
    #     never be null-indicating in this check.
    if isinstance(x, collections.abc.Iterable) and not isinstance(x, str):
        contains_non_null = False

        for item in x:
            if clean_null(item, falsey_is_null) is not None:
                contains_non_null = True
                break

        if not contains_non_null:
            return None

    # Check if x evaluates as a Python literal that is null-indicating
    #     Limit to strings that are parseable to list/set/dict/tuple
    #     or special string literals to improve performance. Any
    #     other strings will never be null-indicating in this check.
    if isinstance(x, str) and (x[:1] in ('[','{','(') or x[1:2] in ('"',"'")):
        try:
            x_eval = ast.literal_eval(x)
            if clean_null(x_eval, falsey_is_null) is None:
                return None
        except ValueError:
            pass

    # Return x if is has not been found null-indicating in the above checks
    return x


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

    return " ".join(x.split())
