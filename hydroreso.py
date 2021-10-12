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

from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, QVariant, Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QAction, QFileDialog, QMessageBox, QProgressBar
from qgis.core import *

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .hydroreso_dialog import HydroresoDialog
from .select_edges_to_reverse_dialog import SelectEdgesToReverseDialog
import os.path
import numpy as np


class Hydroreso:
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
            'Hydroreso_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Hy2roresO')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'Hydroreso')
        self.toolbar.setObjectName(u'Hydroreso')

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
        return QCoreApplication.translate('Hydroreso', message)


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

        icon_path = ':/plugins/hydroreso/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Hy2roresO'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Hy2roresO'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """
        Run method that performs all the real work
        """
        # Create the dialog (after translation) and keep reference
        self.dlg = HydroresoDialog()
        
        # show the dialog
        self.dlg.show()

        # Run the dialog event loop
        result = self.dlg.exec_()

        # See if OK was pressed
        if result:
            # All the real work happens here
            self.run_process()

    def run_process(self):
        """
        Do the whole stuff
        """
        # Get the hierarchisation order to compute
        strahler_order = self.dlg.checkBox_strahler.isChecked()
        horton_order = self.dlg.checkBox_horton.isChecked()
        shreve_order = self.dlg.checkBox_shreve.isChecked()

        if not strahler_order and not horton_order and not shreve_order:
            show_message_no_stream_order_selected()

#        #TODO: Handle if it already exists a "strahler" field
#        if "strahler" in input_layer.dataProvider().layers():
#            msgBox = QMessageBox(
#                    QMessageBox.Warning,
#                    'Error',
#                    "There is already one field named 'strahler'",
#                    QMessageBox.Ok)
#            msgBox.exec_()
#
#            self.close

        else:
            # Handle progress bar
            progressMessageBar = self.iface.messageBar().createMessage("Initialisation...")
            progress = QProgressBar()
            progress.setMaximum(100)
            progress.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
            progressMessageBar.layout().addWidget(progress)
            self.iface.messageBar().pushWidget(progressMessageBar)
            message_in_bar = progressMessageBar.children()[2]
            
            # Handle progress bar
            progress.setValue(10)
            
            # Get the selected input layer from the interface
            current_layer_string = str(self.dlg.comboBox_layers.currentText())
            input_layer = QgsProject.instance().mapLayersByName(current_layer_string)[0]
            
            # Get provided information about the input layer
            name_column = str(self.dlg.qcombobox_1.currentText())
            alt_init_column = str(self.dlg.qcombobox_2.currentText())
            alt_final_column = str(self.dlg.qcombobox_3.currentText())

            # Get features of the input layer
            features = list(input_layer.dataProvider().getFeatures())

            # Handle progress bar
            message_in_bar.setText('Edges and nodes creation...')
            progress.setValue(15)
            
            # Instances creation
            edges, nodes = create_edges_nodes(features, name_column, alt_init_column, alt_final_column)
            set_edges_connected_nodes(nodes, edges)

            # Handle progress bar
            message_in_bar.setText('Checking for geometries...')
            progress.setValue(20)
            
            # Edges direction
            # Option reverse edges checked
            reverseIsChecked = self.dlg.checkBox_reverse.isChecked()
            # Option add a field reversed checked
            field_reverse = self.dlg.checkBox_addReverseField.isChecked()
            # If the option reverse edges is checked
            if reverseIsChecked:
                # Find edges probably wrong
                abnormal_edges = test_direction(edges, nodes)
                # Corresponding features
                abnormal_features = edges_to_features(abnormal_edges, input_layer)

                selectEdgesToReverse_dlg = SelectEdgesToReverseDialog(abnormal_features, input_layer)

                # Answer interface
                features_to_reverse = selectEdgesToReverse_dlg.features_to_reverse

                # Reverse edges chosen by user
                edges_to_reverse = features_to_edges(features_to_reverse, edges)
                reverse_all_edges(edges_to_reverse)

            # Handle progress bar
            message_in_bar.setText('Finding sources and sinks...')
            progress.setValue(30)

            # Sources and sinks detection
            sources_edges, sinks_edges = find_sources_sinks(edges)

            # Handle progress bar
            message_in_bar.setText('Detecting islands...')
            progress.setValue(40)
            
            #Islands detection
            streams_in_islands = detect_islands(input_layer, edges)
            create_islands(streams_in_islands)

            # Generate orders list to compute
            orders_to_compute = []
            if strahler_order:
                orders_to_compute.append("strahler")
            if horton_order:
                orders_to_compute.append("horton")
            if shreve_order:
                orders_to_compute.append("shreve")

            # Handle progress bar
            message_in_bar.setText('Orders computation...')
            progress.setValue(60)
            
            # Order computation
            process_network(edges, sources_edges, orders_to_compute, edges.copy(), {}, {}, {})
            
            # Handle progress bar
            message_in_bar.setText('Updating table...')
            progress.setValue(75)
            
            # Update the layer creating a new field
            update_table(input_layer, orders_to_compute, field_reverse, edges)
            
            # Handle progress bar
            message_in_bar.setText('Saving layer...')
            progress.setValue(99)
            
            # Option save output layer checked
            save_output_layer_checkbox = self.dlg.checkBox_saveLayer.isChecked()
            if save_output_layer_checkbox:
                path_to_saving_location_output_layer = self.dlg.output_layer.text()
                save_output_layer(input_layer, path_to_saving_location_output_layer)
            
            # Handle progress bar
            message_in_bar.setText('Finished!')
            progress.setValue(100)
            
            # Show success
            show_field_created_successfully()
            
            # Clear message bar
            self.iface.messageBar().clearWidgets()

# ________ CLASSES _________________________________________________________

class Edge:
    """
    Class of an Edge of the river network.
    Instantiated with attributes of the features of the layer of the network.
    """
    def __init__(self, geom, id_edge, node_start, node_end):
        # Geometry of the feature (line)
        self.geom = geom
        # ID of the edge (same as the ID of the feature; integer)
        self.id_edge = id_edge
        # Start node of the edge
        self.node_start = node_start
        # End node of the edge
        self.node_end = node_end
        # Dictionary of stream orders computed by the plugin
        self.stream_orders = {}
        # True if the edge is reversed for the computation of the orders
        self.reversed = False
        # ID of the stroke of the edge (necessary for Horton order)
        self.id_stroke = None 
        # Island object of the edge, if it belongs to an island
        self.island = None
        # Name of the river the edge is a part of
        self.name = None
        # Initial altitude of the edge
        self.alt_init = None
        # Final altitude of the edge
        self.alt_final = None
        
    
    def copy_edge(self):
        """
        Copy an Edge object.
        Create an Edge object that has the same attributes.
        
        :return: Copy of the edge
        :rtype: Edge object
        """
        new_edge = Edge(self.geom, self.id_edge, self.node_start.copy_node(), self.node_end.copy_node())
        new_edge.stream_orders = self.stream_orders.copy()
        new_edge.reversed = self.reversed
        new_edge.id_stroke = self.id_stroke
        if self.island == None:
            new_edge.island = None
        else:
            new_edge.island = self.island.copy_island()
        new_edge.name = self.name
        new_edge.alt_init = self.alt_init
        new_edge.alt_final = self.alt_final
        
        return new_edge
        
class Node:
    """
    Class of a Node of the river network.
    Instantiated with attributes of the features of the layer of the network.
    """
    def __init__(self, geom, id_node):
        # Geometry of the feature (point)
        self.geom = geom
        # ID of the node (ID of one of its connected edges and number 1 or 2 concatenated)
        self.id_node = id_node
        # List of the incoming edges of the node
        self.edges_in = []
        # List of the outgoing edges of the node
        self.edges_out = []
        
    def copy_node(self):
        """
        Copy a Node object.
        Create a Node object that has the same attributes.
        
        :return: Copy of the node
        :rtype: Node object
        """
        new_node = Node(self.geom, self.id_node)
        new_node.edges_in = self.edges_in
        new_node.edges_out = self.edges_out
        
        return new_node


class Island:
    """
    Class of an Island of the river network.
    Instantiated with the edges of the island.
    """
    def __init__(self, island_edges):
        # Edges that make up the island (Edge objects)
        self.edges = island_edges
        # Incoming edges of the island (Edge objects)
        self.edges_in = []
        # Outgoing edges of the island (Edge objects)
        self.edges_out = []
        # Stroke ID of the island (integer)
        self.id_stroke = None
        
    def copy_island(self):
        """
        Copy an Island object.
        Create an Island object that has the same attributes.
        
        :return: Copy of the island
        :rtype: Island object
        """
        new_island = Island(self.edges)
        new_island.edges_in = self.edges_in
        new_island.edges_out = self.edges_out
        new_island.id_stroke = self.id_stroke
        
        return new_island
        
    def compute_edges_in_out(self):
        """
        Compute the incoming and outgoing edges of the island.
        Set attributes edges_in and edges_out from the edges of the island and
        their connections to the network.
        """
        self.compute_edges_in()
        self.compute_edges_out()
    
    def compute_edges_in(self):
        """
        Compute the incoming edges of the island.
        Set attribute edges_in from the edges of the island and their 
        connections to the network.
        """
        # New value of the attribute edges_in
        edges_incoming_island = []
        
        # For each edge of the island
        for island_edge in self.edges:
            # Incoming edges of the edge of the island
            incoming_edges = island_edge.node_start.edges_in
            # For each incoming edge
            for incoming_edge in incoming_edges:
                # If the incoming edge is not in the island too, and if it
                # is not already listed
                incoming_edge_in_island = incoming_edge in self.edges
                if not incoming_edge_in_island and incoming_edge not in edges_incoming_island:
                    # Add to the list
                    edges_incoming_island.append(incoming_edge)
        
        # Incoming edges of the island         
        self.edges_in = edges_incoming_island
        
        
    def compute_edges_out(self):
        """
        Compute the outgoing edges of the island.
        Set attribute edges_out from the edges of the island and their 
        connections to the network.
        """
        # Same process as compute_edges_in method
        edges_outgoing_island = []
        
        for island_edge in self.edges:
            outgoing_edges = island_edge.node_end.edges_out
  
            for outgoing_edge in outgoing_edges:
                outgoing_edge_in_island = outgoing_edge in self.edges
            
                if not outgoing_edge_in_island and outgoing_edge not in edges_outgoing_island:
                    edges_outgoing_island.append(outgoing_edge)
                    
        self.edges_out = edges_outgoing_island


# ________ INSTANCES _________________________________________________________

def create_edges_nodes(features, name_column, alt_init_column, alt_final_column):
    """
    Instantiate all the Edge and Node objects that make up the river network.
    The name of the river and the altitudes are attributes of the objects 
    if the names of the columns are given in arguments.
    
    :param features: list of all the features of the river network layer
    :type features: list of QgsFeatures objects
    :param name_column: name of the column of the name of the river 
                        (selected by the user, empty string if not selected)
    :type name_column: string
    :param alt_init_column: name of the column of the initial altitude
                        (selected by the user, empty string if not selected) 
    :type alt_init_column: string
    :param alt_final_column: name of the column of the final altitude
                        (selected by the user, empty string if not selected) 
    :type alt_final_column: string
                      
    :return: list of all the edges, list of all the nodes making up the river network
    :rtype: list of Edge objects, list of Node objects
    """
    # Lists to return
    edges = []
    nodes = [] 

    # For each feature of the river network layer
    for i in range(len(features)):
        # ID of the feature
        id_feature = features[i].id()
        # Geometry of the feature
        geom = features[i].geometry()
        
        # Geometries of the first and last nodes of the feature (points of the 
        # polyline)
        node1_geom = geom.asPolyline()[0]
        node2_geom = geom.asPolyline()[-1]
        
        # Instantiate first nodes of the network
        if len(nodes) == 0:
            # First node
            # Geometry of the first node, ID is the ID of the feature and 
            # number 1 concatenated
            node1 = Node(node1_geom, id_feature*10 + 1)
            nodes.append(node1)
            # Second node
            # Geometry of the second node, ID is the ID of the feature and 
            # number 2 concatenated
            node2 = Node(node2_geom, id_feature*10 + 2)
            nodes.append(node2)    
        
        # Test if the nodes already exist
        equals_node1 = False 
        equals_node2 = False
        for node in nodes:
            if node1_geom == node.geom:
                node1 = node
                equals_node1 = True
            if node2_geom == node.geom:
                node2 = node
                equals_node2 = True
         
        # If the nodes do not exist already, intantiate them
        # Add the nodes to the list of all the instantiated nodes
        if not equals_node1:
            node1 = Node(node1_geom, id_feature*10 + 1)
            nodes.append(node1)
        if not equals_node2:
            node2 = Node(node2_geom, id_feature*10 + 2)
            nodes.append(node2)
            
        # Instantiate edge
        # Takes geometry of the feature, ID is the same ID as the feature, 
        # the two nodes instantiated
        edge = Edge(geom, id_feature, node1, node2)
        
        # If columns were selected by the user, fill attributes
        # Name of the river
        if name_column == "":
            edge.name = None
        else:
            edge.name = features[i][name_column]
        # Initial altitude   
        if alt_init_column == "":
            edge.alt_init = None
        else:
            edge.alt_init = features[i][alt_init_column]
        # Final altitude
        if alt_final_column == "":
            edge.alt_final = None
        else:
            edge.alt_final = features[i][alt_final_column]
        
        # Add the edge to the list of all the instantiated edges
        edges.append(edge)
        
    return edges, nodes

def set_edges_connected_nodes(nodes, edges):
    """
    Fill the lists of incoming and outgoing edges of the input nodes 
    (lists are attributes of Node objects).
    
    The connection between nodes and edges is given by the start node and 
    end node of each edge.
    
    :param nodes: list of all the nodes making up the river network
    :type nodes: list of Node objects
    :param edges: list of all the edges making up the river network
    :type edges: list of Edge objects
    """
    # For each node of the network
    for node in nodes:
        # For each edge of the network
        for edge in edges :
            # start node and end node of the edge
            node1 = edge.node_start
            node2 = edge.node_end
            # If the current node is the start node of the edge
            if node1.id_node == node.id_node:
                # Then the edge exists the node
                node.edges_out.append(edge)
            # If the current node is the end node of the edge
            if node2.id_node == node.id_node:
                # Then the edge enters the node
                node.edges_in.append(edge)
 
def create_islands(streams_in_islands):
    """
    Instanciation of Island objects from the list of the edges that make up the
    island.
    
    The instantiated objects are stored as attributes of the edges that belong 
    to the island.
    
    :param streams_in_islands: edges that belong to the island
    :type streams_in_islands: list of lists of Edge objects
    """
    # If there are islands
    if streams_in_islands != []:
        # For each island
        for island_edges in streams_in_islands:
            # Instantiate Island object with its edges
            island = Island(island_edges)
            island.compute_edges_in_out()
            # The Island object is an attribute of its edges
            for edge in island_edges:
                edge.island = island
            

# ________ CORRECT EDGE DIRECTIONS ___________________________________________

def test_direction(edges, nodes):
    """
    Test the direction of edges and return the list of abnormal edges
    (probable wrong direction).
    
    Uses altitudes if known or studies links in graph if altitude is unknown.
    
    :param edges: list of all the edges making up the river network
    :type edges: list of Edge objects
    :param nodes: list of all the nodes making up the river network
    :type nodes: list of Node objects
    
    :return: list of abnormal edges
    :rtype: list of Edge objects
    """
    abnormal_edges = []
    
    for edge in edges:
        # Test altitudes
        # If altitudes are known and initial altitude is inferior to final 
        # altitude, the edge is abnormal
        if edge.alt_init != None and edge.alt_final != None and edge.alt_init < edge.alt_final :
            abnormal_edges.append(edge)
    
        # Test network connections
        # Test each node
        for node in nodes:
            
            # If node has no incoming edge, and several outgoing edges (ie not 
            # a source) then the node is probably wrong
            if len(node.edges_in) == 0 and len(node.edges_out) > 1 :
                # For each outgoing edge of the node
                for edge_out in node.edges_out:
                    # If the other node of the edge seems also wrong, the 
                    # edge is abnormal
                    node_end_abnormal = is_node_abnormal(edge_out.node_end)
                    if node_end_abnormal:
                        abnormal_edges.append(edge_out)
                        
                    # If the other node may be correct
                    else:
                        # Try and reverse the edge
                        reverse(edge_out)
                        # Test if it makes the other node of the edge wrong
                        next_node = next_node_of_edge(node, edge_out)
                        # If it doesn't, the edge is abnormal
                        if not is_node_abnormal(next_node):
                            abnormal_edges.append(edge_out)
                        # Cancel the reversal
                        reverse(edge_out)
                        # Cancel attribute reversed
                        edge_out.reversed = False 
                        
            # Same process if the node has no outgoing edge, and several 
            # incoming edges (ie not a sink)           
            if len(node.edges_out) == 0 and len(node.edges_in) > 1 :
                for edge_in in node.edges_in:
                    node_start_abnormal = is_node_abnormal(edge_in.node_start)
                    if node_start_abnormal:
                        abnormal_edges.append(edge_in)
                    else:
                        reverse(edge_in)
                        next_node = next_node_of_edge(node, edge_in)
                        if not is_node_abnormal(next_node):
                            abnormal_edges.append(edge_in)
                        reverse(edge_in)
                        # Cancel attribute reversed
                        edge_in.reversed = False
                            
        return abnormal_edges

    
def is_node_abnormal(node):
    """
    Test if a node is abnormal, ie if all its connected edges are in the same
    direction (all incoming or all outgoing edges) and the node is not a source
    nor a sink (it has more than one incoming or outgoing edge). A node that is 
    not a source nor a sink should indeed have at least one incoming edge and 
    one outgoing edge (unless it is a multiple source or sink).
    
    Returns True if the node is regarded as abnormal.
    
    :param node: node to test
    :type node: Node object
    """
    # Returns True if the edge is abnormal: it has no incoming edge and several
    # outgoing edges, or no outgoing edge and several incoming edges
    return (len(node.edges_in) == 0 and len(node.edges_out) > 1) or (len(node.edges_out) == 0 and len(node.edges_in) > 1)

def next_node_of_edge(node, edge):
    """
    Return the node of the edge that is not the input node.
    
    :param node: current node
    :type node: Node object
    :param edge: current edge
    :type edge: Edge object
    
    :return: next node of the edge
    :rtype: Node object
    """
    # If the input node is the start node of the edge, return the end node
    if edge.node_start.id_node == node.id_node:
        return edge.node_end
    
    # If the input node is the end node of the edge, return the start node
    if edge.node_end.id_node == node.id_node:
        return edge.node_start
    
    
def reverse(edge):
    """
    Reverse an Edge object.
    The method swaps the nodes of the edge, updates the incoming and outgoing
    edges lists of the nodes, reverses the geometry of the edge and updates
    the attribute edge.reverse to True.
    Only the object is altered, the input layer remains unchanged.
    
    :param edge: edge to reverse
    :type edge: Edge object
    """
    
    # Update edges connected to nodes
    edge.node_start.edges_out.pop(edge.node_start.edges_out.index(edge))
    edge.node_start.edges_in.append(edge)
    
    edge.node_end.edges_in.pop(edge.node_end.edges_in.index(edge))
    edge.node_end.edges_out.append(edge)
    
    # Swap nodes
    node_start = edge.node_start
    node_end = edge.node_end
    edge.node_start = node_end
    edge.node_end = node_start
    
    # Reverse geometry
    geom = edge.geom
    polyline = geom.asPolyline()
    polyline.reverse() 
    newgeom = QgsGeometry.fromPolylineXY(polyline)
    edge.geom = newgeom
    
    # Update attribute
    edge.reversed = True

    
def reverse_all_edges(edges_to_reverse):
    """
    Reverse edges of the input list (call reverse(edge) method).
    
    :param edges_to_reverse: list of edges to reverse
    :edges_to_reverse type: list of Edge objects
    """
    for edge in edges_to_reverse:
        reverse(edge)
    
def edges_to_features(list_edges, input_layer):
    """
    Transform a list of Edges objects into a list of the corresponding features
    of the layer.
    
    :param list_edges: list of the edges corresponding to the desired features
    :type list_edges: list of Edge objects
    :param input_layer: layer of the features (and the corresponding edges)
    :type input_layer: QgsVectorLayer object
    
    :return: list of features
    :rtype: list of QgsFeatures objects
    """
    # List of the features to return
    list_features = []
    # For each edge of the list
    for edge in list_edges:
        # ID of the edge
        id_edge = edge.id_edge
        # Corresponding feature: same ID
        feature = input_layer.getFeature(id_edge)
        # Update list
        list_features.append(feature)
        
    return list_features
        
def features_to_edges(list_features, edges):
    """
    Transform a list of QgsFeatures objects into a list of the corresponding 
    Edge objects of the layer.
    
    :param list_features: list of the features corresponding to the desired edges
    :type list_features: list of QgsFeatures objects
    :param input_layer: layer of the features (and the corresponding edges)
    :type input_layer: QgsVectorLayer object
    
    :return: list of edges
    :rtype: list of Edge objects
    """
    # List of the edges to return
    list_edges = []
    # For each feature of the list
    for feature in list_features:
        # ID of the feature
        id_feature = feature.id()
        # Corresponding edge: index in the edges list
        edge = edges[id_feature-1]
        # Update list
        list_edges.append(edge)
        
    return list_edges


# ________ SOURCES AND SINKS _________________________________________________
                
def find_sources_sinks(edges):
    """
    Find source edges and sink edges of the network.
    A source edge is an edge exiting a node that is only connected to this edge.
    A sink edge is an edge entering a node that is only connected to this edge.
    
    :param edges: list of all the edges making up the river network
    :type edges: list of Edge objects
    
    :return: list of source edges, list of sink edges
    :rtype: list of Edge objects, list of Edge objects
    """
    # Lists to return
    sources_edges = []
    sinks_edges = []
    
    # For each edge of the network
    for edge in edges:
        # Get connected edges
        start_edges = len(edge.node_start.edges_in)
        end_edges = len(edge.node_end.edges_out)
        # If there is no start edge, the edge is a source
        if start_edges == 0:     
            sources_edges.append(edge)
        # If there is no end edge, the edge is a sink
        if end_edges == 0:
            sinks_edges.append(edge)
    
    return sources_edges, sinks_edges

# ________ ISLANDS DETECTION _________________________________________________

def detect_islands(stream_layer, edges):
    """
    Detect islands in the network.
    Return a list of lists of the edges that make up each island.
    
    :param stream_layer: layer of the river network
    :type edges: QgsVectorLayer object
    :param edges: list of all the edges that make up the river network
    :type edges: list of Edge objects
    
    :return: list of lists of edges of the islands
    :rtype: list of lists of Edge objects
    """
    # Island detection algorithm: creates polygons for islands (faces of the graph)
    poly = polygonize(stream_layer)
    
    # If there are islands
    if poly != None:
        # Features (islands) of the polygonized layer
        listFeatures = iterator_to_list(poly.dataProvider().getFeatures())
        # Aggregate the geometries of the islands into one geometry
        # (in particular, complex islands made up by several single geometries
        # become one bigger geometry)
        aggr = aggregate(listFeatures)
        # Split the aggregated geometry into single geometries (one per island)
        geom = multi_to_single(aggr)
        # Create a layer of the islands
        island_layer = create_layer_geom(geom, stream_layer.crs().toWkt(), name="islands")
        # Get the streams (features) inside or delimiting islands
        streams_in_islands_features = relate_stream_island(stream_layer, island_layer)
        # Merge islands that are successive into one complex island 
        # (successive islands are not adjacent but there is no edge between them 
        # (that does not belong to an island)   
        merged_streams_in_islands_features = merge_successive_islands_streams(streams_in_islands_features)
        
        # Get the Edge objects corresponding to the features of the layer
        # that are in islands
        streams_in_islands = []
        for list_island_features in merged_streams_in_islands_features:
            list_island = features_to_edges(list_island_features, edges)
            streams_in_islands.append(list_island)
        
    # If there is no island
    else :
        streams_in_islands = []
    
    # Edges of the islands    
    return streams_in_islands



def polygonize(input_layer, name="temp"):
        """
        Island detection algorithm.
        If there is no island, return None.
        
        :param input_layer: layer of the river network
        :input_layer type: QgsVectorLayer object
        :param name: name of the layer if displayed
        :name type: string
        
        :return: layer of faces of the network (islands, polygons)
        :rtype: QgsVectorLayer object
        """
        source = input_layer

        # Create output layer
        output = QgsVectorLayer("Polygon?crs=" + input_layer.crs().authid(), name, "memory")
        
        # Get the data provider
        output_dp = output.dataProvider()
        
        # Allow editing of the selected layer
        output.startEditing()
        # Add a "real" field type with the name "AREA" to the output layer
        output_dp.addAttributes( [ QgsField("AREA", QVariant.Double) ] )
        # Update the attribute table
        output.updateFields()
        # Find index of the newly-created "Area" field
        idx = output_dp.fieldNameIndex( "AREA" )

        # Get the features of the layer
        allLinesList = []
        features = source.getFeatures(QgsFeatureRequest().setSubsetOfAttributes([]))
        for current, inFeat in enumerate(features):
            if inFeat.geometry():
                allLinesList.append(inFeat.geometry())
    
        allLines = QgsGeometry.unaryUnion(allLinesList)
    
        polygons = QgsGeometry.polygonize([allLines])
        
        # If there is no island
        if polygons.isEmpty():
            return None
    
        # If there are islands
        if not polygons.isEmpty():
            feature_list = []
            # For each polygon geometry
            for i in range(polygons.constGet().numGeometries()):
                # Create output feature
                outFeat = QgsVectorLayerUtils.createFeature(output)
                
                # Give geometry to the output feature
                geom = QgsGeometry(polygons.constGet().geometryN(i).clone())
                outFeat.setGeometry(geom)
                
                # Set the area of a polygon in the "area" field
                outFeat[idx] = polygons.constGet().geometryN(i).area()
                output.updateFeature(outFeat)
                
                # Add created feature to feature list
                feature_list.append(outFeat)
                
                # Add new feature to output layer
                output_dp.addFeatures([outFeat])
        
        # Save the output layer
        output.commitChanges()
        
        return output

def display_layer(layer):
    """
    (dev)
    Display the input layer in the QGIS project.
    """
    # Import layer in QGIS
    QgsProject.instance().addMapLayer(layer)
    # Set the layer visible
    iface.mapCanvas().refreshAllLayers()

def display_geom(list_geom, name="temp"):
    """
    (dev)
    Create a Polygon layer with the input list of geometries (must be polygons)
    and display the created layer in the QGIS project.
    
    :param list_geom: list of polygons
    :list_geom type: list of QgsGeometry
    :param name: (optional) Name of the layer to display. Default = "temp"
    :name type: string
    
    :return: layer of polygons
    :rtype: QgsVectorLayer object
    """
    # Create output layer
    output = QgsVectorLayer("Polygon", name, "memory")
    
    # Get the data provider
    output_dp = output.dataProvider()
    
    for geom in list_geom:
        
        outFeat = QgsVectorLayerUtils.createFeature(output)
                    
        outFeat.setGeometry(geom)
        
        # Add new feature to output layer
        output_dp.addFeatures([outFeat])
    
    output.commitChanges()
    
    display_layer(output)
    
    return output


def create_layer_geom(list_geom, crs, name="temp"):
    """
    Create a Polygon layer with the input list of geometries (must be polygons).
    
    :param list_geom: list of polygons
    :list_geom type: list of QgsGeometry
    
    :param crs: the crs of the output layer
    :type crs: string (format Wkt)
    
    :param name: (optional) Name of the layer to display. Default = "temp"
    :name type: string
    
    :return: layer of polygons
    :rtype: QgsVectorLayer object
    """
    # Create output layer
    output = QgsVectorLayer("Polygon?crs=" + crs, name, "memory")
    
    # Get the data provider
    output_dp = output.dataProvider()
    
    for geom in list_geom:
        
        outFeat = QgsVectorLayerUtils.createFeature(output)
                    
        outFeat.setGeometry(geom)
        
        # Add new feature to output layer
        output_dp.addFeatures([outFeat])
    
    output.commitChanges()
    
    return output

def iterator_to_list(iterator):
    """
    Transform the input iterator into a list.
    :param iterator:
    :iterator type:
    """
    liste = [elem for elem in iterator]
    return liste

def aggregate(listFeatures):
    """
    Aggregate the geometries of the input list of features into one geometry.
    
    :param listFeatures: features to aggregate
    :listFeatures type: list of QgsFeatures objects
    
    :return: the aggregated geometry
    :rtype: QgsGeometry object
    """
    aggr = listFeatures[0].geometry()
    
    for i in range (1, len(listFeatures)):
        aggr = aggr.combine(listFeatures[i].geometry())
    
    return aggr
    
def multi_to_single(geom):
    """
    Transform the input multi-polygon into a list of single-polygons.
    
    :param geom: multi-polygon
    :geom type: QgsGeometry object
    
    :return: list of the single geometries
    :rtype: list of QgsGeometry objects
    """
    multiGeom = QgsGeometry()
    geometries = []
    if geom.type() == 2:
            if geom.isMultipart():
                multiGeom = geom.asMultiPolygon()
                for i in multiGeom:
                    geometries.append(QgsGeometry().fromPolygonXY(i))
            else:
                geometries.append(geom)
    return geometries


def relate_stream_island(stream_layer, island_layer):
    """
    Return the streams inside or delimiting islands.
    The topology is defined by DE-9IM matrices.
    
    :param stream_layer: the layer of the river network
    :stream_layer type: QgisVectorLayer object (lines)
    :param island_layer: the layer of the islands 
    :island_layer type: QgisVectorLayer object (polygons)
    
    :return: list of lists of all the streams that make up the islands
    :rtype: list of lists of QgisFeatures objects
    """
    # Get the features of the stream and island layers
    streams_list = list(stream_layer.dataProvider().getFeatures())
    islands_list = list(island_layer.dataProvider().getFeatures())

    # Initialise output list
    streams_in_island_list = []

    
    for island in islands_list:
        # Initialise list of output list
        island_list = []
        # Get the AbstractGeometry object for the current island
        current_island_abstract_geom = island.geometry().constGet() 
        
        for stream in streams_list:
            # Get the AbstractGeometry object for the current stream
            current_stream_abstract_geom = stream.geometry().constGet()
            # Create QgsGeometryEngine object
            engine = QgsGeometry.createGeometryEngine(current_stream_abstract_geom)
            # Prepares the geometry, so that subsequent calls to spatial relation methods are much faster
            engine.prepareGeometry()      
            
            # Test if the current stream fits with the DE-9IM matrices
            if engine.relatePattern(current_island_abstract_geom,'F1FF0F212') or engine.relatePattern(current_island_abstract_geom,'1FF00F212') or engine.relatePattern(current_island_abstract_geom,'1FF0FF212') or engine.relatePattern(current_island_abstract_geom,'1FFF0F212'):
                # If so, then the current stream is appended to the output list
                island_list.append(stream)
                
        streams_in_island_list.append(island_list)
        
    return streams_in_island_list

def merge_successive_islands_streams(streams_in_island_list):
    """
    Compute successive islands.
    Successive islands are islands that are not adjacent, and there is no 
    edge between them (that does not belong to an island).
    The topology is defined by a DE-9IM matrix.
    Successive islands are merged into one complex island: lists of edges of 
    successives islands are concatenated into one list.
    Return the list of lists of features (edges) of the islands.
    
    :param streams_in_island_list: list of lists of all the streams that
                                   make up the islands
    :type streams_in_island_list: list of lists of QgisFeatures objects
    
    :return: list of lists of all the streams that make up the islands, 
             successive islands merged
    :rtype: list of lists of QgisFeatures objects
    """
    
    # Initialise output list
    merged_streams_in_island_list = []

    # For each island
    for index_island in range(len(streams_in_island_list) - 1):
        tested_island_streams = streams_in_island_list[index_island].copy()
            
        # Test if is successive to other islands (topology defined by DE-9IM matrix)
        list_island_touched = []
        for other_index_island in range(index_island + 1, len(streams_in_island_list)):
            compared_island_streams = streams_in_island_list[other_index_island].copy()
            
            touch_other_island = False
            # For each stream of the first island
            for stream in tested_island_streams:
                current_island_stream_abstract_geom = stream.geometry().constGet()
                engine = QgsGeometry.createGeometryEngine(current_island_stream_abstract_geom)
                engine.prepareGeometry()    
                # For each stream of the other island
                for other_stream in compared_island_streams:
                    other_island_stream_abstract_geom = other_stream.geometry().constGet() 
                    # Islands are successive if the frontiers of two streams of 
                    # each island touch
                    if engine.relatePattern(other_island_stream_abstract_geom,'FF1F00102'):
                        touch_other_island = True
            
            # If islands are successive, add to the list
            if touch_other_island:
                list_island_touched.append(compared_island_streams)
        
        # All the streams that make up one pair of successive islands         
        merged_streams_in_island = tested_island_streams
        for island_touched in list_island_touched:
            merged_streams_in_island += island_touched
        
        # List of lists of streams of pairs of successive islands
        merged_streams_in_island_list.append(merged_streams_in_island)
    
    # Pairs that make up a series are merged into one list of successive islands
    merged_streams_in_island_list = merge_duplicate(merged_streams_in_island_list)
    
    # List of lists of streams of successive islands
    return merged_streams_in_island_list
    

def merge_duplicate(merged_streams_in_island_list):
    """
    Merge lists that have at least one common element into one list.
    
    :param merged_streams_in_island_list: list of lists to test and merge
    :type merged_streams_in_island_list: list of lists
    
    :return: list of merged lists
    :rtype: list of lists
    """
    # List of lists to merge
    list_islands = merged_streams_in_island_list.copy()
    
    # For each pair of lists
    for list1 in list_islands:
        for list2 in list_islands:
            if list1 != list2:
                # Test if there is a common element
                to_merge = False
                for elem in list2:
                    if elem in list1:
                        to_merge = True
                # If so, merge
                if to_merge:
                    for elem in list2:
                        if elem not in list1:
                            list1.append(elem)
                    list_islands.pop(list_islands.index(list2))
    
    # List or merged lists               
    return list_islands
                        
    
    
    
    
# ________ ORDERS ____________________________________________________________


def compute_stroke(dict_strokes, edge, list_incoming_edges):
    """
    Compute the stroke of the input edge. 
    Return the ID of the stroke.
    
    :param dict_strokes: dictionary of the strokes already built 
                    {key= stroke ID: values= list of the edges of the stroke}
    :type dict_strokes: dictionary {integer:list of Edge objects}
    :param edge: edge of which the stroke is computed
    :type edge: Edge object
    :param list_incoming_edges: list of the incoming edges of the input edge
    :type list_incoming_edges: list of Edge objects
    
    :return: ID of the stroke of the input edge
    :rtype: integer
    """
    
    #Creation of dictionaries containing for the first one the length of the 
    #several strokes entering the edge under study, and for the second one the angles
    #between the edges entering the edge under study and this particular edge
    dict_length = {}
    dict_angle = {}
    
    #looking over the different incoming edges
    for incoming_edge in list_incoming_edges :
        
        #collecting information from these incoming edges
        id_incoming_edge = incoming_edge.id_stroke
        stroke = dict_strokes[id_incoming_edge]
        
        incoming_edge_name = incoming_edge.name
        
        #first condition : the incoming edge and the edge that has been entered 
        #have the same existing name
        if incoming_edge_name == edge.name and edge.name != None:
            
            #returning the id of the stroke that corresponds to the edge under study
            return id_incoming_edge
        
        #calculating the length of the strokes entering the edge
        length = compute_length(stroke)
        
        #and putting them in the dictionary dict_length
        dict_length[length] = id_incoming_edge
        
    #collecting the maximum length from the strokes entering the edge
    list_length = list(dict_length.keys())
    max_length = max(list_length)
    
    three_times_longer = True
    
    #second condition : if the length of the longest stroke is three times longer than
    #the other strokes entering the edge
    #if the boolean three_times_longer becomes False, one stroke is less than three
    #times longer than the longest stroke
    for length in list_length:
        if length != max_length:
            if max_length/length < 3:
                three_times_longer = False
    
    #if the longest stoke is three times longer than the others stroke, its id
    #is returned
    if three_times_longer:
        return dict_length[max_length]
    
    
    #calculationg for each incoming edge the angle with the edge under study
    for incoming_edge in list_incoming_edges:
        
        #collecting the id from the stroke corresponding to the incoming edge
        id_incoming_edge = incoming_edge.id_stroke
        
        #calculation of the angle
        #angle_incoming_edge = compute_angle(incoming_edge, edge)
        angle_incoming_edge = compute_angle(incoming_edge, edge)
        
        #modulo
        if angle_incoming_edge < 0:
            angle_incoming_edge += 2*np.pi
        if angle_incoming_edge >= 2*np.pi:
            angle_incoming_edge -= 2*np.pi
            
       #adding it to the dictionary
        dict_angle[angle_incoming_edge] = id_incoming_edge
    
    #list of the angles
    list_angle = list(dict_angle.keys())
    #find the flattest angle
    list_differences_to_pi = [abs(angle - np.pi) for angle in list_angle]
    smallest_difference = min(list_differences_to_pi)
    index_smallest = list_differences_to_pi.index(smallest_difference)
    flattest_angle = list_angle[index_smallest]
    
    #id of the stroke of the edge forming the flattest angle
    return dict_angle[flattest_angle]
        

def compute_length(stroke):
    """
    Return the total length of a stroke (sum of the lengths of the geometries
    of the edges that make up the stroke).
    
    :param stroke: list of edges
    :type stroke: list of Edge objects
    """
    # List of the geometries that make up the stroke
    list_geom = [edge.geom for edge in stroke]
    
    # Total length
    length = 0
    for geom in list_geom:
        length += geom.length()
        
    return length
    

def compute_angle(edge_in, edge_out):
    """
    Compute the angle formed by edge_in and edge_out, edge_in entering the node
    edge_out exits.
    
    :param edge_in: one side of the angle
    :type edge_in: Edge object
    :param edge_out: one side of the angle
    :type edge_out: Edge object
    """
    # First edge forming the angle
    node_start_in = edge_in.node_end.geom
    node_end_in = edge_in.geom.asPolyline()[-2]
    # Second edge
    node_start_out = edge_out.node_start.geom
    node_end_out = edge_out.geom.asPolyline()[1]

    # Azimuth of each edge
    azimuth_in = azimuth_angle(node_start_in, node_end_in)
    azimuth_out = azimuth_angle(node_start_out, node_end_out)

    # The angle formed by the edges is the difference of the azimuths
    angle = azimuth_out - azimuth_in
    
    return angle

def azimuth_angle(node_start, node_end):
    """
    Compute the azimuth of a line defined by its start node and its end node.
    
    :param node_start: origin of the line
    :type node_start: QgsPointXY object
    :param node_end: end of the line
    :type node_start: QgsPointXY object
    """
    delta_x = node_end.x() - node_start.x()
    delta_y = node_end.y() - node_start.y()
    distance = np.sqrt(delta_x**2 + delta_y**2)
    
    azimuth = 2*np.arctan2(delta_x, delta_y + distance)
    
    return azimuth


def compute_stroke_of_island(dict_strokes, island, incoming_edges_island):
    """
    Compute the stroke of the island. 
    Return the ID of the stroke.
    
    :param dict_strokes: dictionary of the strokes already built 
                    {key= stroke ID: values= list of the edges of the stroke}
    :type dict_strokes: dictionary {integer:list of Edge objects}
    :param island: island of which the stroke is computed
    :type island: Island object
    :param incoming_edges_island: list of the incoming edges of the island
    :type incoming_edges_island: list of Edge objects
    
    :return: ID of the stroke of the input edge
    :rtype: integer
    """
    # First condition
    # If the edge splits into two streams when entering the island, and there 
    # is only one edge that splits, its stroke is also the stroke of the island
    edges_split = []
    for incoming_edge_island in incoming_edges_island:
        # Edges entering the end node of the current edge
        node_end_incoming_edges = incoming_edge_island.node_end.edges_in
        # Amongst them, edges that belong to the island
        node_end_incoming_edges_island = []
        for node_end_incoming_edge in node_end_incoming_edges:
            if node_end_incoming_edge in island.edges:
                node_end_incoming_edges_island.append(node_end_incoming_edge)
        
        # If there is no edge that belongs to the island and that enters the end 
        # node of the current edge, then the edge splits into two streams
        if len(node_end_incoming_edges_island) == 0:
            edges_split.append(incoming_edge_island)
            
    # There is a unique edge that splits in two        
    if len(edges_split) == 1:
        # ID of the stroke of the island
        return edges_split[0].id_stroke
        
    
    # Second condition
    # The stroke of the island is the longest upstream stroke
    dict_length = {}
    for incoming_edge_island in incoming_edges_island:
        # ID of the stroke
        incoming_stroke_id = incoming_edge_island.id_stroke
        # Edges of the stroke
        incoming_stroke = dict_strokes[incoming_stroke_id]
        # Length of the stroke
        length_stroke = compute_length(incoming_stroke)
        # Length indexed by ID
        dict_length[length_stroke] = incoming_stroke_id

    # List of all upstream lengths
    list_length = list(dict_length.keys())
    # Maximum length
    max_length = max(list_length)
    # ID of the stroke of the island is ID of the stroke of maximum length
    return dict_length[max_length]


def compute_stroke_outgoing_island(dict_strokes, dict_forks, island_id_stroke, outgoing_edges_island):
    """
    Compute the stroke of the outgoing edges of the island. 
    Set the attribute id_stroke of the edges.
    
    :param dict_strokes: dictionary of the strokes already built 
                    {key= stroke ID: values= list of the edges of the stroke}
    :type dict_strokes: dictionary {integer:list of Edge objects}
    :param dict_forks: dictionary of the strokes already built that split
                    {key= upstream stroke ID: values= list of stroke IDs after the stroke}
    :type dict_forks: dictionary {integer:list of Edge objects}
    :param island_id_stroke: stroke ID of the island
    :type island_id_stroke: integer 
    :param outgoing_edges_island: list of the outgoing edges of the island
    :type outgoing_edges_island: list of Edge objects
    """
    # If there is a unique outgoing edge, its stroke is 
    # the stroke of the island
    if len(outgoing_edges_island) == 1:
        outgoing_edges_island[0].id_stroke = island_id_stroke
        dict_strokes[island_id_stroke].append(outgoing_edges_island[0])                     
    
    # Else, the island forms a fork and there are two arms to the stroke
    else:
        # Edges of the stroke of the island
        upstream_edges_stroke = dict_strokes[island_id_stroke]
        
        # One arm continues the stroke of the island
        outgoing_edges_island[0].id_stroke = island_id_stroke
        dict_strokes[island_id_stroke].append(outgoing_edges_island[0]) 
                             
        # The other receive new IDs and form new arms
        existing_ids = list(dict_strokes.keys())
        id_new_stroke = max(existing_ids) + 1
        # Link arms
        dict_forks[island_id_stroke] = []               
        # For each other arm
        for i in range(1, len(outgoing_edges_island)):
            # New ID
            outgoing_edges_island[i].id_stroke = id_new_stroke
            # New arm : upstream edges and downstream edge
            dict_strokes[id_new_stroke] = upstream_edges_stroke + [outgoing_edges_island[i]]
            # Link arms
            dict_forks[island_id_stroke].append(id_new_stroke)
            # Increment ID for next arm
            id_new_stroke += 1
            

def is_upstream_processed(incoming_edges, edges_to_process):
    """
    Check if all incoming edges have been processed. 
    Return True if processed.
    
    :param incoming_edges: list of edges to check (incoming edges of a current edge)
    :type incoming_edges: list of Edge objects
    :param edges_to_process: list of edges left to process
    :type edges_to_process: list of Edge objects
    """
    upstream_processed = True 
    
    for incoming_edge in incoming_edges :
        # Check if each incoming edge is still in the list of edges to process
        if incoming_edge in edges_to_process:
            # If the edge is in the list of edges to process, it has not been 
            # processed yet
            upstream_processed = False
            
    return upstream_processed


# Strahler, Shreve, Horton, strokes
def process_network(edges, sources_edges, orders_to_compute, edges_to_process, dict_strokes, dict_strokes_in_island, dict_forks):
    """
    Compute stream orders: Strahler, Shreve and / or Horton, according to the
    selection of the user.
    The computed orders are attributes of the Edge objects.
    
    :param edges: list of all the edges making up the river network
    :type edges: list of Edge objects
    :param sources_edges: list of all source edges of the river network
    :type sources_edges: list of Edge objects
    :param orders_to_compute: list of the orders to compute (selected by the user)
    :type orders_to_compute: list of strings
    :param edges_to_process: list of the edges left to process
    :type edges_to_process: list of Edge objects
    :param dict_strokes: dictionary of the strokes already built (except edges of islands)
                    {key= stroke ID: values= list of the edges of the stroke}
    :type dict_strokes: dictionary {integer:list of Edge objects}
    :param dict_strokes_in_island: dictionary of the strokes already built of
                                   edges in islands
                    {key= stroke ID: values= list of the edges of the stroke}
    :type dict_strokes_in_island: dictionary {integer:list of Edge objects}
    :param dict_forks: dictionary of the strokes already built that split
                    {key= upstream stroke ID: values= list of stroke IDs after the stroke}
    :type dict_forks: dictionary {integer:list of Edge objects}
    """
                        
    # ID of the stroke (initial computation)
    id_stroke = 0
    
    # Initialize with sources
    for source in sources_edges:
        # Source not already processed
        if source in edges_to_process:
            # Orders 
            if "strahler" in orders_to_compute or "horton" in orders_to_compute:
                source.stream_orders["strahler"] = 1
            if "shreve" in orders_to_compute:
                source.stream_orders["shreve"] = 1
                                    
            # Stroke      
            if "horton" in orders_to_compute :
                # The stroke of a source in an island will be the stroke of the 
                # island computed later
                if source.island == None :
                    dict_strokes[id_stroke] = [source]
                    source.id_stroke = id_stroke
                    id_stroke += 1
            
            # Edge processed
            edges_to_process.pop(edges_to_process.index(source))
    
    edges_to_process_start_loop = []
    # While there still are edges to process
    while len(edges_to_process) > 0 and edges_to_process_start_loop != edges_to_process:
    
        edges_to_process_start_loop = edges_to_process.copy()
        
        # For each edge left to process
        for edge in edges_to_process:

            # NOT IN ISLAND 
            
            # Check if edge is not in an island
            if edge.island == None:
            
                # Check if incoming edges have been processed
                list_incoming_edges = edge.node_start.edges_in
                upstream_processed = is_upstream_processed(list_incoming_edges, edges_to_process)
                
                # If upstream edges already processed, compute orders
                if upstream_processed :
                    
                    # Orders
                    # Strahler (necessary for Horton order)
                    if "strahler" in orders_to_compute or "horton" in orders_to_compute:
                        upstream_orders = [incoming_edge.stream_orders["strahler"] for incoming_edge in list_incoming_edges]
                        max_strahler = max(upstream_orders)
                        count_max = upstream_orders.count(max_strahler)
                        
                        if count_max > 1:
                            edge.stream_orders["strahler"] = max_strahler + 1
                        else :
                            edge.stream_orders["strahler"] = max_strahler
                    
                    if "shreve" in orders_to_compute:
                        upstream_orders = [incoming_edge.stream_orders["shreve"] for incoming_edge in list_incoming_edges]
                        edge.stream_orders["shreve"] = sum(upstream_orders)
                        
                    if "horton" in orders_to_compute:
                        # Strokes (only useful for Horton order calculation)
                        # Find the stroke
                        id_stroke = compute_stroke(dict_strokes, edge, list_incoming_edges)
                        # Update the stroke
                        dict_strokes[id_stroke].append(edge)
                        edge.id_stroke = id_stroke
                    
                    edges_to_process.pop(edges_to_process.index(edge))
                    
                # If upstream edges not processed yet, pass    
                else :
                    continue
                
                
            # ISLAND  
            
            # If edge is in an island
            else:
                
                # Outgoing edges of the island
                outgoing_edges_island = edge.island.edges_out
                    
                # Incoming edges of the island
                incoming_edges_island = edge.island.edges_in
                
                # If upstream edges of the island already processed, compute orders
                upstream_island_processed = is_upstream_processed(incoming_edges_island, edges_to_process)                    

                if upstream_island_processed:
                    
                    # Stroke ID of the island
                    if "horton" in orders_to_compute:
                        edge.island.id_stroke = compute_stroke_of_island(dict_strokes, edge.island, incoming_edges_island)
                        # Sources in island
                        for source_edge in sources_edges:
                            if source_edge.island == edge.island:
                                # The stroke of the source is the stroke 
                                # of the island (sources out of islands 
                                # define their own stroke)
                                id_stroke_island = edge.island.id_stroke
                                source_edge.id_stroke = id_stroke_island
                                if id_stroke_island not in list(dict_strokes_in_island.keys()):                                
                                    # Initialise dictionary
                                    dict_strokes_in_island[id_stroke_island] = [source_edge]                              
                                else:
                                    dict_strokes_in_island[id_stroke_island].append(source_edge) 
                                
                    # INSIDE THE ISLAND
                    # Edges to process inside the island
                    edge_island_to_process = []
                    for edge_island in edge.island.edges:
                        for edge_island_in_list_to_process in edges_to_process:
                            if edge_island_in_list_to_process.id_edge == edge_island.id_edge:
                                edge_island_to_process.append(edge_island)

                    
                    edge_island_to_process_start_loop = []
                    while len(edge_island_to_process) > 0 and edge_island_to_process_start_loop != edge_island_to_process:
                        
                        edge_island_to_process_start_loop = edge_island_to_process.copy()
                        
                        # Edges that make up the island
                        for edge_island in edge_island_to_process:

                            # Incoming edges of the edge of the island (may be in island too)
                            incoming_edges = edge_island.node_start.edges_in
                                                
                            # If upstream edges of the edge already processed, compute orders
                            upstream_processed = is_upstream_processed(incoming_edges, edge_island_to_process)
                            if upstream_processed:
                                # Strahler
                                # Inside the island, just take the max value of the incoming streams
                                if "strahler" in orders_to_compute or "horton" in orders_to_compute:
                                    upstream_orders = [incoming_edge.stream_orders["strahler"] for incoming_edge in incoming_edges]
                                    edge_island.stream_orders["strahler"] = max(upstream_orders)
                                # Shreve                  
                                # Inside the island, just take the max value of the incoming streams
                                if "shreve" in orders_to_compute:
                                    upstream_orders = [incoming_edge.stream_orders["shreve"] for incoming_edge in incoming_edges]                                     
                                    edge_island.stream_orders["shreve"]  = max(upstream_orders)
                                # Horton
                                if "horton" in orders_to_compute:
                                    # Find the stroke
                                    id_stroke = edge.island.id_stroke                                        
                                    # Update the stroke
                                    if id_stroke not in list(dict_strokes_in_island.keys()):                                
                                        # Initialise dictionary
                                        dict_strokes_in_island[id_stroke] = [edge_island]                              
                                    else:
                                        dict_strokes_in_island[id_stroke].append(edge_island)                                            
                                    edge_island.id_stroke = id_stroke
                                    
                                # List of all edges left to process (outer while loop)
                                edges_to_process.pop(edges_to_process.index(edge_island))
                                # List of edges of the island left to process (inner while loop)
                                edge_island_to_process.pop(edge_island_to_process.index(edge_island))
                            
                            # If upstream edges of the edge in the island not processed yet, pass
                            else:
                                continue
    
                    # OUTSIDE THE ISLAND                    
                    
                    # The strokes computation is applied to all outgoing strokes at once to make sure
                    # the stroke computation of an outgoing edge is not independent of the strokes of 
                    # the other outgoing edges (unicity of strokes)
                    # The objects and dictionaries are not local variables when in functions, they are
                    # altered directly in the function
                    if "horton" in orders_to_compute:
                        compute_stroke_outgoing_island(dict_strokes, dict_forks, edge.island.id_stroke, outgoing_edges_island)
                    
                    # Regular orders computation for the outgoing edges of the island
                    # using the incoming edges of the island (the inner island edges orders
                    # computation is independent and has been processed above)
                    for outgoing_edge_island in outgoing_edges_island:
                        if outgoing_edge_island in edges_to_process:
                            if "strahler" in orders_to_compute or "horton" in orders_to_compute:
                                upstream_orders = [incoming_edge_island.stream_orders["strahler"] for incoming_edge_island in incoming_edges_island]
                                max_strahler = max(upstream_orders)
                                count_max = upstream_orders.count(max_strahler)
                                
                                if count_max > 1:
                                    outgoing_edge_island.stream_orders["strahler"] = max_strahler + 1
                                else :
                                    outgoing_edge_island.stream_orders["strahler"] = max_strahler
                                                                                                                          
                            if "shreve" in orders_to_compute:
                                upstream_orders = [incoming_edge_island.stream_orders["shreve"] for incoming_edge_island in incoming_edges_island]
                                outgoing_edge_island.stream_orders["shreve"] = sum(upstream_orders)
    
                            edges_to_process.pop(edges_to_process.index(outgoing_edge_island))
                    
                # If upstream edges of the island not processed yet, pass    
                else:                                                       
                    continue
    
    # Horton order computation needs Strahler orders to be entirely computed
    if "horton" in orders_to_compute:
        # Merge the strokes back together (main strokes, edges in islands, forks)
        dict_merged_strokes = merge_strokes(dict_strokes, dict_strokes_in_island, dict_forks)
        compute_horton(dict_merged_strokes)
        
        
    # LOOPS
    # If there are edges that failed to be processed, they are probably in a 
    # loop
    # Detect loop, process the edges in loop if they exist
    nb_edges_to_process = len(edges_to_process)
    if edges_to_process != []:
        for left_edge in edges_to_process:
            edges_in_loop = is_in_loop(left_edge, edges_to_process)
            if edges_in_loop != []:
                loop_processed = process_loop(edges_in_loop, orders_to_compute, edges_to_process, dict_strokes_in_island)          
                if loop_processed:
                    break
        # execute function process_network (to process downstream edges) if 
        # there was a loop
        if nb_edges_to_process != len(edges_to_process):
            process_network(edges, sources_edges, orders_to_compute, edges_to_process, dict_strokes, dict_strokes_in_island, dict_forks)
 
    
def is_in_loop(left_edge, edges_to_process):
    """
    Test if an edge is connected to a loop in the network.
    Return the edges of the loop in a list (return an empty list if no loop was 
    detected).
    
    :param left_edge: edge to test (could not be processed by process_network)
    :type left_edge: Edge object
    :param edges_to_process: list of edges left to process
    :type edges_to_process: list of Edge objects
    
    :return: list of the edges of the loop (or empty list if no loop)
    :rtype: list of Edge objects
    """
    # Incoming edge (initialisation)
    previous = left_edge.copy_edge()
    # Edges of the loop
    edges_in_loop = []
    # There is a loop (boolean)
    loop_exists = False
    # Incoming edges 
    list_previous = []
    
    # While the edge has incoming edges
    while previous != None :
        # Get the incoming edges
        incoming_edges = previous.node_start.edges_in
        previous = None
        # Get an incoming edge that could not be processed 
        # (condition to be in a loop)
        for in_edge in incoming_edges:
            if in_edge in edges_to_process:
                previous = in_edge

        # If the incoming edge has already been read, it is in a loop
        if previous in list_previous:
            # If the incoming_edge is read for the third time, it closes the loop
            if previous in edges_in_loop:
                loop_exists = True 
                break 
            else :
                edges_in_loop.append(previous)
        else :
            list_previous.append(previous)
      
    # If there is no loop, return empty list
    if not loop_exists :
        edges_in_loop = []
    # List of edges of the loop
    return edges_in_loop
  
    
def process_loop(edges_in_loop, orders_to_compute, edges_to_process, dict_strokes_in_island):
    """
    Process edges of a loop.
    Their order and their stroke take the same value. The orders are computed 
    with orders of the incoming edges of the edges of the loop that are known 
    (regular Strahler or Shreve, only on already processed incoming edges).
    The stroke is the stroke of the island (any loop is an island).
    
    :param edges_in_loop: list of the edges of the loop
    :type edges_in_loop: list of Edge objects
    :param orders_to_compute: list of the orders to compute (selected by the user)
    :type orders_to_compute: list of strings
    :param edges_to_process: list of edges left to process
    :type edges_to_process: list of Edge objects
    :param dict_strokes_in_island: dictionary of the strokes already built of
                                   edges in islands
                    {key= stroke ID: values= list of the edges of the stroke}
    :type dict_strokes_in_island: dictionary {integer:list of Edge objects}
    
    :return: indicate if the loop was successfully processed 
            (can be processed only if incoming edges were already processed)
    :rtype: boolean
    """
    # Orders of incoming edges of the loop (that are not null)
    list_incoming_strahler = []
    list_incoming_shreve = []
    # For each edge of the loop, get the orders of its incoming edges that 
    # are already processed (out of the loop)
    for edge_loop in edges_in_loop:
        incoming_edges = edge_loop.node_start.edges_in
        if "strahler" in orders_to_compute or "horton" in orders_to_compute:
            for edge_in in incoming_edges:
                # If the order was computed
                if "strahler" in edge_in.stream_orders.keys():
                    # Get the order
                    list_incoming_strahler.append(edge_in.stream_orders["strahler"])
                    
        if "shreve" in orders_to_compute:
            for edge_in in incoming_edges:
                if "shreve" in edge_in.stream_orders.keys():
                    list_incoming_shreve.append(edge_in.stream_orders["shreve"])
      
    # If there are incoming edges which were already processed, 
    # process the loop edges
    if list_incoming_strahler != [] or list_incoming_shreve != []:
        processed = True
    else : 
        processed = False
    
    if processed :
        # For each edge of the loop
        for edge_loop in edges_in_loop:
            # Strahler is the strahler order on all processed incoming edges
            if "strahler" in orders_to_compute or "horton" in orders_to_compute:
                max_strahler = max(list_incoming_strahler)
                nb_max = list_incoming_strahler.count(max_strahler)
                if nb_max > 1:
                    edge_loop.stream_orders["strahler"] = max_strahler + 1
                else:
                    edge_loop.stream_orders["strahler"] = max_strahler
         
            # Shreve is the shreve order on all processed incoming edges
            if "shreve" in orders_to_compute:
                edge_loop.stream_orders["shreve"] = sum(list_incoming_shreve)
    
            # The stroke is the stroke of the island the loop delimits 
            # or is part of
            if "horton" in orders_to_compute:
                # Find the stroke
                id_stroke = edge_loop.island.id_stroke                                        
                # Update the stroke
                if id_stroke not in list(dict_strokes_in_island.keys()):                                
                    # Initialise dictionary
                    dict_strokes_in_island[id_stroke] = [edge_loop]                              
                else:
                    dict_strokes_in_island[id_stroke].append(edge_loop)                                            
                edge_loop.id_stroke = id_stroke

        # The edge of the loop is processed        
        edges_to_process.pop(edges_to_process.index(edge_loop))
        
    # The loop was processed
    return processed
                
            


def merge_strokes(dict_strokes, dict_strokes_in_island, dict_forks):
    """
    Merge the strokes of the islands and of the forks with the main stroke.
    
    :param dict_strokes: dictionary of the strokes already built (except edges of islands)
                    {key= stroke ID: values= list of the edges of the stroke}
    :type dict_strokes: dictionary {integer:list of Edge objects}
    :param dict_strokes_in_island: dictionary of the strokes already built of
                                   edges in islands
                    {key= stroke ID: values= list of the edges of the stroke}
    :type dict_strokes_in_island: dictionary {integer:list of Edge objects}
    :param dict_forks: dictionary of the strokes already built that split
                    {key= upstream stroke ID: values= list of stroke IDs after the stroke}
    :type dict_forks: dictionary {integer:list of Edge objects}
    """
    # Dictionary of the strokes after merging
    dict_merged_strokes = {}
    # IDs of the strokes that have a fork
    arm_keys = list(dict_forks.keys())
    # IDs of the strokes that are arms of a fork
    arm_values = []
    
    # Get all the IDs of strokes that are arms of a fork
    for arm_id in arm_keys:
        for value in dict_forks[arm_id]:
            arm_values.append(value)
            
    # For each stroke
    for stroke_id in dict_strokes.keys():
        edges_merged_stroke = []
   
        # If the stroke is not an arm of a fork    
        if stroke_id not in arm_values:
            # Get its edges
            edges_merged_stroke = dict_strokes[stroke_id].copy()
            
            # If the stroke has islands
            if stroke_id in dict_strokes_in_island.keys():
                # Get the strokes of the islands
                edges_merged_stroke += dict_strokes_in_island[stroke_id].copy()              
                
            # If the stroke is a fork
            if stroke_id in arm_keys:
                edges_arms = []
                # Get the strokes of its other arms
                for arm_ids in dict_forks[stroke_id]:
                    edges_arms += dict_strokes[arm_ids].copy()
                edges_merged_stroke += edges_arms.copy()
            
            # Add the merged strokes to the dictionary
            dict_merged_strokes[stroke_id] = edges_merged_stroke
    
    # Dictionary of the merged strokes           
    return dict_merged_strokes


def compute_horton(dict_strokes):
    """
    Compute the Horton order using the input strokes.
    The computed orders are attributes of the Edge objects.
    
    :param dict_strokes: dictionary of all the strokes built, except edges in 
                         islands
                    {key= stroke ID: values= list of the edges of the stroke}
    :type dict_strokes: dictionary {integer:list of Edge objects}
    """
    # For each stroke
    for stroke_id in dict_strokes.keys():
        # List of the edges that make up the stroke
        edges_stroke = dict_strokes[stroke_id].copy()
        # List of the Strahler orders of the edges of the stroke
        strahler_orders = [edge.stream_orders["strahler"] for edge in edges_stroke]
        # Maximum of the Strahler orders of the stroke
        max_strahler = max(strahler_orders)
        # Each edge of the stroke takes this maximum as its Horton order
        for edge in edges_stroke:                
            edge.stream_orders["horton"] = max_strahler

# ___________ WRITE IN TABLE _________________________________________________ 

def update_table(input_layer, orders_to_compute, field_reverse, edges):
    """
    Updates the table of the layer by adding a column named like the name of
    the order and filling it with the orders calculated before. 
    Updates the table with a field "reversed" if the user selected the option 
    (True if the edge has been reversed for the computation of the orders).
    
    :param input_layer: layer of the river network
    :type input_layer: QgsVectorLayer object
    :param orders_to_compute: list of the orders to compute (selected by the user)
    :type orders_to_compute: list of strings
    :param field_reverse: field reversed is added to the table (selected by the user))
    :type field_reverse: boolean
    :param edges: list of all the edges making up the river network
    :type edges: list of Edge objects
    """
    # Orders fields
    for order in orders_to_compute:
        
        # Object giving access to the layer data
        input_layer_dp = input_layer.dataProvider()
        
        # Allow editing of the input layer
        input_layer.startEditing()
        # Add a field named after the order to the input layer
        input_layer_dp.addAttributes( [ QgsField(order, QVariant.Int) ] )
        input_layer.updateFields()
        
        # Index of the created field
        idx = input_layer_dp.fieldNameIndex( order )
        
        # Get the list of features (lines of the table)
        featuresList = iterator_to_list(input_layer_dp.getFeatures())
        
        # For each edge
        for edge in edges:

            if order in edge.stream_orders.keys():
                # Value of the order of the edge
                order_edge = edge.stream_orders[order]
            else : 
                order_edge = None
            
            # For each feature (each line)
            for feature in featuresList:
                # If the line corresponds to the edge
                if feature.id() == edge.id_edge:
                    # Set the value of the order in the field
                    input_layer.changeAttributeValue(feature.id(), idx, order_edge)
         
        # Commit changes
        input_layer.commitChanges()

        if order == "horton":
            
            # Same process to add the field "id_stroke" and fill it with the 
            # attribute values of the edges
            
            # Add a field
            field_name = "id_stroke"
            input_layer_dp = input_layer.dataProvider()
            input_layer.startEditing()
            input_layer_dp.addAttributes( [ QgsField(field_name, QVariant.Int) ] )
            input_layer.updateFields()
            # Index of the field
            idx = input_layer_dp.fieldNameIndex(field_name)
            
            # Get the features of the table
            featuresList = iterator_to_list(input_layer_dp.getFeatures())
            
            # Fill the field
            for edge in edges:
                field_value = edge.id_stroke
                for feature in featuresList:
                    if feature.id() == edge.id_edge:
                        input_layer.changeAttributeValue(feature.id(), idx, field_value)
             
            # Commit changes
            input_layer.commitChanges()


    # Reversed field
    # If the option is selected by the user
    if field_reverse:
        # Same process to add the field "reversed" and fill it with the 
        # attribute values of the edges
        
        # Add a field
        field_name = "reversed"
        input_layer_dp = input_layer.dataProvider()
        input_layer.startEditing()
        input_layer_dp.addAttributes( [ QgsField(field_name, QVariant.Int) ] )
        input_layer.updateFields()
        # Index of the field
        idx = input_layer_dp.fieldNameIndex(field_name)
        
        # Get the features of the table
        featuresList = iterator_to_list(input_layer_dp.getFeatures())
        
        # Fill the field
        for edge in edges:
            field_value = edge.reversed
            for feature in featuresList:
                if feature.id() == edge.id_edge:
                    input_layer.changeAttributeValue(feature.id(), idx, field_value)
         
        # Commit changes
        input_layer.commitChanges()


# ________ SAVE OUTPUT _______________________________________________________

def show_field_created_successfully():
    """
    Display a message box that indicates when the input layer has been
    updated.
    """
    msgBox = QMessageBox(
        QMessageBox.Information,
        'Success',
        'Field(s) was (were) created successfully!',
        QMessageBox.Ok)
    msgBox.exec_()

def show_message_no_stream_order_selected():
    """
    Display a message box that indicates when no stream order was checked for
    computation by the user.
    """
    msgBox = QMessageBox(
        QMessageBox.Information,
        'Error',
        'Please select at least one stream order computation.',
        QMessageBox.Ok)
    msgBox.exec_()

def save_output_layer(output, path_to_saving_location):
    """
    Save the output layer
    
    :param output: output layer to be saved
    :output type: QgsVectorLayer
    
    :param path_to_saving_location: the path to the place where the layer has 
                                    to be saved
    :path_to_saving_location type: string
    """
    # Write the output layer
    try:
        QgsVectorFileWriter.writeAsVectorFormat(output, path_to_saving_location, "utf-8", output.crs(), "ESRI Shapefile")
    except BaseException:
        msgBox = QMessageBox(
            QMessageBox.Information,
            'Error',
            'An error has occured during the saving of your output layer. Please check the path to your saving location or save it manually.',
            QMessageBox.Ok)
        msgBox.exec_()