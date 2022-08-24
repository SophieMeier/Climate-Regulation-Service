# -*- coding: iso-8859-1 -*-

# PYTHON-VERSION 3.6
# SOFTWARE: PYCHARM 2019.3.1, ARCGISpro 3.0.0
# LANGUAGE: English & German

### INDICATOR CLIMATE REGULATION IN CITIES ### KLIMAREGULATIONSINDIKATOR FÜR STÄDTE

# SHORT DESCRIPTION OF THE INDICATOR
# Using land cover type, percentage of tree canopy cover, and area size, a cooling capacity value (CCA value) is determined for each area in 
# Cities with a population of 50,000 or more. By intersecting population data with cooling capacity information with can be determined, 
# where residents are provided with cooling capacity by urban greenery and to what degree.

# KURZBESCHREIBUNG DES INDIKATORS
# Über den Bodenbedeckungstyp, den Anteil der Baumkronenbedeckung und der Flächengröße wird ein Kühlungskapazitätswert (CCA-Wert) für jede Fläche in 
# Städten ab 50.000 Einwohnern ermittelt. Durch die Verschneidung von Einwohnerdaten mit der Information zur Kühlungskapazität mit kann ermittelt werden, 
# wo Einwohner in welchem Maß mit Kühlungsleistung durch urbanes Grün versorgt werden.

# ENVIRONMENT OPTIONS / UMGBUNGSEINSTELLUNGEN
import arcpy
import math
from arcpy import env
from arcpy.sa import *
arcpy.env.parallelProcessingFactor = "100%"
arcpy.env.overwriteOutput = True

# Snap-Raster: INSPIRE-conform-Grid (EU standard) with 10x10 m Raster Cell Size 
# Fang-Raster: INSPIRE-konformes Grid (nach EU-Standard) mit 10x10m Rasterzellgröße 
arcpy.env.snapRaster = "D:/tarox1_user5/OESL_P644_671/INSPIRE_Grid/inspire_grids_10.gdb/raster_10_complete" 
arcpy.env.extent = "MAXOF"

# YEAR / JAHR
Jahr = "_2018"

# INPUT AND OUTPUT GEODATABASES / EINGANGS- UND AUSGABE-GEODATABASES
# Please replace by own paths # Bitte eigenen Pfad angeben
Eingangsdaten_gdb = "E:/Meier/Stadtklima/Eingangsdaten.gdb"   
output_gdb_1 = "E:/Meier/Stadtklima/output_1" + Jahr + ".gdb" # output for ...
output_gdb_2 = "E:/Meier/Stadtklima/output_2" + Jahr + ".gdb" # output for ...
output_gdb_3 = "E:/Meier/Stadtklima/output_3" + Jahr + ".gdb" # output for ...

# DATA SETS - find description in ReadMe 
# DATENSÄTZE - Beschreibung im ReadMe
# Please replace by own paths # Bitte eigenen Pfad angeben
lbm_DE = "D:/tarox1_user5/OESL_P644_671/LBM/oriG/lbm_de_2018.gdb/lbm_de_2018_v2"
Einwohnergrid = "D:/tarox1_user5/OESL_P644_671/Einwohnerzahlen/zensus2011.gdb/grid_r100_zensus11ew"
Stadtgruenraster = "D:/tarox1_user5/OESL_P644_671/Stadtklima/Sentinel_II.gdb/s2_2018_lcc_classes_1_8_atkismod"
Street_Tree = "D:/tarox1_user5/OESL_P644_671/Urban_Atlas/Street_Tree_Layer_2018.gdb/UA_STL_2018"
Urban_Functional_Areas = "D:/tarox1_user5/OESL_P644_671/Urban_Atlas/Street_Tree_Layer_2018.gdb/UA_Boundary_STL_2018"
lyr = Eingangsdaten_gdb + "\\VG25_2016_join_50000EW.lyr"
vg25_GEM_Selektion_Stadt = "D:/tarox1_user5/OESL_P644_671/VG_ATKIS/VG_25/stadte_50000_ew.gdb/VG25_2016_join_50000EW"    

# PROCESSING STEPS # PROZESSIERUNGSSCHRITTE

# SELECT CITIES WITH A POPULATION OF 50,000 OR MORE (FROM VG25) WITHIN THE URBAN ATLAS FUNCTIONAL AREAS
# VIA SELECT BY LOCATION
    # the clip function would not work in this step, because otherwise you would select small splinters of VG25 municipalities, which were not actually
        # been included in the Urban Atlas, but partially extend into the Urban Functional Areas. Therefore the function "Select by location" was taken.
# STÄDTE AB 50.000 EINWOHNERN (AUS VG25) INNERHALB DER URBAN ATLAS FUNCTIONAL AREAS SELEKTIEREN
# ÜBER SELECT BY LOCATION
    # die Clip-Funktion würde in diesem Schritt nicht funktionieren, da man sonst kleine Splitter von VG25-Gemeinden mit selektieren würde, die eigentlich nicht
        # im Urban Atlas erfasst worden sind, aber teilweise in die Urban Functional Areas hineinragen. Daher wurde die Funktion "Select by location" genommen

print("Select cities within the Urban Atlas / Städte innerhalb des Urban Atlas auswählen")
lyr = Eingangsdaten_gdb + "\\lyr"
arcpy.MakeFeatureLayer_management(vg25_GEM_Selektion_Stadt, lyr)
arcpy.SelectLayerByLocation_management(lyr, 'HAVE_THEIR_CENTER_IN', Urban_Functional_Areas, "", "NEW_SELECTION", "")
vg_25_sel_Stadt_SEL = Eingangsdaten_gdb + "\\vg_25_sel_Stadt_SEL"
arcpy.CopyFeatures_management(lyr, vg_25_sel_Stadt_SEL)

# IN SOME CASES, THE VG25 COMMUNITIES ARE LARGER THAN THE URBAN-FUNCTIONAL AREAS, THEREFORE THE VG25 GEOMETRIES WHICH ARE
    # OUTSIDE THE URBAN-FUNCTIONAL-AREAS ARE REMOVED
# TEILWEISE SIND DIE VG25-GEMEINDEN GRÖSSER ALS DIE URBAN-FUNCTIONAL AREAS, DESWEGEN WERDEN DIE VG25-GEOMETRIEN
    # AUSSERHALB DER URBAN-FUNCTIONAL-AREAS ENTFERNT

vg_25_sel_Stadt_UA = Eingangsdaten_gdb + "\\vg_25_sel_Stadt_UA"
arcpy.analysis.Clip(vg_25_sel_Stadt_SEL, Urban_Functional_Areas, vg_25_sel_Stadt_UA)

print("Select LBM-DE within the urban geometries (common area of VG25 and Urban Functional Areas)")
print ("LBM-DE innerhalb der Stadtgeometrien (gemeinsame Fläche von VG25 und Urban Functional Areas) selektieren")
# LBM-DE ZURECHTSCHNEIDEN AUF DIE NEU ERSTELLTE GEOMETRIE ZU STÄDTEN AB 50.000 EINWOHNER (VG25) INNERHALB DER URBAN FUNCTIONAL AREAS
lbm_Stadt_alt = Eingangsdaten_gdb + "\\lbm_Stadt_alt" + Jahr
arcpy.analysis.Clip(lbm_DE, vg_25_sel_Stadt_UA, lbm_Stadt_alt)

lbm_Stadt_alt_sing = Eingangsdaten_gdb + "\\lbm_Stadt_alt_sing" + Jahr
arcpy.management.MultipartToSinglepart(lbm_Stadt_alt, lbm_Stadt_alt_sing)

lbm_Stadt = Eingangsdaten_gdb + "\\lbm_Stadt" + Jahr
lbm_Stadt_lyr = Eingangsdaten_gdb + "\\lbm_Stadt_lyr" + Jahr
arcpy.MakeFeatureLayer_management(lbm_Stadt_alt_sing, lbm_Stadt_lyr)
arcpy.SelectLayerByAttribute_management(lbm_Stadt_lyr, "NEW_SELECTION",'"Shape_Area" < 100')
arcpy.Eliminate_management(lbm_Stadt_lyr, lbm_Stadt, "AREA", '"Shape_Area" > 100')

