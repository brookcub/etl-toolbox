import pytest
from etl_toolbox.mapping_functions import map_labels


@pytest.mark.parametrize("labels, fingerprint_map, expected", [
    (
        ['NAME1', 'NAME2', 'PHON#'],
        {'name1': 'first_name', 'name2': 'last_name', 'phon': 'phone'},
        ['first_name', 'last_name', 'phone']
        ),
    (
        ['$amount', 'field_2', 'sessionID', 'method', ''],
        {'field2': 'first_name', 'amount': 'cost', 'emailaddress': 'email'},
        ['cost', 'first_name', None, None, None]
        )
])
def test_map_labels(labels, fingerprint_map, expected):
    assert map_labels(labels, fingerprint_map) == expected


@pytest.mark.parametrize("labels, fingerprint_map, special_characters, expected", [
    (
        ['#', '$', 'EML_Addr'],
        {'$': 'cost', '#': 'phone', 'emladdr': 'email'},
        '$#',
        ['phone', 'cost', 'email']
        )
])
def test_map_labels_w_special_characters(labels, fingerprint_map,
                                         special_characters, expected):
    assert map_labels(labels, fingerprint_map,
                      special_characters=special_characters) == expected


@pytest.mark.parametrize("labels, fingerprint_map, expected", [
    (
        ['$amount', 'field_2', 'sessionID', 'method', ''],
        {'field2': 'first_name', 'amount': 'cost', 'emailaddress': 'email'},
        (['cost', 'first_name', None, None, None], {'sessionID', 'method', ''})
        )
])
def test_map_labels_w_return_unmapped(labels, fingerprint_map, expected):
    assert map_labels(labels, fingerprint_map, return_unmapped=True) == expected
