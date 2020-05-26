import pytest
from etl_toolbox.cleaning_functions import fingerprint, clean_whitespace


@pytest.mark.parametrize("input, expected", [
    ('(Aa_Bb_Cc)',              'aabbcc'),
    (' sdfD 432   ^%',          'sdfd432'),
    ('###$@!%^&*()-=',          ''),
    ('F\nP\n\t\tZ    ',         'fpz'),
    (u'a\u00E3aa\u00E5a\ufffd', 'aaaa')
])
def test_fingerprint(input, expected):
    assert fingerprint(input) == expected


@pytest.mark.parametrize("input, special_characters, expected", [
    ('Phone#', '#',             'phone#'),
    ('$AMOUNT  ', '$',          '$amount'),
    ('\\backslashes\\', '\\',   '\\backslashes\\'),
    ('%(MULTIPLE$@()_', '%_@(', '%(multiple@(_')
])
def test_fingerprint_special_characters(input, special_characters, expected):
    assert fingerprint(input, special_characters) == expected


@pytest.mark.parametrize("input, expected", [
    (''' 123   abc 456
            def\t\t 789\t''',   '123 abc 456 def 789'),
    ('   spaces   ',            'spaces'),
    ('\t\n\r\f\v',              ''),
    (u'\u2008 and \u3000',      'and'),
    (u'''\u0009 \u000A \u000B
        \u000C \u000D a \u0020 
        \u0085 \u00A0 \u1680
        \u2000 \u2001 \u2002 b
        \u2003 \u2004 \u2005
        \u2006 \u2007 \u2008
        \u2009 \u200A \u2028 c
        \u2029 \u202F \u205F
        \u3000''',              'a b c'),
    ('',                        '')
])
def test_clean_whitespace(input, expected):
    assert clean_whitespace(input) == expected
