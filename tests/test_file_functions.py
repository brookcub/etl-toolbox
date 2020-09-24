import os
import pytest

from etl_toolbox.file_functions import get_file_list_from_dir


@pytest.mark.parametrize("dir, recursive, include_regex, expected", [
    (
        os.path.join('test_data', 'test_dir'),
        False,
        None,
        [os.path.join('test_data', 'test_dir', '1.csv'),
         os.path.join('test_data', 'test_dir', '2.csv'),
         os.path.join('test_data', 'test_dir', '3.json')]
        ),
    (
        os.path.join('test_data', 'test_dir'),
        True,
        None,
        [os.path.join('test_data', 'test_dir', '1.csv'),
         os.path.join('test_data', 'test_dir', '2.csv'),
         os.path.join('test_data', 'test_dir', '3.json'),
         os.path.join('test_data', 'test_dir', 'a', '1.csv'),
         os.path.join('test_data', 'test_dir', 'b', '3.csv'),
         os.path.join('test_data', 'test_dir', 'b', 'c', '2.txt')]
        ),
    (
        os.path.join('test_data', 'test_dir'),
        False,
        r'.*\.json$',
        [os.path.join('test_data', 'test_dir', '3.json')]
        ),
    (
        os.path.join('test_data', 'test_dir'),
        True,
        r'.*2\..*',
        [os.path.join('test_data', 'test_dir', '2.csv'),
         os.path.join('test_data', 'test_dir', 'b',  'c', '2.txt')]
        )
])
def test_get_file_list_from_dir(dir, recursive, include_regex, expected):
    assert sorted(
        get_file_list_from_dir(dir, recursive=recursive, include_regex=include_regex)
    ) == sorted(expected)
