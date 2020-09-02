'''
This module contains functions for working with files and directories.
'''

import os
import re


def get_file_list_from_dir(dir, recursive=False, include_regex=None):
    r"""
    Returns a `list` of the files in a directory

    Example:
      >>> get_file_list_from_dir('test_data/test_dir') # doctest:+SKIP
      ['test_data/test_dir/1.csv',
       'test_data/test_dir/2.csv',
       'test_data/test_dir/3.json']

    :param recursive:
        (optional) If set to ``True``, the returned `list` will include files
        from ``dir`` and all of its subdirectories. Default is ``False``.

        Example:
          >>> get_file_list_from_dir('test_data/test_dir',
          ...                        recursive=True)  # doctest:+SKIP
          ['test_data/test_dir/1.csv',
           'test_data/test_dir/2.csv',
           'test_data/test_dir/3.json',
           'test_data/test_dir/a/1.csv',
           'test_data/test_dir/b/3.csv',
           'test_data/test_dir/b/c/2.txt']

    :param include_regex:
        (optional) Only include files whose path matches this regex. Default
        is ``None`` (list is unfiltered).

        Example:
          >>> get_file_list_from_dir('test_data/test_dir',
          ...                        include_regex=r'.*\.csv$') # doctest:+SKIP
          ['test_data/test_dir/1.csv',
           'test_data/test_dir/2.csv']

    :return:
        Returns `list` of file paths.
    """

    file_list = []

    # Collect file paths
    for root, dirs, files in os.walk(dir):
        for f in files:
            file_list.append(os.path.normpath(os.path.join(root, f)))

        if not recursive:
            break

    # Apply filter
    if include_regex is not None:
        file_list = [f for f in file_list if re.match(include_regex, f)]

    return file_list
