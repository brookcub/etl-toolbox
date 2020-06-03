import pytest
import itertools
from etl_toolbox.mapping_functions import map_labels, rename_duplicate_labels

##
## map_labels() tests
##

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


##
## rename_duplicate_labels() tests
##

@pytest.mark.parametrize("labels, expected", [
    (
        ['email', 'email', 'email', 'phone', 'name', 'email', 'phone'],
        ['email_1', 'email_2', 'email_3', 'phone_1', 'name', 'email_4', 'phone_2']
        ),
    (
        ['name', 'date', 'time', 'phone', 'email'],
        ['name', 'date', 'time', 'phone', 'email']
        )
])
def test_rename_duplicate_labels(labels, expected):
    assert rename_duplicate_labels(labels) == expected


@pytest.mark.parametrize("labels, rename_generator, expected", [
    (
        ['email', 'email', 'email', 'phone', 'name', 'email', 'phone'],
        # Hip lambda generator comprehension:
        lambda x: (str(i) + x for i in itertools.count()),
        ['0email', '1email', '2email', '0phone', 'name', '3email', '1phone']
        ),
    (
        ['name', 'date', 'time', 'phone', 'email'],
        lambda x: (str(i) + x for i in itertools.count()),
        ['name', 'date', 'time', 'phone', 'email']
        )
])
def test_rename_duplicate_labels_w_rename_generator(labels, rename_generator, expected):
    assert rename_duplicate_labels(labels, rename_generator=rename_generator) == expected
