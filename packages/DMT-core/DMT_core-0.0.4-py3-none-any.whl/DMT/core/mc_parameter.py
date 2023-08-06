""" Base class to handle Verilog-AMS modelcard parameters.

Each parameter has a type, unit, boundaries and invalid values (excludes),
this is taken care of here.
Usually the user has a group of parameters stored in a Composition.
The composition exposes methods to manage the group safely. In generall here many copies are used,
in the exposes methods always deepcopies are returned and set to the composition. This reduces crazy errors, but also need to be handled with care.

Additionally parameters can be compared, they are considered equal, if they have the
same name and value. Also compositions can be compared, they are equal, if they have
the same parameters and all parameters are equal.

Finally the classes here also add some pretty printing and loading and saving using pickle.

Author: Mario Krattenmacher | Mario.Krattenmacher@tu-dresden.de
Author: Markus Müller       | Markus.Mueller3@tu-dresden.de
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
import numpy as np
import logging
import copy
import os
import json
import _pickle as cpickle
from pathlib import Path
from pint.formatting import siunitx_format_unit
from pint.errors import UndefinedUnitError

from DMT.core import unit_registry
from DMT.exceptions import ValueExcludedError, ValueTooLargeError, ValueTooSmallError, BoundsError, ParaExistsError

try:
    # try to import only, so it is a soft dependency...
    from pylatex import LongTable, MultiColumn, Section, NoEscape
    from DMT.external.pylatex import Tex # pylint: disable=ungrouped-imports
except ImportError:
    pass


class McParameter(object):
    """ Objects of this class represent a model card parameter. If you want to store many of them, see McParameterComposition class.

    Attributes
    ----------
    _value   :  np.array([np.float64])
        The value of this parameter.
    name     :  string
        The name of the parameter.
    inc_min  :  bool
        If True, value==min is allowed.
    inc_max  :  bool
        If True, value==max is allowed.
    min      :  np.array([np.float64])
        The minimum boundary of this parameter.
    max      :  np.array([np.float64])
        The maximum boundary of this parameter.
    exclude  :  float64
        Optional value that can be excluded as a valid value for value. E.g. if min=-1, max=1, sometimes you might want to exclude 0.
    val_type : type
        The type of the value.

    Parameters
    ----------
    value : float64
        Value for the parameter. Can also be a other Parameter, then all attributes are copied.
    name : str
        Name of the parameter.
    unit : pint.unit
        Unit of the python Pint package.
    minval : float64
        Minimum boundary value of the parameter.
    maxval : float64
        Maximum boundary value of the parameter.
    group  : str
        Display is sorted by groups.

    Methods
    -------
    check_bounds(value)
        Check wheather or not value is within the bounds of this parameter.

    """
    def __init__(self, name, value=None, minval=None, maxval=None, value_type=np.float, inc_min=True, inc_max=True, exclude=None,
    group='',unit=unit_registry.dimensionless, description='' ):

        if not isinstance(name, str):
            raise IOError('DMT -> McParameter: Parameter name not a string.')
        self.name       =  name
        self.inc_min    =  inc_min
        self.inc_max    =  inc_max
        if value_type in (int, np.int):
            self._val_type  =  np.int
        elif value_type in (float, np.float):
            self._val_type  =  np.float
        else:
            raise NotImplementedError('The type ' + str(value_type) + ' of parameter value is not known! Allowed: int, np.int, float, np.float.')

        if minval is None:
            self._min   =  -np.inf
        else:
            self._min   =  self._val_type(minval)
        if maxval is None:
            self._max   =  np.inf
        else:
            self._max   =  self._val_type(maxval)

        self.exclude    =  exclude
        self._value     =  self._val_type(value)
        self.unit       =  unit
        self.group      =  group
        self.description =  description

    def dict_json(self):
        """ Returns a compact formated json dump of this parameter
        """
        if self._val_type in (int, np.int):
            str_type  =  'int'
        elif self._val_type in (float, np.float):
            str_type  =  'float'
        else:
            str_type = str(self._val_type) # make it saveable always...

        try:
            desc = self.description
        except AttributeError:
            desc = ''

        return {
            'name': self.name,
            'value': self._value,
            'min': self._min,
            'max': self._max,
            'inc_min': self.inc_min,
            'inc_max': self.inc_max,
            'exclude': self.exclude,
            'type': str_type,
            'unit': str(self.unit),
            'group': self.group,
            'description': desc,
            '__McParameter__': 1.0, # make versions, so we can introduce compatibility here!
        }

    @classmethod
    def load_json(cls, dict_parameter):
        """ Creates a McParameter from a dictionary obtained by a json.load.
        """
        if '__McParameter__' in dict_parameter and dict_parameter['__McParameter__'] == 1.0:
            try:
                value_type = {'int': np.int, 'float':np.float}[dict_parameter['type']]
            except KeyError:
                value_type = dict_parameter['type']

            try:
                unit = unit_registry(dict_parameter['unit']).units
            except UndefinedUnitError:
                unit = None

            return McParameter(
                dict_parameter['name'],
                value=dict_parameter['value'],
                unit=unit,
                minval=dict_parameter['min'],
                maxval=dict_parameter['max'],
                group=dict_parameter['group'],
                value_type=value_type,
                inc_min=dict_parameter['inc_min'],
                inc_max=dict_parameter['inc_max'],
                exclude=dict_parameter['exclude'],
                description=dict_parameter.get('description', ''),
            )
        else:
            raise ValueError('DMT->McParameter: This dict is not a serialized McParameter')

    @property
    def val_type(self):
        """ Return the type of the value.
        """
        return self._val_type

    @val_type.setter
    def val_type(self, new_type):
        """ Set the type of this parameter.
        """
        if new_type in (int, np.int):
            if self._value == np.int(self._value): # test if roundable...
                self._value = np.int(self._value)
                self._val_type = np.int
            else:
                raise IOError("The parameter value was a floating number and it was tried to set the parameter type to integer. The parameter name is: " + self.name)
        elif new_type in (float, np.float):
            self._value = np.float(self._value) # can be set always
            self._val_type = new_type
        else:
            raise IOError("This type can not be set for McParameter: " + str(new_type) + ". The parameter name is: " + self.name)

    @property
    def min(self):
        """ Return The minimum boundary as an array of length one.
        """
        return self._min

    @min.setter
    def min(self, min_new):
        """ Set the minimum boundary and throw errors if min>value or min>max, testing inc_min before doing so.
        """
        if min_new > self.max:
            raise BoundsError('DMT -> McParameter: The new minimum is above the maximum of the parameter')

        if self.inc_min:
            if min_new > self.value:
                raise BoundsError('DMT -> McParameter: Parameter min value of ' + self.name + ' can not be set to ' + str(min_new) + ' since value is currenty ' + str(self.value) + ' .')
        else:
            if min_new >= self.value:
                raise BoundsError('DMT -> McParameter: Parameter min value of ' + self.name + ' can not be set to ' + str(min_new) + ' since value is currenty ' + str(self.value) + ' .')

        self._min = self.val_type(min_new)

    @property
    def max(self):
        """ Return The minimum boundary as an array of length one.
        """
        return self._max

    @max.setter
    def max(self, max_new):
        """ Set the max boundary and throw errors if max<value or max<max, testing inc_max before doing so.
        """
        if max_new < self.min:
            raise BoundsError('DMT -> McParameter: The new minimum is above the maximum of the parameter')

        if self.inc_max:
            if max_new < self.value:
                raise BoundsError('DMT -> McParameter: Parameter max value of ' + self.name + ' can not be set to ' + str(max_new) + ' since value is currenty ' + str(self.value) + ' .')
        else:
            if max_new <= self.value:
                raise BoundsError('DMT -> McParameter: Parameter max value of ' + self.name + ' can not be set to ' + str(max_new) + ' since value is currenty ' + str(self.value) + ' .')

        self._max = self.val_type(max_new)

    @property
    def value(self):
        """ Returns the value.
        """
        return self._value

    @value.setter
    def value(self, value):
        if isinstance(value, McParameter):
            self.name       = value.name
            self._min       = value._min # pylint: disable=protected-access
            self._max       = value._max # pylint: disable=protected-access
            self.inc_max    = value.inc_max
            self.inc_min    = value.inc_min
            self.exclude    = value.exclude
            self._val_type  = value.val_type
            self.value      = value.value
        else:
            value = self.check_bounds(value)
            self._value  =  value

    def _set_forced(self, value):
        """ force setting the value. ATTENTION: When used, the boundaries may be set to inf!
        """
        try:
            # try without changing bounds
            self.value = value
        except (ValueTooLargeError,ValueTooSmallError,ValueExcludedError):
            if isinstance(value, McParameter):
                raise IOError('McParameter _set_forced: The given McParameter is already inconsistent. Stop.')
            else:
                # set to no bounds
                if self.val_type == np.float:
                    self._min = -np.inf
                    self._max = np.inf
                elif self.val_type == np.int: # inf not possible in integer...
                    self._min = np.iinfo(np.int).min
                    self._max = np.iinfo(np.int).max
                else:
                    raise NotImplementedError()
                self._value = self.val_type(value)

    def check_bounds(self,value):
        """ Check wheather the value parameter is inside the boundaries defined by self.min and self.max.

        Parameters
        ----------
        value  :  int or float or convertable to float
            Value that shall be checked.

        Returns
        -------
        value  :  int or float
            Checked value
        """
        # type check, either int or float is allowed
        if self.val_type == np.int:
            if np.int(value) != value:
                raise TypeError("The parameter {:s} is of type Integer!".format(self))

            value = np.int(value)
        elif not isinstance(value, (int, float, np.int, np.float)): # for floats also integer are allowed. This catches everything else like strings or lists etc.
            raise TypeError("The parameter {:s}  is of type Float!".format(self))

        # range check
        value_too_large = False
        value_too_small = False
        value_excluded  = False

        if self.inc_min         and value < self.min:
            value_too_small = True
        elif not self.inc_min   and value <= self.min:
            value_too_small = True

        if self.inc_max         and value > self.max:
            value_too_large = True
        elif not self.inc_max   and value >= self.max:
            value_too_large = True

        # exclude check
        if self.exclude is not None:
            if value == self.exclude:
                value_excluded = True

        if value_too_large:
            raise ValueTooLargeError(
                "Value of {0:s} above its maximum! Given: {1:e}! Maximum boundary : {2:e}!".format(self, value, self.max)
            )

        if value_too_small:
            raise ValueTooSmallError(
                "Value of {0:s} below its minimum! Given: {1:e}! Minimum boundary : {2:e}!".format(self, value, self.min)
            )

        if value_excluded:
            raise ValueExcludedError(
                "Value of {0:s} is excluded! Given: {1:e}! Excluded : {2:e}!".format(self, value, self.exclude)
            )

        return value

    def __format__(self, wanted_format):
        """ Allows formating of McParameters using "{}".format(mc_parameter).

        If a number format (defg) is given, the value is formated, for strings (s) the name.
        Additionally the unit (u) in siunitx format is possible.
        """
        if ('d' in wanted_format) or ('e' in wanted_format) or ('f' in wanted_format) or ('g' in wanted_format):
            if self.value is None:
                return '-' #dirty
            else:
                return ('{0:' + wanted_format +'}').format(self.value)
        elif 's' in wanted_format:
            return ('{0:' + wanted_format +'}').format(self.name)
        elif 'u' in wanted_format:
            if hasattr(self, 'unit') and self.unit is not None and not self.unit.dimensionless:
                return siunitx_format_unit(self.unit)
            else:
                return '-'
        else:
            raise IOError('The format {:s} is unknown for McParameters!'.format(wanted_format))

    def __eq__(self, other):
        """ Comparing parameters, equal if name and value is equal.
        """
        if isinstance(other, McParameter):
            return (self.name == other.name) and (self.value == other.value)

        return NotImplemented


class McParameterComposition(object):
    """

    This parameter composition has properties which as a single parameter. This way a group of parameters and a single parameter can be treated equally.

    Attributes
    ----------
    paras : list
        The parameters of this group
    """
    def __init__(self, __McParameterComposition__=1.0, **_kwargs):

        if __McParameterComposition__ != 1.0:
            raise NotImplementedError('DMT->McParameterComposition: Unknown version of composition to create!')
        self.__McParameterComposition__ = __McParameterComposition__

        self.paras = list()

    def info_json(self):
        """ Returns a dict with serializeable content for the json file to create. Add the info about the concrete subclass to create here!
        """
        if hasattr(self, '__McParameterComposition__'):
            return {'__McParameterComposition__': self.__McParameterComposition__ } # make versions, so we can introduce compatibility here!
        else:
            return {'__McParameterComposition__': 1.0 } # make versions, so we can introduce compatibility here!

    def dump_json(self, file_path):
        """ Writes itself and the parameters in the composition to a file.

        To manipulate what is written to the file, change :method:`DMT.core.mc_parameter.McParameterComposition.dumps_json()`
        """
        content = [self.info_json()]
        for para in sorted(self.paras, key=lambda x: (x.group, x.name)):
            content.append(para.dict_json())

        with open(file_path, 'w') as file_json:
            file_json.write('[\n    ')
            json.dump(self.info_json(), file_json)
            for para in sorted(self.paras, key=lambda x: (x.group, x.name)):
                file_json.write(',\n    ')
                json.dump(para.dict_json(), file_json)
            file_json.write('\n]')

    @classmethod
    def loads_json(cls, dict_parameter):
        """ Creates a McParameterComposition from a dictionary obtained by a json.load.
        """
        if '__McParameterComposition__' in dict_parameter:
            return McParameterComposition(**dict_parameter)
        else:
            raise IOError('DMT->McParameterComposition: The given dict has no __McParameterComposition__ key!')

    @classmethod
    def load_json(cls, file_path):
        with open(file_path, 'r') as file_json:
            content = json.load(file_json)

        composition = None
        for dict_content in content:
            if '__McParameterComposition__' in dict_content:
                composition = cls.loads_json(dict_content)
                break

        if composition is None:
            raise IOError('DMT->McParameterComposition: Did not create the composition')

        for dict_content in content:
            try:
                composition.add(McParameter.load_json(dict_content))
            except ParaExistsError:
                composition.set(McParameter.load_json(dict_content))
            except ValueError:
                pass

        return composition

    def get(self, parameters):
        """ Returns a McParameterComposition with copies of all given parameter names.

        Parameters
        -----------
        parameters  : str, iterable(str) or McParameterComposition

        Returns
        ---------
        mcard_collection : McParameterComposition

        Raises
        --------
        KeyError
            If the para was not in self.
        """
        if isinstance(parameters, (McParameterComposition, list, tuple)):
            mcard_collection  =  McParameterComposition()
            for para in parameters:
                mcard_collection.add(self.get(para))

            return mcard_collection

        try:
            if isinstance(parameters, McParameter):
                my_para = next(para for para in self.paras if para.name == parameters.name)
            elif isinstance(parameters, str):
                my_para = next(para for para in self.paras if para.name == parameters)
            else:
                raise IOError("The parameter is neither of type McParameter or str.")

            return copy.deepcopy(my_para)

        except StopIteration as err:
            raise KeyError("The parameter {0:s} is not part of this parameter collection!".format(parameters)) from err

    def __getitem__(self, para):
        """ Allows paras['c10']

        """
        return self.get(para)

    def set(self, parameters):
        """ Set existing paramaters in self.

        Parameters
        -----------
        parameters : McParameter or McParameterCollection
            For each parameter, if it is found in self, it is removed and the given is added. If it is not found, a KeyError is raised.

        Raises
        --------
        KeyError
            If the para was not in self.
        """
        if isinstance(parameters, McParameterComposition):
            for para in parameters:
                try:
                    self.set(para)
                except KeyError:
                    self.add(para)
            return

        try:
            index    = self.name.index(parameters.name)
        except ValueError as err:
            raise KeyError("The parameter {0:s} is not part of this parameter collection!".format(parameters)) from err

        self.remove(parameters.name)
        self.add(parameters, index=index)

    def __setitem__(self, name, value):
        """ Allows paras['c10']
        """
        para = self[name]
        para.value = value
        self.set(para)

    def set_values(self, dict_parameters, force=False):
        """ Sets a dictionary of {'name':value} to the parameters in this collection

        Parameters
        -----------
        dict_parameters : {str: float64}
            For each parameter, if it is found in self, the given value is set.
        force : boolean, optional
            If True, values are force set. If not existing, parameter is added. Set false if bounds from VA-File are used...

        Raises
        --------
        KeyError
            If the para was not in self.
        """
        for name, value in dict_parameters.items():
            try:
                index    = self.name.index(name)
            except ValueError as err:
                if force:
                    para = McParameter(name=name, value=value)
                    self.add(para)
                    index    = self.name.index(name)
                else:
                    raise KeyError("The parameter {0:s} is not part of this parameter collection!".format(name)) from err

            try:
                self.paras[index].value = value
            except ValueError as err:
                if force:
                    para = self.get(name)
                    para._set_forced(value) #pylint:disable=protected-access
                    self.set(para)
                else:
                    raise

    def get_values(self, parameters):
        """ Returns a list of the values of parameters.

        Parameters
        -----------
        parameters : {name:value}
            A dict with the name of the parameter as key and value as value.

        Raises
        --------
        KeyError
            If the para was not in self.
        """
        values = {}
        for i,name in enumerate(parameters):
            try:
                index    = self.name.index(name)
            except ValueError as err:
                raise KeyError("The parameter {0:s} is not part of this parameter collection!".format(name)) from err

            values[name] = self.paras[index].value

        return values

    def set_bounds(self, dict_parameters):
        """ Sets a dictionary of {'name':(min, max )} to the parameters in this collection

        Parameters
        -----------
        dict_parameters : {str: (float64, float64)}
            For each parameter, if it is found in self, the given values are set as minimum and maximum.

        Raises
        --------
        KeyError
            If the para was not in self.
        """
        for name, values in dict_parameters.items():
            try:
                index    = self.name.index(name)
            except ValueError as err:
                raise KeyError("The parameter {0:s} is not part of this parameter collection!".format(name)) from err

            self.paras[index].min = values[0]
            self.paras[index].max = values[1]

    def to_kwargs(self):
        """ Returns itself as a dictionary fitting to unpack into a function call.

        Returns
        ---------
        dict
            {name: value}
        """
        dict_a = {}
        for para in self.paras:
            dict_a[para.name] = para.value

        return dict_a

    def print_parameters(self, paras=None, line_break=''):
        """ Just some pretty printing

        Parameters
        ------------
        param : list[str], optional
            List of parameter names to print, if not given, all children are returned!
        line_break : str, optional
            Is added after each parameter, can be used as line breaks

        Returns
        --------
        str
            String with all parameters.
        """
        temp_str  =  ''
        if paras is None:
            # if None iterate through all
            paras = self
        else:
            paras = self.get(paras)

        for para in sorted(paras, key=lambda x: (x.group, x.name)):
            temp_str += "  {0:<12s} = {0:10.5e} ".format(para) + line_break

        return temp_str

    def print_to_file(self, path_to_file, line_break=''):
        """ Prints the parameters into a file. Uses :meth:`print_parameters` to obtain the string to print.

        Parameters
        ------------
        path_to_file : str
            Path to the file to write. '.txt' is added automatically.
        line_break : str, optionally
            Is added after each parameter, can be used as line breaks
        """
        if not path_to_file.endswith('.txt'):
            path_to_file = path_to_file + '.txt'

        with open(path_to_file, "w") as my_file:
            my_file.write(
                    self.print_parameters(line_break=line_break)
            )
            my_file.write("\n")

    def save(self, path, force=True):
        """ Saves the object to a pickle file, the file is silently overwritten per default.

        Parameters
        -----------
        path : str or os.Pathlike
            Path to the file to write.
        force : {True, False}, optional
            Flag to turn off overwriting.

        Raises
        -------
        FileExistsError
            If the file already exists and force is false.
        """
        # create all directories until database
        if not isinstance(path, Path):
            path = Path(path)

        if path.is_file() and not force:
            raise FileExistsError

        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open('wb') as my_pickle:
            cpickle.dump(self, my_pickle)

    # def save_json(self, path, force=True):
    #     """ Saves the parameters to a json file, the file is silently overwritten per default.

    #     Parameters
    #     -----------
    #     path : str or os.Pathlike
    #         Path to the file to write.
    #     force : {True, False}, optional
    #         Flag to turn off overwriting.

    #     Raises
    #     -------
    #     FileExistsError
    #         If the file already exists and force is false.
    #     """
    #     # create all directories until database
    #     if not isinstance(path, Path):
    #         path = Path(path)

    #     if path.is_file() and not force:
    #         raise FileExistsError

    #     path.parent.mkdir(parents=True, exist_ok=True)

    #     #create dict from information in modelcard
    #     all_paras = {}
    #     for para in self:
    #         all_paras[para.name] = {}
    #         all_paras[para.name]['low'] = para.low

    #     with path.open('wb') as fp:
    #         json.dump(sample, fp)

    @classmethod
    def load(cls, path):
        """ Load an object from a pickle file.

        Parameters
        -----------
        path : str
            Path to the file to load.

        Returns
        ----------
        compostion : McParameterComposition
        """
        with open(path, 'rb') as my_db:
            composition = cpickle.load(my_db)

        return composition

    @property
    def name(self):
        """ Returns all names of the parameters in the composition
        """
        # names = np.chararray(len(self.paras), itemsize=20)
        # for i in range(len(self.paras)):
        #     names[i] = self.paras[i].name
        return [para.name for para in self.paras]

    @property
    def group(self):
        """ Returns all groups of the parameters in the composition
        """
        groups = []
        for para in self:
            try:
                groups.append(para.group)
            except AttributeError:
                groups.append('')

        return set(groups)

    @property
    def value(self):
        """ Returns all parameter values as a np.ndarray.
        """
        vals = np.empty(len(self))

        for i_para, para in enumerate(self):
            vals[i_para] = para.value

        return vals

    @value.setter
    def value(self, value):
        """ Sets all values for all Parameters. Value is a list, the children are set in the given order.
        """
        if len(value) != len(self):
            raise IOError("The amount of values to set must be the same as the amount of parameters in the composition!")

        for para, val in zip(self.paras, value):
            para.value = val

    def remove(self, parameters):
        r""" Removes the given parameter names from the parameter composition.

        Parameters
        -----------
        parameters : str, iterable(str), McParameter or McParameterComposition

        """
        if isinstance(parameters, (list, tuple)):
            for para in parameters:
                self.remove(para)
            return
        elif isinstance(parameters, McParameterComposition):
            for para in parameters:
                self.remove(para.name)
            return

        if isinstance(parameters, McParameter):
            parameters = parameters.name # extract the name

        try:
            i_para = next(i for i, my_para in enumerate(self.paras) if my_para.name == parameters)
        except StopIteration as err:
            raise KeyError("The parameter {0:s} is not part of this parameter collection and can not be removed!".format(parameters)) from err

        del self.paras[i_para]

    @property
    def min(self):
        """ All minimal values of this group
        """
        vals = np.empty(len(self))
        for i_para, para in enumerate(self.paras):
            vals[i_para] = para.min

        return vals

    @min.setter
    def min(self, min_new):
        """ Sets all minimal values, sets each minimum specifically
        """
        if len(min_new) != len(self):
            raise IOError("The amount of minimum boundaries to set must be the same as the amount of parameters in the composition!")

        for para, min_a in zip(self.paras, min_new):
            para.min = min_a

    @property
    def max(self):
        """ All maximal values of this group
        """
        vals = np.empty(len(self))
        for i_para, para in enumerate(self.paras):
            vals[i_para] = para.max

        return vals

    @max.setter
    def max(self, max_new):
        """ Sets all maximal values, sets each maximum specifically
        """
        if len(max_new) != len(self):
            raise IOError("The amount of minimum boundaries to set must be the same as the amount of parameters in the composition!")

        for para, max_a in zip(self.paras, max_new):
            para.max = max_a

    def print_tex(self):
        """ Prints a modelcard as a tex table using PyLaTeX
        """
        #try to clean first
        try:
            clean_mcard = self.get_clean_modelcard()
        except (AttributeError, KeyError, ValueError): # was a broad except (add more types if needed)
            clean_mcard = self

        doc = Tex()
        # Generate data table
        with doc.create(Section('Modelcard')):
            doc.append('The final modelcard is summarized in the table below:')
            with doc.create(LongTable("| l S s | ", width=3)) as data_table: # pylatex does not count s S columns from siunitx
                data_table.add_hline()
                data_table.add_row(["parameter name", NoEscape("{value}"), NoEscape("{unit}")])
                data_table.add_hline()
                data_table.end_table_header()
                data_table.add_hline()
                data_table.add_row((MultiColumn(3, align='r',
                                    data='continued on next Page'),), strict=False)
                data_table.add_hline()
                data_table.end_table_footer()
                data_table.add_hline()
                data_table.add_row((MultiColumn(3, align='r',
                                    data='Finish'),), strict=False)
                data_table.add_hline()
                data_table.end_table_last_footer()
                # for group in sorted(self.group):
                group = None
                for para in sorted(clean_mcard, key=lambda x: (x.group, x.name)):

                    row = [
                        "{0:<12s}".format(para),
                        NoEscape("{0:g}".format(para)),
                        NoEscape("{0:u}".format(para))
                    ]
                    data_table.add_row(row, strict=False)

                    if group is None:
                        group = para.group

                    if group != para.group:
                        data_table.add_hline() # horizontal line after each group
                        group = para.group

        return doc

    def __iter__(self):
        # return iter(self.paras)
        return iter(copy.deepcopy(self.paras))

    def sort_paras(self):
        """ Sorts the parameters according to the groups.
        """
        self.paras.sort(key=lambda x: (x.group, x.name))

    def iter_alphabetical(self):
        """ Returns an iterator on parameters sorted alphabetically by name
        """
        return iter(sorted(copy.deepcopy(self.paras), key=lambda para: para.name))

    def __len__(self):
        return len(self.paras)

    def __contains__(self, other):
        return other.name in self.name

    def add(self, paras, index=None):
        """ Add a parameter to self. This is only allowed, if the parameter name is not already known to the composition.
        """
        if isinstance(paras, (McParameterComposition)):
            if index is None:
                for para in paras.paras: # deepcopy is in the McParameter add
                    self.add(para)
            else:
                for para in paras.paras[::-1]: # reverse order if index is given -> insert turns the order around again
                    self.add(para, index=index)
            return

        if isinstance(paras, McParameter):
            if paras.name in self.name:
                raise ParaExistsError("Tried to set parameter {:s}, which was already defined.".format(paras))
            else:
                if index is None:
                    self.paras.append(copy.deepcopy(paras))
                else:
                    self.paras.insert(index, copy.deepcopy(paras))
        else:
            raise TypeError('McParameterComposition accepts only McParameter or McParameterComposition!')

    def __add__(self, other):
        """ Allows appending of two compositions by mc1 + mc2
        """
        if isinstance(other, (McParameter, McParameterComposition)):
            mc_return = copy.deepcopy(self)
            mc_return.add(other)

            return mc_return
        else:
            return NotImplemented

    def __radd__(self, other):
        """ Called when parameter + composition is used. Here we need to take care of the index!
        """
        if isinstance(other, (McParameter, McParameterComposition)):
            mc_return = copy.deepcopy(self)
            mc_return.add(other, index=0) # insert at start

            return mc_return
        else:
            return NotImplemented

    def eq_paras(self, other):
        """ Compares the parameters in two McParameterCompositions or subclasses
        """
        str_diff_vars = ""
        for para in self.paras:
            try:
                if para.value != other.get(para.name).value:
                    str_diff_vars += "{0:<12s}: {0:10.4e} || {1:10.4e}\n".format(
                        para,
                        other.get(para)
                    )
            except KeyError:
                str_diff_vars += "The second modelcard does not have a {:s} parameter!\n".format(para)

        # find parameters in other which are not in self!
        for para in other:
            if para.name not in self.name:
                str_diff_vars += "The first modelcard does not have a {:s} parameter!\n".format(para)

        if str_diff_vars:
            logging.info(str_diff_vars)
            return False

        return True

    def __eq__(self, other):
        """ Allows comparing 2 model cards using mc1 == mc2

        """
        if isinstance(other, McParameterComposition):
            # can only compare to other compositions
            return self.eq_paras(other)

        return NotImplemented