lbm_Stadt_sing = Eingangsdaten_gdb + "\\lbm_Stadt_sing" + Jahr
arcpy.management.MultipartToSinglepart(lbm_Stadt, lbm_Stadt_sing)

# LAND COVER TYPES (BD) (SEE ZARDO ET AL. 2017 AND SYRBE ET AL. 2022)/ BODENBEDECKUNGSTYP (BD) (SIEHE ZARDO ET AL. 2017 UND SYRBE ET AL. 2022):
     # V: sealed/versiegelt
     # O: open soil / offener Boden
     # H: heterogeneous / heterogen
     # WS: water surface / Wasser
     # G: grass / Gras
     # WL: forest / Wald

print("Create field for land cover type 'BD' and assign types to CLC classes")
print("Feld für Bodenbedeckung 'BD' anlegen und CLC-Klassen im LBM-DE den Bodenbedeckungstypen zuweisen")
    if len(arcpy.ListFields(lbm_Stadt_sing, "BD")) > 0:
        print("Field already exists / Feld schon vorhanden")
else:
    arcpy.AddField_management(lbm_Stadt_sing, "BD", "TEXT", "","", "", "", "NULLABLE", "", "")

with arcpy.da.UpdateCursor(lbm_Stadt_sing, ['CLC18', 'BD']) as cursorCLC:
    for rowCLC in cursorCLC:
        if rowCLC[0] == '111':        # CORINE land cover class (CLC) : continuous urban fabric / durchgängig städtische Prägung
            rowCLC[1] = 'V'             # land cover type BD: sealed / Versiegelt
        elif rowCLC[0] == '112':      # CLC: discontinuous urban fabric / Nicht durchgängig städtische Prägung
            rowCLC[1] = 'H'             # BD: heterogeneous / heterogen
        elif rowCLC[0] == '121':      # CLC: industrial and commercial units / Industrie- und Gewerbefläche
            rowCLC[1] = 'V'
        elif rowCLC[0] == '122':      # CLC: road and rail networks and associated land / Straßen- und Eisenbahnnetze
            rowCLC[1] = 'V'
        elif rowCLC[0] == '123':      # CLC: port areas / Hafengebiete
            rowCLC[1] = 'V'
        elif rowCLC[0] == '124':      # CLC: airport / Flughafen
            rowCLC[1] = 'V'
        elif rowCLC[0] == '131':      # CLC: mineral extraction sites / Abbauflächen
            rowCLC[1] = 'O'             # BD: open soil / offener Boden
        elif rowCLC[0] == '132':      # CLC: dumps sites / Deponien und Abraumhalden
            rowCLC[1] = 'H'
        elif rowCLC[0] == '133':      # CLC: construction sites / Baustellen
            rowCLC[1] = 'H'
        elif rowCLC[0] == '141':      # CLC: green urban area / Städtische Grünflächen
            rowCLC[1] = 'G'             # BD: grass / Gras
        elif rowCLC[0] == '142':      # CLC: sport and leisure facilities / Sport- und Freizeitanlagen
            rowCLC[1] = 'H'
        elif rowCLC[0] == '211':      # CLC: non-irrigated arable land / nicht bewässertes Ackerland
            rowCLC[1] = 'O'
        elif rowCLC[0] == '221':      # CLC: vineyards / Weinbauflächen
            rowCLC[1] = 'G'
        elif rowCLC[0] == '222':      # CLC: fruit tree and berry plantations / Obst- und Beerenobstbestände
            rowCLC[1] = 'G'
        elif rowCLC[0] == '231':      # CLC: pasture, meadows / Wiesen und Weiden
            rowCLC[1] = 'G'
        elif rowCLC[0] == '311':      # CLC: broad-leaved forest / Laubwälder
            rowCLC[1] = 'WL'            # BD: forest / Wald
        elif rowCLC[0] == '312':      # CLC:  coniferous forest / Nadelwälder
            rowCLC[1] = 'WL'
        elif rowCLC[0] == '313':      # CLC: mixed forest / Mischwälder
            rowCLC[1] = 'WL'
        elif rowCLC[0] == '321':      # CLC: natural grassland / Natürliches Grünland
            rowCLC[1] = 'G'
        elif rowCLC[0] == '322':      # CLC: moors and heathland / Heiden und Moorheiden
            rowCLC[1] = 'G'
        elif rowCLC[0] == '324':      # CLC: transitional woodland, shrub / Wald-Strauch-Übergangsstadien
            rowCLC[1] = 'G'
        elif rowCLC[0] == '331':      # CLC: beaches, dunes and sand plains / Strände, Dünen und Sandflächen
            rowCLC[1] = 'O'
        elif rowCLC[0] == '332':      # CLC: bare rock / Felsflächen ohne Vegetation
            rowCLC[1] = 'O'
        elif rowCLC[0] == '333':      # CLC: sparsely vegetated areas / Flächen mit spärlicher Vegetation
            rowCLC[1] = 'O'
        elif rowCLC[0] == '334':      # CLC: burnt areas / Brandflächen
            rowCLC[1] = 'O'
        elif rowCLC[0] == '335':      # CLC: glaciers and perpetual snow / Gletscher und Dauerschneegebiete (nicht in den ausgewählten Stadtgebieten in Deutschland vorzufinden)
            rowCLC[1] = 'WS'            # BD: water surface / Wasser
        elif rowCLC[0] == '411':      # CLC: inland marshes / Sümpfe
            rowCLC[1] = 'WS'
        elif rowCLC[0] == '412':      # CLC: peatbogs / Torfmoore
            rowCLC[1] = 'WS'
        elif rowCLC[0] == '421':      # CLC: coastal salt marshes / Salzwiesen
            rowCLC[1] = 'WS'
        elif rowCLC[0] == '423':      # CLC: intertidal flats / Watt
            rowCLC[1] = 'WS'
        elif rowCLC[0] == '511':      # CLC: watercourses / Gewässerläufe
            rowCLC[1] = 'WS'
        elif rowCLC[0] == '512':      # CLC: water bodies / Wasserflächen
            rowCLC[1] = 'WS'
        elif rowCLC[0] == '521':      # CLC: coastal lagoons / Lagunen
            rowCLC[1] = 'WS'
        elif rowCLC[0] == '522':      # CLC: estuaries / Mündungsgebiete
            rowCLC[1] = 'WS'
        elif rowCLC[0] == '523':      # CLC: sea and ocean / Meere und Ozeane
            rowCLC[1] = 'WS'

        cursorCLC.updateRow(rowCLC)
    del rowCLC, cursorCLC

# DETERMINATION OF THE PROPORTION OF TREES IN EACH CLC-CLASS IN LBM-DE - FOR THIS PURPOSE, INFORMATION ON TREES FROM THE
# URBAN GREEN MONITORING RASTER DATASET WAS USED, WHICH HAS FOLLOWING CLASSES
# ERMITLUNG DES BAUMANTEILS JEDER CLC-KLASSE IM LBM-DE - HIERZU WURDEN INFORMATIONEN ZU BÄUMEN AUS DEM
# STADTGRÜNMONITORING-RASTERDATENSATZ VERWENDET, DAS FOLGENDE KLASSEN ENTHÄLT

     # 1: Built-up / bebaut
     # 2: Open ground / offener Boden
     # 3: Broad-leaved tree / Laubholz
     # 4: Coniferous tree / Nadelholz
     # 5: Arable land (low seasonal vegetation) / Ackerland (niedrige saisonale Vegetation)
     # 6: Meadow (low seasonal vegetation) / Wiese (niedrige ganzjährige Vegetation)
     # 7: Water / Wasser
     # 8: Built-up, but considerably vegetated / Bebaut, stark durchgrünt
        
