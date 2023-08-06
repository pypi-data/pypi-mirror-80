#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A set of dataclasses concerning roles of persons and their particulars.
"""
import os
import sys
from dataclasses import dataclass, field
from typing import List, Set

PACKAGE_PARENT = ".."
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
)  # isort:skip # noqa # pylint: disable=wrong-import-position
sys.path.append(
    os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT))
)  # isort: skip # noqa # pylint: disable=wrong-import-position

from personroles.politician_role import Politician  # type: ignore  # noqa
from personroles.resources.helpers import AttrDisplay  # type: ignore # noqa
from personroles.resources.helpers import NotInRange  # type: ignore # noqa


@dataclass
class _MoP_default:
    parl_pres: bool = field(default=False)
    parl_vicePres: bool = field(default=False)
    parliament_entry: str = field(default="unknown")  # date string: "11.3.2015"  # noqa
    parliament_exit: str = field(default="unknown")  # dto.
    speeches: List[str] = field(
        default_factory=lambda: []
    )  # identifiers for speeches  # noqa
    reactions: List[str] = field(
        default_factory=lambda: []
    )  # identifiers for reactions
    membership: Set[str] = field(
        default_factory=lambda: set()
    )  # years like ["2010", "2011", ...]


@dataclass
class _MoP_base:
    legislature: str
    state: str


@dataclass
class MoP(_MoP_default, Politician, _MoP_base, AttrDisplay):
    def __post_init__(self):
        if int(self.legislature) not in range(14, 18):
            raise NotInRange("Number for legislature not in range")
        else:
            self.membership.add(self.legislature)
        Politician.__post_init__(self)


if __name__ == "__main__":

    mop = MoP(
        "14",
        "NRW",
        "SPD",  # type: ignore
        "Tom",  # type: ignore
        "Schwadronius",
        party_entry="1990",  # type: ignore
        peer_title="Junker von",
        date_of_birth="1950",
    )
    print(mop)

    mop.add_Party("Grüne", party_entry="30.11.1999")
    mop.change_ward("Düsseldorf II")
    print(mop)
