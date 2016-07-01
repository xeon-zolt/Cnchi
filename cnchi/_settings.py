#!/usr/bin/env python
#  -*- coding: utf-8 -*-
#
#  _settings.py
#
#  Copyright © 2016 Antergos
#
#  This file is part of The Antergos Build Server, (AntBS).
#
#  AntBS is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  AntBS is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  The following additional terms are in effect as per Section 7 of the license:
#
#  The preservation of all legal notices and author attributions in
#  the material or in the Appropriate Legal Notices displayed
#  by works containing it is required.
#
#  You should have received a copy of the GNU General Public License
#  along with AntBS; If not, see <http://www.gnu.org/licenses/>.

""" Classes and data descriptor objects for the storage and retrieval of shared data/settings. """

from config import settings


class Singleton(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__call__(*args, **kwargs)

        return cls._instance


class DataObject:
    """
    Generic object used to store data/settings as attributes.

    Args:
        from_dict (dict): Initialize object using dict.

    """

    def __init__(self, from_dict=None):
        _from_dict = from_dict is not None and isinstance(from_dict, dict)
        self._initialized = False

        if _from_dict and not self._initialized:
            for key, val in from_dict.items():
                setattr(self, key, val)

            self._initialized = True


class SharedData(metaclass=Singleton):
    """
    Descriptor that facilitates shared data storage/retrieval.

    Attributes:
        name      (str):  The name of the bound attribute.
        from_dict (dict): Initial data to store.

    """

    _data = None

    def __init__(self, name, from_dict=None):
        self.name = name

        if self._data is None:
            self._data = DataObject(from_dict=from_dict)

    def __get__(self, instance, cls):
        return self._data


class NonSharedData(metaclass=Singleton):
    """
    Data descriptor that facilitates per-instance data storage/retrieval.

    Attributes:
        name      (str): The name of the bound attribute.
        from_dict (dict): Initial data to store.

    """

    _data = None

    def __init__(self, name):
        self.name = name

        if self._data is None:
            self._data = dict()

    def __get__(self, instance, cls):
        self._instance_data_check(instance)
        return self._data[instance.name]

    def __set__(self, instance, value):
        self._instance_data_check(instance)
        self._data[instance.name] = value

    def _instance_data_check(self, instance):
        if instance.name not in self._data:
            self._data[instance.name] = DataObject()


