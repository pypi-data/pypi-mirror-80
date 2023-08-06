#!/usr/bin/env python
# test_person.py
"""Tests for `person` package."""
import pytest
from context import constants  # noqa
from context import helpers  # noqa
from context import politician_role  # noqa

# pylint: disable=redefined-outer-name


def test_person_Politician(politician_fixture):
    # pylint: disable=W0612, W0613

    pol_1 = politician_role.Politician(
        "CDU",
        "Regina",
        "Dinther",
        peer_title="van",
        electoral_ward="Rhein-Sieg-Kreis IV",
    )

    assert pol_1.first_name == "Regina"
    assert pol_1.last_name == "Dinther"
    assert pol_1.gender == "female"
    assert pol_1.peer_preposition == "van"
    assert pol_1.party_name == "CDU"
    assert pol_1.ward_no == 28
    assert pol_1.voter_count == 110389

    pol_1.party_name = "fraktionslos"
    assert pol_1.party_name == "fraktionslos"
    assert pol_1.parties == [
        helpers.Party(
            party_name="CDU", party_entry="unknown", party_exit="unknown"
        )  # noqa
    ]  # noqa

    pol_2 = politician_role.Politician(
        "CDU",
        "Regina",
        "Dinther",
        electoral_ward="Landesliste",
    )  # noqa

    assert pol_2.electoral_ward == "ew"

    pol_3 = politician_role.Politician(
        "Piraten",
        "Heiner",
        "Wiekeiner",
        electoral_ward="Kreis Aachen I",
    )  # noqa

    assert pol_3.voter_count == 116389

    with pytest.raises(helpers.NotGermanParty):
        pol_4 = politician_role.Politician(
            "Thomas", "Gschwindner", "not_a_German_party"
        )  # noqa

    pol_4 = politician_role.Politician("FDP", "Thomas", "Gschwindner")
    pol_4.add_Party("FDP")

    assert pol_4.party_name == "FDP"
    assert pol_4.parties == [
        helpers.Party(
            party_name="FDP", party_entry="unknown", party_exit="unknown"
        )  # noqa
    ]  # noqa

    pol_4.add_Party("not_a_German_party")

    assert pol_4.party_name == "FDP"
    assert pol_4.parties == [
        helpers.Party(
            party_name="FDP", party_entry="unknown", party_exit="unknown"
        )  # noqa
    ]  # noqa

    pol_4.add_Party("AfD")

    assert pol_4.parties == [
        helpers.Party(
            party_name="FDP", party_entry="unknown", party_exit="unknown"
        ),  # noqa
        helpers.Party(
            party_name="AfD", party_entry="unknown", party_exit="unknown"
        ),  # noqa
    ]

    pol_4.add_Party("AfD", party_entry="2019")

    assert pol_4.party_entry == "2019"
    assert pol_4.parties == [
        helpers.Party(
            party_name="FDP", party_entry="unknown", party_exit="unknown"
        ),  # noqa
        helpers.Party(
            party_name="AfD", party_entry="2019", party_exit="unknown"
        ),  # noqa
    ]

    pol_4.add_Party("AfD", party_entry="2019", party_exit="2020")

    assert pol_4.party_exit == "2020"
    assert pol_4.parties == [
        helpers.Party(
            party_name="FDP", party_entry="unknown", party_exit="unknown"
        ),  # noqa
        helpers.Party(party_name="AfD", party_entry="2019", party_exit="2020"),
    ]

    pol_5 = politician_role.Politician(
        "Linke", "Heiner", "Wiekeiner", electoral_ward="Köln I"
    )  # noqa

    assert pol_5.ward_no == 13
    assert pol_5.voter_count == 121721

    pol_6 = politician_role.Politician("Grüne", "Heiner", "Wiekeiner")

    assert pol_6.electoral_ward == "ew"
    assert pol_6.ward_no is None
    assert pol_6.voter_count is None

    pol_6.change_ward("Essen III")

    assert pol_6.electoral_ward == "Essen III"
    assert pol_6.ward_no == 67
    assert pol_6.voter_count == 104181