# COMBINE BOTH DATASETS WITH TREE COVER INFORMATION INTO ONE DATASET (STREET TREE LAYER WITH TREE DATA FROM URBAN GREENING RASTER)
# IN CASE OF OVERLAYS, THE TREE DATA FROM THE URBAN GREEN MONITORING LAYER HAVE A HIGHER PRIORITY THAN THE STREET TREE LAYER

# BEIDE DATENSÄTZE MIT BAUMBEDECKUNGSINFORMATIONEN IN EINEN DATENSATZ VEREINIGEN (STREET TREE LAYER MIT BAUMDATEN AUS DEM STADTGRUENRASTER KOMBINIEREN)
# BEI UEBERLAGERUNGEN HABEN DIE BAUMDATEN AUS DEM STADTGRÜN-RASTER DIE HOEHERE PRIORITAET, ALS DER STREET TREE LAYER
        
print("Convert Streettree layer to 10x10m grid and insert into urban green grid as category 9")
print("Streettree-Layer in 10x10m Raster umwandeln und als Kategorie 9 in Stadtgrünraster einfügen")

if len(arcpy.ListFields(Street_Tree, "Klasse")) > 0:
    print("Feld schon vorhanden")
else:
    arcpy.AddField_management(Street_Tree, "Klasse", "LONG", "","", "", "", "NULLABLE", "", "")
arcpy.CalculateField_management(Street_Tree, "Klasse", '9')

Street_Tree_rast = output_gdb_1 + "\\Street_Tree_rast"
arcpy.PolygonToRaster_conversion(Street_Tree, "Klasse", Street_Tree_rast, "MAXIMUM_COMBINED_AREA", "", 10)

print("Extract pixels containing tree information from the urban green monitoring grid: Class 3 and 4")
print("Aus dem Stadtgrünmonitoring-Raster die Pixel extrahieren, welche Baum-Informationen enthalten: Klasse 3 und 4")
path_recl_Stadtgruen_3_4 = output_gdb_1 + "\\Stadtgruenrast_3_4"
remap = RemapValue([[1, "NoData"], [2, "NoData"], [3, 3], [4, 4], [5, "NoData"], [6, "NoData"], [7, "NoData"], [8, "NoData"]])
out_raster = Reclassify(Stadtgruenraster, "Value", remap, "NoData")
out_raster.save(path_recl_Stadtgruen_3_4)

print("Extract pixels containing tree information from the urban green monitoring grid: Class 8")
print("Aus dem Stadtgrünmonitoring-Raster die Pixel extrahieren, welche Baum-Informationen enthalten: Klasse 8")
path_recl_Stadtgruen_8 = output_gdb_1 + "\\Stadtgruenrast_8"
remap = RemapValue([[1, "NODATA"], [2, "NODATA"], [3, "NODATA"], [4, "NODATA"], [5, "NODATA"], [6, "NODATA"], [7, "NODATA"], [8, 8]])
out_raster = Reclassify(Stadtgruenraster, "Value", remap, "NODATA")
out_raster.save(path_recl_Stadtgruen_8)

print("Street Tree Layer und Stadtgrünraster zusammenfügen")
path_Stadtgruen_Streettree = output_gdb_2 + "\\Stadtgruenrast_3_4_8_9"
mosaik_dataset = [path_recl_Stadtgruen_3_4, Street_Tree_rast, path_recl_Stadtgruen_8]
arcpy.management.MosaicToNewRaster(mosaik_dataset, output_gdb_2, "Stadtgruenrast_3_4_8_9", "", "4_BIT", "10", "1", "FIRST", "")

# ZIEL: RASTERUNG DES LBM-DES IN 10x10m RASTER (GLEICHE AUFLÖSUNG, WIE DAS STADTGRÜNRASTER)
# JEDEM RASTERPIXEL WURDE DER ID-WERT DES JEWEILIGEN LBM-DE-POLYGONS ZUGEWIESEN
print("ID für jedes Polygon im LBM-DE erstellen")
if len(arcpy.ListFields(lbm_Stadt_sing, "ID")) > 0:
    print("Feld schon vorhanden")
else:
    arcpy.AddField_management(lbm_Stadt_sing, "ID", "DOUBLE", "", "", "", "", "NULLABLE", "", "")
arcpy.CalculateField_management(lbm_Stadt_sing, "ID", '!OBJECTID_1!')

print("LBM-DE in 10x10m Raster umwandeln")
lbm_Stadt_ID_rast = output_gdb_1 + "\\lbm_stadt_rast"
arcpy.PolygonToRaster_conversion(lbm_Stadt_sing, "ID", lbm_Stadt_ID_rast, "MAXIMUM_COMBINED_AREA", "", 10)

# ERMITTELN WIEVIELE RASTERZELLEN DER KLASSE 3 (LAUBBAUM), 4 (NADELBAUM), 9 (Street Tree Layer) UND 8 (BEBAUT - STARK DURCHGRÜNT) 
# JEWEILS IN WELCHER LBM-DE FLÄCHE LIEGEN UND DIE FLÄCHENGRÖSSE BERECHNEN - DIE ERGEBNISDATEI IST EINE TABELLE
print("Ermitteln wieviele Rasterzellen an Bäumen und bebaut-stark durchgrünt in welcher LBM-DE-Fläche vorkommen")
tabl_kl_3_4_8_9 = output_gdb_1 + "\\tab_Stadtgruenrast_3_4_8_9"
TabulateArea(lbm_Stadt_ID_rast, "Value", path_Stadtgruen_Streettree, "Value", tabl_kl_3_4_8_9, "10", "CLASSES_AS_FIELDS")

print("Für jede Klasse eine Spalte erstellen, in der die Flächengröße berechnet wird (Anzahl der Zellen x 100m² (10x10m)")
# Flächengröße berechnen für Klasse 3 (Auf Basis der Rasterflächen)
if len(arcpy.ListFields(tabl_kl_3_4_8_9, "VALUE_3_Area")) > 0:
    print("Feld schon vorhanden")
else:
    arcpy.AddField_management(tabl_kl_3_4_8_9, "VALUE_3_Area", "DOUBLE", "","", "", "", "NULLABLE", "", "")
arcpy.CalculateField_management(tabl_kl_3_4_8_9, "VALUE_3_Area", '!VALUE_3!', "PYTHON3")

# Flächengröße berechnen für Klasse 4 (Auf Basis der Rasterflächen)
if len(arcpy.ListFields(tabl_kl_3_4_8_9, "VALUE_4_Area")) > 0:
    print("Feld schon vorhanden")
else:
    arcpy.AddField_management(tabl_kl_3_4_8_9, "VALUE_4_Area", "DOUBLE", "","", "", "", "NULLABLE", "", "")
arcpy.CalculateField_management(tabl_kl_3_4_8_9, "VALUE_4_Area", "!VALUE_4!", "PYTHON3")

# ANALYSEN MIT GRÜNVOLUMENDATEN VON FÜNF STÄDTEN ZEIGTEN, DASS DIE KLASSE 8 (BEBAUT, STARK DURCHGRÜN) IM DURCHSCHNITT NUR 18 PROZENT BAUMBEDECKUNG BEINHALTET
# SIEHE SYRBE ET AL. (2022)
# DAHER WIRD DIE FLÄCHENGRÖSSE (10x10m = 100m²) DER KLASSE 8 MIT 0,18 MULTIPLIZIERT

# Flächengröße berechnen für Klasse 8 (Auf Basis der Rasterflächen)
if len(arcpy.ListFields(tabl_kl_3_4_8_9, "VALUE_8_Area")) > 0:
    print("Feld schon vorhanden")
else:
    arcpy.AddField_management(tabl_kl_3_4_8_9, "VALUE_8_Area", "DOUBLE", "","", "", "", "NULLABLE", "", "")
arcpy.CalculateField_management(tabl_kl_3_4_8_9, "VALUE_8_Area", "!VALUE_8!*0.18", "PYTHON3")

