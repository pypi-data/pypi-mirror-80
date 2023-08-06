""" singleton

Provides a meta class to ensure single instantiation.

"""
# DMT
# Copyright (C) 2019  Markus Müller and Mario Krattenmacher and the DMT contributors <https://gitlab.hrz.tu-chemnitz.de/CEDIC_Bipolar/DMT/>
#
# This file is part of DMT.
#
# DMT is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DMT is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

class Singleton(type):
    """ Implements the Singleton design pattern. Classes that use this class as a metaclass can only be initiated once.

    If a new object of a singleton class is instanciated, the already existing one is returned.
    But the added implementation here, tries to transfer the given kwargs to the old object.

    Source:
    https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
    """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
            obj = cls._instances[cls]
        else:
            obj = cls._instances[cls]
            if args:
                raise AttributeError('DMT: Can not set an value to an unknown attribute of the object.', 'Make sure, that all the wanted parameters are kwargs.')

            # Try to set kwargs as parameters for the class.
            for attr, value in kwargs.items():
                if hasattr(obj, attr) and not callable(getattr(obj, attr)):
                    setattr(obj, attr, value)
                else:
                    raise AttributeError('DMT: Can not set an attribute which is not a member of the object')

        return obj