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