# Flächengröße berechnen für Klasse 9 (= Street Tree Layer)
if len(arcpy.ListFields(tabl_kl_3_4_8_9, "VALUE_9_Area")) > 0:
    print("Feld schon vorhanden")
else:
    arcpy.AddField_management(tabl_kl_3_4_8_9, "VALUE_9_Area", "DOUBLE", "","", "", "", "NULLABLE", "", "")
arcpy.CalculateField_management(tabl_kl_3_4_8_9, "VALUE_9_Area", "!VALUE_9!", "PYTHON3")

# ZUSAMMENRECHNEN DER BAUMBEDECKUNG (SUMME DER FLÄCHENGRÖSSE VON LAUBBAUM, NADELBAUM, 18-PROZENTIGER ANTEIL VON BEBAUT, STARK DURCHGRÜNT)
print("Ein neues Feld erstellen in das die Gesamtfläche der Baumbedeckung berechnet wird, alle Spalten der Klassenflächengrößen zusammenrechnen")
if len(arcpy.ListFields(tabl_kl_3_4_8_9, "Baumbed_Area")) > 0:
    print("Feld schon vorhanden")
else:
    arcpy.AddField_management(tabl_kl_3_4_8_9, "Baumbed_Area", "DOUBLE", "","", "", "", "NULLABLE", "", "")
arcpy.management.CalculateField(tabl_kl_3_4_8_9, "Baumbed_Area", "!VALUE_3_Area!+!VALUE_4_Area!+!VALUE_8_Area!+!VALUE_9_Area!", "PYTHON3")

# IM LBM-DE EINE UNVERÄNDERLICHE SPALTE MIT DER FLÄCHENGRÖSSE ANLEGEN
if len(arcpy.ListFields(lbm_Stadt_sing, "AREA")) > 0:
    print("Feld schon vorhanden")
else:
    arcpy.AddField_management(lbm_Stadt_sing, "AREA", "DOUBLE", "","", "", "", "NULLABLE", "", "")
arcpy.management.CalculateField(lbm_Stadt_sing, "AREA", "!Shape_Area!", "PYTHON3")

# DIE WERTE ZUR BAUMBEDECKUNG AUS DEM STADTGRÜNMONITORING-RASTER AN DAS LBM-DE ANHÄNGEN ÜBER DIE ZU BEGINN ERZEUGTE ID FÜR JEDES LBM-DE-POLYGON
print("Baumbedeckungsfläche an LBM-DE anhängen über ID")
arcpy.management.JoinField(lbm_Stadt_sing, "ID", tabl_kl_3_4_8_9, "VALUE")
lbm_Stadt_Baumbed = output_gdb_2 + "\\lbm_Stadt_Baumbed"
arcpy.conversion.FeatureClassToFeatureClass(lbm_Stadt_sing, output_gdb_2, "lbm_Stadt_Baumbed")

print("Felder im ursprünglichen LBM-DE-Datensatz nach dem Join wieder bereinigen")
FCfields = [f.name for f in arcpy.ListFields(lbm_Stadt_sing)]
nicht_loeschen = ['AREA', 'Baumbed_Area', 'BD', 'ID', 'CLC_num', 'CLC_st1', 'Cellcode50000', 'CellCode', 'FID_grid_50000_complete', 'SHAPE_Leng', 
                  'CLC18', 'METHOD_AKT', 'LBMDE_ID', 'ZUS_AKT', 'VEG_AKT', 'SIE_AKT', 'LN_AKT','LB_AKT', 'LAND', 'Shape_Length', 'Shape_Area', 'Shape', 'OBJECTID_1']
Felder_loeschen = list(set(FCfields) - set(nicht_loeschen))
arcpy.DeleteField_management(lbm_Stadt_sing, Felder_loeschen)

# BERECHNUNG DES PROZENTUALEN ANTEILS DER BAUMBEDECKUNG (FLÄCHE DER BAUMBEDECKUNG IM LBM-DE-POLYGON/GESAMTFLÄCHE DES POLYGONS*100)
print("Ein neues Feld erstellen, in dem der Anteil der Baumbedeckung berechnet wird")
if len(arcpy.ListFields(lbm_Stadt_Baumbed, "Baumbed_Ant")) > 0:
    print("FELD SCHON VORHANDEN")
else:
    arcpy.AddField_management(lbm_Stadt_Baumbed, "Baumbed_Ant", "DOUBLE", "","", "", "", "NULLABLE", "", "")
print("Berechnung des prozentualen Anteils der Baumbedeckung")
arcpy.management.CalculateField(lbm_Stadt_Baumbed, "Baumbed_Ant", "(!Baumbed_Area!/!AREA!)*100", "PYTHON3")

# AUS DEM PROZENTUALEN ANTEIL DER BAUMBEDECKUNG KANN FÜR JEDES POLYGON DIE BAUMANTEILSKLASSEN ERMITTELT WERDEN ...
# ... DIE BAUMANTEILSKLASSE IST NACH ZARDO ET AL. (2017) FOLGENDERMASSEN FESTGELEGT: 0, 20, 40, 60, 80, 100 PROZENT.
# ... !  ACHTUNG, der oberste Wert (im Moment 151) muss bei der Berechnung für Gesamtdeutschland eventuell nochmal angepasst werden ! ...
print("Erstellen eines Feldes in dem die Baumanteilsklasse zugewiesen wird")
if len(arcpy.ListFields(lbm_Stadt_Baumbed, "Baumbed_Klasse")) > 0:
    print("Feld schon vorhanden")
else:
    arcpy.AddField_management(lbm_Stadt_Baumbed, "Baumbed_Klasse", "LONG", "","", "", "", "NULLABLE", "", "")

# Baumanteilswerten zwischen >=80 und 100 (und darüber hinaus, Werte über 100 entstehen durch grobe Rasterauflösung des Stadtgrünrasters), 
# werden der Klasse "100" zugewiesen
# Anteilswerten zwischen 60 und 80 werden der Klasse "80" zugewiesen

# 20: bis 20 Prozent
# 40: bis 40 Prozent
# 60: bis 60 Prozent
# 80: bis 80 Prozent
# 100: bis 100 Prozent

with arcpy.da.UpdateCursor(lbm_Stadt_Baumbed, ["Baumbed_Ant"]) as cursor:
    for row in cursor:
        if row[0] == None:
            row[0] = 0
            cursor.updateRow(row)
    del row, cursor

expression = "test(!Baumbed_Ant!, !Baumbed_Klasse!)"
codeblock = """def test(Anteil, Klasse):
    if Anteil >= 80:
        return 100
    elif Anteil > 60 and Anteil <= 80:
        return 80
    elif Anteil > 40 and Anteil <= 60:
        return 60
    elif Anteil > 20 and Anteil <= 40:
        return 40
    elif Anteil >= 0 and Anteil <= 20:
        return 20"""

arcpy.CalculateField_management(lbm_Stadt_Baumbed, "Baumbed_Klasse", expression, "", codeblock)

# EINSCHRÄNKUNG DES VERFAHRENS: DIE BAUMANTEILSBERECHNUNG AUS DEM RASTERDATENSATZ DES STADTGRÜNS IST UNGENAU
# DA EINE ÜBERTRAGUNG DER GROBEN RASTERWERTE AUF DEN GENAUEREN VEKTORDATENSATZ DES LBM-DE STATTFINDET.
# AUF DIESE WEISE KOMMT ES TEILWEISE BEI SEHR KLEINEN LBM-DE-POLYGONEN ZU BAUMBEDECKUNGSANTEILEN ÜBER 100 PROZENT
# DESWEGEN WIRD UNTERSUCHT, OB DIE ELIMINIERUNG (EINGLIEDERUNG VON FLÄCHEN GRÖSSER 100 KM2) DIESE FEHLER ETWAS BEHEBEN KANN

# EVENTUELL KÖNNTE MAN DEN BERECHNETEN BAUMBEDECKUNGSANTEIL MIT DER MITGELIEFERTEN SPALTE ZUM VEGETATIONSANTEIL IM LBM-DE NOCHMAL ABGLEICHEN

