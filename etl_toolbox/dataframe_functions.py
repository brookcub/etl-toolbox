'''
.. epigraph:: Functions for working with :class:`pandas.DataFrame`\\ s
'''

import numpy as np
import pandas as pd

from .cleaning_functions import clean_null, fingerprint


def find_column_labels(
    df, label_fingerprints, label_match_thresh=3, special_characters=''
):
    """
    Finds a row of column labels within a :class:`pandas.DataFrame` based on
    a collection of expected ``label_fingerprints``.

    ``df.columns`` is updated to contain the found column labels and all rows
    before and including the column label row are removed.

    .. note::
       All labels must be in the same row. This function will not attempt to
       correct translational errors.

    Usage:
      >>> import pandas as pd
      >>> from etl_toolbox.dataframe_functions import find_column_labels
      >>> df = pd.DataFrame(
      ...     [
      ...         ["created by:", "etl-toolbox",             "",         "-"],
      ...         [ "2020-06-07",         "---",       "3 rows", "4 columns"],
      ...         [           "",            "",             "",         "-"],
      ...         [      "email",        "date",        "phone",        "id"],
      ...         ["aaa@aaa.com",     "04mar14", "999-333-4444",       "AAA"],
      ...         ["baa@baa.com",     "05aug13", "111-222-3333",       "BAA"],
      ...         ["caa@caa.com",     "01jun15", "777-777-7777",       "CAA"]
      ...     ]
      ... )
      >>> print(df)
                   0            1             2          3
      0  created by:  etl-toolbox                        -
      1   2020-06-07          ---        3 rows  4 columns
      2                                                  -
      3        email         date         phone         id
      4  aaa@aaa.com      04mar14  999-333-4444        AAA
      5  baa@baa.com      05aug13  111-222-3333        BAA
      6  caa@caa.com      01jun15  777-777-7777        CAA
      >>> label_fingerprints = {'email', 'date', 'phone'}
      >>> find_column_labels(df, label_fingerprints)
      >>> print(df)
               email     date         phone   id
      0  aaa@aaa.com  04mar14  999-333-4444  AAA
      1  baa@baa.com  05aug13  111-222-3333  BAA
      2  caa@caa.com  01jun15  777-777-7777  CAA

    :param df:
        A :class:`pandas.DataFrame` containing column labels as a row, possibly
        preceded by misc. non-data rows.

    :param label_fingerprints:
        Fingerprinted label names that are expected in the column labels row.
        It can contain many variations on the expected label names, which
        makes this function useful for cleaning multiple files with varied
        column labels.

        Example:
          >>> label_fingerprints = {'email', 'emailaddr', 'phone', 'phonenum'}

        .. note::
           If a `dict` is provided, the keys will be used as the fingerprints
           and the values will be ignored.

        A ``fingerprint_map`` dictionary created for use in the
        :mod:`~etl_toolbox.mapping_functions` module can be passed as
        ``label_fingerprints``.

    :type label_fingerprints: set, list, or dict

    :param label_match_thresh:
        The number of fingerprints that must be found in
        ``label_fingerprints`` for a row to be identified as the label row.
        Default is ``3``.

        This exists to prevent false matches caused by non-data header rows
        containing values that are also expected column labels.

        For example, in the following :class:`~pandas.DataFrame`, row 1 will be
        misidentified as the label row if the ``label_match_thresh`` is set
        to ``1``:

          >>> import pandas as pd
          >>> from etl_toolbox.dataframe_functions import find_column_labels
          >>> df = pd.DataFrame(
          ...     [
          ...         [      "name:", "data report",             "",         "-"],
          ...         [      "date:",  "2001-05-03",       "3 rows", "4 columns"],
          ...         [           "",            "",             "",         "-"],
          ...         [      "email",        "date",        "phone",        "id"],
          ...         ["aaa@aaa.com",     "04mar14", "999-333-4444",       "AAA"],
          ...         ["baa@baa.com",     "05aug13", "111-222-3333",       "BAA"],
          ...         ["caa@caa.com",     "01jun15", "777-777-7777",       "CAA"]
          ...     ]
          ... )
          >>> print(df)
                       0            1             2          3
          0        name:  data report                        -
          1        date:   2001-05-03        3 rows  4 columns
          2                                                  -
          3        email         date         phone         id
          4  aaa@aaa.com      04mar14  999-333-4444        AAA
          5  baa@baa.com      05aug13  111-222-3333        BAA
          6  caa@caa.com      01jun15  777-777-7777        CAA
          >>> label_fingerprints = {'email', 'date', 'phone'}
          >>> find_column_labels(df, label_fingerprints, label_match_thresh=1)
          >>> print(df)
                   date: 2001-05-03        3 rows 4 columns
          0                                               -
          1        email       date         phone        id
          2  aaa@aaa.com    04mar14  999-333-4444       AAA
          3  baa@baa.com    05aug13  111-222-3333       BAA
          4  caa@caa.com    01jun15  777-777-7777       CAA

        ``3`` is a good value for most datasets with a known set of
        ``label_fingerprints``. It can be set lower if the incoming data has
        few columns and/or highly varied label names.

        If this argument is set to ``0``, the function will raise a
        :exc:`ValueError`.

    :type label_match_thresh: int, optional

    :param special_characters:
        (optional) A string of special characters to preserve while creating
        the fingerprints for lookup in ``label_fingerprints``. See
        :func:`cleaning_functions.fingerprint()
        <etl_toolbox.cleaning_functions.fingerprint>` for details.

        .. note::
           Any special characters that appear in the elements of
           ``label_fingerprints`` should be included here.

    :type special_characters: string, optional

    :raises IndexError:
        Raised if a label row can not be identified in the given
        :class:`~pandas.DataFrame`.

    :raises ValueError:
        Raised if the ``label_match_thresh`` is set to `0`.

    :return:
        Returns ``None``. The ``df`` argument is mutated.
    """
    if(label_match_thresh == 0):
        raise(ValueError("label_match_thresh can not be 0."))

    # Check whether the index is something other than the default RangeIndex,
    # and temporarily change it to a RangeIndex if it is.
    #
    # This is necessary because pandas doesn't provide a way to drop rows in
    # place using integer locations, however using the named index will produce
    # unexpected results if the DataFrame has duplicate index values.
    initial_index = df.index
    initial_index_is_default = index_is_default(df)

    if not initial_index_is_default:
        df.reset_index(drop=True, inplace=True)

    # Iterate over rows to find the label index
    label_index = None

    for i, row in df.iterrows():
        # Count the number of fingerprinted cell values found in
        # label_fingerprints for this row
        label_count = 0

        for cell in row.iteritems():
            cell_fingerprint = fingerprint(
                cell[1], special_characters=special_characters
            )

            if cell_fingerprint in label_fingerprints:
                label_count += 1

        # When label row is found, record the index and break
        if label_count >= label_match_thresh:
            label_index = i
            break

    if label_index is None:
        raise IndexError(
            'Label row could not be identified. Make sure '
            'label_fingerprints contains the expected label names.'
        )

    # Set DataFrame column labels
    df.rename(columns=df.loc[label_index], inplace=True)

    # Remove rows up to and including the label index
    df.drop(df.loc[:label_index].index, inplace=True)

    # If the initial index was a default RangeIndex, reset it so it is
    # numbered from 0.
    # Otherwise, restore the intial index, sliced to line up with the
    # modified DataFrame.
    if initial_index_is_default:
        df.reset_index(drop=True, inplace=True)
    else:
        df.index = initial_index[label_index + 1:]


