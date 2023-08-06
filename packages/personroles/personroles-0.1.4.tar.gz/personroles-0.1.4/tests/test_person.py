#!/usr/bin/env python
# test_person.py
"""Tests for `person` package."""
from dataclasses import dataclass

import pytest
from context import constants  # noqa
from context import helpers  # noqa
from context import person

# pylint: disable=redefined-outer-name


names = [
    ["Alfons-Reimund Horst Emil", "Boeselager"],
    ["Horatio R.", "Pimpernell"],
    ["Sven Jakob", "Große Brömer"],
]


def equivalent_names(n1, n2):
    fn = n2[0].split()[0]
    ln = n2[-1]
    try:
        mn_2 = n2[0].split()[2]
    except IndexError:
        mn_2 = None
    try:
        mn_1 = n2[0].split()[1]
    except IndexError:
        mn_1 = None

    return (
        (n1.first_name == fn)
        and (n1.middle_name_1 == mn_1)
        and (n1.middle_name_2 == mn_2)
        and (n1.last_name == ln)
    )


@pytest.mark.parametrize("n", names)
def test_person_Name_para(n):
    name = person.Name(*n)
    assert equivalent_names(name, n)


def test_person_Name(name_fixture):
    # pylint: disable=W0612, W0613

    name = person.Name("Alfons-Reimund Horst Emil", "Boeselager")
    assert name.first_name == "Alfons-Reimund"
    assert name.middle_name_1 == "Horst"
    assert name.middle_name_2 == "Emil"
    assert name.last_name == "Boeselager"


def test_person_Academic(academic_fixture):
    # pylint: disable=W0612, W0613

    academic = person.Academic(
        "Horatio",
        "Pimpernell",
        middle_name_1="R.",
        academic_title="Prof.Dr.   Dr",  # noqa
    )
    assert academic.first_name == "Horatio"
    assert academic.middle_name_1 == "R."
    assert academic.last_name == "Pimpernell"
    assert academic.academic_title == "Prof. Dr. Dr."

    academic = person.Academic(
        "Horatio Rübennase D.", "Pimpernell", academic_title="Prof.Dr.Dr"
    )
    assert academic.first_name == "Horatio"
    assert academic.middle_name_1 == "Rübennase"
    assert academic.middle_name_2 == "D."
    assert academic.last_name == "Pimpernell"
    assert academic.academic_title == "Prof. Dr. Dr."

    academic = person.Academic("Horatio", "Pimpernell", academic_title="B.A.")
    assert academic.academic_title == "B. A."


def test_person_Noble(noble_fixture):
    # pylint: disable=W0612, W0613

    noble = person.Noble("Sepp Theo", "Müller", peer_title="von und zu")

    assert noble.first_name == "Sepp"
    assert noble.middle_name_1 == "Theo"
    assert noble.last_name == "Müller"
    assert noble.peer_preposition == "von und zu"

    noble = person.Noble("Seppl", "Müller", peer_title="Junker van")

    assert noble.first_name == "Seppl"
    assert noble.last_name == "Müller"
    assert noble.peer_title == "Junker"
    assert noble.peer_preposition == "van"

    noble = person.Noble("Sven Oskar", "Müller", peer_title="Graf Eumel von")

    assert noble.first_name == "Sven"
    assert noble.middle_name_1 == "Oskar"
    assert noble.last_name == "Müller"
    assert noble.peer_title == "Graf"
    assert noble.peer_preposition == "von"


def test_person_Person(person_fixture):
    # pylint: disable=W0612, W0613

    pers = person.Person(
        "Hugo", "Berserker", academic_title="MBA", date_of_birth="2000"
    )  # noqa

    assert pers.gender == "male"
    assert pers.academic_title == "MBA"
    assert pers.age == "20"

    pers = person.Person(
        "Siggi Mathilde", "Berserker", date_of_birth="1980-2010"
    )  # noqa

    assert pers.gender == "unknown"
    assert pers.middle_name_1 == "Mathilde"
    assert pers.year_of_birth == "1980"
    assert pers.deceased is True
    assert pers.year_of_death == "2010"

    pers = person.Person("Sigrid", "Berserker", date_of_birth="10.1.1979")  # noqa

    assert pers.gender == "female"
    assert pers.year_of_birth == "1979"

    pers = person.Person(
        "Sigrid", "Berserker", date_of_birth="10.1.1979 - 22.10.2019"
    )  # noqa

    assert pers.date_of_birth == "10.1.1979"
    assert pers.date_of_death == "22.10.2019"


def test_person_TooManyFirstNames(toomanyfirstnames_fixture):
    # pylint: disable=W0612, W0613

    name = person.Name
    with pytest.raises(helpers.TooManyFirstNames):
        name("Alfons-Reimund Horst Emil Pupsi", "Schulze")


def test_person_AttrDisplay(capsys, attrdisplay_fixture):
    # pylint: disable=W0612, W0613

    @dataclass
    class MockClass(helpers.AttrDisplay):
        a: str
        b: str
        c: str

    var_1 = "späm"
    var_2 = "ham"
    var_3 = "ew"

    mock_instance = MockClass(var_1, var_2, var_3)
    print(mock_instance)
    captured = capsys.readouterr()

    expected = """MockClass:\na=späm\nb=ham\n\n"""

    assert expected == captured.out