# ERMITTLUNG DER FLÄCHENGRÖSSE ÜBER 2 HEKTAR / UNTER 2 HEKTAR
# Dies wird nur für unversiegelte Flächen gemacht (Offener Boden, heterogen, Wasser, Gras, Wald) 

# 1) dissolven aller benachbarter Flächen, die nicht versiegelt sind, daraus eine Flächengröße ermitteln und zuweisen, ob diese dissolvte Fläche unter 2 ha (Wert 0) 
# und über 2 ha (Wert 1) groß ist
# 2) anschließend die Information über die (dissolvte)  Flächengröße (0,1) den einzelnen (undissolvten Flächen) als neue Spalte anhängen (Spalte unter 2ha/über2ha)
# 3) anschließend über die Spalte unter 2ha/über2ha und  die Spalte des Baumanteils der einzelnen Flächen den CCA-Wert zuweisen über Funktion "UpdateCursor"

print("Extraktion der unversiegelten LBM-DE-Flächen")
BD_unversiegelt = output_gdb_2 + "\\BD_unversiegelt"
arcpy.Select_analysis(lbm_Stadt_Baumbed, BD_unversiegelt, "BD NOT IN ('V')")

print("Dissolven der unversiegelten Flächen")
BD_unversiegelt_dis = output_gdb_2 + "\\BD_unversiegelt_dis"
arcpy.analysis.PairwiseDissolve(BD_unversiegelt, BD_unversiegelt_dis, "BD", "", "SINGLE_PART")

# Feld hinzufügen mit der Information ob die Fläche über 2 ha oder unter 2 ha groß ist
print("Feld hinzufügen mit der Information ob über 2ha oder unter 2 ha")
if len(arcpy.ListFields(BD_unversiegelt_dis, "Ueber2ha_unter2ha")) > 0:
    print("Feld schon vorhanden")
else:
    arcpy.AddField_management(BD_unversiegelt_dis, "Ueber2ha_unter2ha", "LONG", "","", "", "", "NULLABLE", "", "")

with arcpy.da.UpdateCursor(BD_unversiegelt_dis, ['Shape_Area', 'Ueber2ha_unter2ha']) as cursorCLC:
    for rowCLC in cursorCLC:
        if rowCLC[0] < 20000:        # Flächen unter 2 ha (20.000 m²) erhalten Wert "0"
            rowCLC[1] = 0
        elif rowCLC[0] > 20000:      # Flächen über 2 ha (20.000 m²) erhalten Wert "1"
            rowCLC[1] = 1

        cursorCLC.updateRow(rowCLC)
    del rowCLC, cursorCLC

# Selektion von Flächen von Flächen über 2 ha in BD_unversiegelt_dis (Select-Funktion)
print("Selektion der dissolvten Flächen, die größer sind als 2 Hektar")
BD_unversiegelt_dis_2ha = output_gdb_2 + "\\BD_unversiegelt_2ha"
arcpy.Select_analysis(BD_unversiegelt_dis, BD_unversiegelt_dis_2ha, "Ueber2ha_unter2ha = 1")
arcpy.management.DeleteField(BD_unversiegelt_dis_2ha, "BD")

# über Identity die Spalten von Selektierten 2ha Flächen an lbm_Stadt_Baumbed anhängen
# wurde getestet, indem die durch die Identity-Funktion gekennzeichneten Flächen in lbm_Stadt_Baumbed mit der Flächengröße
# der selektierten Flächen aus dem dissolven Feature verglichen wurden

lbm_Stadt_Baumbed_2ha = output_gdb_2 + "\\lbm_stadt_Baumbedeck_2ha"
arcpy.analysis.Identity(lbm_Stadt_Baumbed, BD_unversiegelt_dis_2ha, lbm_Stadt_Baumbed_2ha, "ALL", "", "NO_RELATIONSHIPS")

lbm_Stadt_Baumbed_2ha_sing = output_gdb_2 + "\\lbm_Stadt_Baumbedeck_2ha_sing"
arcpy.management.MultipartToSinglepart(lbm_Stadt_Baumbed_2ha, lbm_Stadt_Baumbed_2ha_sing)


# Versiegelten Flächen größer als 2 ha den Wert 1 zuordnen
with arcpy.da.UpdateCursor(lbm_Stadt_Baumbed_2ha_sing, ['Shape_Area', 'BD', 'Ueber2ha_unter2ha']) as cursorCLC:
    for rowCLC in cursorCLC:
        if rowCLC[0] < 20000 and rowCLC[1] == 'V':        # Flächen unter 2 ha (20.000 m²) erhalten Wert "0"
            rowCLC[2] = 0
        elif rowCLC[0] > 20000 and rowCLC[1] == 'V':      # Flächen über 2 ha (20.000 m²) erhalten Wert "1"
            rowCLC[2] = 1

        cursorCLC.updateRow(rowCLC)
    del rowCLC, cursorCLC

# Feld für Kühlkapazität anhängen (CCA)
print("Feld für Wert des Climate Cooling Assessments anhängen CCA")
if len(arcpy.ListFields(lbm_Stadt_Baumbed_2ha_sing, "CCA")) > 0:
    print("Feld schon vorhanden")
else:
    arcpy.AddField_management(lbm_Stadt_Baumbed_2ha_sing, "CCA", "LONG", "","", "", "", "NULLABLE", "", "")

# Kühlkapazitätswerte zuweisen
# Abweichend von Zardo erhalten versiegelte Flächen mit 0-20 Prozent Baumbedeckung ungeachtet von ihrer Größe immer den Wert 11, statt 20

