Results
=================

Hy2roresO handles a multitude of configurations in hydrological networks, which is a novelty comparing to former plugins from GRASS or QGIS which were less precise or even wrong.

To begin with, the "Strahler" QGIS plugin handled, as its name recalls, only the Strahler stream orders of a network by selecting its sink, with several mistakes when processing in specific configurations.
The GRASS plugin (v.stream.order) handled the Strahler and Shreve stream orders, however the results were not good. There was also a section to handle the Horton stream order, but it was not implemented.

Hy2roresO gives the input layer Strahler, Shreve and Horton stream orders and also takes into account wrong directions from some edges and computation of the strokes, which is a major improvement comparing to what existed before.

Let's have a look at the results Hy2roresO creates with a few examples of different configurations in hydrological networks.

Simple network 
-------------------

In former plugins processing the different orders at stake, this configuration has never been a problem, and Hy2roresO also delivers a right result for these simple networks.

Lonely island
------------------

Hy2roresO handles lonely island so as the outgoing edge has the same order than the incoming edge, which was not the case in former plugins. This way, the orders do not increment dramatically each time an island is met by the algorithm.

Complex island
-------------------

A succession of adjacent islands is what we call a complex island. When processing previous plugins, this part has always been an issue. With Hy2roresO, it is handled correctly so as the orders do not increase dramatically too and stay right.

Whole network
------------------

Hy2roresO handles every edge of the network, while previous plugins struggled managing to process them all.
