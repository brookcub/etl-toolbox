import pytest
import pandas as pd
import numpy as np

from etl_toolbox.dataframe_functions import dataframe_clean_null
from etl_toolbox.dataframe_functions import find_column_labels
from etl_toolbox.dataframe_functions import index_is_default
from etl_toolbox.dataframe_functions import merge_columns_by_label


@pytest.mark.parametrize('df, label_fingerprints, expected', [
    ### Test 1
    (
        # df
        pd.DataFrame([
            ['', 'created by: ', 'Brookcub Industries', 'for testing purposes', ''],
            ['', '', '', '', ''],
            ['Dte', '2020-06-07', '3 rows', None, ''],
            ['', '', None, 'some columns', ''],
            ['ooooo', '00000', '-----', '_____', '     '],
            ['EML-addr', 'Dte', 'col3', 'phn-nmbr', 'NOM'],
            ['test@test.com', '04mar14', '12045', '999-333-4444', 'AAA'],
            ['green@green.com', None, '32124', '111-222-3333', 'BAA'],
            ['EML-addr', 'Dte', 'col3', 'phn-nmbr', 'NOM'],
            ['one@one.com', '01jun15', 77777, '777-777-7777', 'CAA']
            ]),
        # label_fingerprints
        {
            'emladdr': 'email_address',
            'dte': 'date',
            'phnnmbr': 'phone_number',
            'nom': 'name',
            'time': 'time'
            },
        # expected
        pd.DataFrame([
            ['test@test.com', '04mar14', '12045', '999-333-4444', 'AAA'],
            ['green@green.com', None, '32124', '111-222-3333', 'BAA'],
            ['EML-addr', 'Dte', 'col3', 'phn-nmbr', 'NOM'],
            ['one@one.com', '01jun15', 77777, '777-777-7777', 'CAA']
            ],
            columns=['EML-addr', 'Dte', 'col3', 'phn-nmbr', 'NOM']
            )
        ),
    ### Test 2, named index containing duplicates
    (
        # df
        pd.DataFrame([
            ['misc.', 'numbers', '', ''],
            ['', '', '', ''],
            ['', '', '', 'counts'],
            ['c', 'S', 'something-else', ''],
            [1, 1, 1, 0],
            [2, 3, 6, 0],
            [3, 6, 18, 0]
            ],
            index=['aaa', 'bbb', 'ccc', 'ccc', 'ddd', 'ddd', 'ccc']
            ),
        # label_fingerprints
        [
            'c',
            's',
            'somethingelse'
            ],
        # expected
        pd.DataFrame([
            [1, 1, 1, 0],
            [2, 3, 6, 0],
            [3, 6, 18, 0]
            ],
            index=['ddd', 'ddd', 'ccc'],
            columns=['c', 'S', 'something-else', ''],
            dtype='object'
            )
        )
])
def test_find_column_labels(df, label_fingerprints, expected):
    find_column_labels(df, label_fingerprints)

    assert df.equals(expected)
    assert df.columns.equals(expected.columns)
    assert df.index.equals(expected.index)


@pytest.mark.parametrize('df, label_fingerprints, label_match_thresh, exception_type', [
    ### Test 1 - test that IndexError is raised if label row isn't found
    (
        # df
        pd.DataFrame([
            ['', 'created by: ', 'Brookcub Industries', 'for testing purposes', ''],
            ['', '', '', '', ''],
            ['Dte', '2020-06-07', '3 rows', None, ''],
            ['', '', None, 'some columns', ''],
            ['ooooo', '00000', '-----', '_____', '     '],
            ['EML-addr', 'Dte', 'col3', 'phn-nmbr', 'NOM'],
            ['test@test.com', '04mar14', '12045', '999-333-4444', 'AAA'],
            ['green@green.com', None, '32124', '111-222-3333', 'BAA'],
            ['EML-addr', 'Dte', 'col3', 'phn-nmbr', 'NOM'],
            ['one@one.com', '01jun15', 77777, '777-777-7777', 'CAA']
            ]),
        # label_fingerprints
        {
            'emladdr': 'email_address',
            'dte': 'date',
            'time': 'time'
            },
        # label_match_thresh
        3,
        # exception_type
        IndexError
    ),
    ### Test 2 - test that ValueError is raised if label_match_thresh is set to 0
    (
        # df
        pd.DataFrame([
            ['eleifend vitae', 0.2289343509, '+'],
            ['non lorem vitae odio', 0.1746509874, '-']
            ]),
        # label_fingerprints
        {
            'emladdr': 'email_address',
            'dte': 'date',
            'time': 'time'
            },
        # label_match_thresh
        0,
        # exception_type
        ValueError
    )
])
def test_find_column_labels_exceptions(df, label_fingerprints, label_match_thresh, exception_type):
    with pytest.raises(exception_type):
        assert find_column_labels(df, label_fingerprints, label_match_thresh=label_match_thresh)


