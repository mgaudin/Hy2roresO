Documentation
=============


Classes
-------

.. py:class::  Hydroreso(self)

   .. py:method:: run_process(self)
    
        Do the whole stuff

---------------------
 
.. py:class::  Edge(self)

   Class of an Edge of the river network.
   Instantiated with attributes of the features of the layer of the network.
   
   
   .. py:method:: __init__(self, geom, id_edge, node_start, node_end)
       
       Constructor of the class
       
       :param geom: Geometry of the feature (line)
       :type geom:
       
       :param id_edge: ID of the edge (same as the ID of the feature; integer)
       :type id_edge:
       
       :param node_start: Start node of the edge
       :type node_start:
       
       :param node_end: End node of the edge
       :type node_end:


   .. py:method:: copy_edge(self)

       Copy an ``Edge`` object.
       Create an ``Edge`` object that has the same attributes.

       :return: Copy of the edge
       :rtype: Edge object


---------------------


.. py:class::  Node(self)

    Class of a ``Node`` of the river network.
    Instantiated with attributes of the features of the layer of the network.

.. py:method::  __init__(self, geom, id_node)

       Constructor of the class
       
       :param geom: Geometry of the feature (point)
       :type geom:
       
       :param id_node: ID of the node (ID of one of its connected edges and number 1 or 2 concatenated)
       :type id_node:
       
        
.. py:method:: copy_node(self)

    Copy a ``Node`` object.
    Create a Node object that has the same attributes.

    :return: Copy of the node
    :rtype: Node object


---------------------


.. py:class::  Island(self)

    Class of an ``Island`` of the river network.
    
    Instantiated with the edges of the island.

   .. py:method::  __init__(self, island_edges)

       Constructor of the class
      
       :param island_edges: Edges that make up the island (Edge objects)
       :island_edges type:


   .. py:method::  copy_island(self)

       Copy an ``Island`` object.
       
       Create an ``Island`` object that has the same attributes.

       :return: Copy of the island
       :rtype: Island object


   .. py:method::  compute_edges_in_out(self)

       Compute the incoming and outgoing edges of the island.
       
       Set attributes edges_in and edges_out from the edges of the island and
       their connections to the network.

    
   .. py:method::  compute_edges_in(self)

       Compute the incoming edges of the island.

       Set attribute edges_in from the edges of the island and their 
       connections to the network.


   .. py:method::  compute_edges_out(self)

       Compute the outgoing edges of the island.
       
       Set attribute edges_out from the edges of the island and their 
       connections to the network.


-----------------------------


Instanciations of the classes
-----------------------------

.. py:function:: create_edges_nodes(features, name_column, alt_init_column, alt_final_column)

    Instantiate all the ``Edge`` and ``Node`` objects that make up the river network.
    
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


.. py:function:: set_edges_connected_nodes(nodes, edges)

    Fill the lists of incoming and outgoing edges of the input nodes 
    (lists are attributes of Node objects).
    
    The connection between nodes and edges is given by the start node and 
    end node of each edge.
    
    :param nodes: list of all the nodes making up the river network
    :type nodes: list of Node objects
    
    :param edges: list of all the edges making up the river network
    :type edges: list of Edge objects

 
.. py:function:: create_islands(streams_in_islands)

    Instanciation of ``Island`` objects from the list of the edges that make up the
    island.
    
    The instantiated objects are stored as attributes of the edges that belong 
    to the island.
    
    :param streams_in_islands: edges that belong to the island
    :type streams_in_islands: list of lists of Edge objects


            
Correct edges directions
------------------------


.. py:function:: test_direction(edges, nodes)

    Test the direction of edges and return the list of abnormal edges
    (probable wrong direction).
    
    Uses altitudes if known or studies links in graph if altitude is unknown.
    
    :param edges: list of all the edges making up the river network
    :type edges: list of Edge objects
    
    :param nodes: list of all the nodes making up the river network
    :type nodes: list of Node objects
    
    :return: list of abnormal edges
    :rtype: list of Edge objects

    
.. py:function:: is_node_abnormal(node)

    Test if a node is abnormal, ie if all its connected edges are in the same
    direction (all incoming or all outgoing edges) and the node is not a source
    nor a sink (it has more than one incoming or outgoing edge). A node that is 
    not a source nor a sink should indeed have at least one incoming edge and 
    one outgoing edge (unless it is a multiple source or sink).
    
    Returns True if the node is regarded as abnormal.
    
    :param node: node to test
    :type node: Node object


.. py:function:: next_node_of_edge(node, edge)

    Return the node of the edge that is not the input node.
    
    :param node: current node
    :type node: Node object
    :param edge: current edge
    :type edge: Edge object
    
    :return: next node of the edge
    :rtype: Node object
    
    
