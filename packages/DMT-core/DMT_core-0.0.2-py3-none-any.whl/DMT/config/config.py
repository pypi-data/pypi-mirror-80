""" DMT config management

Collects the config from 3 different locations:

* Local script directory. (DMT_config.yaml)
* User's home directory (~/.DMT/DMT_config.yaml)
* DMT package installation directory (DMT_config.yaml)

They are all read and finally taken in the order given here. This means that anything given in the local directory overwrites all others.

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
from pkg_resources import Requirement, resource_filename
from pathlib import Path
import os.path
import yaml

path_config = os.path.dirname(os.path.abspath(__file__))
default_config_file = os.path.join(path_config, "DMT_default_config.yaml")
with open(default_config_file) as yaml_data_file:
    DATA_CONFIG = yaml.safe_load(yaml_data_file)

try:
    user_config = Path.home() / '.DMT' / 'DMT_config.yaml'
    # with open(os.path.expanduser(os.path.join('~', '.DMT', 'DMT_config.yaml'))) as yaml_data_file:
    with user_config.open() as yaml_data_file:
        data_user = yaml.safe_load(yaml_data_file)

    for key, value in DATA_CONFIG.items():
        if key in data_user.keys():
            if hasattr(DATA_CONFIG[key],'update'):
                DATA_CONFIG[key].update(data_user[key])
            else:
                if isinstance(DATA_CONFIG[key], list): # lists are appended.
                    DATA_CONFIG[key] = DATA_CONFIG[key] + data_user[key]
                else:
                    DATA_CONFIG[key] = data_user[key]
except FileNotFoundError:
    pass

try:
    local_config = Path('DMT_config.yaml')
    with local_config.open() as yaml_data_file:
        data_folder = yaml.safe_load(yaml_data_file)

    for key, value in DATA_CONFIG.items():
        if key in data_folder.keys():
            try:
                DATA_CONFIG[key].update(data_folder[key])
            except AttributeError:
                if isinstance(DATA_CONFIG[key], list): # lists are appended.
                    DATA_CONFIG[key] = DATA_CONFIG[key] + data_folder[key]
                else:
                    DATA_CONFIG[key] = data_folder[key]
except FileNotFoundError:
    pass

USER_NAME  = DATA_CONFIG['user_name']
USER_EMAIL = DATA_CONFIG['user_email']
""" Name of the DMT user for documentation. """

DIRECTORIES = DATA_CONFIG["directories"]
for key, str_path in DIRECTORIES.items():
    try:
        DIRECTORIES[key] = Path(str_path).expanduser()
    except TypeError:
        pass

DATA_CONFIG["directories"] = DIRECTORIES


DB_DIR = DIRECTORIES['database']


#measurement data overview report template
#https://stackoverflow.com/questions/14050281/how-to-check-if-a-python-module-exists-without-importing-it
if DATA_CONFIG["directories"]["libautodoc"] is not None:
    try:
        DATA_CONFIG["directories"]["libautodoc"] = os.path.expanduser(DATA_CONFIG["directories"]["libautodoc"])
    except TypeError:
        pass

# not needed anymore. It is directly obtained from DATA_CONFIG.
# This allows to add configs without changing anything here. Do it always like this in future!
COMMANDS = DATA_CONFIG["commands"]

COMMAND_TEX = (DATA_CONFIG["commands"]["TEX"], DATA_CONFIG["commands"]["TEXARGS"])
""" TEX build command """

# COMMAND_TRADICA = DATA_CONFIG["commands"]["TRADICA"]
# """ TRADICA command """

# COMMAND_COOS = DATA_CONFIG["commands"]["COOS"]
# """ COOS command """

# COMMAND_DEVICE = DATA_CONFIG["commands"]["DEVICE"]
# """ DEVICE command """

# COMMAND_ADS = DATA_CONFIG["commands"]["ADS"]
# """ ADS simulator command """

# COMMAND_SIMU = DATA_CONFIG["commands"]["SIMU"]
# """ SIMU simulator command """

# COMMAND_NGSPICE = DATA_CONFIG["commands"]["NGSPICE"]
# """ SIMU simulator command """

USE_HDF5STORE = DATA_CONFIG["useHDF5Store"]
""" Saves data as HDF5 Databases, if False, pickle is used. """

# DO NOT ADD ANYTHING HERE. JUST DIRECTLY IMPORT DATA_CONFIG INSIDE YOUR MODULE
# If wanted add documentation here and/or in DMT_config.yaml