expression_CCA = "test(!Baumbed_Klasse!, !BD!, !Ueber2ha_unter2ha!)"
codeblock_CCA = """def test(Baumbed_Klasse, Bodenbed, Ueber_2ha):
    if Baumbed_Klasse == 20 and Bodenbed == 'V' and Ueber_2ha == 0:
        return 11
    elif Baumbed_Klasse == 20 and Bodenbed == 'O' and Ueber_2ha == 0:
        return 18
    elif Baumbed_Klasse == 20 and Bodenbed == 'H' and Ueber_2ha == 0:
        return 19
    elif Baumbed_Klasse == 20 and Bodenbed == 'G' and Ueber_2ha == 0:
        return 19
    elif Baumbed_Klasse == 20 and Bodenbed == 'WS' and Ueber_2ha == 0:
        return 20
    elif Baumbed_Klasse == 20 and Bodenbed == 'WL' and Ueber_2ha == 0:
        return 55

    elif Baumbed_Klasse == 40 and Bodenbed == 'V' and Ueber_2ha == 0:
        return 22
    elif Baumbed_Klasse == 40 and Bodenbed == 'O' and Ueber_2ha == 0:
        return 27
    elif Baumbed_Klasse == 40 and Bodenbed == 'H' and Ueber_2ha == 0:
        return 28
    elif Baumbed_Klasse == 40 and Bodenbed == 'G' and Ueber_2ha == 0:
        return 28
    elif Baumbed_Klasse == 40 and Bodenbed == 'WS' and Ueber_2ha == 0:
        return 28
    elif Baumbed_Klasse == 40 and Bodenbed == 'WL' and Ueber_2ha == 0:
        return 55

    elif Baumbed_Klasse == 60 and Bodenbed == 'V' and Ueber_2ha == 0:
        return 29
    elif Baumbed_Klasse == 60 and Bodenbed == 'O' and Ueber_2ha == 0:
        return 33
    elif Baumbed_Klasse == 60 and Bodenbed == 'H' and Ueber_2ha == 0:
        return 36
    elif Baumbed_Klasse == 60 and Bodenbed == 'G' and Ueber_2ha == 0:
        return 37
    elif Baumbed_Klasse == 60 and Bodenbed == 'WS' and Ueber_2ha == 0:
        return 37
    elif Baumbed_Klasse == 60 and Bodenbed == 'WL' and Ueber_2ha == 0:
        return 55

    elif Baumbed_Klasse == 80 and Bodenbed == 'V' and Ueber_2ha == 0:
        return 37
    elif Baumbed_Klasse == 80 and Bodenbed == 'O' and Ueber_2ha == 0:
        return 44
    elif Baumbed_Klasse == 80 and Bodenbed == 'H' and Ueber_2ha == 0:
        return 46
    elif Baumbed_Klasse == 80 and Bodenbed == 'G' and Ueber_2ha == 0:
        return 46
    elif Baumbed_Klasse == 80 and Bodenbed == 'WS' and Ueber_2ha == 0:
        return 46
    elif Baumbed_Klasse == 80 and Bodenbed == 'WL' and Ueber_2ha == 0:
        return 55

    elif Baumbed_Klasse == 100 and Bodenbed == 'V' and Ueber_2ha == 0:
        return 55
    elif Baumbed_Klasse == 100 and Bodenbed == 'O' and Ueber_2ha == 0:
        return 55
    elif Baumbed_Klasse == 100 and Bodenbed == 'H' and Ueber_2ha == 0:
        return 55
    elif Baumbed_Klasse == 100 and Bodenbed == 'G' and Ueber_2ha == 0:
        return 55
    elif Baumbed_Klasse == 100 and Bodenbed == 'WS' and Ueber_2ha == 0:
        return 55
    elif Baumbed_Klasse == 100 and Bodenbed == 'WL' and Ueber_2ha == 0:
        return 55

    elif Baumbed_Klasse == 20 and Bodenbed == 'V' and Ueber_2ha == 1:
        return 11
    elif Baumbed_Klasse == 20 and Bodenbed == 'O' and Ueber_2ha == 1:
        return 65
    elif Baumbed_Klasse == 20 and Bodenbed == 'H' and Ueber_2ha == 1:
        return 68
    elif Baumbed_Klasse == 20 and Bodenbed == 'G' and Ueber_2ha == 1:
        return 70
    elif Baumbed_Klasse == 20 and Bodenbed == 'WS' and Ueber_2ha == 1:
        return 75
    elif Baumbed_Klasse == 20 and Bodenbed == 'WL' and Ueber_2ha == 1:
        return 100

    elif Baumbed_Klasse == 40 and Bodenbed == 'V' and Ueber_2ha == 1:
        return 40
    elif Baumbed_Klasse == 40 and Bodenbed == 'O' and Ueber_2ha == 1:
        return 74
    elif Baumbed_Klasse == 40 and Bodenbed == 'H' and Ueber_2ha == 1:
        return 76
    elif Baumbed_Klasse == 40 and Bodenbed == 'G' and Ueber_2ha == 1:
        return 78
    elif Baumbed_Klasse == 40 and Bodenbed == 'WS' and Ueber_2ha == 1:
        return 81
    elif Baumbed_Klasse == 40 and Bodenbed == 'WL' and Ueber_2ha == 1:
        return 100

    elif Baumbed_Klasse == 60 and Bodenbed == 'V' and Ueber_2ha == 1:
        return 60
    elif Baumbed_Klasse == 60 and Bodenbed == 'O' and Ueber_2ha == 1:
        return 83
    elif Baumbed_Klasse == 60 and Bodenbed == 'H' and Ueber_2ha == 1:
        return 84
    elif Baumbed_Klasse == 60 and Bodenbed == 'G' and Ueber_2ha == 1:
        return 85
    elif Baumbed_Klasse == 60 and Bodenbed == 'WS' and Ueber_2ha == 1:
        return 87
    elif Baumbed_Klasse == 60 and Bodenbed == 'WL' and Ueber_2ha == 1:
        return 100

    elif Baumbed_Klasse == 80 and Bodenbed == 'V' and Ueber_2ha == 1:
        return 80
    elif Baumbed_Klasse == 80 and Bodenbed == 'O' and Ueber_2ha == 1:
        return 91
    elif Baumbed_Klasse == 80 and Bodenbed == 'H' and Ueber_2ha == 1:
        return 92
    elif Baumbed_Klasse == 80 and Bodenbed == 'G' and Ueber_2ha == 1:
        return 93
    elif Baumbed_Klasse == 80 and Bodenbed == 'WS' and Ueber_2ha == 1:
        return 94
    elif Baumbed_Klasse == 80 and Bodenbed == 'WL' and Ueber_2ha == 1:
        return 100

    elif Baumbed_Klasse == 100 and Bodenbed == 'V' and Ueber_2ha == 1:
        return 100
    elif Baumbed_Klasse == 100 and Bodenbed == 'O' and Ueber_2ha == 1:
        return 100
    elif Baumbed_Klasse == 100 and Bodenbed == 'H' and Ueber_2ha == 1:
        return 100
    elif Baumbed_Klasse == 100 and Bodenbed == 'G' and Ueber_2ha == 1:
        return 100
    elif Baumbed_Klasse == 100 and Bodenbed == 'WS' and Ueber_2ha == 1:
        return 100
    elif Baumbed_Klasse == 100 and Bodenbed == 'WL' and Ueber_2ha == 1:
        return 100
    else:
        return 0"""

arcpy.CalculateField_management(lbm_Stadt_Baumbed_2ha_sing, "CCA", expression_CCA, "", codeblock_CCA)

# Dissolven der Klassen über 80, diese erhalten einen Puffer von 100 METERN
CCA_groesser_80 = output_gdb_3 + "\\CCA_groesser_80"
arcpy.Select_analysis(lbm_Stadt_Baumbed_2ha_sing, CCA_groesser_80, "CCA > 80")

print("Dissolven der unversiegelten Flächen über 80")
CCA_groesser_80_dis = output_gdb_3 + "\\CCA_groesser_80_dis"
arcpy.analysis.PairwiseDissolve(CCA_groesser_80, CCA_groesser_80_dis, "", "", "SINGLE_PART")

print("Selektieren von Flächen grösser 2 ha")
CCA_groesser_80_2ha_dis = output_gdb_3 + "\\CCA_groesser_80_2ha_dis"
arcpy.Select_analysis(CCA_groesser_80_dis, CCA_groesser_80_2ha_dis, "Shape_Area >= 20000")

print("Puffern")
CCA_groesser_80_dis_puf = output_gdb_3 + "\\CCA_groesser_80_dis_puf_100"
arcpy.analysis.Buffer(CCA_groesser_80_2ha_dis, CCA_groesser_80_dis_puf, 100, "OUTSIDE_ONLY", "", "ALL", "", "PLANAR")

# Flächen innerhalb der Puffer selektieren
print("intersect")
lbm_Stadt_puf = output_gdb_3 + "\\lbm_Stadt_puf"
arcpy.analysis.Intersect([lbm_Stadt_Baumbed_2ha_sing, CCA_groesser_80_dis_puf], lbm_Stadt_puf, "ALL", "", "INPUT")

print("Repair")
arcpy.management.RepairGeometry(lbm_Stadt_puf, "DELETE_NULL", "")

print("Multipart to Singlepart")
lbm_Stadt_puf_sing = output_gdb_3 + "\\lbm_Stadt_puf_sing"
arcpy.management.MultipartToSinglepart(lbm_Stadt_puf, lbm_Stadt_puf_sing)

# Feld für Kühlkapazität anhängen (CCA)
print("Feld für Wert des Climate Cooling Assessments anhängen CCA")
if len(arcpy.ListFields(lbm_Stadt_puf_sing, "CCA_puf")) > 0:
    print("Feld schon vorhanden")
else:
    arcpy.AddField_management(lbm_Stadt_puf_sing, "CCA_puf", "LONG", "", "", "", "", "NULLABLE", "", "")

