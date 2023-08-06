""" Base class to handle verilog-a modelcards.

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
import os
import re
import warnings
import hashlib
import pickle
import logging
import scipy.io as sciio
import ast
import operator
from DMT.core import unit_registry
from DMT.core.mc_parameter import McParameterComposition, McParameter


class MCard(McParameterComposition):
    """ DMT class that implements attributes and methods that are common between all ModelCards such as HICUM and BSIM.

    Parameters
    -----------
    nodes_list        :  tuple(str)
        Port list for this model.
    default_subckt_name  :  str
        Default name for the subcircuit to be included.
    default_module_name  :  str
        Default name of the module of the VA-File for this device.
    version              :  float
        Version of the model.
    va_file : str, optional
        Path to a Verilog-AMS file
    list_opvars : list
        Names of all the operation point variables aviable from the analyzed VA-Code.
    circuit : {None,:class:`~DMT.core.circuit.Circuit`}
        Circuit to simulate this model card.
    mod_name : str
        Name of the Model, this is used by EvalTradica, so it must fit there, e.g. 'HICUM'
    level_num : str
        Level of the Model, this is used by EvalTradica, so it must fit there, e.g. '2'

    Attributes
    -----------
    nodes_list : tuple(str)
        Port list for this model.
    circuit : {None,:class:`~DMT.core.circuit.Circuit`}
        Circuit to simulate this model card.
    default_subckt_name : str
        Default name for the subcircuit to be included.
    default_module_name : str
        Default name of the module of the VA-File for this device.
    version : float
        Version of the model.
    va_file : str
        Path to a Verilog-AMS file
    list_opvars : list
        Names of all the operation point variables aviable from the analyzed VA-Code.
    mod_name : str
        Name of the Model, this is used by EvalTradica, so it must fit there, e.g. 'HICUM'
    level_num : str
        Level of the Model, this is used by EvalTradica, so it must fit there, e.g. '2'
    """
    def __init__(self, nodes_list, default_subckt_name, default_module_name, version, va_file=None,
    possible_groups=None, mod_name='', level_num='', list_op_vars=None, __MCard__=1.0, **kwargs):
        super().__init__(**kwargs)
        self.__MCard__ = __MCard__

        self.nodes_list           =  nodes_list
        self.default_subckt_name  =  default_subckt_name
        self.default_module_name  =  default_module_name
        self.version              =  version
        self._va_file             =  None

        if list_op_vars is None:
            self.list_opvars = []
        else:
            self.list_opvars = list_op_vars
        self.mod_name  = mod_name # for TRADICA
        self.level_num = level_num # for TRADICA

        if possible_groups is None:
            self.possible_groups  = {}
        else:
            self.possible_groups  = possible_groups

        if va_file is not None:
            self.va_file          =  va_file

    def info_json(self):
        """ Returns a dict with serializeable content for the json file to create. Add the info about the concrete subclass to create here!
        """
        info_dict = super().info_json()

        if hasattr(self, '__MCard__'):
            info_dict['__MCard__'] = self.__MCard__ # make versions, so we can introduce compatibility here!
        else:
            info_dict['__MCard__'] = 1.0 # make versions, so we can introduce compatibility here!

        info_dict['nodes_list']           = self.nodes_list
        info_dict['default_subckt_name']  = self.default_subckt_name
        info_dict['default_module_name']  = self.default_module_name
        info_dict['version']              = self.version
        info_dict['list_opvars']          = self.list_opvars
        info_dict['mod_name']             = self.mod_name
        info_dict['level_num']            = self.level_num
        info_dict['possible_groups']      = self.possible_groups
        info_dict['va_file']              = self._va_file
        return info_dict

    @classmethod
    def loads_json(cls, dict_parameter):
        """ Creates a McCard from a dictionary obtained by a json.load.
        """
        if '__MCard__' in dict_parameter:
            MCard(**dict_parameter)
        else:
            raise IOError('DMT->MCard: The given dict has no __MCard__ key!')

    @property
    def va_file(self):
        """ Just return the verilog file
        """
        return self._va_file

    @va_file.setter
    def va_file(self, new_va_file):
        """ make sure all the parameters are read (setting to self._va_file is done twice, I now...).
        """
        self.read_va_file_boundaries_opvars(new_va_file)
        self._va_file = new_va_file

    def get_circuit(self):
        """ Here the modelcard defines it's default simulation circuit.
        """
        raise NotImplementedError('The default modelcard has no circuit :(.')

    def print_to_file(self, path_to_file, file_mode='w', subckt_name=None, module_name=None, line_break='\n'):
        """ Generates a .lib file which can be included into an ADS netlist.

        Existence of lib file is not checked before writing!
        Name of File: path_to_file + ".lib"

        Parameters
        -----------
        path_to_file : str
            Absolute or relative path with file name to the file to generate.
        file_mode : str, optional
            Mode to open the file. Can be used to append :).
        subckt_name : str
            Name of the subcircuit to be included
        module_name : str
            Name of the module from the corresponding VA-File
        line_break : str, optional
            Is added after each parameter, is used as line breaks.
        """
        if subckt_name is None:
            subckt_name = self.default_subckt_name
        if module_name is None:
            module_name = self.default_module_name

        with open(path_to_file + ".lib", file_mode) as my_file:
            my_file.write("simulator lang = spectre\n")

            my_file.write("subckt " + subckt_name + " (" + ' '.join(self.nodes_list) + ")\n")
            my_file.write(" Q1 (" + ' '.join(self.nodes_list) + ") " + module_name + " (\\\n")

            for para in self:
                my_file.write(
                    "  {0:<12s} = {0:10.3e} {1}".format(
                        para, line_break
                    )
                )

            my_file.write(")\n")
            my_file.write("ends " + subckt_name + "\n")

    def get_parameter_string(self):
        """ Returns all parameters combined as a string.

        The string starts with
        "version: x.xxx " (15 Characters)

        Use: hashing or without version as library
        """
        temp_str = "version: {:.3f}".format(self.version)
        return temp_str + self.print_parameters()

    def read_va_file_boundaries_opvars(self, va_file):
        """ Reads the parameter boundaries and possible OPvars from a Verilog-AMS-File

        Needs only to be done once per VA-File, as the boundaries then can
        be saved/loaded from a mcp (see save_model)

        Parameters
        -----------
        va-file : str
            Absolute or relative Path to the VA-File including Filename and Ending

        """
        logging.info("Reading parameter boundaries and operation point variables from %s", va_file)
        self.list_opvars = []
        self._va_file = va_file

        with open(va_file, "r") as my_file:
            lines = my_file.readlines()

        unit_converter = {
            's'     : unit_registry.second,
            'A'     : unit_registry.ampere,
            'A^2s'  : unit_registry.ampere*unit_registry.ampere*unit_registry.second,
            'V'     : unit_registry.volt,
            '1/V'   : 1/unit_registry.volt,
            'K'     : unit_registry.kelvin,
            '1/K'   : 1/unit_registry.kelvin,
            'C'     : unit_registry.celsius,
            'Ohm'   : unit_registry.ohm,
            'F'     : unit_registry.farad,
            'Coul'  : unit_registry.coulomb,
            'K/W'   : unit_registry.kelvin/unit_registry.watt,
            'J/W'   : unit_registry.joule/unit_registry.watt,
            'V/K'   : unit_registry.volt/unit_registry.kelvin,
            '1/K^2' : 1/unit_registry.kelvin/unit_registry.kelvin,
            'Ws/K'  : unit_registry.watt*unit_registry.second/unit_registry.kelvin,
            'M^(1-AF)' : unit_registry.dimensionless,
        }

        group = None
        for line in lines:
            if re.match(r"\s*module", line):
                # module hic0_full (c,b,e,s,tnode);
                # module hicumL2va (c,b,e,s,tnode);
                mo_module_name = re.search(r"module\s(\S+?)\s*\((.+?)\)", line)
                self.default_module_name = mo_module_name.group(1)
                self.nodes_list = mo_module_name.group(2).split(',')
            elif line.startswith(r"//"):
                # only commented lines
                comment = line.replace('//', '').strip()
                try:
                    group = self.possible_groups[comment]
                    dummy = 1
                except KeyError:
                    group = None

            elif re.match(r"\s*parameter", line):
                # found a parameter line
                mo_parameter  =  re.search(
                    r"parameter\s+(real|integer)\s+(\w+)\s*=\s*(\S+)", line
                )
                if mo_parameter:
                    parameter_type     =  mo_parameter.group(1)
                    parameter_name     =  mo_parameter.group(2)
                    parameter_default  =  mo_parameter.group(3)
                else:
                    logging.error("DMT -> MCard -> read_va_file_boundaries(): Something went wrong at evaluation of each line, current line:\n%s", line)

                parameter_default = parameter_default.replace(';', '')
                if parameter_type == "integer":
                    parameter_type      = np.int
                    parameter_default   = np.int(parameter_default)
                elif parameter_type == "real":
                    parameter_type      = np.float
                    if parameter_default == '`INF':
                        parameter_default   = np.inf
                    else:
                        parameter_default   = np.float(parameter_default)

                tuple_parameter_boundaries  =  re.findall(r"from\s+(\S+)", line)
                if tuple_parameter_boundaries:
                    parameter_boundaries = tuple_parameter_boundaries[0].split(":")
                    # at the moment only 1st group is used, if VA-Code with
                    # parameter real a = 1 from 0:10 from 20:30
                    # is analyzed this needs to be extended!

                    if "(" in parameter_boundaries[0]:
                        parameter_include_min = False
                    else:  # else should be "[", not checked now
                        parameter_include_min = True

                    if ")" in parameter_boundaries[1]:
                        parameter_include_max = False
                    else:  # else should be "]", not checked now
                        parameter_include_max = True

                    if parameter_type == np.int:
                        parameter_min = np.int(re.search(r"([-.0-9e]+)", parameter_boundaries[0]).group(1))
                        parameter_max = np.int(re.search(r"([-.0-9e]+)", parameter_boundaries[1]).group(1))
                    elif parameter_type == np.float:
                        try:
                            parameter_min = np.float(re.search(r"([-.0-9e]+)", parameter_boundaries[0]).group(1))
                        except (AttributeError, ValueError):
                            if 'INF' in parameter_boundaries[0].upper():
                                parameter_min = -np.inf
                            else:
                                raise
                        try:
                            parameter_max = np.float(re.search(r"([-.0-9e]+)", parameter_boundaries[1]).group(1))
                        except (AttributeError, ValueError):
                            if 'INF' in parameter_boundaries[1].upper():
                                parameter_max = np.inf
                            else:
                                raise
                        # if more are added also add them to the validity checker!!
                    else:  # is impossible, only possibilities are real or integer (see 1st RegExp)
                        raise NotImplementedError(
                            "This parameter type is not implemented: " + parameter_type
                        )
                else:
                    if parameter_type == np.float:
                        parameter_min      =  -np.inf
                        parameter_max      =  np.inf
                    elif parameter_type == np.int: # inf not possible in integer...
                        parameter_min      =  np.iinfo(np.int).min
                        parameter_max      =  np.iinfo(np.int).max
                    parameter_include_min  =  True
                    parameter_include_max  =  True

                tuple_parameter_excludes  =  re.findall(r"exclude\s+(\S+)", line)
                if tuple_parameter_excludes:
                    parameter_excludes  =  tuple_parameter_excludes[0]
                else:
                    parameter_excludes  =  None
                # at the moment only 1st group is used, if VA-Code with
                # parameter integer a = 1 from -1:2 exclude 0 exclude 1
                # parameter integer a = 1 from -1:2 exclude 0:1
                # is analyzed this needs to be extended!

                search_unit = re.search(r'unit\s*=\s*\"(.+?)\"', line)
                if search_unit:
                    # convert from VA to pint...
                    unit = unit_converter[search_unit.group(1)]
                else:
                    unit = unit_registry.dimensionless

                search_desc = re.search(r'(desc|info)\s*=\s*\"(.+?)\"', line) # 'desc' is VA standard, 'info' is ADMS standard
                if search_desc:
                    desc = search_desc.group(2)
                else:
                    desc = None

                try:
                    para          = self.get(parameter_name)
                except KeyError:
                    para          = McParameter(parameter_name, value=parameter_default, value_type=parameter_type)

                para.val_type =  parameter_type
                para.max      =  parameter_max
                para.min      =  parameter_min
                para.inc_max  =  parameter_include_max
                para.inc_min  =  parameter_include_min
                para.exclude  =  None
                if group is None:
                    warnings.warn('The group of the parameter {:s} is unknown from the VA-File'.format(para))
                else:
                    para.group    =  group

                if desc is not None:
                    para.description = desc

                if unit is not None:
                    para.unit = unit
                if parameter_excludes is not None:  # just assume it is the type parameter...
                    para.exclude  =  int(parameter_excludes)

                if para in self:
                    self.set(para)
                else:
                    self.add(para)

            elif re.match(r"\s*\(\*\s*desc\s*=", line):
                # regex to extract all parts of the opvars definition
                # https://regex101.com/r/1h7EzI/2
                mo_opvar  =  re.search(
                    r'desc=\"(.*?)\"(,\s*units=\"(.*?)\"|).+?\*\)\s+(\w+)\s+(\w+)',
                    line
                ) # https://regex101.com/r/Rm8Hjt/1
                # search for string, analyse the groups:
                # if
                desc     =  mo_opvar.group(1)
                unit     =  mo_opvar.group(3)
                dtyp     =  mo_opvar.group(4)
                varname  =  mo_opvar.group(5)

                self.list_opvars.append(varname)
                setattr(
                    self,
                    "opvar_" + varname,
                    {
                        "desc": desc,
                        "unit": unit,
                        "data_type" : dtyp,
                    }
                )

    def __eq__(self, other):
        """ Allows comparing 2 model cards using mc1 == mc2

        mc1 != mc2 is included per default using python3:
        https://docs.python.org/3/reference/datamodel.html#object.__ne__

        """
        if isinstance(other, self.__class__):
            if self.version == other.version:
                # class, version and parameters equal is enough in most cases!
                return self.eq_paras(other)
            else:
                return False

        return NotImplemented

    def save_model(self, path_to_file, hashing=True, file_type="pickle"):
        """ Saves the model to a file

        Easiest way is to save as pickle, since then also the limits are saved!

        Parameters
        -----------
        path_to_file : str
            A relative or absolute path to the save folder
        hashing : {True, False}
            If False, path_to_file should include the filename
        file_type : str, {"pickle","mat"}
            Save type pickle is python internal, mat-file is already known
            File ending for pickle: ".mcp" ModelCard Pickled

        Returns
        --------
        filename : str
        """
        if hashing:
            hasher = hashlib.md5()
            ba_parameters = str.encode(self.get_parameter_string())
            hasher.update(ba_parameters)
            filename = hasher.digest().decode("utf-8")
            path_to_folder = path_to_file
        else:
            (path_to_folder, filename) = os.path.split(path_to_file)

        if file_type == "pickle":
            # no try to provoke the errors!
            with open(os.path.join(path_to_folder, filename + ".mcp"), "wb") as myfile:
                pickle.dump(self, myfile, 4)
                # 4 is the protocol version,
                # used hard numbering here to stay compatible as it is aviable from python 3.4 on

        elif file_type == "mat":
            raise NotImplementedError(
                "Save as Matfile is not implemented at the moment!"
            )
        else:
            raise IOError("File type to save not known!\nGiven was: " + file_type)

        logging.info("Saved model parameters to a %s model card named: %s", file_type, filename)
        return filename

    def load_model(self, path_to_file, force=True):
        """ Loads the model from a file

        The loading method is determined according to the file ending (last 3 characters!!)
        Possible is "mcp" (see save_model), "txt" or "mat" (planned)

        Parameters
        -----------
        path_to_file : str
            Filename (with ending!) including a relative or absolute path
        force : boolean, optional
            If True, values are force set. Set false if bounds from VA-File are used...
        """
        modcard = None

        # Loading protocol depends on file ending
        (_path_to_folder, filename) = os.path.split(path_to_file)
        file_ending = filename[-3:]
        if file_ending == "mcp" or filename.endswith('mcard'):
            logging.info("Loading model parameters from pickled model card: %s", filename)

            with open(path_to_file, "rb") as myfile:
                modcard = pickle.load(myfile)

        elif file_ending == "mat":
            logging.info("Loading model parameters from mat-File: %s", filename)

            modcard = sciio.loadmat(path_to_file)
            for key, value in modcard.items():
                if not key.startswith("__"):
                    modcard[key] = np.ndarray.item(value)

        elif file_ending == "txt":
            logging.info("Loading model parameters from a txt-File: %s", filename)

            modcard = []

            with open(path_to_file, "r") as myfile:
                # read the file line by line
                str_modelcard = myfile.readline()
                str_temp = myfile.readline()
                while str_temp:
                    str_modelcard = str_modelcard + str_temp
                    str_temp = myfile.readline()

            # split it
            re_object = re.findall(r"[a-zA-Z0-9]+\s*=\s*\S+", str_modelcard)

            for param_value in re_object:
                param_value = param_value.split("=")
                modcard.append(
                    (param_value.strip(), float(param_value[1].strip()))
                )
        elif file_ending == "lib":
            logging.info("Loading model parameters from a TRADICA lib-File: %s", filename)

            modcard = []

            with open(path_to_file, "r") as myfile:
                # read the file line by line
                str_lib = myfile.read()

            # replace variables ?

            # get the model part
            try:
                str_lib = re.search(r"(model|subckt)(.*)(ends|)", str_lib, flags=re.DOTALL|re.IGNORECASE).group(2)
            except AttributeError:
                pass

            # split it
            # re_object = re.findall(r"([a-zA-Z0-9]+\s*=\s*[a-zA-Z0-9.+()-]+\s*)", str_lib) # new and better: https://regex101.com/r/Bwvc69/1
            # re_object = re.findall(r"([a-zA-Z0-9]+)\s*=\s*[\(|]\s*(\S+)\s*[\|]", str_lib) # even newer and better https://regex101.com/r/DsZP2J/1
            re_object = re.findall(r"([a-zA-Z0-9]+)\s*=\s*((\(|)\s*\S+\s*(\)|))", str_lib) # even newer and better https://regex101.com/r/DsZP2J/2

            for param_name, param_value, _bracket_start, _bracket_close in re_object:
                name  = param_name.strip().lower()
                if name=='level' or name=='version' or name=='lang':
                    continue
                value = param_value.strip()
                if ')' in value and '(' not in value: # cuts out an probable single closing bracket.
                    value = value.replace(')', '').strip()
                if '***' in value: # appears sometimes in TRADICA files
                    continue

                value = Calculator.evaluate(value) # allow calculations in parameter value
                if value is None:
                    raise IOError("Error while reading lib-file! Could not evaluate the parameter value '" + param_value[1].strip() + "' of the parameter " + name + "!")
                modcard.append((name, value))
        else:
            raise IOError(
                "Was not able to load parameters from given file!\nGiven was: "
                + path_to_file
            )

        if modcard is None:
            raise IOError("Loading from file did not work!")

        if isinstance(modcard, list):
            for (parameter_name, parameter_value) in modcard:
                try:
                    # do not reset the limits if parameter is already in modelcard
                    self.set_values({parameter_name: parameter_value}, force=force)
                except KeyError:
                    self.add(McParameter(parameter_name, value=parameter_value))
                except ValueError:
                    # if force==False and parameter value is out of bounds -> do not set the value...
                    logging.info('DMT->MCard: The parameter %s was not loaded from %s since the value %f was out of bounds.', parameter_name, path_to_file, parameter_value)

        elif isinstance(modcard, McParameterComposition):
            for para in modcard:
                if not hasattr(para, 'group'):
                    para.group = None

                try:
                    self.set(para)
                except KeyError:
                    self.add(para)
        elif isinstance(modcard, dict):
            for (parameter_name, parameter_value) in modcard.items():
                if not parameter_name.startswith("__"):
                    try:
                    # do not reset the limits if parameter is already in modelcard
                        self.set_values({parameter_name: parameter_value}, force=force)
                    except KeyError:
                        self.add(McParameter(parameter_name, value=parameter_value))
        else:
            raise OSError("Loading from file worked, but I do not know how to handle the loaded content of type " + str(type(modcard)) + "!")


class Calculator(ast.NodeVisitor):
    """ Small "safe" calculator to allow calculations of model parameters.

    Avoiding the unsafe "eval"...

    Source:
    https://stackoverflow.com/a/33030616

    """
    _UnaryOP_MAP = {
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
        ast.Invert: operator.neg,
    }
    """ Implemented unary operators of the calculator (1 Number operations). """
    _BinaryOP_MAP = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
    }
    """ Implemented binary operators of the calculator (2 Number operations). """

    def visit_UnaryOp(self, node):
        operand = self.visit(node.operand)
        return self._UnaryOP_MAP[type(node.op)](operand)


    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return self._BinaryOP_MAP[type(node.op)](left, right)

    def visit_Num(self, node):
        return node.n

    def visit_Expr(self, node):
        return self.visit(node.value)

    @classmethod
    def evaluate(cls, expression):
        tree = ast.parse(expression)
        calc = cls()
        return calc.visit(tree.body[0])