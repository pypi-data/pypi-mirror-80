#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A set of dataclasses concerning roles of persons and their particulars.
"""
import os
import sys
from dataclasses import dataclass, field
from typing import List, Optional

PACKAGE_PARENT = ".."
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
)  # isort:skip # noqa # pylint: disable=wrong-import-position
sys.path.append(
    os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT))
)  # isort: skip # noqa # pylint: disable=wrong-import-position

from personroles.person import Person  # type: ignore  # noqa
from personroles.resources import helpers  # type: ignore  # noqa
from personroles.resources.constants import (  # type: ignore # noqa
    GERMAN_PARTIES,
    PEER_PREPOSITIONS,
    PEERTITLES,
)
from personroles.resources.helpers import AttrDisplay  # type: ignore # noqa
from personroles.resources.helpers import NotInRange  # type: ignore # noqa
from personroles.resources.helpers import Party  # type: ignore # noqa
from personroles.resources.helpers import TooManyFirstNames  # noqa


@dataclass
class _Politician_default:
    electoral_ward: str = field(default="ew")
    ward_no: Optional[int] = field(default=None)
    voter_count: Optional[int] = field(default=None)
    minister: Optional[str] = field(default=None)
    offices: List[str] = field(default_factory=lambda: [])
    parties: List[str] = field(default_factory=lambda: [])

    def renamed_wards(self):
        wards = {
            "Kreis Aachen I": "Aachen III",
            "Hochsauerlandkreis II – Soest III": "Hochsauerlandkreis II",
            "Kreis Aachen II": "Aachen IV"
            if self.last_name in ["Wirtz", "Weidenhaupt"]
            else "Kreis Aachen I",
        }
        if self.electoral_ward in wards.keys():
            self.electoral_ward = wards[self.electoral_ward]

    def scrape_wiki_for_ward(self) -> None:
        import requests
        from bs4 import BeautifulSoup  # type: ignore

        URL_base = "https://de.wikipedia.org/wiki/Landtagswahlkreis_{}"
        URL = URL_base.format(self.electoral_ward)
        req = requests.get(URL)
        bsObj = BeautifulSoup(req.text, "lxml")
        table = bsObj.find(class_="infobox float-right toptextcells")
        self.scrape_wiki_table_for_ward(table)

    def scrape_wiki_table_for_ward(self, table) -> None:
        for td in table.find_all("td"):
            if "Wahlkreisnummer" in td.text:
                ward_no = td.find_next().text.strip()
                ward_no = ward_no.split(" ")[0]
                self.ward_no = int(ward_no)
            elif "Wahlberechtigte" in td.text:
                voter_count = td.find_next().text.strip()
                voter_count = self.fix_voter_count(voter_count)
                self.voter_count = int(voter_count)

    def fix_voter_count(self, voter_count):
        if voter_count[-1] == "]":
            voter_count = voter_count[:-3]
        if " " in voter_count:
            voter_count = "".join(voter_count.split(" "))
        else:
            voter_count = "".join(voter_count.split("."))
        return voter_count


@dataclass
class Politician(
    _Politician_default,
    helpers._Party_default,
    Person,
    helpers._Party_base,
    AttrDisplay,
):
    def __post_init__(self):
        Party.__post_init__(self)
        Person.__post_init__(self)
        Person.get_sex(self)
        Person.get_age(self)
        self.change_ward()
        if self.party_name in GERMAN_PARTIES:
            self.parties.append(
                Party(self.party_name, self.party_entry, self.party_exit)
            )
        if self.minister and self.minister not in self.offices:
            self.offices.append(self.minister)

    def add_Party(
        self, party_name, party_entry="unknown", party_exit="unknown"
    ):  # noqa
        if party_name in GERMAN_PARTIES:
            if self.party_is_in_parties(party_name, party_entry, party_exit):
                pass
            else:
                self.parties.append(Party(party_name, party_entry, party_exit))
                self.party_name = party_name
                self.party_entry = party_entry
                self.party_exit = party_exit

    def align_party_entries(
        self, party, party_name, party_entry, party_exit
    ) -> Party:  # noqa
        if party_entry != "unknown" and party.party_entry == "unknown":
            party.party_entry = party_entry
        if party_exit != "unknown" and party.party_exit == "unknown":
            party.party_exit = party_exit
        return party

    def party_is_in_parties(self, party_name, party_entry, party_exit):
        parties_tmp = self.parties[:]
        for party in parties_tmp:
            if party_name == party.party_name:
                party_updated = self.align_party_entries(
                    party, party_name, party_entry, party_exit
                )
                self.parties.remove(party)
                self.parties.append(party_updated)
                self.party_entry = party_updated.party_entry
                self.party_exit = party_updated.party_exit
                return True
        return False

    def change_ward(self, ward=None):
        if ward:
            self.electoral_ward = ward
        if self.electoral_ward not in ["ew", "Landesliste"]:
            self.renamed_wards()
            self.scrape_wiki_for_ward()
        else:
            self.electoral_ward = "ew"


if __name__ == "__main__":

    politician = Politician(
        "SPD",
        "Bärbel",
        "Gutherz",
        academic_title="Dr.",
        date_of_birth="1980",
        electoral_ward="Köln I",
    )
    print(politician)
