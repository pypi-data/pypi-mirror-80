# Description
This repository provides an interface to access local acceleration limitations for trajectory planning at TUM/FTM. In
addition to location-dependent acceleration limits, vehicle velocity dependent acceleration limits can be accessed when
provided.
The initial acceleration limits are loaded from a csv-file. There is an option to update the local acceleration in
real-time when the tire performance assessment module is running in parallel and communication is enabled.

# List of components
* `MapInterface.py`: Provides an interface to the local trajectory planner and to the tire performance assessment module
* `import_veh_dyn_info.py`: Imports local acceleration limitation from file