@pytest.mark.parametrize('df, expected', [
    ### Test 1
    (
        # df
        pd.DataFrame([
            ['AAA', 'aaa@aaa.com', '111-111-1111', '111@aaa.com', 'AAA', '555@aaa.com', '555-555-5555'],
            ['BAA', 'baa@baa.com', '222-222-2222', '222@baa.com', 'BAA', '666@baa.com', '666-666-6666'],
            ['CAA', 'caa@caa.com', '333-333-3333', '333@caa.com', 'CAA', '777@caa.com', '777-777-7777'],
            ['DAA', 'daa@daa.com', '444-444-4444', '444@daa.com', 'DAA', '888@daa.com', '888-888-8888']
            ],
            columns=['id', 'email', 'phone', 'email', 'name', 'email', 'phone']
            ),
        # expected
        pd.DataFrame([
            ['AAA', ['aaa@aaa.com', '111@aaa.com', '555@aaa.com'], ['111-111-1111', '555-555-5555'], 'AAA'],
            ['BAA', ['baa@baa.com', '222@baa.com', '666@baa.com'], ['222-222-2222', '666-666-6666'], 'BAA'],
            ['CAA', ['caa@caa.com', '333@caa.com', '777@caa.com'], ['333-333-3333', '777-777-7777'], 'CAA'],
            ['DAA', ['daa@daa.com', '444@daa.com', '888@daa.com'], ['444-444-4444', '888-888-8888'], 'DAA']
            ],
            columns=['id', 'email', 'phone', 'name']
            )
        )
])
def test_merge_columns_by_label(df, expected):
    merge_columns_by_label(df)
    assert df.equals(expected)
    assert df.columns.equals(expected.columns)


@pytest.mark.parametrize('df, expected', [
    ### Test 1
    (
        # df
        pd.DataFrame([
            ['AAA', 'aaa@aaa.com', '111-111-1111', '111@aaa.com', 'AAA', '555@aaa.com', '555-555-5555'],
            ['BAA', 'baa@baa.com', '222-222-2222', 'baa@baa.com', 'BAA', '666@baa.com', '666-666-6666'],
            ['CAA', 'caa@caa.com', '333-333-3333', 'caa@caa.com', 'CAA', '333-333-3333', '333-333-3333'],
            ['DAA', 'daa@daa.com', '444-444-4444', '444@daa.com', 'DAA', '888@daa.com', '888-888-8888']
            ],
            columns=['id', 'email', 'phone', 'email', 'name', 'email', 'phone']
            ),
        # expected
        pd.DataFrame([
            ['AAA', {'aaa@aaa.com', '111@aaa.com', '555@aaa.com'}, {'111-111-1111', '555-555-5555'}, 'AAA'],
            ['BAA', {'baa@baa.com', '666@baa.com'}, {'222-222-2222', '666-666-6666'}, 'BAA'],
            ['CAA', {'caa@caa.com', '333-333-3333'}, {'333-333-3333'}, 'CAA'],
            ['DAA', {'daa@daa.com', '444@daa.com', '888@daa.com'}, {'444-444-4444', '888-888-8888'}, 'DAA']
            ],
            columns=['id', 'email', 'phone', 'name']
            )
        ),
    ### Test 2
    (
        # df
        pd.DataFrame([
            ['AAA', 'aaa@aaa.com', '111-111-1111', '111@aaa.com', 'AAA', '', '555-555-5555'],
            ['BAA', 'baa@baa.com', '222-222-2222', 'baa@baa.com', 'BAA', '', '666-666-6666'],
            ['CAA', 'caa@caa.com', '333-333-3333', 'caa@caa.com', 'CAA', '', '333-333-3333'],
            ['DAA', 'daa@daa.com', '444-444-4444', '444@daa.com', 'DAA', '', '888-888-8888']
            ],
            columns=[None, 'email', 'phone', 'email', None, None, 'phone']
            ),
        # expected
        pd.DataFrame([
            [{'AAA',''}, {'aaa@aaa.com', '111@aaa.com'}, {'111-111-1111', '555-555-5555'}],
            [{'BAA',''}, {'baa@baa.com'}, {'222-222-2222', '666-666-6666'}],
            [{'CAA',''}, {'caa@caa.com'}, {'333-333-3333'}],
            [{'DAA',''}, {'daa@daa.com', '444@daa.com'}, {'444-444-4444', '888-888-8888'}]
            ],
            columns=[None, 'email', 'phone']
            )
        )
])
def test_merge_columns_by_label_dedup(df, expected):
    merge_columns_by_label(df, deduplicate_values=True)
    assert df.equals(expected)
    assert df.columns.equals(expected.columns)


