How to...?
==========

To use Hy2roresO properly, make sure you have opened the vector layer corresponding to the network you want to analyse.

To open the Hy2roresO plugin, go to the menu Extension, then find Hy2roresO and open it. You can also find it thanks to its icon : ICON

Step 1 : essential parameters
-------------

You will find yourself in front of a window :

The first parameters you must enter are :
- the layer which you want to apply the algorithm
- the stream orders you want to get thanks to the plugin : Strahler, Shreve and Horton (you can see the description of each of these orders here)

Click on **Next** to go to the next parameters.

Step 2 : optional parameters 
---------------

You can now enter more optional parameters to specify the names of the fields corresponding to the **name of the river**, its **flow**, the field corresponding to the **initial altitude** and the one corresponding to the **final altitude** of each section of the network.

These parameters are optional : if they are not specified, the algorithm will still run, but may be less efficient because these parameters can be a key for a better hierarchisation.

Click on **Next** to get to the next step.

Step 3 : process and output
----------------

On this window you can :
- authorize the algorithm to reverse streams that may not be entered well and therefore cause some mistakes in the attribution of the orders (checked initially)
- add a boolean field *reversed* to the layer you are applying the algorithm on, if during the algorithm some streams have been reversed (checked initially)
- save the output layer, and choose the path where you want to save this layer
- add the layer to the project instead of updating the input layer

Once you have finished, you can click on **Next** to get more informations about the elaboration of the plugin.

You can finally click on **OK** to run the algorithm.

*Note : You can click on OK right from the start once you have selected a layer and at least one order to calculate. The algorithm will run with all the next parameters and options being entered as they are initially. You can also come back to the previous step whenever you want by clickin on Previous*

During the algorithm
~~~~~~~~~~~~~~


During the process of the algorithm, if you have chosen to authorize the algorithm to reverse some streams, you may find this type of window : WINDOW

You can reverse the feature which is being processed or not. You can also, according to the number of streams that could be reversed, ask to reverse them all or to let them all at their initial state.

End of the algorithm
-----------------

The algorithm is finished when you meet this final window : WINDOW 

