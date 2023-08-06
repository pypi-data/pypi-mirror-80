# DMT Core Package

DeviceModelingToolkit (DMT) is a python tool targeted at helping modeling engineers extract model parameters, run circuit and TCAD simulations and automate their infrastructure. This open-source package contains only the
sub-package "core" from DMT, which allows to:

 - import measurement data into pandas DataFrames using data_reader
 - provide plotting capabilities for electrical quantities
 - define interfaces for TCAD and circuit simulators
 - and much more...

The project ist still in ints infancy, though many things already work. Here is an incomplete list of already working stuff of the full DMT version:

- HiCUML2 scalable model parameter extraction
- HiCUML0 model parameter extraction
- NGSpice and ADS circuit simulator interface
- DEVICE and COOS TCAD simulator interface
- Data management with pandas
- Typical electrical engineering relevant equations such as S-to-Z parameter conversions and so on are mostly implemented
- Many examples
- Many test cases
- Support VerilogAE
