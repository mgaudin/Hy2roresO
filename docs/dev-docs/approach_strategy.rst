Approach & Strategy
================

General strategy
--------------

Hy2roresO is a QGIS plugin developed in Python 3.6 for QGIS 3.0.
The implemented algorithm is iterative. The algorithm goes through the river network starting from the sources and down to the sinks.
The orders computation relies on instances of classes specifically designed for the plugin. They will be detailed further in the documentation.
**This section aims to present the main hypotheses** we were led to make to enable the orders algorithm to work on complex networks that have singular configurations such as islands, when the theoretical algorithms of all three orders expect a network shaped as a binary tree (see the Introduction of the User documentation_ about the Strahler, Shreve and Horton algorithms). However, such networks are not the river structures that exist in reality. The goal of the hypotheses made for the implementation of our algorithm is to adapt the general spirit of each order algorithm defined only for binary trees to the more complex reality.
.. _documentation: ../user-docs/presentation.html

Input data
------------

The data and chosen options the plugin needs as input are the orders to compute and the layer of the river network. The network layer must be a linear vectorial layer. The network should not contain artificial zones such as irrigation zones, since such configurations are not specifically handled by the algorithm and the result may be meaningless. Forks of streams that do not occur in an island (two or more streams exiting an island), immediately at the sources (multiple sources exiting a single node) or at the sinks of the network (deltas) may also introduce mistakes in the strokes computation, that might spread into the downstream network calculation afterwards (see the upstream length criteria for strokes computation below). 
Be aware that the layer must also not contain duplicated geometries. Duplicated geometries are hard to notice since you cannot see them simply by displaying the layer, and they significantly alter the orders computation. Duplicated geometries are processed as two streams connected to the same nodes, but they do not make up an island (islands have a non-zero area). Thus duplicated geometries artificially increase the Strahler and Shreve orders at each node, completely distorting the results.

The algorithm 
--------------

Classes
~~~~~~~~~~~~

Instead of working directly on the features of the layer or using an external library, the plugin implements three classes instantiated using the layer features that make travelling through the network easy (and independent from external parts).
The algorithm sets 3 classes for each geometry type: *Edge* (lines of the networks), *Node* (connecting points) and *Island* (edges delimiting a surface, face of the network). Their attributes register their interconnection in the layer network.

.. figure:: ../_static/classes_Hy2roresOv1.0.png
   :align: center
   
   Class diagram of the algorithm; the methods are not listed here
    
Initialization
~~~~~~~~~~~~

At the beginning of the process, a method initializes each feature of the layer as an edge and its initial and final nodes, with all their attributes.
The objects instantiated are stored in two lists that are passed as arguments to all the other methods.

Correct streams direction
~~~~~~~~~~~~

Methods were implemented to check and correct the streams direction. If the option in the launcher interface is checked, directions are tested.  
The checking method is called if the checkbox in the plugin, that asks the user if he wants to be proposed some streams to reverse, is checked. 

A stream direction is suspected to be incorrect if it meets one of the two following criteria:
 * The altitudes are known (fields name filled by the user in the launcher) and the initial altitude is lower than the final altitude of the edge;
 * A connected node is not a source or a sink (degree larger than 1) and has only incoming edges or only outgoing edges.
 
The suspicious edges are displayed thanks to a dialog box to the user, who can choose for each edge if they want to reverse it or not by knowing the direction of connected streams and the structure of the network. Obviously, amongst all the suspicious edges, only the edges approved by the user will be reversed for the orders computation.

If the edge is reversed, the information is stored as a boolean attribute of the object and a field can be added to the input layer to restore this information to the user (option in the launcher).

*Note: Changing the direction of the stream will not change the geometry of the feature of the input layer. It will only change the attributes of the object instantiated from the layer feature, that only exist within the plugin.*


Orders
~~~~~~~~~~~~

The orders are defined in the user documentation_. They are computed in the algorithm, and a column for each order chosen will be created in the output layer containing these orders.
 .. _documentation: ../user-docs/presentation.html
 
The algorithm also handles cases that have not been treated properly in former plugins, such as the islands. If there is a succession of adjacent island (complex island), these islands are aggregated to form a simple island, so as to generalize the case as if it was a simple island.

Strahler stream order
++++++++++++++++

For each edge is calculated a Strahler order. It follows the rules defined for this order. 
When arriving in an island, the code first checks if every incoming edge in the island has been treated. When so, it calculates the Strahler stream order of the outgoing edge of the island according the orders from these incoming edges. It finally attributes to the edges defining the island an order HOW
IMAGES

Shreve stream order
++++++++++++++++

For each edge is also calculated a Shreve order, it follows the rules defined for this order and the same method as for the attribution of the Strahler stream order.
IMAGES

Horton stream order
++++++++++++++++

For each edge can also be calculated the Horton stream order. To compute it, we need to define the strokes of the network.

Conditions to elaborate the strokes
###################

Each source gets an identifier of stroke. Then, arriving in an intersection (node), the id of the outgoing edge is chosen according to this 4 conditions [TOUYA2007]_ :
 - the name of the outgoing edge exists and is exactly the same as one of its incoming edges
 - the incoming edge that has the highest flow (if it exists in the data). This condition is not handled in the algorithm.
 - one of the incoming stroke is more than 3 times longer than the other incoming strokes
 - the stroke that creates an angle that is the closest to 180 degrees (more continuous)

After defining the strokes, we can attribute for each edges of a stroke the same Horton stream order, which is the maximum of the Strahler order of the edges of the stroke. The main stroke gets therefore the maximum Strahler stream order, and so one until each stroke is treated.

When handling an island, the stroke is calculated according to the conditions of name and length of the incoming strokes. The island is isolated and the outgoing edge is set to be attributed a stroke identifier from one of the incoming edges.
Then, every edge defining the island is given the identifier that was given to the outgoing edge. The island is completely part of the stroke this way, which was one of our suppositions (the island is there seen as a node).

When there is a delta or more than one outgoing edge from an island, the stroke is determined as the same stroke from the incoming edge. 

.. [TOUYA2007] http://recherche.ign.fr/labos/cogit/publiCOGITDetail.php?idpubli=4181&portee=labo&id=1&classement=date&duree=100&nomcomplet=Touya%20Guillaume&annee=2007&principale=

Update of the table
-----------------

The last part of the algorithm concerns the output data. This part creates new columns of attributes to the layer, which are the different orders calculated, a column 'reversed' if it has been chosen and a column with the identifier of the stroke if the Horton stream order has been calculated.
	
If you have chosen to get a new output layer with all the data, then you will get one with the data from the former layer and the new columns. Else the algorithm will update your input layer by adding these new columns.

#TODO: Finally, if there is already a column named like the ones that will be created, the user will be asked if he wants to keep the former column or if he wants to overwrite it.
