import pytest
import pandas as pd
from etl_toolbox.dataframe_functions import find_column_labels
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
        {'emladdr': 'email_address',
         'dte': 'date',
         'phnnmbr': 'phone_number',
         'nom': 'name',
         'time': 'time'},
        # expected
        pd.DataFrame([
            ['test@test.com', '04mar14', '12045', '999-333-4444', 'AAA'],
            ['green@green.com', None, '32124', '111-222-3333', 'BAA'],
            ['EML-addr', 'Dte', 'col3', 'phn-nmbr', 'NOM'],
            ['one@one.com', '01jun15', 77777, '777-777-7777', 'CAA']
            ],
            columns=['EML-addr', 'Dte', 'col3', 'phn-nmbr', 'NOM']
            )
        )
])
def test_find_column_labels(df, label_fingerprints, expected):
    find_column_labels(df, label_fingerprints)
    assert df.equals(expected)
    assert df.columns.equals(expected.columns)


@pytest.mark.parametrize('df, label_fingerprints', [
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
        {'emladdr': 'email_address',
         'dte': 'date',
         'time': 'time'}
        )
])
def test_find_column_labels_exceptions(df, label_fingerprints):
    """test that ValueError is raised if label row isn't found"""
    with pytest.raises(ValueError):
        assert find_column_labels(df, label_fingerprints)


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
        )
])
def test_merge_columns_by_label_dedup(df, expected):
    merge_columns_by_label(df, deduplicate_values=True)
    assert df.equals(expected)
    assert df.columns.equals(expected.columns)