def merge_columns_by_label(df, deduplicate_values=False):
    """
    Merges columns of a :class:`pandas.DataFrame` that have identical labels

    For duplicate column labels in ``df``, the first instance of each label
    will be turned into a column of lists containing the values from all of
    the instances. The other instances will then be dropped.

    .. note::
       This function does not fingerprint the labels for comparison. Column
       labels should be cleaned and mapped before using this tool.

    Usage:
      >>> import pandas as pd
      >>> from etl_toolbox.dataframe_functions import merge_columns_by_label
      >>> df = pd.DataFrame(
      ...     [
      ...         ["AAA", "aaa@aaa.com", "111-111-1111", "111@aaa.com"],
      ...         ["BAA", "baa@baa.com", "222-222-2222", "222@baa.com"],
      ...         ["CAA", "caa@caa.com", "333-333-3333", "333@caa.com"],
      ...         ["DAA", "daa@daa.com", "444-444-4444", "444@daa.com"]
      ...     ],
      ...     columns=["id", "email", "phone", "email"]
      ... )
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
        A :class:`pandas.DataFrame`.

    :param deduplicate_values:
        If ``True``, the values of the combined columns will be deduplicated
        and stored in the modified :class:`~pandas.DataFrame` as a `set`
        instead of a `list`.

    :type deduplicate_values: boolean, optional

    :return:
        Returns ``None``. The ``df`` argument is mutated.
    """

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


