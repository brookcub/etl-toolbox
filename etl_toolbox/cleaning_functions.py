import ast
import collections.abc
import re


def fingerprint(x, special_characters=''):
    """
    Returns a lowercase, alphanumeric representation of x

    Example:
      >>> from etl_toolbox.cleaning_functions import fingerprint
      >>> fingerprint('(Aa_Bb_Cc)')
      'aabbcc'

    :param x:
        The object to be fingerprinted. Will be cast to a string using
        ``str(x)``.

    :param special_characters:
        (optional) A string of special characters to preserve while creating
        the fingerprint.

    :return:
        Returns a string.
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
    Returns ``None`` if x is null-indicating, else returns x

    x is considered null-indicating if any of the following are true:
     - x is ``None``
     - ``len(x) == 0``
     - ``fingerprint(x) in NULL_INDICATORS``
     - ``falsey_is_null and !x``
     - ``falsey_is_null and fingerprint(x) in FALSEY_INDICATORS``
     - x is an iterable consisting of all null-indicating values
     - x evaluates as a Python literal that is null-indicating

    Example:
      >>> from etl_toolbox.cleaning_functions import clean_null
      >>> clean_null('Unknown')
      None

    :param x:
        The object to be evaluated. x can be any type, though this function
        is intended for use with strings, lists, and sets.

        The behavior may not be intuitive for some other types.
        Ex) A dictionary will be considered null-indicating if it is either
            empty, or all of its keys are null-indicating. This function does
            not take dictionary values into account.

    :param falsey_is_null:
        (optional) A boolean which controls the behavior of falsey objects.
        True = all falsey values will be considered null-indicating
        False = not all falsey values will be considered null-indicating
        The default is False.

        A common use case for setting this to True would be when evaluating
        numeric data in which '0' is a meaningful value.

    :param special_characters:
        (optional) A string of special characters to preserve while creating
        the fingerprint of x.

    :return:
        Returns ``None`` or x.
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
    Returns x with whitespace characters cleaned.

    Cleaning rules:
     - all whitespace characters replaced with standard ASCII space (32)
     - consecutive whitespace condensed
     - leading/trailing whitespace removed

    Example:
      >>> from etl_toolbox.cleaning_functions import clean_whitespace
      >>> clean_whitespace(''' 123   abc 456
      ...                               def\t\t 789\t''')
      '123 abc 456 def 789'

    :param x:
        The string to be cleaned.

    :return:
        Returns a string.

    Note: Does not remove unicode formatting characters without White_Space
    property:
     - \u180E \u200B \u200C \u200D \u2060 \uFEFF
    """

    return " ".join(x.split())
