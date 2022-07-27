
# CLIMATE REGULATION INDICATOR FOR CITIES (EXAMPLE GERMANY)

Literature:
Syrbe et al. (2022): Vorschlag für einen Klimaregulationsindikator [Suggestion for a climate regulation indicator]. Naturschutz und Landschaftsplanung.

Model based on: "Climate Cooling Assessment (CCA) von Zardo, L., Geneletti, D., Pérez-Soba, M. und van Eupen, M. (2017): 
Estimating the cooling capacity of green infrastructures to support urban planning. In: Ecosystem Services (26), 225-235."

Python script to calculate the cooling capacity of cities for the atlantic zone (mediterranean zone and continental zone is possible after adapting the model according to values of Zardo et al. (2017). The case study used in the original work (Syrbe et al. 2022) are German cities with more than 50,000 inhabitants within the functional urban areas (Urban Atlas, Copernicus).

The data used in the input are: 

'lbm_DE': Dataset with land use and land cover types (according to CORINE land cover) from the Federal Agency of Cartography and Geodesy. Minimum mapping unit: 1 ha.
Time period used in the model: 2018 (LBM-DE 2018, release 2020).

'Einwohnergrid': Grid with the number of habitats of the buildings in the cities. The original dataset was from Destatis (Zenus) and is a raster file. 
This raster file needs to be converted to vector format by two steps in ArcGIS: 1) Raster to Point, 2) Create Fishnet with and use Points-Features created in 1) as labels. Time period used in the model: 2011

'Stadtgruenraster': Raster dataset from Krüger et al. (2022) including amongst others high vegetation (trees). Three land cover types were chosen from this raster dataset to include into the climate regulation model: broad-leaved tree, coniferous tree, built-up areas mixed with vegetation. Time period used in the model: 2018

Street_Tree: Vector dataset from Copernicus (Street Tree layer). Time period used in the model: 2018, Release 2021 (not validated).

vg25_GEM_Selektion_Stadt': Cities with more than 50,000 inhabitants. Taken from VG25, Federal Agency of Cartography and Geodesy.



* (shortly describe) The statistic/ modelling adopted is...
* (shortly describe) The output produced are...


# Link to resources

* https://code.tutsplus.com/tutorials/top-15-best-practices-for-writing-super-readable-code--net-8118
* https://mitcommlab.mit.edu/broad/commkit/coding-and-comment-style/
