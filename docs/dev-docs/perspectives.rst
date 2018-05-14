Perspectives
============

Hy2roresO deals with a whole bunch of cases that can happen with natural hydrological networks. However, there is still some things that can be realized to improve the plugin.

* One thing that can be done is to create fictive network inside the islands, for example by using a skeleton of the geometry of the island. This could for example improve the definition of strokes that are arriving in an island if this one is twisted for example.
* The method *interpolateAngle()* from the class **QgsGeometry**  was once studied to also deal with the island that are quite twisted, to interpolate the angle between an incoming edge in the island and the outgoing edge from the island. Maybe this could lead to a better process for the strokes.