def index_is_default(df):
    """
    Returns ``True`` if the provided :class:`~pandas.DataFrame` has the
    default :class:`pandas.RangeIndex`.

    Else returns ``False``.
    """

    return df.index.equals(pd.RangeIndex(df.shape[0])) and df.index.name is None


def dataframe_clean_null(
    df,
    empty_row_thresh=1,
    empty_column_thresh=1,
    falsey_is_null=False,
    special_characters='',
):
    """
    Cleans null values of a :class:`pandas.DataFrame` and removes empty
    rows/columns.

    .. warning::
       This function is computationally intensive and might be slow on large
       :class:`~pandas.DataFrame`\\ s.

    Usage:
      >>> import pandas as pd
      >>> from etl_toolbox.dataframe_functions import dataframe_clean_null
      >>> df = pd.DataFrame(
      ...     [
      ...         ["AAA",          None, "111-111-1111", "empty"],
      ...         ["BAA", "baa@baa.com",            "-",     "-"],
      ...         ["CAA", "caa@caa.com", "notavailable",   "..."],
      ...         ["DAA",     "blocked", "444-444-4444",  "null"]
      ...     ],
      ...     columns=["id", "email", "phone", "col4"]
      ... )
      >>> print(df)
          id        email         phone   col4
      0  AAA         None  111-111-1111  empty
      1  BAA  baa@baa.com             -      -
      2  CAA  caa@caa.com  notavailable    ...
      3  DAA      blocked  444-444-4444   null
      >>> dataframe_clean_null(df)
      >>> print(df)
          id        email         phone
      0  AAA          NaN  111-111-1111
      1  BAA  baa@baa.com           NaN
      2  CAA  caa@caa.com           NaN
      3  DAA          NaN  444-444-4444

    :param df:
        A :class:`pandas.DataFrame`.

    :param empty_row_thresh:
        The number of non-null values required for a row to be considered
        populated/non-empty. Default is ``1``.

        If set to ``0``, no rows will be removed.

    :type empty_row_thresh: int, optional

    :param empty_column_thresh:
        The number of non-null values required for a column to be considered
        populated/non-empty. Default is ``1``.

        .. note::
           Rows are dropped before columns, so this threshold will be applied
           to the values that remain **after rows are removed**. If
           ``empty_column_thresh`` is greater than ``1``, the resulting ``df``
           may contain rows with fewer populated cells than
           ``empty_row_thresh``. However, it will never contain completely
           empty rows (unless ``empty_row_thresh`` is ``0``).

        If set to ``0``, no columns will be removed.

    :type empty_column_thresh: int, optional

    :param falsey_is_null:
        Controls whether falsey objects are considered *null-indicating*.
        See :func:`cleaning_functions.clean_null()
        <etl_toolbox.cleaning_functions.clean_null>` for details.
        Default is ``False``.

    :type falsey_is_null: boolean, optional

    :param special_characters:
        A string of special characters to preserve while creating the
        fingerprints. See :func:`cleaning_functions.fingerprint()
        <etl_toolbox.cleaning_functions.fingerprint>` for details.

    :type special_characters: string, optional

    :return:
        Returns ``None``. The ``df`` argument is mutated.
    """

    initial_index_is_default = index_is_default(df)

    # Apply clean_null() to every cell in df
    for i in range(df.shape[0]):
        for j in range(df.shape[1]):
            val = clean_null(
                df.iloc[i, j],
                falsey_is_null=falsey_is_null,
                special_characters=special_characters,
            )
            if val is None:
                df.iloc[i, j] = np.nan

    # Drop rows with fewer populated cells than empty_row_thresh
    df.dropna(axis=0, thresh=empty_row_thresh, inplace=True)

    # Drop columns with fewer populated cells than empty_column_thresh
    df.dropna(axis=1, thresh=empty_column_thresh, inplace=True)

    # Make sure there are no empty rows in the final df
    # (unless empty_row_thresh is 0)
    if empty_column_thresh > 1 and empty_row_thresh != 0:
        df.dropna(axis=0, how='all', inplace=True)

    # Reset the index if it was initially a default index
    if initial_index_is_default:
        df.reset_index(drop=True, inplace=True)
