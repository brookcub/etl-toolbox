import pytest

from etl_toolbox.cleaning_functions import clean_null, clean_whitespace, fingerprint


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
    (None,                      None),
    ('',                        None),
    ('None',                    None),
    ('A',                       'A'),
    ('(>',                      None),
    (0,                         0),
    ('False',                   'False'),
    ([],                        None),
    ([None],                    None),
    ('[None,None]',             None),
    ({'empty'},                 None),
    ((None, 'value'),           (None, 'value')),
    ('{"real_python_literal"}', '{"real_python_literal"}'),
    ('{"fake_python_literal"',  '{"fake_python_literal"'),
    ('[None,{"5"}]',            '[None,{"5"}]'),
    ('[None,{"Null",("","")}]', None)
])
def test_clean_null(input, expected):
    assert clean_null(input) == expected


@pytest.mark.parametrize("input, expected", [
    (None,                      None),
    ('',                        None),
    (0,                         None),
    ('0',                       None),
    ('A',                       'A'),
    ('False',                   None),
    ([False],                   None),
    ('[None,0]',                None),
    ((None, 'value'),           (None, 'value')),
    ('{0.0}',                   None)
])
def test_clean_null_w_falsey_is_null(input, expected):
    assert clean_null(input, falsey_is_null=True) == expected


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
