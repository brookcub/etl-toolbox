'''
.. epigraph:: Functions for mapping collections of values
'''

from .cleaning_functions import fingerprint


def map_labels(
    labels, fingerprint_map, special_characters='', return_unmapped=False
):
    """
    Maps a list of ``labels`` to new values based on provided
    ``fingerprint_map`` and returns that mapped list.

    This is useful for mapping column labels from a dataframe/file to a
    standard schema, particularly when the labels are inconsistent.

    The order of ``labels`` will be preserved in the return, and if a label
    isn't found in ``fingerprint_map``, that label will be ``'-'`` in
    returned list.

    Usage:
      >>> from etl_toolbox.mapping_functions import map_labels
      >>> labels = [1, '2_A', '2b']
      >>> fingerprint_map = {'1': 'one', '2a': 'two_a', 'extrakey': 'value'}
      >>> map_labels(labels, fingerprint_map)
      ['one', 'two_a', '-']

    :param labels:
        The list of labels to map. These will be fingerprinted for their
        lookup in ``fingerprint_map``.

    :param fingerprint_map:
        A dictionary of all expected label fingerprints mapped to formatted
        outputs.

    :param special_characters:
        A string of special characters to preserve while fingerprinting the
        labels. See :func:`cleaning_functions.fingerprint()
        <etl_toolbox.cleaning_functions.fingerprint>` for details.

        .. note::
           This should include any special characters that appear in the keys
           of ``fingerprint_map``.

    :type special_characters: string, optional

    :param return_unmapped:
        If this is set to ``True``, this function will return a tuple of the
        mapped labels and a set of unmapped labels (any value from ``labels``
        whose fingerprint was not found in ``fingerprint_map``). Default is
        ``False``.

        .. note::
           This is useful for tracking unrecognized labels of incoming files in
           an automated ETL system.

    :type return_unmapped: boolean, optional

    :return:
        Returns a list or, if the ``return_unmapped`` option is ``True``,
        returns a tuple, with the first element being a list and the second
        being a set.
    """
    mapped_labels = []
    unmapped_labels = set()

    for x in labels:
        x_fingerprint = fingerprint(x, special_characters=special_characters)

        if x_fingerprint in fingerprint_map:
            x_mapped = fingerprint_map[x_fingerprint]
            mapped_labels.append(x_mapped)
        else:
            mapped_labels.append('-')
            unmapped_labels.add(x)

    if return_unmapped:
        return (mapped_labels, unmapped_labels)

    return mapped_labels


def append_count(x):
    """
    A generator function that yields ``x`` with a numbered suffix.
    """
    i = 0
    while True:
        i += 1
        yield x + '_' + str(i)


def rename_duplicate_labels(labels, rename_generator=append_count):
    """
    Maps a list of ``labels`` such that duplicates are renamed according to the
    ``rename_generator``.

    The order of ``labels`` is preserved in the return, and if a label isn't a
    duplicate, its value will be unchanged. Values will NOT be fingerprinted
    for comparison, so this function is best used after labels have been
    standardized.

    Usage:
      >>> from etl_toolbox.mapping_functions import rename_duplicate_labels
      >>> labels = ['email', 'email', 'phone', 'name', 'email', 'phone']
      >>> rename_duplicate_labels(labels)
      ['email_1', 'email_2', 'phone_1', 'name', 'email_3', 'phone_2']

    :param labels:
        The list of labels to map.

    :param rename_generator:
        A generator function that specifies how to rename duplicate columns. It
        should take a label name as a positional argument and yield the renamed
        label. The default ``rename_generator`` appends a count, separated by
        underscore.

        Example:
          >>> def rename_generator(x):
          ...     i = 0
          ...     while True:
          ...         i += 1
          ...         yield x + '_' + str(i)
          >>> r = rename_generator('label')
          >>> next(r)
          'label_1'
          >>> next(r)
          'label_2'

    :type rename_generator: generator, optional

    :return:
        Returns a list.
    """

    # Create dictionary of duplicate labels with initialized rename_generators
    seen = set()
    duplicates = {}
    for x in labels:
        if x in seen:
            duplicates[x] = rename_generator(x)
        else:
            seen.add(x)

    # Create a new list with each duplicate label renamed according to its
    # rename_generator
    mapped_labels = []
    for x in labels:
        if x in duplicates:
            x_renamed = next(duplicates[x])
            mapped_labels.append(x_renamed)
        else:
            mapped_labels.append(x)

    return mapped_labels