# Flächen im Bereich des Puffers mit CCA-Werten kleiner 81 erhalten eine Erhöhung des CCA-Wertes um 20 (der CCA-Wert verfügt über keine Kommastelle)
# Flächen mit CCA-Werten über 81 im Bereich des Puffers wird kein neuer Wert zugewiesen, sie behalten ihren alten Wert
with arcpy.da.UpdateCursor(lbm_Stadt_puf_sing, ['CCA', 'CCA_puf']) as cursorCLC:
    for rowCLC_CCA80 in cursorCLC:
        if rowCLC_CCA80[0] < 81:
            rowCLC_CCA80[1] = rowCLC_CCA80[0] + 20
        else:
            rowCLC_CCA80[1] = rowCLC_CCA80[0]
        cursorCLC.updateRow(rowCLC_CCA80)
    #del rowCLC_CCA80, cursorCLC

# Füge die gepufferten Flächen mit den Restflächen zusammen, radiere dazu die gepufferten Flächen aus dem Urpsrungsdatensatz weg (erase)
# Füge anschließend das radierte Feature mit dem gepufferten Feature zusammen (merge)
# Übertrage dort, wo sich keine Pufferflächen befinden den CCA-Wert der ursprünglichen Flächen in die CCA-Puf_Spalte

lbm_Stadt_erase = output_gdb_3 + "\\lbm_Stadt_erase"
arcpy.analysis.Erase(lbm_Stadt_Baumbed_2ha_sing, lbm_Stadt_puf_sing, lbm_Stadt_erase, "")

lbm_Stadt_merge = output_gdb_3 + "\\lbm_Stadt_merge"
arcpy.management.Merge([lbm_Stadt_erase, lbm_Stadt_puf_sing], lbm_Stadt_merge, "", "")

lbm_Stadt_merge_sing = output_gdb_3 + "\\lbm_Stadt_merge_sing"
arcpy.management.MultipartToSinglepart(lbm_Stadt_merge, lbm_Stadt_merge_sing)

expression_CCA_puf = "test(!CCA_puf!, !CCA!)"
codeblock_CCA_puf = """def test(CCA_puf, CCA):
    if CCA_puf == None:
        return CCA
    else:
        return CCA_puf"""

arcpy.CalculateField_management(lbm_Stadt_merge_sing, "CCA_puf", expression_CCA_puf, "", codeblock_CCA_puf)

# Durchschnittlichen gewichteten Mittelwert der Kühlkapazität für jede Stadt berechnen
print("ID der Städte anhängen")
lbm_Stadt_merge_AGS = output_gdb_3 + "\\lbm_Stadt_merge_AGS"
arcpy.analysis.Intersect([lbm_Stadt_merge_sing, vg_25_sel_Stadt_UA], lbm_Stadt_merge_AGS, "ALL", "", "INPUT")

lbm_Stadt_merge_AGS_sing = output_gdb_3 + "\\lbm_Stadt_merge_AGS_sing"
arcpy.management.MultipartToSinglepart(lbm_Stadt_merge_AGS, lbm_Stadt_merge_AGS_sing)

# Feld berechnen mit gewichteten CCA-Werten x Fläche
print("Feld für nach Flächengröße gewichtete CCA-Werte anhängen")
if len(arcpy.ListFields(lbm_Stadt_merge_AGS_sing, "CCA_Area")) > 0:
    print("Feld schon vorhanden")
else:
    arcpy.AddField_management(lbm_Stadt_merge_AGS_sing, "CCA_Area", "DOUBLE", "", "", "", "", "NULLABLE", "", "")
arcpy.management.CalculateField(lbm_Stadt_merge_AGS_sing, "CCA_Area", "(!CCA_puf!*!Shape_Area!)", "PYTHON3")

print("für jede Stadt die Summe der gewichteten CCA-Werte und der Flächengröße zusammen addieren ")
tab_CCA_gew_Area = output_gdb_3 + "\\tab_CCA_gew_Area"
stat_fields_1 = [['CCA_Area', 'Sum'], ['Shape_Area', 'Sum']]
case_fields_1 = ['GEN']               # 'GEN':  ID-Feld der Städte aus VG 25
arcpy.Statistics_analysis(lbm_Stadt_merge_AGS_sing, tab_CCA_gew_Area, stat_fields_1, case_fields_1)

# Feld berechnen mit gewichteten Mittelwert der CCA-Werte je Stadt
print("Feld berechnen mit gewichteten Mittelwerten der CCA-Werte je Stadt")
if len(arcpy.ListFields(tab_CCA_gew_Area, "CCA_Mean_gew")) > 0:
    print("Feld schon vorhanden")
else:
    arcpy.AddField_management(tab_CCA_gew_Area, "CCA_Mean_gew", "DOUBLE", "", "", "", "", "NULLABLE", "", "")
arcpy.management.CalculateField(tab_CCA_gew_Area, "CCA_Mean_gew", "(!SUM_CCA_Area!/!SUM_Shape_Area!)", "PYTHON3")

print("die Ergebnistabelle mit den gewichteten CCA-Werten werden an das Feature mit den Gemeindegrenzen anhängen (VG25), um das Ergebnis grafisch darzustellen")
arcpy.management.JoinField(vg_25_sel_Stadt_UA, "GEN", tab_CCA_gew_Area, "GEN")
CCA_gew_Area_vg25_GEM_Selektion_Stadt = output_gdb_3 + "\\CCA_gew_Area_vg25_GEM"
arcpy.CopyFeatures_management(vg_25_sel_Stadt_UA, CCA_gew_Area_vg25_GEM_Selektion_Stadt)

# ANGEHÄNGTE FELDER WERDEN IM DATENSATZ VG_25_sel_Stadt_UA WIEDER ENTFERNT, DAMIT NICHT BEI JEDEM DURCHGANG DES SKRIPTES 
# MEHR UND MEHR ZUSÄTZLICHE SPALTEN ANGEHÄNGT WERDEN
print("angehängte Felder im ursprünglichen VG_25_sel_Stadt_UA-Datensatz wieder löschen")
FCfields = [f.name for f in arcpy.ListFields(vg_25_sel_Stadt_UA)]
nicht_loeschen = ['ADE', 'GF', 'BSG', 'RS', 'AGS', 'SDV_RS', 'GEN', 'BEZ', 'IBZ', 'BEM', 'NBD', 'SN_L', 'SN_R', 'SN_K', 'SN_V1', 'SN_V2', 'SN_G',
                  'FK_S3', 'NUTS', 'RS_0', 'AGS_0', 'WSK', 'Shape_Length', 'Shape_Area', 'Shape', 'OBJECTID_1']
Felder_loeschen = list(set(FCfields) - set(nicht_loeschen))
arcpy.DeleteField_management(vg_25_sel_Stadt_UA, Felder_loeschen)


# EINWOHNERANZAHL MIT EINBEZIEHEN
    # Zusammenfassung der Berechnung:
    # Verschneiden des Einwohnergrids mit dem Kühlkapazitätsdatensatz
    # Einwohneranzahl innerhalb der durch die Verschneidung zerteilten Grid-Zellen neu ermitteln
    # Berechnung der Einwohneranteile, die in oder im 200 m Pufferumkreis von Flächen mit guter bis sehr guter Kühlung leben
    # Flächen mit guter bis sehr guter Kühlung zählen zu der CCA-Klasse 80-100, dies entspricht den CCA-Werten 61-100 )
    # die Berechnung der Einwohneranteile geschieht für jede Stadt seperat

lbm_Stadt_EW = output_gdb_3 + "\\lbm_Stadt_EW"
arcpy.analysis.Intersect([lbm_Stadt_merge_sing, Einwohnergrid], lbm_Stadt_EW, "ALL", "", "INPUT")

lbm_Stadt_EW_sing = output_gdb_3 + "\\lbm_Stadt_EW_sing"
arcpy.management.MultipartToSinglepart(lbm_Stadt_EW, lbm_Stadt_EW_sing)

# Feld für korrigierte Einwohneranzahl anhängen
print("Feld für korrgierte Anzahl der Einwohner anhängen, da Gridzellen aus Einwohnerraster durch intersect mit LBM-DE in kleinere Einheiten zerteilt wurde")
if len(arcpy.ListFields(lbm_Stadt_EW_sing, "EW_kor")) > 0:
    print("Feld schon vorhanden")