@pytest.mark.parametrize('df, expected', [
    ### Test 1
    (
        # df
        pd.DataFrame(
            np.random.randint(0, 100, size=(15, 4)),
            columns=list('ABCD')),
        # expected
        True
        ),
    ### Test 2
    (
        # df
        pd.DataFrame([
            [1, 1, 1, 0],
            [2, 3, 6, 0],
            [3, 6, 18, 0]
            ],
            index=['aaa', 'bbb', 'ccc']
            ),
        # expected
        False
        ),
    ### Test 3
    (
        # df
        pd.DataFrame(
            np.random.randint(0, 10, size=(10, 2)),
            index=pd.RangeIndex(start=0, stop=20, step=2)
            ),
        # expected
        False
        ),
    ### Test 4
    (
        # df
        pd.DataFrame(
            np.random.randint(0, 10, size=(10, 2)),
            index=pd.RangeIndex(start=0, stop=10, name='test')
            ),
        # expected
        False
        ),
])
def test_index_is_default(df, expected):
    assert index_is_default(df) == expected


@pytest.mark.parametrize('df, expected', [
    ### Test 1
    (
        # df
        pd.DataFrame([
            ['AAA', 'None', '111-111-1111', 'empty'],
            ['BAA', 'baa@baa.com', '-', '-'],
            ['CAA', 'caa@caa.com', 'notavailable', '...'],
            ['DAA', 'blocked', '444-444-4444', 'null']
            ],
            columns=['id', 'email', 'phone', 'col4']
            ),
        # expected
        pd.DataFrame([
            ['AAA', np.nan, '111-111-1111'],
            ['BAA', 'baa@baa.com', np.nan],
            ['CAA', 'caa@caa.com', np.nan],
            ['DAA', np.nan, '444-444-4444']
            ],
            columns=['id', 'email', 'phone']
            )
        )
])
def test_dataframe_clean_null(df, expected):
    dataframe_clean_null(df)

    assert df.equals(expected)
    assert df.columns.equals(expected.columns)
    assert df.index.equals(expected.index)


