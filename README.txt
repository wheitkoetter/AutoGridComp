*** AutoGridComp ***
The QGIS plugin AutoGridComp is written in python and automatically compares power grid models, taking into account mathematical, visual and electrical criteria. The tool can also be applied to grid models other than those of power grids. Licensed under the BSD-3-Clause Revised License.


*** INSTALLATION ***
The folder "AutoGridComp" contains the files to build the QGIS plugin. It needs to be copied to "your_path_to_.qgis2_folder/.qgis2/python/plugins". Then AutoGridComp can be installed in the QGIS GUI under "plugins->manage and install plugins".

The "AutoGridComp_working_folder" can be located at any place on your system. Input data have to be copied to this directory and resulting files are created here.


*** FILES ***

- for a flowchart of the files, the plugin is implemented in, see: "flowchart_files_AutoGridComp.png"

FOLDER "AutoGridComp": 

- the following files have been created by QGIS Plugin builder: 
-- ui_autogrid_comp_dialog_base.ui
-- ui_autogrid_comp_dialog_base.py
-- autogrid_comp_dialog.py
-- autogrid_comp.py

The file "autogrid_comp.py" contains the call of the file "agc.py", which is located in the "AutoGridComp_working_folder". When clicking the OK Button in the AutoGridComp GUI, agc.py is automatically started.


FOLDER "AutoGridComp_working_folder":

The file "agc.py" contains the main implementation of the plugin. For better changeability and debugging, agc.py can also be run from the python console within QGIS. In this case just the input data need to be manually inserted in the input section at the top of the agc.py file, that are usually being entered in the GUI.
The file agc.py contains the call of "mathematical_characterisation.py", which contains the calculation of network criteria and the respective resulting data output. It can be run from any python interpreter (no QGIS necessary), but also in this case the input data need to be manually inserted in the input section.


*** LICENSE ***
Code licensed under the BSD-3-Clause Revised License. The copyright owner is the DLR Insitute of Networked Energy Systems.

Author: Wilko Heitkoetter
