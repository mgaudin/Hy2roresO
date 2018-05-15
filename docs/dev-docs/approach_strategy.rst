Approach & Strategy
================

General strategy
--------------

Hy2roresO is a QGIS plugin working using an iterative algorithm. Indeed, the algorithm goes through the network from the sources to the sinks, which is different than the recursive algorithm from the Strahler Plugin from QGIS.
It also uses several global variables during its process, which will be detailed further in the documentation.

Input data
------------

The plugin handles a layer which must be a network. The network should not contain artificial zones such as irrigation zones, since the results in these zones will be irrelevant.
The layer must also not contain duplicated geometries, since it will create irrelevant orders that will be way higher than the good ones.

The algorithm 
--------------

Classes
~~~~~~~~~~~~

The algorithm sets 3 classes : *Edge*, *Node* and *Island*. All of them have attributes that define them and that are useful for the good process of the algorithm.

.. figure:: ../_static/classes_Hy2roresOv1.0.png
   :align: center
   
   Class diagram of the algorithm
    
Initialisation
~~~~~~~~~~~~

At the beginning of the process, a method initializes each feature of the layer as an edge or a node, with all its attributes.
This implies the creation of several global variables such as 

Changes of direction of streams
~~~~~~~~~~~~

A method was created to change the direction of the streams. It is called if the checkbox in the plugin, that asks the user if he wants to be proposed some streams to reverse, is checked. 

There are two criterias that can detect wrong directions from streams:
 * If there is an incoherence in the altitudes (if the beginning altitude is lower than the end altitude)
 * If there are, for a node with a degree different to 1, only incoming edges or only outgoing edges. If so, the algorithm detects them and will propose to reverse only some of them so as to get a better hierarchisation.

Then the algorithm proposes to the user to change the directions of the streams it has detected. The user can therefore reverse them or not manually or automatically thanks to the plugin during the process.

*Note : Changing the direction of the stream will not change the geometry in itself : it will only create an attribute and a column reversed that will be used throughout the process of the algorithm.*

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