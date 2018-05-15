Results
=================

Hy2roresO handles a multitude of configurations in hydrological networks, which is a novelty comparing to former plugins from GRASS or QGIS which were less precise or even wrong at times.

To begin with, the "Strahler" QGIS plugin, as its name recalls, handles only the Strahler stream orders of a network by selecting its sink, with several mistakes when processing in specific configurations (complex river networks).
The GRASS plugin (v.stream.order) handles the Strahler and Shreve stream orders, however the results are not reliable when the process is applied on complex river networks (with islands in particular). There is also a section in the code intended to handle the Horton stream order, but it was not implemented.

Hy2roresO gives the input layer Strahler, Shreve and Horton stream orders and also takes into account the incorrect directions of the  edges that the algorithm suspects to be erroneous and that the user confirms as wrong. It also proposes a strokes calculation of the stream network during Horton stream order computation. These two considerations are a major improvement in comparison to what have been available so far.

Let's have a look at the results Hy2roresO creates with a few examples of various hydrological network configurations.

Simple network 
-------------------

In former plugins processing the different orders at stake, this configuration has never been a problem, and Hy2roresO also delivers a right result for these simple networks.

   +------------------------------------------------------------+------------------------------------------------------------+   
   | .. image:: ../_static/results/Hy2roresO_arbre_strahler.png | Strahler stream order on a simple network                  |
   +------------------------------------------------------------+------------------------------------------------------------+
   | .. image:: ../_static/results/Hy2roresO_arbre_shreve.png   | Shreve stream order on a simple network                    |
   +------------------------------------------------------------+------------------------------------------------------------+
   | .. image:: ../_static/results/Hy2roresO_arbre_horton.png   | Horton stream order on a simple network                    |
   +------------------------------------------------------------+------------------------------------------------------------+

   
Single island
------------------

Hy2roresO handles a single island so as its outgoing edge has the same order as its incoming edge, which was not the case in former plugins. This way, the orders do not increment dramatically each time an island is met by the algorithm.

   +-------------------------------------------------------------+------------------------------------------------------------+   
   | .. image:: ../_static/results/Hy2roresO_simple_strahler.png | Strahler stream order on a single island                   |
   +-------------------------------------------------------------+------------------------------------------------------------+
   | .. image:: ../_static/results/Hy2roresO_simple_shreve.png   | Shreve stream order on a single island                     |
   +-------------------------------------------------------------+------------------------------------------------------------+
   | .. image:: ../_static/results/Hy2roresO_simple_horton.png   | Horton stream order on a single island                     |
   +-------------------------------------------------------------+------------------------------------------------------------+

Complex island
-------------------

A succession of adjacent islands is what we call a complex island. When processing previous plugins, this part has always been an issue. With Hy2roresO, it is handled correctly so as the orders do not increase dramatically and remain right passed the island.

   +---------------------------------------------------------------+------------------------------------------------------------+   
   | .. image:: ../_static/results/Hy2roresO_complexe_strahler.png | Strahler stream order on a complex island                  |
   +---------------------------------------------------------------+------------------------------------------------------------+
   | .. image:: ../_static/results/Hy2roresO_complexe_shreve.png   | Shreve stream order on a complex island                    |
   +---------------------------------------------------------------+------------------------------------------------------------+
   | .. image:: ../_static/results/Hy2roresO_complexe_horton.png   | Horton stream order on a complex island                    |
   +---------------------------------------------------------------+------------------------------------------------------------+

Whole network
------------------

Hy2roresO handles every edge of the network, while previous plugins struggled managing to process them all.

   +-----------------------------------------------------------+------------------------------------------------------------+   
   | .. image:: ../_static/results/Hy2roresO_tout_strahler.png | Strahler stream order on a network                   |
   +-----------------------------------------------------------+------------------------------------------------------------+
   | .. image:: ../_static/results/Hy2roresO_tout_shreve.png   | Shreve stream order on a network                     |
   +-----------------------------------------------------------+------------------------------------------------------------+
   | .. image:: ../_static/results/Hy2roresO_tout_horton.png   | Horton stream order on a network                     |
   +-----------------------------------------------------------+------------------------------------------------------------+

Computation of the strokes
------------------

Unlike the two other plugins, Hy2roresO computes the strokes, which allows to compute the Horton stream order on networks too. Thanks to this order, one can see the main branches of a network, as shown in this result obtained with Hy2roresO :

.. figure:: ../_static/Hy2roresO_Horton.png
   :align: center
   
   Application of the Horton stream order on a network. The bolder the stroke, the higher the Horton order is.

Comparison between the three existing plugins
------------------

There are lots of differences between the three plugins.
Here is a :download:`PDF file <doc/Comparison_plugins_order.pdf>` comparing them all. 
