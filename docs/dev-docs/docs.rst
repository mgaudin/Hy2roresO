Documentation
=========

.. py:class:: Hydroreso(self, test)
    """
    Docstring for class Foo.

    This text tests for the formatting of docstrings generated from output
    ``sphinx.ext.autodoc``. Which contain reST, but sphinx nests it in the
    ``<dl>``, and ``<dt>`` tags. Also, ``<tt>`` is used for class, method names
    and etc, but those will *always* have the ``.descname`` or
    ``.descclassname`` class.

    Normal ``<tt>`` (like the <tt> I just wrote here) needs to be shown with
    the same style as anything else with ````this type of markup````.

    It's common for programmers to give a code example inside of their
    docstring::

        from test_py_module import Foo

        myclass = Foo()
        myclass.dothismethod('with this argument')
        myclass.flush()

        print(myclass)
    """
    
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

The first step of the method is to compare the altitude of the streams. If the initial altitude of the stream is lower than the final altitude, then the algorithm proposes to the user to change the direction of the stream. 
	
The second step is to propose to the user to reverse streams that may be irrelevant seeing the incoming and outgoing streams from its start and end nodes. The user can then also reverse them.

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

Each source gets an identifier of stroke. Then, arriving in an intersection (node), the id of the outgoing edge is chosen according to this 4 conditions [TOUYA 2007]_ :
 - the name of the outgoing edge exists and is exactly the same as one of its incoming edges
 - the incoming edge that has the highest flow (if it exists in the data). This condition is not handled in the algorithm.
 - one of the incoming stroke is more than 3 times longer than the other incoming strokes
 - the stroke that creates an angle that is the closest to 180 degrees (more continuous)
After defining the strokes, we can attribute for each edges of a stroke the same Horton stream order, which is the maximum of the Strahler order of the edges of the stroke. The main stroke gets therefore the maximum Strahler stream order, and so one until each stroke is treated.

.. [TOUYA2007] http://recherche.ign.fr/labos/cogit/publiCOGITDetail.php?idpubli=4181&portee=labo&id=1&classement=date&duree=100&nomcomplet=Touya%20Guillaume&annee=2007&principale=

Update of the table
-----------------

The last part of the algorithm concerns the output data. This part creates new columns of attributes to the layer, which are the different orders calculated, a column 'reversed' if it has been chosen and a column with the identifier of the stroke if the Horton stream order has been calculated.
	
If you have chosen to get a new output layer with all the data, then you will get one with the data from the former layer and the new columns. Else the algorithm will update your input layer by adding these new columns.

#TODO: Finally, if there is already a column named like the ones that will be created, the user will be asked if he wants to keep the former column or if he wants to overwrite it.


.. py:function:: make_stuff(val1, val2)
    
    Return the added values.
    
    :param val1: First number to add.
    :type val1: int
        
    :param val2: Second number to add.
    :type val2: int
    
    :return: Sum
    :rtype: int


.. py:method:: name(parameters)

.. py:attribute:: name
