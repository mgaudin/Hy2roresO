Perspectives
============

Hy2roresO deals with a whole bunch of cases that can happen with natural hydrological networks. However, there still are some things that can be realized to improve the plugin.

* One thing that can be done is to create fictive network inside the islands, for example by using a skeleton of the geometry of the island. This could for example improve the definition of strokes entering and exiting an island, especially it the island is curved. It also would grant the strokes a linear geometry (without the forks due to islands), which is commonly expected of a stroke.
.. figure:: ../_static/skeleton.png
   :align: center

* The method *interpolateAngle()* from the class **QgsGeometry** was briefly studied to better deal with curved islands by interpolating
the angle between the island and its incoming edges, or the island and its outgoing edges. Maybe this could lead to a better process for the strokes. As for now, there is indeed no consideration of angle between the island and its connected edges to define the strokes, which is a major weakness. The angle between an edge and an island is a notion yet to define. 


* The flow of each edge is theorically the second criteria to determine strokes, however it is not handled in our algorithm since flow data is rarely available. Adding a condition on it to the code could be beneficial for a better determination of the strokes. However testing such a field automatically implies that the field must follow a given format, which is tricky to generalize and is hardly reliable due to the diversity of database specifications (especially if strings are allowed).


* The plugin already tests if edges seem to be directed correctly, based on their altitudes and the direction of their connected edges. The detection algorithm would be improved by adding an angle criteria to the tests.