.. py:function:: reverse(edge)

    Reverse an Edge object.
    The method swaps the nodes of the edge, updates the incoming and outgoing
    edges lists of the nodes, reverses the geometry of the edge and updates
    the attribute edge.reverse to True.
    Only the object is altered, the input layer remains unchanged.
    
    :param edge: edge to reverse
    :type edge: Edge object

    
.. py:function:: reverse_all_edges(edges_to_reverse)

    Reverse edges of the input list (call reverse(edge) method).
    
    :param edges_to_reverse: list of edges to reverse
    :type edges_to_reverse: list of Edge objects
    
    
.. py:function:: edges_to_features(list_edges, input_layer)

    Transform a list of Edges objects into a list of the corresponding features
    of the layer.
    
    :param list_edges: list of the edges corresponding to the desired features
    :type list_edges: list of Edge objects
    
    :param input_layer: layer of the features (and the corresponding edges)
    :type input_layer: QgsVectorLayer object
    
    :return: list of features
    :rtype: list of QgsFeatures objects

        
.. py:function:: features_to_edges(list_features, edges)

    Transform a list of QgsFeatures objects into a list of the corresponding 
    Edge objects of the layer.
    
    :param list_features: list of the features corresponding to the desired edges
    :type list_features: list of QgsFeatures objects
    
    :param input_layer: layer of the features (and the corresponding edges)
    :type input_layer: QgsVectorLayer object
    
    :return: list of edges
    :rtype: list of Edge objects


-----------------------------


Sources and sinks
-----------------
               
.. py:function:: find_sources_sinks(edges)

    Find source edges and sink edges of the network.
    
    A source edge is an edge exiting a node that is only connected to this edge.
    A sink edge is an edge entering a node that is only connected to this edge.
    
    :param edges: list of all the edges making up the river network
    :type edges: list of Edge objects
    
    :return: list of source edges, list of sink edges
    :rtype: list of Edge objects, list of Edge objects


-----------------------------


Island detection
----------------


.. py:function:: detect_islands(stream_layer, edges)

    Detect islands in the network.
    Return a list of lists of the edges that make up each island.
    
    :param stream_layer: layer of the river network
    :type stream_layer: QgsVectorLayer object
    
    :param edges: list of all the edges that make up the river network
    :type edges: list of Edge objects
    
    :return: list of lists of edges of the islands
    :rtype: list of lists of Edge objects


.. py:function:: polygonize(input_layer, name="temp")

        Island detection algorithm.
        If there is no island, return None.
        
        :param input_layer: layer of the river network
        :type input_layer: QgsVectorLayer object
        
        :param name: name of the layer if displayed
        :type name: string
        
        :return: layer of faces of the network (islands, polygons)
        :rtype: QgsVectorLayer object


.. py:function:: create_layer_geom(list_geom, crs, name="temp")

    Create a Polygon layer with the input list of geometries (must be polygons).
    
    :param list_geom: list of polygons
    :type list_geom: list of QgsGeometry
    
    :param crs: the crs of the output layer
    :type crs: string (format Wkt)
    
    :param name: (optional) Name of the layer to display. Default = "temp"
    :type name: string
    
    :return: layer of polygons
    :rtype: QgsVectorLayer object


.. py:function:: iterator_to_list(iterator):

    Transform the input iterator into a list.
    
    :param iterator: the iterator to convert
    :type iterator: iterator
    
    :return: the list of the values of the iterator
    :rtype: list


.. py:function:: aggregate(listFeatures)

    Aggregate the geometries of the input list of features into one geometry.
    
    :param listFeatures: features to aggregate
    :type listFeatures: list of QgsFeatures objects
    
    :return: the aggregated geometry
    :rtype: QgsGeometry object

    
.. py:function:: multi_to_single(geom)

    Transform the input multi-polygon into a list of single-polygons.
    
    :param geom: multi-polygon
    :type geom: QgsGeometry object
    
    :return: list of the single geometries
    :rtype: list of QgsGeometry objects


.. py:function:: relate_stream_island(stream_layer, island_layer)

    Return the streams inside or delimiting islands.
    The topology is defined by DE-9IM matrices.
    
    :param stream_layer: the layer of the river network
    :type stream_layer: QgisVectorLayer object (lines)
    
    :param island_layer: the layer of the islands 
    :type island_layer: QgisVectorLayer object (polygons)
    
    :return: list of lists of all the streams that make up the islands
    :rtype: list of lists of QgisFeatures objects


.. py:function:: merge_successive_islands_streams(streams_in_island_list)

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


