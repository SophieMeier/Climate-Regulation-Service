
# INDICATOR TO ESTIMATE CLIMATE REGULATION SERVICE OF VEGETATION IN CITIES 

This python script allows to calculate the cooling capacity of cities for the atlantic zone. The case study used in the original work (Meier et al. 2022) are German cities with more than 50,000 inhabitants within the functional urban areas (according to Copernicus Urban Atlas). The model can be adapted to mediterranean and continental climates when using the proposed values from Zardo et al. (2017). 

SHORT DESCRIPTION OF THE INDICATOR

Based on the land cover type, the percentage of tree canopy cover, and the area size, a cooling capacity value (CCA value) is determined for each area in 
cities. By intersecting population data with the cooling capacity, areas can be identified where the population recieves appropriate cooling from the vegetation and areas where amount of vegetation is relatively low in order to provide a good cooling service.

The cooling capacity is a dimensionless variable from 0 to 100.
The model was developed with cities in Germany (with more than 50,000 inhabitant) that lie within urban functional areas, according to the Urban Atlas (Copernicus). The model is based on the Climate Cooling Assessment (CCA) from Zardo et al. (2017). 

KURZBESCHREIBUNG DES INDIKATORS

Über den Bodenbedeckungstyp, den Anteil der Baumkronenbedeckung und der Flächengröße wird ein Kühlungskapazitätswert (CCA-Wert) für jede Fläche in 
Städten ermittelt. Durch die Verschneidung von Einwohnerdaten mit der Information zur Kühlungskapazität mit kann ermittelt werden, 
wo Einwohner in welchem Maß mit Kühlungsleistung durch urbanes Grün versorgt werden. Die Kühlkapazität is eine dimensionslose Größe mit Werten von 0 bis 100.
Das Modell wurde auf Basis von Städten mit mehr als 50.000 Einwohnern in Deutschland ermittelt, die sich innerhalb der 'Urban Functional Areas" (Urban Atlas, Copernicus) befanden. 
Das Modell basiert auf dem Climate Cooling Assessment (CCA) von Zardo et al. (2017). Die Kühlkapazität ist eine dimensionslose Grüße von 1-100.

INPUT DATA FOR THE MODEL

* 'lbm_DE': Land cover model Germany - dataset with land use and land cover types (according to CORINE land cover) from the Federal Agency of Cartography and Geodesy (BKG). Minimum mapping unit: 1 ha. 
Time period used in the model: 2018 (LBM-DE 2018, source: BKG 2020).

* 'Einwohnergrid': Grid with the number of habitats of the buildings in the cities. The original dataset can be obtained from the German Statistical Office and is a raster file (Zensus-Raster). 
This raster file needs to be converted to vector format by two steps in ArcGIS: 1) Raster to Point, 2) Create Fishnet with and use Points-Features created in 1) as labels. Source: Destatis 2016
Time period of population zensus used in the model: 2011 

* 'Stadtgruenraster': Raster dataset from Krüger et al. (2021) including amongst others high vegetation (trees). Three land cover types were chosen from this raster dataset to include into the climate regulation model: broad-leaved tree, coniferous tree, and built-up areas mixed with vegetation. Time period used in the model: 2018

* 'Street_Tree': Vector dataset from Copernicus (2021) (Urban Atlas - Street Tree layer). Time period used in the model: 2018, Release 2021 (not validated).

* vg25_GEM_Selektion_Stadt': Cities with more than 50,000 inhabitants. Taken from VG25, Federal Agency of Cartography and Geodesy (source: BKG 2017).

* 'Urban_Functional_Areas': Indicates those cities where Street Tree data from Urban Atlas are available (source: Copernicus 2021). Only cities (inhabitants > 50,000) were used in the model that fell in the urban functional areas. As a consequence, some cities, especially in the states of Baden-Württemberg and North Rhine Westfalia could not be considered in the modelling approach.


MODELLING PROCESS

Land use and land cover types get assigned specific climate cooling capacities regarding the tree cover, soil property, and area size. 
Land cover and land use information are taken from the land cover model Germany (LBM-DE), information on tree cover was derived from 'Stadtgruenraster' and the 'Street-Tree" dataset. For areas with a high cooling capacity (above 80) and a area larger than 2 ha, a cooling distance of 100 m was estimated in the case study of Germany (Meier et al. 2022). 

The users are invited to check carfully, if they need to adapt the cooling capacity values, cooling distances and area size thresholds according to the climate and city structure in their specific datasets. 

OUTPUT DATASETS

The output datasets area: 
* a dataset with the climate cooling capacity for each land use/land cover area (each polygon)
* a dataset with the mean climate cooling capacity of each city
* a dataset with the percentage of inhabitants living in areas that show a good - very good cooling capacity (cooling capacity more than 60)


ARTICLE ASSOCIATED WITH THIS MODEL:

Meier et al. (2022): Vorschlag für einen Klimaregulationsindikator [Suggestion for a climate regulation indicator]. Naturschutz und Landschaftsplanung.[language: German]

LINK TO RESOURCES AND LITERATURE

* BKG - Bundesamt für Kartographie und Geodäsie (2017): Verwaltungsgebiete 1:25.000 (VG25) zum Gebietsstand von Deutschland vom 31.12.2016, Stand der Dokumentation: 05.04.2017. Bundesamt für Kartographie und Geodäsie (BKG), Frankfurt (Main).  

* BKG - Bundesamt für Kartographie und Geodäsie(2020): Dokumentation. Digitales Landbedeckungsmodell für Deutschland LBM-DE 2018. Stand 20.11.2020. 
Frankfurt (Main), S.63. 

* Copernicus (2021): Urban Atlas. Street Tree Layer (STL) 2018. URL: https://land.copernicus.eu/local/urban-atlas/street-tree-layer-stl-2018 
(Accessed: 13.12.2021). 

* Destatis (2015): Zensusatlas 2011. Updated in 2015. URL: https://atlas.zensus2011.de/ (Accessed: 27.07.2022). 

* Krüger, T., Eichler, L., Meinel, G., Tenikl, J., Taubenböck, H., Wurm, M. (2022). Urban Green Raster Germany 2018 (1 (2021)) [Data set]. 
https://doi.org/10.26084/ioerfdz-r10-urbgrn2018. 

* Zardo, L., Geneletti, D., Pérez-Soba, M. und van Eupen, M. (2017): Estimating the cooling capacity of green infrastructures to support urban planning. Ecosystem Services (26), 225-235.

* https://code.tutsplus.com/tutorials/top-15-best-practices-for-writing-super-readable-code--net-8118
* https://mitcommlab.mit.edu/broad/commkit/coding-and-comment-style/