else:
    arcpy.AddField_management(lbm_Stadt_EW_sing, "EW_kor", "DOUBLE", "","", "", "", "NULLABLE", "", "")

# Berechnung des Anteils der Bevölkerung innerhalb der kleineren Einheiten der Gridzellen
# 10.000 steht für die Größe der Gridzelle (100x100m)
# Die ursprüngliche Einwohnerzahl innerhalb der 100x100m Zellen steht in Zelle "grid_code"
arcpy.CalculateField_management(lbm_Stadt_EW_sing, "EW_kor", "(!Shape_Area!/10000)*!grid_code!", "PYTHON3")

# Feld für CCA-Klasse anlegen
print("Feld für CCA-Klasse anlegen")
if len(arcpy.ListFields(lbm_Stadt_EW_sing, "CCA_Klasse")) > 0:
    print("Feld schon vorhanden")
else:
    arcpy.AddField_management(lbm_Stadt_EW_sing, "CCA_Klasse", "LONG", "","", "", "", "NULLABLE", "", "")

# CCA-Klasse zuweisen (20, 40, 60, 80, 100)
print("CCA-Klasse berechnen")
expression = "test(!CCA_puf!, !CCA_Klasse!)"
codeblock = """def test(CCA, CCA_Klasse):
    if CCA >= 80 and CCA <= 100:
        return 100
    elif CCA > 60 and CCA <= 80:
        return 80
    elif CCA > 40 and CCA <= 60:
        return 60
    elif CCA > 20 and CCA <= 40:
        return 40
    elif CCA >= 0 and CCA <= 20:
        return 20"""
arcpy.CalculateField_management(lbm_Stadt_EW_sing, "CCA_Klasse", expression, "", codeblock)

# die Berechnung der Einwohneranteile innerhalb der jeweiligen CCA-Klassen wird für jede Stadt separat ausgerechnet
# daher wird eine ID für jede Stadt an jedes Feature angehangen (Feld 'GEN' aus VG 25)
print("ID der Städte anhängen")
lbm_Stadt_EW_AGS = output_gdb_3 + "\\lbm_Stadt_EW_AGS"
arcpy.analysis.Intersect([lbm_Stadt_EW_sing, vg_25_sel_Stadt_UA], lbm_Stadt_EW_AGS, "ALL", "", "INPUT")

print("für jede Stadt die Summe der Einwohner je CCA-Klasse zusammen addieren ")
tab_EW_CCA = output_gdb_3 + "\\tab_EW_CCA"
stat_fields_1 = [['EW_kor', 'Sum']]
case_fields_1 = ['GEN', 'CCA_Klasse']               # 'GEN':  ID-Feld der Städte aus VG 25
arcpy.Statistics_analysis(lbm_Stadt_EW_AGS, tab_EW_CCA, stat_fields_1, case_fields_1)

print("für jede Stadt insgesamt die Summe des Einwohner, ungeachtet der CCA-Klasse, zusammen addieren")
tab_EW_AGS = output_gdb_3 + "\\tab_EW_AGS"
stat_fields_2 = [['EW_kor', 'Sum']]
case_field_2 = ['GEN']
arcpy.Statistics_analysis(lbm_Stadt_EW_AGS, tab_EW_AGS, stat_fields_2, case_field_2)

print("das Feld mit der 'Einwohneranzahl je CCA-Stufe je Stadt'  mit dem Feld zur 'Gesamteinwohnerzahl insgesamt' in einen Datensatz zusammenführen")
arcpy.management.JoinField(tab_EW_CCA, "GEN", tab_EW_AGS, "GEN")
tab_EW_CCA_AGS = output_gdb_3 + "\\tab_EW_CCA_AGS"
arcpy.conversion.TableToTable(tab_EW_CCA, output_gdb_3, "tab_EW_CCA_AGS", "", "", "")

print("Feld für ANTEIL DER EINWOHNER für jede CCA-Klasse erzeugen")
if len(arcpy.ListFields(tab_EW_CCA_AGS, "EW_Ant_CCA")) > 0:
    print("Feld schon vorhanden")
else:
    arcpy.AddField_management(tab_EW_CCA_AGS, "EW_Ant_CCA", "DOUBLE", "","", "", "", "NULLABLE", "", "")

# FELD "SUM_EW_kor": SUMME DER EINWOHNER AUS DEN KLASSEN
# FELD "SUM_EW_kor_1": SUMME DER EINWOHNER INSGESAMT IN DER STADT
arcpy.CalculateField_management(tab_EW_CCA_AGS, "EW_Ant_CCA", "(!SUM_EW_kor!/!SUM_EW_kor_1!)*100", "PYTHON3")

# Selektion der Einwohner, die sich in gut bis sehr gut gekühlten Gebieten aufhalten (entpricht Klasse 80 und Klasse 100, 
# das sind die Kühlkapazitätswerte von 61 bis 100)
print("nur die Flächen selektieren, denen eine Kühlkapazitäts-Klasse von 61 - 100 zugewiesen wurde (entspricht gut bis sehr gut gekühlten Flächen)")
tab_EW_Ant_CCA_AGS_CCA_80_und_mehr = output_gdb_3 + "\\tab_EW_Ant_AGS_CCA_80_und_mehr"
arcpy.analysis.TableSelect(tab_EW_CCA_AGS, tab_EW_Ant_CCA_AGS_CCA_80_und_mehr, "CCA_Klasse >= 80")

print("die Einwohneranteile der CCA-Klassen 80 und 100 zusammen addieren, jeweils für jede Stadt")
tab_EW_CCA_80_und_mehr = output_gdb_3 + "\\tab_EW_CCA_80_und_mehr"
stat_fields_3 = [['EW_Ant_CCA', 'Sum']]
case_field_3 = ['GEN']                                  # 'GEN':  ID-Feld der Städte aus VG 25
arcpy.Statistics_analysis(tab_EW_Ant_CCA_AGS_CCA_80_und_mehr, tab_EW_CCA_80_und_mehr, stat_fields_3, case_field_3)

print("die Ergebnistabelle mit den Einwohneranteilen an das Feature mit den Gemeindegrenzen anhängen (VG25), um das Ergebnis grafisch darzustellen")
arcpy.management.JoinField(vg_25_sel_Stadt_UA, "GEN", tab_EW_CCA_80_und_mehr, "GEN")
CCA_80_u_mehr_Ant_EW_vg25_GEM_Selektion_Stadt = output_gdb_3 + "\\CCA_80_u_mehr_Ant_EW_vg25_GEM"
arcpy.CopyFeatures_management(vg_25_sel_Stadt_UA, CCA_80_u_mehr_Ant_EW_vg25_GEM_Selektion_Stadt)

# ANGEHÄNGTE FELDER WERDEN IM DATENSATZ VG_25_sel_Stadt_UA WIEDER ENTFERNT, DAMIT NICHT BEI JEDEM DURCHGANG DES SKRIPTES 
# MEHR UND MEHR ZUSÄTZLICHE SPALTEN ANGEHÄNGT WERDEN
print("angehängte Felder im ursprünglichen VG_25_sel_Stadt_UA-Datensatz wieder löschen")
FCfields = [f.name for f in arcpy.ListFields(vg_25_sel_Stadt_UA)]
nicht_loeschen = ['ADE', 'GF', 'BSG', 'RS', 'AGS', 'SDV_RS', 'GEN', 'BEZ', 'IBZ', 'BEM', 'NBD', 'SN_L', 'SN_R', 'SN_K', 'SN_V1', 'SN_V2', 'SN_G',
                  'FK_S3', 'NUTS', 'RS_0', 'AGS_0', 'WSK', 'Shape_Length', 'Shape_Area', 'Shape', 'OBJECTID_1']
Felder_loeschen = list(set(FCfields) - set(nicht_loeschen))
arcpy.DeleteField_management(vg_25_sel_Stadt_UA, Felder_loeschen)

print("Berechnung abgeschlossen")
