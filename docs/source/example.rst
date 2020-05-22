============================
Multispectral Photogrammetry
============================

This project was used for remote sensing classification from a multispectral camera. The camera *Parrot Sequoia* was first calibrated and tested on sample areas.
Then, it was fixed to a civil drone and we flew over high altitudes forest to estimate the evolution of vegetation species.
**Colorply** was used to create a multispectral cloud of points, to improve our classification by adding extra features.
The clusters were made from a random forest skeleton, using all radiometries (RED, REG, NIR, GRE) and the points 3D positions.

In this repository, you can run the classification on the provided data [here](test/data/result/RVB_GRE_RED_REG_NIR_NDVI.ply).
For this short example (for fast processing), the classification results are described as follows :


.. image:: images/result_4channels.gif


The confusion matrix for this sample is :

+-------------+-------------+---------+-----------+-----------+
|             | **Terrain** | **Oak** | **Shrub** | **Grass** |
+-------------+-------------+---------+-----------+-----------+
| **Terrain** | **410**     | 0       | 0         | 16        |
+-------------+-------------+---------+-----------+-----------+
| **Oak**     | 0           | **260** | 10        | 0         |
+-------------+-------------+---------+-----------+-----------+
| **Shrub**   | 0           | 10      | **137**   | 16        |
+-------------+-------------+---------+-----------+-----------+
| **Grass**   | 23          | 0       | 11        | **192**   |
+-------------+-------------+---------+-----------+-----------+


**Global accuracy : 92.07%.**

.. image:: images/result_classif.gif

