Introduction
============

The classification of a hydrographic network is a way of ranking all the branches of this network by assigning to each 
a whole value that characterizes its importance. Several different classifications have been developed, Strahler's 
classification in particular is very commonly used. Shreve and Horton’s classification are also classifications 
that are frequently used. These three classifications are those calculated by processing Hy2roresO.

Strahler stream order
---------------------

Presentation
~~~~~~~~~~~~

The Strahler number is a numerical measure of a tree or a network’s branching complexity.
This number was first developed in hydrology by Robert E. Horton (1945) and Arthur Newell Strahler (1952, 1957). 
In this application, they are used to define stream size based on a hierarchy of tributaries.

In the application of the Strahler stream order to hydrology, each segment of a stream or river within a river network 
is treated as a node in a tree, with the next segment downstream as its parent. When two first-order streams come together, 
they form a second-order stream. When two second-order streams come together, they form a third-order stream. 
Streams of lower order joining a higher order stream do not change the order of the higher stream. 
Thus, if a first-order stream joins a second-order stream, it remains a second-order stream. 
It is not until a second-order stream combines with another second-order stream that it becomes a third-order stream.

The Strahler stream order of a sink is the highest one of the river, and does usually not exceed 10.

Hypotheses
~~~~~~~~~~

Some hypothesis were made during the computing of the plugin. For more details about these hypothesis, 
please refer to the Programmer Documentation.

.. image:: :/_static/strahler.png

Shreve stream order
-------------------

Presentation
~~~~~~~~~~~~

The Shreve stream order is another order used in hydrology with the similar aim of defining the stream size of a hydrologic network.

The Shreve system also gives the outermost tributaries the number "1". At a confluence the numbers are added together, 
contrary to the Strahler stream order. This means that the Shreve stream order of a sink can be very high.

Shreve stream order is preferred in hydrodynamics: it sums the number of sources in each catchment above a stream gauge or outflow, 
and correlates roughly to the discharge volumes and pollution levels. Like the Strahler method, it is dependent on the precision 
of the sources included, but less dependent on map scale. It can be made relatively scale-independent by using suitable normalisation 
and is then largely independent of an exact knowledge of the upper and lower courses of an area.

Hypotheses
~~~~~~~~~~

Some hypothesis were made during the computing of the plugin. For more details about these hypothesis, 
please refer to the Programmer Documentation.

.. image:: :/_static/shreve.png

Horton stream order
-------------------

Presentation
~~~~~~~~~~~~

The Horton stream order is the third most commonly used stream order in hydrology. It is based on a different idea 
which takes into account the strokes and the Strahler stream order.
Horton’s stream order applies to the stream as a whole and not according to the edges of the network. 
The first step of its process is to define the strokes, which are CECILE. 
The second step is to, according to the strokes and the Strahler stream order, define the Horton stream order for each stroke. 
The main stroke is first to be set its Horton stream order which corresponds to its Strahler stream order, 
and then each stroke is given a Horton stream order corresponding to its Strahler order. 


Hypotheses
~~~~~~~~~~

Some hypothesis were made during the computing of the plugin. For more details about these hypothesis, 
please refer to the Programmer Documentation.

.. image:: :/_static/horton.png
