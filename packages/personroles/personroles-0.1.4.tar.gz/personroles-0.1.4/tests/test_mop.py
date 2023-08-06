#!/usr/bin/env python
# test_person.py
"""Tests for `person` package."""
import pytest
from context import constants  # noqa
from context import helpers  # noqa
from context import mop_role

# pylint: disable=redefined-outer-name


def test_person_MoP(mop_fixture):
    # pylint: disable=W0612, W0613

    mop = mop_role.MoP(
        "14",
        "NRW",
        "Grüne",
        "Alfons-Reimund",
        "Hubbeldubbel",
        peer_title="auf der",
        electoral_ward="Ennepe-Ruhr-Kreis I",
        minister="JM",
    )

    assert mop.legislature == "14"
    assert mop.first_name == "Alfons-Reimund"
    assert mop.last_name == "Hubbeldubbel"
    assert mop.gender == "male"
    assert mop.peer_preposition == "auf der"
    assert mop.party_name == "Grüne"
    assert mop.parties == [
        helpers.Party(
            party_name="Grüne", party_entry="unknown", party_exit="unknown"
        )  # noqa
    ]  # noqa
    assert mop.ward_no == 105
    assert mop.minister == "JM"

    mop.add_Party("fraktionslos")
    assert mop.party_name == "fraktionslos"
    assert mop.parties == [
        helpers.Party(
            party_name="Grüne", party_entry="unknown", party_exit="unknown"
        ),  # noqa
        helpers.Party(
            party_name="fraktionslos",
            party_entry="unknown",
            party_exit="unknown",  # noqa
        ),
    ]


def test_person_NotInRangeError(notinrange_fixture):
    # pylint: disable=W0612, W0613
    mop = mop_role.MoP

    with pytest.raises(helpers.NotInRange):
        mop("100", "NRW", "SPD", "Alfons-Reimund", "Hubbeldubbel")
