from etl_toolbox.cleaning_functions import fingerprint


def find_column_labels(df, label_fingerprints, label_match_thresh=3, special_characters=''):
    """
    Finds a row of column labels within a pandas `DataFrame`

    ``df.columns`` is updated to contain the found column labels and all rows
    before and including the column label row are removed.

    Note that all labels must be in the same row, this function will not
    attempt to correct translational errors.

    Example:
      ...
      >>> print(df)
                   0            1             2          3
      0  created by:  etl-toolbox
      1   2020-06-07          ---        3 rows  4 columns
      2
      3        email         date         phone         id
      4  aaa@aaa.com      04mar14  999-333-4444        AAA
      5  baa@baa.com      05aug13  111-222-3333        BAA
      6  caa@caa.com      01jun15  777-777-7777        CAA
      >>> label_fingerprints = {'email', 'date', 'phone'}
      >>> find_column_labels(df, label_fingerprints)
      >>> print(df)
               email         date         phone         id
      0  aaa@aaa.com      04mar14  999-333-4444        AAA
      1  baa@baa.com      05aug13  111-222-3333        BAA
      2  caa@caa.com      01jun15  777-777-7777        CAA

    :param df:
        A pandas `DataFrame` containing column labels as a row, possibly
        preceded by misc. non-data rows.

    :param label_fingerprints:
        A `set` of fingerprinted label names that are expected in the column
        labels row. It can contain many variations on the expected label
        names, which makes this function useful for cleaning multiple files
        with varied column labels.

        Example:
          >>> label_fingerprints = {'email', 'emailaddr', 'phone', 'phonenum'}

        This argument can also a `list` or `dict`. If a `dict` is provided,
        the keys will be used as the set of fingerprints and values will be
        ignored.

        If you have a ``fingerprint_map`` dictionary for use with the
        `mapping_functions` module, that can be passed as ``label_fingerprints``.

    :param label_match_thresh:
        (optional) The number of fingerprints that must be found in
        ``label_fingerprints`` before a row is identified as the label row.
        The default is `3`.

        This exists to prevent false matches caused by non-data header rows
        containing values that are also expected column labels.

        For example, in the following `DataFrame`, rows 0 or 1 could be
        misidentified as the label row if the `label_match_thresh` is set
        to `0`:
          >>> print(df)
                       0            1             2     3
          0        name:  data report
          1        date:   2001-05-03
          2        rows:            3
          3
          4        email         date         phone  name
          5  aaa@aaa.com   1999-03-07  999-333-4444   AAA
          6  baa@baa.com   1999-11-15  111-222-3333   BAA
          7  caa@caa.com   2000-06-22  777-777-7777   CAA

        `3` is a good value for most datasets with a known set of
        ``label_fingerprints``. It can be set lower if the incoming data has
        few columns and/or highly varied label names.

    :param special_characters:
        (optional) A string of special characters to preserve while creating
        the fingerprints for lookup in ``label_fingerprints``.

        Any special characters that appear in the elements of
        ``label_fingerprints`` should be included here.

    :raises ValueError:
            Raised if a label row can not be identified in the given `DataFrame`.

    :return:
        Returns ``None``. The ``df`` argument is mutated.
    """

    # Iterate over rows to find the label index
    label_index = None

    for i, row in df.iterrows():
        # Count the number of fingerprinted cell values found in
        # label_fingerprints for this row
        label_count = 0

        for cell in row.iteritems():
            cell_fingerprint = fingerprint(cell[1], special_characters=special_characters)

            if cell_fingerprint in label_fingerprints:
                label_count += 1

        # When label row is found, record the index and break
        if label_count >= label_match_thresh:
            label_index = i
            break

    if label_index is None:
        raise ValueError('Label row could not be identified. Make sure '
                         'label_fingerprints contains the expected label names.')

    # Set DataFrame column labels
    df.rename(columns=df.iloc[label_index], inplace=True)

    # Remove rows up to and including the label index
    df.drop(df.loc[:label_index].index, inplace=True)
    df.reset_index(drop=True, inplace=True)


def merge_columns_by_label(df, deduplicate_values=False):
    '''
    Merges columns of a pandas `DataFrame` that have identical labels

    For duplicate column labels in ``df``, the first instance of each label
    will be turned into a column of `list`s containing the values from all of
    the instances. The other instances will then be dropped.

    Note that this does not fingerprint the labels for comparison. Column
    labels should be cleaned and mapped before using this tool.

    Example:
      ...
      >>> print(df)
          id        email         phone        email
      0  AAA  aaa@aaa.com  111-111-1111  111@aaa.com
      1  BAA  baa@baa.com  222-222-2222  222@baa.com
      2  CAA  caa@caa.com  333-333-3333  333@caa.com
      3  DAA  daa@daa.com  444-444-4444  444@daa.com
      >>> merge_columns_by_label(df)
      >>> print(df)
          id                       email         phone
      0  AAA  [aaa@aaa.com, 111@aaa.com]  111-111-1111
      1  BAA  [baa@baa.com, 222@baa.com]  222-222-2222
      2  CAA  [caa@caa.com, 333@caa.com]  333-333-3333
      3  DAA  [daa@daa.com, 444@daa.com]  444-444-4444

    :param df:
        A pandas `DataFrame`.

    :param deduplicate_values:
        (optional) If set to ``True``, the values of the combined columns will
        be deduplicated and stored in the modified `DataFrame` as a `set`
        instead of a `list`.

    :return:
        Returns ``None``. The ``df`` argument is mutated.
    '''

    # Get the set of duplicate column labels
    duplicate_labels = set(df.columns[df.columns.duplicated()])

    for label in duplicate_labels:
        # Get integer location of first instance of label
        position_array = df.columns.get_loc(label)
        first_iloc = next(i for i, x in enumerate(position_array) if x)

        # Set the values of that column to a list (or set) combining all of the
        # instances of label
        if deduplicate_values:
            deduped_column = []
            for cell in df[label].values:
                deduped_column.append(set(cell))
            df.iloc[:, first_iloc] = deduped_column
        else:
            df.iloc[:, first_iloc] = df[label].values.tolist()

        # Temporarily rename first instance while others are dropped
        temp_labels = df.columns.tolist()
        temp_labels[first_iloc] = 'temp'
        df.columns = temp_labels
        df.drop(columns=label, inplace=True)

        # Rename back to the original label
        temp_labels = df.columns.tolist()
        temp_labels[first_iloc] = label
        df.columns = temp_labels
