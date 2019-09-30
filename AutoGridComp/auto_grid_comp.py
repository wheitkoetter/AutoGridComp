# -*- coding: utf-8 -*-
"""
/***************************************************************************
 AutoGridComp
                                 A QGIS plugin
 compares grids automatically
                             -------------------
        begin                : 2019-09-24
        copyright            : (C) 2019 by Wilko Heitkoetter/DLR Institute of Networked Energy Systems
        email                : wilko.heitkoetter@dlr.de
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
This program is licensed under the BSD-3-Clause Revised License. Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

    (1) Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer. 

    (2) Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in
    the documentation and/or other materials provided with the
    distribution.  
    
    (3)The name of the author may not be used to
    endorse or promote products derived from this software without
    specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE. 
 ***************************************************************************/
"""
######### import for plugin structure ###################
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from auto_grid_comp_dialog import AutoGridCompDialog
import os.path

######### import for comparison ##############
import qgis
from PyQt4 import QtGui
from qgis.gui import *
from qgis.core import *
import processing
import glob
import os

from qgis.utils import iface
import sys

################################################

class AutoGridComp:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'AutoGridComp_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&AutoGridComp')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'AutoGridComp')
        self.toolbar.setObjectName(u'AutoGridComp')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('AutoGridComp', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = AutoGridCompDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/AutoGridComp/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'AutoGridComp'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&AutoGridComp'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar



    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        
        
        
        # start comparison when push button was clicked
        self.dlg.button_start_comparison.clicked.connect(self.comparison)        
        
        
	result = self.dlg.exec_()
        
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
       
            pass
###############Wilko_ start Comparison###########################
    def comparison(self):

	ui_target_link_l_id_colu=self.dlg.lineEdit_215_l_id.text()
	ui_target_link_length=self.dlg.lineEdit_214_l_length.text() 
	ui_target_link_wire_colu=self.dlg.lineEdit_213_l_wires.text()
	ui_target_link_cable_colu=self.dlg.lineEdit_212_l_cables.text()
	ui_target_link_freq_colu=self.dlg.lineEdit_211_l_frequency.text()
	ui_target_link_volt_colu=self.dlg.lineEdit_210_l_voltage.text()
	ui_target_link_v_id2_colu=self.dlg.lineEdit_209_l_vertex_2.text()
	ui_target_link_v_id1_colu=self.dlg.lineEdit_208_l_vertex_1.text()
	ui_target_link_wkt=self.dlg.lineEdit_207_l_geo.text()
	ui_links_target_file=self.dlg.lineEdit_206_l_file.text()
	ui_target_vert_freq_colu=self.dlg.lineEdit_205_v_frequency.text()
	ui_target_vert_volt_colu=self.dlg.lineEdit_204_v_voltage.text()
	ui_dist_target_field=self.dlg.lineEdit_203_v_vertex.text()	
	ui_target_vertices_geom=self.dlg.lineEdit_202_v_geo.text()
	ui_dist_target_file=self.dlg.lineEdit_201_v_file.text()
	ui_target_network_name=ui_path=self.dlg.lineEdit_200_v_name.text()

	ui_input_link_l_id_colu=self.dlg.lineEdit_115_l_id.text()
	ui_input_link_length=self.dlg.lineEdit_114_l_length.text()  
	ui_input_link_wire_colu=self.dlg.lineEdit_113_l_wires.text()
	ui_input_link_cable_colu=self.dlg.lineEdit_112_l_cables.text()
	ui_input_link_freq_colu=self.dlg.lineEdit_111_l_frequency.text()
	ui_input_link_volt_colu=self.dlg.lineEdit_110_l_voltage.text()
	ui_input_link_v_id2_colu=self.dlg.lineEdit_109_l_vertex_2.text()
	ui_input_link_v_id1_colu=self.dlg.lineEdit_108_l_vertex_1.text()
	ui_input_link_wkt=self.dlg.lineEdit_107_l_geo.text()
	ui_links_input_file=self.dlg.lineEdit_106_l_file.text()
	ui_input_vert_freq_colu=self.dlg.lineEdit_105_v_frequency.text()
	ui_input_vert_volt_colu=self.dlg.lineEdit_104_v_voltage.text()
	ui_dist_input_field=self.dlg.lineEdit_103_v_vertex.text()	
	ui_input_vertices_geom=self.dlg.lineEdit_102_v_geo.text()
	ui_dist_input_file=self.dlg.lineEdit_101_v_file.text()
	ui_input_network_name=self.dlg.lineEdit_100_v_name.text()

    	ui_path=self.dlg.lineEdit_000_path.text()

	ui_check_electrical=self.dlg.checkBox_5_electrical.isChecked()
	ui_check_mathematical=self.dlg.checkBox_4_mathematical.isChecked()
	ui_check_visual=self.dlg.checkBox_3_visual.isChecked()
	ui_check_two_grids=self.dlg.checkBox_2_two_grids.isChecked()
	ui_check_onl_charac_sing=self.dlg.checkBox_1_only_charac_single.isChecked()                

# pass variables to agc.py

#	 sys.argv = ['/home/wilkohe/.qgis2/python/plugins/AutoGridComp/agc.py',ui_path,ui_check_onl_charac_sing,ui_check_two_grids,ui_check_visual,ui_check_mathematical,ui_check_electrical]

#        sys.argv = ['/home/wilkohe/.qgis2/python/plugins/AutoGridComp/agc.py',ui_path,ui_input_network_name,ui_dist_input_file,ui_input_vertices_geom,ui_dist_input_field,ui_input_vert_volt_colu,ui_input_vert_freq_colu]
#        sys.argv = ['/home/wilkohe/.qgis2/python/plugins/AutoGridComp/agc.py',ui_target_network_name,ui_dist_target_file,ui_target_vertices_geom,ui_dist_target_field,ui_target_vert_volt_colu,ui_target_vert_freq_colu]
#        execfile('/home/wilkohe/.qgis2/python/plugins/AutoGridComp/agc.py')

	agc_call=''+ui_path+'/agc.py'
#	sys.argv = [agc_call,ui_path,ui_check_onl_charac_sing,ui_check_two_grids,ui_check_visual,ui_check_mathematical,ui_check_electrical]  # not necessary to pass the variables actively
#       sys.argv = [agc_call,ui_path,ui_input_network_name,ui_dist_input_file,ui_input_vertices_geom,ui_dist_input_field,ui_input_vert_volt_colu,ui_input_vert_freq_colu]
#       sys.argv = [agc_call,ui_target_network_name,ui_dist_target_file,ui_target_vertices_geom,ui_dist_target_field,ui_target_vert_volt_colu,ui_target_vert_freq_colu]

        execfile(agc_call)

        
##############end comparison#############################################
