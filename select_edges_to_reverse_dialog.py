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
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
from qgis.core import *
from qgis.utils import iface

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'select_edges_to_reverse_dialog_base.ui'))
        
class SelectEdgesToReverseDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, abnormal_features_list, input_layer, parent=None):
        """Constructor."""
        super(SelectEdgesToReverseDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        self.setupUi(self)
        self.features_to_reverse = []
        self.remaining_features = abnormal_features_list
        
        self.break_ = False
        
        self.buttonYes.clicked.connect(self.handleYesButtonClicked)
        self.buttonNo.clicked.connect(self.handleNoButtonClicked)
        self.buttonYesToAll.clicked.connect(self.handleYesToAllButtonClicked)
        self.buttonNoToAll.clicked.connect(self.handleNoToAllButtonClicked)
        
        self.process_abnormal_features(abnormal_features_list, input_layer)
        
    def process_abnormal_features(self, abnormal_features_list, input_layer):
        """
        Main method for handling the user's response to the dialog box on whether
        or not one wants to reverse a given feature
        
        The methode displays an symbology with arrows on the layer of the stream
        to indicate to the user the direction of a stream line.
        It ranges the given feature list of abnormal stream lines, and for each
        of them, it zooms to the feature and asks the user if one wants that the
        processing algorithm of stream order computation considers the direction
        of the feature as reversed.
        If the user gives a positive answer, the feature is appended to the
        the attribute 'features_to_reverse' of the class
        
        :param abnormal_features_list: A list of abnormal features
        :abnormal_features_list type: list of QgsFeatures
        
        :param input_layer: Layer of the stream lines
        :input_layer type: QgsVectorLayer
        
        :return: Fill the attribute 'features_to_reverse' of the class
        :rtype: void
        """
        # Get the active layers before process
        active_layer = iface.activeLayer()
        
        # Set the input layer as the active layer
        iface.setActiveLayer(input_layer)
        
        # Set the directions of the flow on the layer
        set_arrows(input_layer)
        
        # Get the number of abnormal features
        remaining_features_to_process = len(abnormal_features_list)
        
        for feature in abnormal_features_list:
            
            # 
            if self.break_:
                break
            
            # Save current feature as a class attribute
            self.current_feature = feature
            
            # Get the feature in the input layer
            input_layer.select(feature.id())
            # Zoom on the feature
            iface.mapCanvas().zoomToSelected()
            
            # Set text on the interface
            self.labelTxt_1.setText('Do you want to reverse Feature ' + str(feature.id()) + '?')
            self.labelTxt_2.setText('Remaining features to process : ' + str(remaining_features_to_process - 1))
            
            # Main loop of the dialog window
            self.exec_()
            
            # Once one button has been clicked
            # Remove the feature of selection
            input_layer.removeSelection()

            self.remaining_features.pop(self.remaining_features.index(self.current_feature))
            
            # Decrement the number of features to process
            remaining_features_to_process -= 1

        # Remove the directions of the flow on the layer
        unset_arrows(input_layer)
        
        # Set back the active layer(s) to the one active before process
        iface.setActiveLayer(active_layer)
        
        # Go to the layer extent
        iface.mapCanvas().setExtent(input_layer.extent())
        
    def handleYesButtonClicked(self):
        """
        Method to handle is the user click "Yes" button on the dialog window.
        
        It appends the current feature to the 'features_to_reverse' class
        attribute.
        """
        print('Yes')
        self.features_to_reverse.append(self.current_feature)
        self.close()
        
    def handleNoButtonClicked(self):
        """
        Method to handle is the user click "Yes" button on the dialog window.
        """
        print('No')
        self.close()
    
    def handleYesToAllButtonClicked(self):
        """
        Method to handle is the user click "Yes to all" button on the dialog window.
        """
        print('Yes To All')
        self.features_to_reverse += self.remaining_features.copy()
        self.break_ = True
        self.close()
    
    def handleNoToAllButtonClicked(self):
        """
        Method to handle is the user click "No to all" button on the dialog window.
        """
        print('No to All')
        self.break_ = True
        self.close()

def set_arrows(input_layer):
    """
    Give a spectific symbology to the input layer
    
    :param input_layer: A layer
    :input_layer type: QgsVectorLayer
    """
    # Get the renderer of the layer
    layer_renderer = input_layer.renderer()
    
    # Create symbology
    marker = {'interval': '3', 'interval_map_unit_scale': '3x:0,0,0,0,0,0', 'interval_unit': 'MM', 'offset': '0', 'offset_along_line': '0', 'offset_along_line_map_unit_scale': '3x:0,0,0,0,0,0', 'offset_along_line_unit': 'MM', 'offset_map_unit_scale': '3x:0,0,0,0,0,0', 'offset_unit': 'MM', 'placement': 'centralpoint', 'rotate': '1'}
    arrow = {'angle': '90', 'color': '255,0,0,255', 'horizontal_anchor_point': '1', 'joinstyle': 'bevel', 'name': 'arrow', 'offset': '0,0', 'offset_map_unit_scale': '3x:0,0,0,0,0,0', 'offset_unit': 'MM', 'outline_color': '35,35,35,255', 'outline_style': 'solid', 'outline_width': '0', 'outline_width_map_unit_scale': '3x:0,0,0,0,0,0', 'outline_width_unit': 'MM', 'scale_method': 'diameter', 'size': '2.5', 'size_map_unit_scale': '3x:0,0,0,0,0,0', 'size_unit': 'MM', 'vertical_anchor_point': '1'}
    
    # Assign symbology to symbology holder
    symbol_layer = QgsMarkerLineSymbolLayer.create(marker)
    # Get subsymbol
    subSymbol = symbol_layer.subSymbol()
    arrow_symbol = QgsSimpleMarkerSymbolLayer.create(arrow)
    # Delete existing subsymbol
    subSymbol.deleteSymbolLayer(0)
    # Append the arrow symbol
    subSymbol.appendSymbolLayer(arrow_symbol)
    
    # Append a new symbology to the renderer of the current layer
    layer_renderer.symbol().appendSymbolLayer(symbol_layer)
    
    # Refresh
    iface.layerTreeView().refreshLayerSymbology(input_layer.id())

def unset_arrows(input_layer):
    """
    Remove the arrow symbology of the input_layer
    
    :param input_layer: A layer
    :input_layer type: QgsVectorLayer
    """
    # Get the renderer of the layer
    layer_renderer = input_layer.renderer()
    
    # Get the number of symbol layers the layer has
    nb_sl = layer_renderer.symbol().symbolLayerCount()
    # Replace the renderer of the current layer
    layer_renderer.symbol().deleteSymbolLayer(nb_sl - 1)
    
    # Refresh
    iface.layerTreeView().refreshLayerSymbology(input_layer.id())