@pytest.mark.parametrize('df, expected, empty_row_thresh, empty_column_thresh', [
    ### Test 1
    (
        # df
        pd.DataFrame([
            ['Golden jackal', 'Canis aureus', 'unknown', 'L', [], ''],
            ['Pie, rufous tree', 'Dendrocitta vagabunda', '65-1835935', 'M', {}, ''],
            ['Eurasian badger', 'Meles meles', '48-7685429', 'S', 'none', ''],
            ['', '', '', '', '', ''],
            ['', '', '', '', 'actual value', ''],
            ['', '', '', '', 'actual value', 'actual value2'],
            ['Karjalankarhukoira', '', '', '', 'actual value', ''],
            ['Arctic tern', 'Sterna paradisaea', '69-5988769', 'false', '', ''],
            ['Grant\'s gazelle', 'Gazella granti', '-', '-', ['none'], ''],
            ['Swallowtail butterfly', '-blank-', '-', '-', np.nan, '']
            ],
            columns=['common_name', 'scientific_name', 'EIN', 'shirt_size', 'col5', 'col6']
            ),
        # expected
        pd.DataFrame([
            ['Golden jackal', 'Canis aureus', np.nan, 'L'],
            ['Pie, rufous tree', 'Dendrocitta vagabunda', '65-1835935', 'M'],
            ['Eurasian badger', 'Meles meles', '48-7685429', 'S'],
            ['Karjalankarhukoira', np.nan, np.nan, np.nan],
            ['Arctic tern', 'Sterna paradisaea', '69-5988769', 'false'],
            ['Grant\'s gazelle', 'Gazella granti', np.nan, np.nan]
            ],
            columns=['common_name', 'scientific_name', 'EIN', 'shirt_size']
            ),
        # empty_row_thresh
        2,
        # empty_column_thresh
        3
        ),
    ### Test 2
    (
        # df
        pd.DataFrame([
            ['AAA', 'None', '111-111-1111', 'empty'],
            ['BAA', 'baa@baa.com', '-', '-'],
            ['CAA', 'caa@caa.com', 'notavailable', '...'],
            ['DAA', 'blocked', '444-444-4444', 'null'],
            ['none', 'blank', 'na', 'nbsp']
            ],
            columns=['id', 'email', 'phone', 'col4']
            ),
        # expected
        pd.DataFrame([
            ['AAA', np.nan, '111-111-1111', np.nan],
            ['BAA', 'baa@baa.com', np.nan, np.nan],
            ['CAA', 'caa@caa.com', np.nan, np.nan],
            ['DAA', np.nan, '444-444-4444', np.nan],
            [np.nan, np.nan, np.nan, np.nan]
            ],
            columns=['id', 'email', 'phone', 'col4']
            ).astype('object'),
        # empty_row_thresh
        0,
        # empty_column_thresh
        0,
        ),
    ### Test 3
    (
        # df
        pd.DataFrame([
            ['AAA', 'None', '111-111-1111', 'empty'],
            ['BAA', 'baa@baa.com', '-', '-'],
            ['CAA', 'caa@caa.com', 'notavailable', '...'],
            ['DAA', 'blocked', '444-444-4444', 'null'],
            ['none', 'blank', 'na', 'nbsp']
            ],
            columns=['id', 'email', 'phone', 'col4']
            ),
        # expected
        pd.DataFrame([
            ['AAA', np.nan, '111-111-1111'],
            ['BAA', 'baa@baa.com', np.nan],
            ['CAA', 'caa@caa.com', np.nan],
            ['DAA', np.nan, '444-444-4444'],
            [np.nan, np.nan, np.nan]
            ],
            columns=['id', 'email', 'phone']
            ).astype('object'),
        # empty_row_thresh
        0,
        # empty_column_thresh
        2
        )
])
def test_dataframe_clean_null_w_thresh(df, expected, empty_row_thresh, empty_column_thresh):
    dataframe_clean_null(df, empty_row_thresh=empty_row_thresh, empty_column_thresh=empty_column_thresh)

    assert df.equals(expected)
    assert df.columns.equals(expected.columns)
    assert df.index.equals(expected.index)


@pytest.mark.parametrize('df, special_characters, falsey_is_null, expected', [
    ### Test 1
    (
        # df
        pd.DataFrame([
            ['eleifend vitae', 0.2289343509, '+', 'false'],
            ['non lorem vitae odio', 0.1746509874, '-', 'false'],
            ['egestas', 0.248639792, '-', 'false'],
            ['', '', '', 'false'],
            ['Sed diam lorem, auctor quis, tristique', 0.1489477999, '+', 'false'],
            ['false', 0, '-', False]
            ],
            columns=['words', 'number', 'polarity', 'false']
            ),
        # special_characters
        '+-',
        # falsey_is_null
        True,
        # expected
        pd.DataFrame([
            ['eleifend vitae', 0.2289343509, '+'],
            ['non lorem vitae odio', 0.1746509874, '-'],
            ['egestas', 0.248639792, '-'],
            ['Sed diam lorem, auctor quis, tristique', 0.1489477999, '+'],
            [np.nan, np.nan, '-']
            ],
            columns=['words', 'number', 'polarity'],
            dtype='object'
            ),
        )
])
def test_dataframe_clean_null_w_cleaning_params(df, special_characters, falsey_is_null, expected):
    dataframe_clean_null(df, special_characters=special_characters, falsey_is_null=falsey_is_null)

    assert df.equals(expected)
    assert df.columns.equals(expected.columns)
    assert df.index.equals(expected.index)
