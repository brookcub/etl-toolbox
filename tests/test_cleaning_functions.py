import pytest
from etl_toolbox.cleaning_functions import fingerprint


@pytest.mark.parametrize("input, expected", [
    ('AaBbCc',                  'aabbcc'),
    (' sdfD 432   ^%',          'sdfd432'),
    ('###$@!%^&*()-=',          ''),
    ('F\nP\n\t\tZ    ',         'fpz')
])
def test_fingerprint(input, expected):
    assert fingerprint(input) == expected
