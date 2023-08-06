#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Some helper functions
"""
from dataclasses import dataclass, field

from .constants import GERMAN_PARTIES  # type: ignore  # noqa


class NotInRange(Exception):

    """
    Until term 13 the available PDF files are scanned in and need OCR to be
    scraped. Therefore only terms 14 to currently term 17 are accepted.
    """

    pass


class NotGermanParty(Exception):

    """
    Since this project focusses on Germany the current range of parties that
    will be accepted is reduced to German parties.
    """

    pass


class TooManyFirstNames(Exception):

    """
    Currently only one first name and two middle names are supported.
    Example: Tom H. Paul last_name
    """

    def __init__(self, message):
        """use like: raise TooManyFirstNames ("message")"""
        Exception.__init__(self)
        print(message)


class AttrDisplay:

    """
    Mark Lutz, Programming Python
    Provides an inheritable display overload method that shows instances
    with their class names and a name=value pair for each attribute stored
    on the instance itself (but not attrs inherited from its classes). Can
    be mixed into any class, and will work on any instance.
    """

    def gather_attrs(self) -> list:
        """
        Check if attributes have content and add them to a list called attrs.
        """
        attrs = []
        for key in sorted(self.__dict__):
            if self.__dict__[key] and self.__dict__[key] not in [
                "unknown",
                "ew",
                None,
            ]:
                attrs.append(f"{key}={getattr(self, key)}")
        return attrs

    def __str__(self) -> str:
        """
        Instances will printed like this:
            class name
            attr1=value1
            attr2=value2
            ...
        """
        comp_repr = (
            f"{self.__class__.__name__}:\n"
            + "\n".join(str(attr) for attr in self.gather_attrs())
            + "\n"
        )
        return comp_repr


@dataclass
class _Party_base:
    party_name: str  # type: ignore  # noqa


@dataclass
class _Party_default:
    party_entry: str = field(default="unknown")
    party_exit: str = field(default="unknown")


@dataclass
class Party(_Party_default, _Party_base, AttrDisplay):
    def __post_init__(self):
        if self.party_name not in GERMAN_PARTIES:
            raise NotGermanParty
