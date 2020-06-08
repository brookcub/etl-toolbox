import pytest
import pandas as pd
from etl_toolbox.dataframe_functions import find_column_labels


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
