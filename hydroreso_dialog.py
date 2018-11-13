# -*- coding: utf-8 -*-
#*******************************************************************************
# This plugin is released under the 3-Clause BSD License
#
# see license-3-Clause-BSD.txt
#
# see <a href="https://opensource.org/licenses/BSD-3-Clause">https://opensource.org/licenses/BSD-3-Clause</a>
#
# @author Michaël Gaudin, Alice Gonnaud, Guillaume Vasseur
#
# @copyright 2018 - Michaël Gaudin, Alice Gonnaud, Guillaume Vasseur, ENSG
#*****************************************************************************/

import os

from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from qgis.core import QgsProject, QgsMapLayer
from qgis.utils import reloadPlugin

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'hydroreso_dialog_base.ui'))
        
class HydroresoDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(HydroresoDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        
        # Initial page
        self.stackedWidget.setCurrentIndex(0)
        
        # Set up the combo box with the layers
        self.setUpComboBoxLayer()
        self.getFieldsFromSelectedLayer()
        
        # Update buttons
        self.update_prev_next_buttons()
        self.stackedWidget.currentChanged.connect(self.update_prev_next_buttons)
        
        # Handle actions on button click
        self.buttonNext.clicked.connect(self.__next__)
        self.buttonPrevious.clicked.connect(self.prev)
        
        # Update fields of the selected layer
        self.comboBox_layers.currentIndexChanged[int].connect(self.getFieldsFromSelectedLayer)
        
        # Browse to save output layer field
        self.output_layer.clear()
        self.btnBrowse_1.clicked.connect(self.select_output_file)
    
    def update_prev_next_buttons(self):
        """
        Disable click on previous button on the first page and on next button
        on the last page
        """
        i = self.stackedWidget.currentIndex()
        self.buttonPrevious.setEnabled(i > 0)
        self.buttonNext.setEnabled(i < 3)
    
    def __next__(self):
        """
        Change page to next page
        """
        i = self.stackedWidget.currentIndex()
        self.stackedWidget.setCurrentIndex(i + 1)
    
    def prev(self):
        """
        Change page to previous page
        """
        i = self.stackedWidget.currentIndex()
        self.stackedWidget.setCurrentIndex(i - 1)
    
    def setUpComboBoxLayer(self):
        """
        """
        # Add layers to the combobox
        layers = QgsProject.instance().mapLayers().values()
        for layer in layers:
            if layer.type() == QgsMapLayer.VectorLayer:
                self.comboBox_layers.addItem( layer.name(), layer )

    def getFieldsFromSelectedLayer(self):
        """
        """
        current_layer_string = str(self.comboBox_layers.currentText())
        if not current_layer_string == '':
            current_layer = QgsProject.instance().mapLayersByName(current_layer_string)[0]

            # Lists Initialisation
            qcombobox_1_list = [""]
            qcombobox_2_list = [""]
            qcombobox_3_list = [""]
            
            # Filling the lists that will be displayed in the ComboBoxes
            for feature in current_layer.fields():
                qcombobox_1_list.append(feature.name())
                qcombobox_2_list.append(feature.name())
                qcombobox_3_list.append(feature.name())
            
            # Initialisation of ComboBoxes
            self.qcombobox_1.clear()
            self.qcombobox_2.clear()
            self.qcombobox_3.clear()
            
            # Filling of ComboBoxes
            self.qcombobox_1.addItems(qcombobox_1_list)
            self.qcombobox_2.addItems(qcombobox_2_list) 
            self.qcombobox_3.addItems(qcombobox_3_list)
        
    def select_output_file(self):
        """
        Handler for selecting the output file
        """
        filename = QFileDialog.getSaveFileName(self, "Select output file ", "", "Esri Shapefile (*.shp)")
        self.output_layer.setText(str(filename[0]))