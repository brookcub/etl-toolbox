'''
.. epigraph:: Basic transformations for cleaning individual units of data
'''

import ast
import collections.abc
import re


def fingerprint(x, special_characters=''):
    """
    Returns a lowercase, alphanumeric representation of ``x``

    Usage:
      >>> from etl_toolbox.cleaning_functions import fingerprint
      >>> fingerprint('(Aa_Bb_Cc)')
      'aabbcc'

    :param x:
        The object to be fingerprinted. Will be cast to a string using
        ``str(x)``.

    :param special_characters:
        A string of special characters to preserve while creating the
        fingerprint of ``x``. Any special characters which are individually
        meaningful for the data should be included here.

          >>> fingerprint('(Aa_Bb_Cc)', special_characters='_')
          'aa_bb_cc'

        .. note::
           An example of where this might be useful is when fingerprinting
           column labels on a data set. Some datasets use ``$`` as a label for
           price/cost or ``#`` as a label for phone number or id number. In
           that case, ``special_characters`` should be set to ``'#$'`` so that
           those values are preserved.

    :type special_characters: string, optional

    :return:
        Returns a string.
    """
    remove_regex = r'[^0-9a-z{}]'.format(re.escape(special_characters))

    return re.sub(remove_regex, '', str(x).lower())


#: A list of strings that are considered equivalent to ``None``. Used by
#: :func:`clean_null()`.
NULL_INDICATORS = [
    '',
    'blank',
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

#: A list of strings that are considered to be falsey.
#: Used by :func:`clean_null()`.
FALSEY_INDICATORS = [
    'false',
    '0'
]


def clean_null(x, falsey_is_null=False, special_characters=''):
    """
    Returns ``None`` if ``x`` is *null-indicating*, else returns ``x``

    ``x`` is considered *null-indicating* if any of the following are true:

    - ``x is None``
    - ``len(x) == 0``
    - ``fingerprint(x) in NULL_INDICATORS`` (see: :const:`NULL_INDICATORS`)
    - ``falsey_is_null and !x``
    - ``falsey_is_null and fingerprint(x) in FALSEY_INDICATORS`` (see:
      :const:`FALSEY_INDICATORS`)
    - ``x`` is an iterable consisting of all *null-indicating* values \n
      - Ex: ``x == ['empty', None, {None}]``
    - ``x`` evaluates as a Python literal that is *null-indicating* \n
      - Ex: ``x == '{None, None}'``

    Usage:
      >>> from etl_toolbox.cleaning_functions import clean_null
      >>> clean_null('Unknown') is None
      True
      >>> clean_null(['empty', None, {None}]) is None
      True
      >>> clean_null('false') is None
      False
      >>> clean_null('false', falsey_is_null=True) is None
      True

    :param x:
        The object to be evaluated. ``x`` can be any type, though this function
        is intended for use with strings, lists, and sets.

        .. warning::
            The behavior of :func:`clean_null()` may not be intuitive for types
            other than `string`, `list`, and `set`. For example, a `dict` will
            be considered *null-indicating* if it is either empty, or all of
            its **keys** are *null-indicating*. **Dictionary values will be
            ignored.**

    :param falsey_is_null:
        Controls whether falsey objects are considered *null-indicating*.

        - If ``True``, all falsey values will be considered *null-indicating*
        - If ``False``, falsey values will not be considered *null-indicating*
          (unless they are otherwise *null-indicating* regardless of falsiness)

        Default is ``False``.

        .. note::
            A common use case for setting ``falsey_is_null`` to ``True`` would
            be when evaluating non-numeric data such as locations or phone
            numbers. In these data sets, ``0`` is not a meaningful value and is
            likely just functioning as a placeholder for null.

    :type falsey_is_null: boolean, optional

    :param special_characters:
        A string of special characters to preserve while creating the
        fingerprint of ``x``. See :func:`fingerprint()` for more details.

    :type special_characters: string, optional

    :return:
        Returns ``None`` or ``x``.
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
        except Exception:
            pass

    # Return x if is has not been found null-indicating in the above checks
    return x


def clean_whitespace(x):
    """
    Returns ``x`` with whitespace characters trimmed and condensed

    Cleaning rules:
     - all whitespace characters replaced with standard ASCII space (32)
     - consecutive whitespace condensed
     - leading/trailing whitespace removed

    Usage:
      >>> from etl_toolbox.cleaning_functions import clean_whitespace
      >>> clean_whitespace(''' 123   abc 456
      ...                               def\t\t 789\t''')
      '123 abc 456 def 789'

    :param x:
        The string to be cleaned.

    :type x: string

    :return:
        Returns a string.

    .. note::
        :func:`clean_whitespace()` does not remove unicode formatting
        characters without the **White_Space** character property:

        .. hlist::
           :columns: 3

           - **U+180E**
           - **U+200B**
           - **U+200C**
           - **U+200D**
           - **U+2060**
           - **U+FEFF**
    """

    return " ".join(x.split())
