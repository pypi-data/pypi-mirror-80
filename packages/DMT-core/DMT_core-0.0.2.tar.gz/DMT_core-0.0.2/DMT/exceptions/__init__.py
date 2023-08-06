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
name = "exceptions"

class Stopped(Exception):
    """Raised if the bounds are attempted to be changed such that self.low > self.up or such that the current value is not inside the new bounds. """

class Canceled(Exception):
    """Raised if the bounds are attempted to be changed such that self.low > self.up or such that the current value is not inside the new bounds. """

class ValueAtBoundsError(ValueError):
    """ Raised when the input error is excluded. """

class SimulationUnsuccessful(Exception):
    """ Raised if the output of a simulation is not valid. """

class ValueTooLargeError(ValueError):
    """ Raised when the input value is too large. """

class ValueTooSmallError(ValueError):
    """ Raised when the input value is too small. """

class ValueExcludedError(ValueError):
    """ Raised when the input error is excluded. """

class ParaExistsError(LookupError):
    """ Raised when a parameter is added to a composition in which a parameter with the same name already exists."""

class BoundsError(ValueError):
    """ Raised if the bounds are attempted to be changed such that self.low > self.up or such that the current value is not inside the new bounds. """

class DataReferenceEmpty(Exception):
    """ The xstep supplied init_data_reference_method did not generate reference data. """

class UnknownColumnError(Exception):
    """ Raise if unknown columns in measurement data. """

class UnknownNodesError(Exception):
    """ Raised if an known node is encountered during clean_names(). """

class NoOpenDeembeddingDut(Exception):
    """ A suitable Open Deembedding Dut has not been found by DutLib.sort_duts. """

class NoShortDeembeddingDut(Exception):
    """ A suitable Short Deembedding Dut has not been found by DutLib.sort_duts. """

class DeviceContactConfigError(Exception):
    """ Raised by EvalTradica, if the given contact configuration (f.e. CBEBC) is unknown. """

class SpecifierNotKnown(IOError):
    """ This specifier is unknown to DMT. """

class NanInfError(IOError):
    """ Nan or Inf Error during calculation. """