.. py:function:: merge_duplicate(merged_streams_in_island_list)

    Merge lists that have at least one common element into one list.
    
    :param merged_streams_in_island_list: list of lists to test and merge
    :type merged_streams_in_island_list: list of lists
    
    :return: list of merged lists
    :rtype: list of lists


------------------------


Orders
------    

.. py:function:: compute_stroke(dict_strokes, edge, list_incoming_edges)

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
        

.. py:function:: compute_length(stroke)

    Return the total length of a stroke (sum of the lengths of the geometries
    of the edges that make up the stroke).
    
    :param stroke: list of edges
    :type stroke: list of Edge objects


.. py:function:: compute_angle(edge_in, edge_out):

    Compute the angle formed by edge_in and edge_out, edge_in entering the node
    edge_out exits.
    
    :param edge_in: one side of the angle
    :type edge_in: Edge object
    
    :param edge_out: one side of the angle
    :type edge_out: Edge object


.. py:function:: azimuth_angle(node_start, node_end):

    Compute the azimuth of a line defined by its start node and its end node.
    
    :param node_start: origin of the line
    :type node_start: QgsPointXY object
    
    :param node_end: end of the line
    :type node_start: QgsPointXY object


.. py:function:: compute_stroke_of_island(dict_strokes, island, incoming_edges_island)

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


.. py:function:: compute_stroke_outgoing_island(dict_strokes, dict_forks, island_id_stroke, outgoing_edges_island)

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


.. py:function:: is_upstream_processed(incoming_edges, edges_to_process)

    Check if all incoming edges have been processed.
    
    Return True if processed.
    
    :param incoming_edges: list of edges to check (incoming edges of a current edge)
    :type incoming_edges: list of Edge objects
    
    :param edges_to_process: list of edges left to process
    :type edges_to_process: list of Edge objects


.. py:function:: process_network(edges, sources_edges, orders_to_compute, edges_to_process, dict_strokes, dict_strokes_in_island, dict_forks)

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

    
.. py:function:: is_in_loop(left_edge, edges_to_process)

    Test if an edge is connected to a loop in the network.
    Return the edges of the loop in a list (return an empty list if no loop was 
    detected).
    
    :param left_edge: edge to test (could not be processed by process_network)
    :type left_edge: Edge object
    
    :param edges_to_process: list of edges left to process
    :type edges_to_process: list of Edge objects
    
    :return: list of the edges of the loop (or empty list if no loop)
    :rtype: list of Edge objects

    
.. py:function:: process_loop(edges_in_loop, orders_to_compute, edges_to_process, dict_strokes_in_island)

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
    
    :param dict_strokes_in_island: dictionary of the strokes already built of edges in islands ; {key= stroke ID: values= list of the edges of the stroke}
    :type dict_strokes_in_island: dictionary {integer:list of Edge objects}
    
    :return: indicate if the loop was successfully processed 
            (can be processed only if incoming edges were already processed)
    :rtype: boolean


.. py:function:: merge_strokes(dict_strokes, dict_strokes_in_island, dict_forks)

    Merge the strokes of the islands and of the forks with the main stroke.
    
    :param dict_strokes: dictionary of the strokes already built (except edges of islands) ; {key= stroke ID: values= list of the edges of the stroke}
    :type dict_strokes: dictionary {integer:list of Edge objects}
    
    :param dict_strokes_in_island: dictionary of the strokes already built of edges in islands ; {key= stroke ID: values= list of the edges of the stroke}
    :type dict_strokes_in_island: dictionary {integer:list of Edge objects}
    
    :param dict_forks: dictionary of the strokes already built that split ; {key= upstream stroke ID: values= list of stroke IDs after the stroke}
    :type dict_forks: dictionary {integer:list of Edge objects}

    
.. py:function:: compute_horton(dict_strokes)

    Compute the Horton order using the input strokes.
    
    The computed orders are attributes of the Edge objects.
    
    :param dict_strokes: dictionary of all the strokes built, except edges in 
                         islands
                    {key= stroke ID: values= list of the edges of the stroke}
    :type dict_strokes: dictionary {integer:list of Edge objects}


----------------------------

Write in table
--------------

.. py:function:: update_table(input_layer, orders_to_compute, field_reverse, edges)

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


-----------------------------

Dialog messages
---------------

.. py:function:: show_field_created_successfully()

    Display a message box that indicates when the input layer has been
    updated.


.. py:function:: show_message_no_stream_order_selected()

    Display a message box that indicates when no stream order was checked for
    computation by the user.


-----------------------------


Save output
-----------

.. py:function:: save_output_layer(output, path_to_saving_location)

    Save the output layer
    
    :param output: output layer to be saved
    :output type: QgsVectorLayer
    
    :param path_to_saving_location: the path to the place where the layer has 
                                    to be saved
    :type path_to_saving_location: string
