
# CLIMATE REGULATION INDICATOR FOR CITIES 

Python script to calculate the cooling capacity of cities for the atlantic zone (mediterranean zone and continental zone is possible after adapting according to Zardo et al. (2017). The case study used in the original work (Syrbe et al. 2022) are German cities with more than 50,000 inhabitants within the functional urban areas (Urban Atlas, Copernicus).

Syrbe et al. (2022): Vorschlag für einen Klimaregulationsindikator [Suggestion for a climate regulation indicator]. Naturschutz und Landschaftsplanung.

SHORT DESCRIPTION OF THE INDICATOR

Using land cover type, percentage of tree canopy cover, and area size, a cooling capacity value (CCA value) is determined for each area in 
Cities with a population of 50,000 or more. By intersecting population data with cooling capacity information with can be determined, 
where residents are provided with cooling capacity by urban greenery and to what degree.
The model was developed with cities in Germany (more than 50,000 inhabitant) that lie within urban functional areas according to the Urban Atlas (Copernicus).
The model based on the Climate Cooling Assessment (CCA) from Zardo et al. (2017).

KURZBESCHREIBUNG DES INDIKATORS

Über den Bodenbedeckungstyp, den Anteil der Baumkronenbedeckung und der Flächengröße wird ein Kühlungskapazitätswert (CCA-Wert) für jede Fläche in 
Städten ab 50.000 Einwohnern ermittelt. Durch die Verschneidung von Einwohnerdaten mit der Information zur Kühlungskapazität mit kann ermittelt werden, 
wo Einwohner in welchem Maß mit Kühlungsleistung durch urbanes Grün versorgt werden.
Das Modell wurde auf Basis von Städten mit mehr als 50.000 Einwohnern in Deutschland ermittelt, die sich innerhalb der 'Urban Functional Areas" (Urban Atlas, Copernicus) befanden. 
Das Modell basiert auf dem Climate Cooling Assessment (CCA) von Zardo et al. (2017).


The input data used in the model are: 

'lbm_DE': Land cover model Germany - dataset with land use and land cover types (according to CORINE land cover) from the Federal Agency of Cartography and Geodesy. Minimum mapping unit: 1 ha.
Time period used in the model: 2018 (LBM-DE 2018, release 2020).

'Einwohnergrid': Grid with the number of habitats of the buildings in the cities. The original dataset was from Destatis (Zenus) and is a raster file. 
This raster file needs to be converted to vector format by two steps in ArcGIS: 1) Raster to Point, 2) Create Fishnet with and use Points-Features created in 1) as labels. Time period used in the model: 2011

'Stadtgruenraster': Raster dataset from Krüger et al. (2022) including amongst others high vegetation (trees). Three land cover types were chosen from this raster dataset to include into the climate regulation model: broad-leaved tree, coniferous tree, built-up areas mixed with vegetation. Time period used in the model: 2018

'Street_Tree': Vector dataset from Copernicus (Urban Atlas - Street Tree layer). Time period used in the model: 2018, Release 2021 (not validated).

vg25_GEM_Selektion_Stadt': Cities with more than 50,000 inhabitants. Taken from VG25, Federal Agency of Cartography and Geodesy.

MODELLING PROCESS

Land use and land cover types get assigned specific climate cooling capacities regarding the tree cover, soil property, and area size. 
Land cover and land use information are taken from the land cover model Germany (lbm-de), information on tree cover was derived from 'Stadtgruenraster' and the 'Street-Tree" dataset. For areas with a high cooling capacity (above 80) and a area larger than 2 ha, cooling distance of 100 m was estimated in the case study of Germany (based on Jaganmohan et al. 2016). 
The users are invited to set own cooling distances and area size thresholds according to the climate and city structure in their specific datasets. 

OUTPUT DATASETS

* (shortly describe) The statistic/ modelling adopted is...
* (shortly describe) The output produced are...


LINK TO RESOURCES

Jaganmohan M, Knapp S, Buchmann CM, Schwarz N. The Bigger, the Better? The Influence of Urban Green Space Design on Cooling Effects for Residential Areas. J Environ Qual. 2016 Jan;45(1):134-45. doi: 10.2134/jeq2015.01.0062. PMID: 26828169.

Zardo, L., Geneletti, D., Pérez-Soba, M. und van Eupen, M. (2017): Estimating the cooling capacity of green infrastructures to support urban planning. Ecosystem Services (26), 225-235.

* https://code.tutsplus.com/tutorials/top-15-best-practices-for-writing-super-readable-code--net-8118
* https://mitcommlab.mit.edu/broad/commkit/coding-and-comment-style/
