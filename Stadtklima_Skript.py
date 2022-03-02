# -*- coding: iso-8859-1 -*-

# PYTHON-VERSION 3.6
# PROGRAMM: PYCHARM 2019.3.1

# INDIKATOR STADTKLIMA-REGULATION

# LITERATUR:
# Climate Cooling Assessment (CCA) von Zardo, L., Geneletti, D., P�rez-Soba, M. und van Eupen, M. (2017): Estimating the cooling capacity of green infrastructures to support urban planning. In: Ecosystem Services (26), 225-235.
# Moyzes (2020): Entwicklung eines Indikators zur Bewertung der �kosystemleistung "Klimaregulation" in St�dten. Masterarbeit Technische Universit�t Dresden, Fakult�t f�r Umweltwissenschaften, S.98.

# KURZBESCHREIBUNG DES INDIKATORS
# �ber den Bodenbedeckungstyp, den Anteil der Baumkronenbedeckung und der Fl�chengr��e wird ein K�hlungskapazit�tswert (CCA-Wert) in St�dten ab 50.000 Einwohnern ermittelt.
# Durch die Verschneidung von Einwohnerdaten mit der Information zur K�hlungskapazit�t mit kann ermittelt werden, wo Einwohner in welchem Ma� mit K�hlungsleistung durch urbanes Gr�n versorgt werden.
# Berechnet mit LBM-DE 2018, neue Version von 2021

# UMGEBUNGSEINSTELLUNGEN
import arcpy
import math
from arcpy import env
from arcpy.sa import *
arcpy.env.parallelProcessingFactor = "100%"
arcpy.env.overwriteOutput = True
arcpy.env.snapRaster = "E:/Meier/Stadtklima/Eingangsdaten.gdb/s2_2018_lcc_classes_1_8_atkismod_Dresden"
arcpy.env.snapRaster = "D:/tarox1_user5/OESL_P644_671/INSPIRE_Grid/inspire_grids_10.gdb/raster_10_complete" # INSPIRE-Grid mit 10x10m Rasterzellgr��e
arcpy.env.extent = "MAXOF"

# JAHR - ZEITSCHNITT
Jahr = "_2018"

# Geodatabases
Eingangsdaten_gdb = "E:/Meier/Stadtklima/Eingangsdaten.gdb"
output_gdb_1 = "E:/Meier/Stadtklima/output_1" + Jahr + ".gdb"
output_gdb_2 = "E:/Meier/Stadtklima/output_2" + Jahr + ".gdb"
output_gdb_3 = "E:/Meier/Stadtklima/output_3" + Jahr + ".gdb"

# Datens�tze
# lbm_DE = "E:/Meier/Stadtklima/Eingangsdaten.gdb/de_lbm_de_2018_r50000_Dresden_VG25_GEM_2016"
lbm_DE = "D:/tarox1_user5/OESL_P644_671/LBM/oriG/lbm_de_2018.gdb/lbm_de_2018_v2"
Einwohnergrid = "D:/tarox1_user5/OESL_P644_671/Einwohnerzahlen/zensus2011.gdb/grid_r100_zensus11ew"
    # Einwohnerraster in Vektorformat umwandeln:
        # 1) Raster to point
        # 2) Fishnet erzeugen mit Punkten aus 1) als 'Labels'
# Stadtgruenraster = "E:/Meier/Stadtklima/Eingangsdaten.gdb/s2_2018_lcc_classes_1_8_atkismod_Dresden"
Stadtgruenraster = "D:/tarox1_user5/OESL_P644_671/Stadtklima/Sentinel_II.gdb/s2_2018_lcc_classes_1_8_atkismod"
# Street_Tree = "D:/tarox1_user5/OESL_P644_671/Stadtklima/Street_Tree_Layer.gdb/Street_Tree_Layer_Dresden"
Street_Tree = "D:/tarox1_user5/OESL_P644_671/Urban_Atlas/Street_Tree_Layer_2018.gdb/UA_STL_2018"
vg25_GEM_Selektion_Stadt = "D:/tarox1_user5/OESL_P644_671/VG_ATKIS/VG_25/stadte_50000_ew.gdb/VG25_2016_join_50000EW"       # enth�lt St�dte ab 50.000 Einwohner
lyr = Eingangsdaten_gdb + "\\VG25_2016_join_50000EW.lyr"
Urban_Functional_Areas = "D:/tarox1_user5/OESL_P644_671/Urban_Atlas/Street_Tree_Layer_2018.gdb/UA_Boundary_STL_2018"




# ST�DTE AB 50.000 EINWOHNERN (AUS VG25) INNERHALB DER URBAN ATLAS FUNCTIONAL AREAS SELEKTIEREN
# �BER SELECT BY LOCATION
    # die Clip-Funktion w�rde in diesem Schritt nicht funktionieren, da man sonst kleine Splitter von VG25-Gemeinden mit selektieren w�rde, die eigentlich nicht
    # im Urban Atlas erfasst worden sind, aber teilweise in die Urban Functional Areas hineinragen. Daher wurde die Funktion "Select by location" genommen


# Street Tree Layer rastern - dann als neue Kategorie 9 einf�hren
# Priorit�t f�r Stadtgr�nmonitoring-Raster ist immer hoeher

print("Streettree-Layer in 10x10m Raster umwandeln und als Kategorie 9 in Stadtgr�nraster einf�gen")
print("Feld f�r  Kategorie 9 erstellen")
if len(arcpy.ListFields(Street_Tree, "Klasse")) > 0:
    print("Feld schon vorhanden")
else:
    arcpy.AddField_management(Street_Tree, "Klasse", "LONG", "","", "", "", "NULLABLE", "", "")
arcpy.CalculateField_management(Street_Tree, "Klasse", '9')

Street_Tree_rast = output_gdb_1 + "\\Street_Tree_rast"
arcpy.PolygonToRaster_conversion(Street_Tree, "Klasse", Street_Tree_rast, "MAXIMUM_COMBINED_AREA", "", 10)

# AUS DEM STADTGR�NMONITORING-RASTER DIE PIXEL EXTRAHIEREN WELCHE BAUM-INFORMATION ENTHALTEN: KLASSE 3: LAUBBAUM ,4: NADELBAUM)
print("Reklassifikation des Stadtgr�nmonitoring-Rasters")
path_recl_Stadtgruen_3_4 = output_gdb_1 + "\\Stadtgruenrast_3_4"
remap = RemapValue([[1, "NoData"], [2, "NoData"], [3, 3], [4, 4], [5, "NoData"], [6, "NoData"], [7, "NoData"], [8, "NoData"]])
out_raster = Reclassify(Stadtgruenraster, "Value", remap, "NoData")
out_raster.save(path_recl_Stadtgruen_3_4)

# AUS DEM STADTGR�NMONITORING-RASTER DIE PIXEL EXTRAHIEREN WELCHE BAUM-INFORMATION ENTHALTEN: 8: BEBAUT, STARK DURCHGR�NT)
print("Reklassifikation des Stadtgr�nmonitoring-Rasters")
path_recl_Stadtgruen_8 = output_gdb_1 + "\\Stadtgruenrast_8"
remap = RemapValue([[1, "NODATA"], [2, "NODATA"], [3, "NODATA"], [4, "NODATA"], [5, "NODATA"], [6, "NODATA"], [7, "NODATA"], [8, 8]])
out_raster = Reclassify(Stadtgruenraster, "Value", remap, "NODATA")
out_raster.save(path_recl_Stadtgruen_8)

# RASTER-DATENSATZ MIT BAUMINFORMATION: STREET TREE LAYER MIT BAUMDATEN AUS STADTGRUENRASTER ZUSAMMENF�GEN
# BEI UEBERLAGERUNGEN HABEN DIE BAUMDATEN AUS DEM STADTGRUENMONITORING LAYER DIE HOEHERE PRIORITAET, GEFOLGT VOM STREET TREE LAYER UND
# ABSCHLIESSEND DIE RASTERZELLEN BEBAUT-STARK DURCHGR�NT AUS DEM STADTGRUENRASTER
print("Street Tree Layer und Stadtgr�nraster zusammenf�gen")
path_Stadtgruen_Streettree = output_gdb_2 + "\\Stadtgruenrast_3_4_8_9"
mosaik_dataset = [path_recl_Stadtgruen_3_4, Street_Tree_rast, path_recl_Stadtgruen_8]
arcpy.management.MosaicToNewRaster(mosaik_dataset, output_gdb_2, "Stadtgruenrast_3_4_8_9", "", "4_BIT", "10", "1", "FIRST", "")

# ZIEL: RASTERUNG DES LBM-DES IN 10x10m RASTER (GLEICHE AUFL�SUNG, WIE DAS STADTGR�NRASTER)
# JEDEM RASTERPIXEL WURDE DER ID-WERT DES JEWEILIGEN LBM-DE-POLYGONS ZUGEWIESEN
print("ID f�r jedes Polygon im LBM-DE erstellen")
if len(arcpy.ListFields(lbm_Stadt_sing, "ID")) > 0:
    print("Feld schon vorhanden")
else:
    arcpy.AddField_management(lbm_Stadt_sing, "ID", "DOUBLE", "", "", "", "", "NULLABLE", "", "")
arcpy.CalculateField_management(lbm_Stadt_sing, "ID", '!OBJECTID_1!')


print("LBM-DE in 10x10m Raster umwandeln")
lbm_Stadt_ID_rast = output_gdb_1 + "\\lbm_stadt_rast"
arcpy.PolygonToRaster_conversion(lbm_Stadt_sing, "ID", lbm_Stadt_ID_rast, "MAXIMUM_COMBINED_AREA", "", 10)

# ERMITTELN WIEVIELE RASTERZELLEN DER KLASSE 3 (LAUBBAUM), 4 (NADELBAUM), 9 (Street Tree Layer) UND 8 (BEBAUT - STARK DURCHGR�NT) JEWEILS IN WELCHER LBM-DE FL�CHE LIEGEN UND...
# ... DIE FL�CHENGR�SSE BERECHNEN
# DIE ERGEBNISDATEI IST EINE TABELLE
print("Ermitteln wieviele Rasterzellen an B�umen und bebaut-stark durchgr�nt in welcher LBM-DE-Fl�che vorkommen")
tabl_kl_3_4_8_9 = output_gdb_1 + "\\tab_Stadtgruenrast_3_4_8_9"
TabulateArea(lbm_Stadt_ID_rast, "Value", path_Stadtgruen_Streettree, "Value", tabl_kl_3_4_8_9, "10", "CLASSES_AS_FIELDS")

print("F�r jede Klasse eine Spalte erstellen, in der die Fl�chengr��e berechnet wird (Anzahl der Zellen x 100m� (10x10m)")
# Fl�chengr��e berechnen f�r Klasse 3 (Auf Basis der Rasterfl�chen)
if len(arcpy.ListFields(tabl_kl_3_4_8_9, "VALUE_3_Area")) > 0:
    print("Feld schon vorhanden")
else:
    arcpy.AddField_management(tabl_kl_3_4_8_9, "VALUE_3_Area", "DOUBLE", "","", "", "", "NULLABLE", "", "")
arcpy.CalculateField_management(tabl_kl_3_4_8_9, "VALUE_3_Area", '!VALUE_3!', "PYTHON3")

# Fl�chengr��e berechnen f�r Klasse 4 (Auf Basis der Rasterfl�chen)
if len(arcpy.ListFields(tabl_kl_3_4_8_9, "VALUE_4_Area")) > 0:
    print("Feld schon vorhanden")
else:
    arcpy.AddField_management(tabl_kl_3_4_8_9, "VALUE_4_Area", "DOUBLE", "","", "", "", "NULLABLE", "", "")
arcpy.CalculateField_management(tabl_kl_3_4_8_9, "VALUE_4_Area", "!VALUE_4!", "PYTHON3")

# ANALYSEN MIT GR�NVOLUMENDATEN VON F�NF ST�DTEN ZEIGTEN, DASS DIE KLASSE 8 (BEBAUT, STARK DURCHGR�N) IM DURCHSCHNITT NUR 18 PROZENT BAUMBEDECKUNG BEINHALTET...
# ...DAHER WIRD DIE FL�CHENGR�SSE (10x10m = 100m�) DER KLASSE 8 MIT 0,18 MULTIPLIZIERT
# Fl�chengr��e berechnen f�r Klasse 8 (Auf Basis der Rasterfl�chen)
if len(arcpy.ListFields(tabl_kl_3_4_8_9, "VALUE_8_Area")) > 0:
    print("Feld schon vorhanden")
else:
    arcpy.AddField_management(tabl_kl_3_4_8_9, "VALUE_8_Area", "DOUBLE", "","", "", "", "NULLABLE", "", "")
arcpy.CalculateField_management(tabl_kl_3_4_8_9, "VALUE_8_Area", "!VALUE_8!*0.18", "PYTHON3")

# Fl�chengr��e berechnen f�r Klasse 9 (= Street Tree Layer)
if len(arcpy.ListFields(tabl_kl_3_4_8_9, "VALUE_9_Area")) > 0:
    print("Feld schon vorhanden")
else:
    arcpy.AddField_management(tabl_kl_3_4_8_9, "VALUE_9_Area", "DOUBLE", "","", "", "", "NULLABLE", "", "")
arcpy.CalculateField_management(tabl_kl_3_4_8_9, "VALUE_9_Area", "!VALUE_9!", "PYTHON3")

# ZUSAMMENRECHNEN DER BAUMBEDECKUNG (SUMME DER FL�CHENGR�SSE VON LAUBBAUM, NADELBAUM, 18-PROZENTIGER ANTEIL VON BEBAUT, STARK DURCHGR�NT)
print("Ein neues Feld erstellen in das die Gesamtfl�che der Baumbedeckung berechnet wird, alle Spalten der Klassenfl�chengr��en zusammenrechnen")
if len(arcpy.ListFields(tabl_kl_3_4_8_9, "Baumbed_Area")) > 0:
    print("Feld schon vorhanden")
else:
    arcpy.AddField_management(tabl_kl_3_4_8_9, "Baumbed_Area", "DOUBLE", "","", "", "", "NULLABLE", "", "")
arcpy.management.CalculateField(tabl_kl_3_4_8_9, "Baumbed_Area", "!VALUE_3_Area!+!VALUE_4_Area!+!VALUE_8_Area!+!VALUE_9_Area!", "PYTHON3")

# IM LBM-DE EINE UNVER�NDERLICHE SPALTE MIT DER FL�CHENGR�SSE ANLEGEN
if len(arcpy.ListFields(lbm_Stadt_sing, "AREA")) > 0:
    print("Feld schon vorhanden")
else:
    arcpy.AddField_management(lbm_Stadt_sing, "AREA", "DOUBLE", "","", "", "", "NULLABLE", "", "")
arcpy.management.CalculateField(lbm_Stadt_sing, "AREA", "!Shape_Area!", "PYTHON3")

# DIE WERTE ZUR BAUMBEDECKUNG AUS DEM STADTGR�NMONITORING-RASTER AN DAS LBM-DE ANH�NGEN �BER DIE ZU BEGINN ERZEUGTE ID F�R JEDES LBM-DE-POLYGON
print("Baumbedeckungsfl�che an LBM-DE anh�ngen �ber ID")
arcpy.management.JoinField(lbm_Stadt_sing, "ID", tabl_kl_3_4_8_9, "VALUE")
lbm_Stadt_Baumbed = output_gdb_2 + "\\lbm_Stadt_Baumbed"
arcpy.conversion.FeatureClassToFeatureClass(lbm_Stadt_sing, output_gdb_2, "lbm_Stadt_Baumbed")

print("Felder im urspr�nglichen LBM-DE-Datensatz nach dem Join wieder bereinigen")
FCfields = [f.name for f in arcpy.ListFields(lbm_Stadt_sing)]
nicht_loeschen = ['AREA', 'Baumbed_Area', 'BD', 'ID', 'CLC_num', 'CLC_st1', 'Cellcode50000', 'CellCode', 'FID_grid_50000_complete', 'SHAPE_Leng', 'CLC18', 'METHOD_AKT', 'LBMDE_ID', 'ZUS_AKT', 'VEG_AKT', 'SIE_AKT', 'LN_AKT','LB_AKT', 'LAND', 'Shape_Length', 'Shape_Area', 'Shape', 'OBJECTID_1']
Felder_loeschen = list(set(FCfields) - set(nicht_loeschen))
arcpy.DeleteField_management(lbm_Stadt_sing, Felder_loeschen)

# BERECHNUNG DES PROZENTUALEN ANTEILS DER BAUMBEDECKUNG (FL�CHE DER BAUMBEDECKUNG IM LBM-DE-POLYGON/GESAMTFL�CHE DES POLYGONS*100)
print("Ein neues Feld erstellen, in dem der Anteil der Baumbedeckung berechnet wird")
if len(arcpy.ListFields(lbm_Stadt_Baumbed, "Baumbed_Ant")) > 0:
    print("FELD SCHON VORHANDEN")
else:
    arcpy.AddField_management(lbm_Stadt_Baumbed, "Baumbed_Ant", "DOUBLE", "","", "", "", "NULLABLE", "", "")
print("Berechnung des prozentualen Anteils der Baumbedeckung")
arcpy.management.CalculateField(lbm_Stadt_Baumbed, "Baumbed_Ant", "(!Baumbed_Area!/!AREA!)*100", "PYTHON3")

# AUS DEM PROZENTUALEN ANTEIL DER BAUMBEDECKUNG KANN F�R JEDES POLYGON DIE BAUMANTEILSKLASSEN ERMITTELT WERDEN ...
# ... DIE BAUMANTEILSKLASSE IST NACH ZARDO ET AL. (2017) FOLGENDERMASSEN FESTGELEGT: 0, 20, 40, 60, 80, 100 PROZENT.
# ... !  ACHTUNG, der oberste Wert (im Moment 151) muss bei der Berechnung f�r Gesamtdeutschland eventuell nochmal angepasst werden ! ...
print("Erstellen eines Feldes in dem die Baumanteilsklasse zugewiesen wird")
if len(arcpy.ListFields(lbm_Stadt_Baumbed, "Baumbed_Klasse")) > 0:
    print("Feld schon vorhanden")
else:
    arcpy.AddField_management(lbm_Stadt_Baumbed, "Baumbed_Klasse", "LONG", "","", "", "", "NULLABLE", "", "")

# Baumanteilswerten zwischen >=80 und 100 (und dar�ber hinaus, Werte �ber 100 entstehen durch grobe Rasteraufl�sung des Stadtgr�nrasters), werden die Klasse "100" zugewiesen
# Anteilswerten zwischen 60 und 80 werden die Klasse "80" zugewiesen

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

# EINSCHR�NKUNG DES VERFAHRENS: DIE BAUMANTEILSBERECHNUNG AUS DEM RASTERDATENSATZ DES STADTGR�NS IST UNGENAU
# DA EINE �BERTRAGUNG DER GROBEN RASTERWERTE AUF DEN GENAUEREN VEKTORDATENSATZ DES LBM-DE STATTFINDET.
# AUF DIESE WEISE KOMMT ES TEILWEISE BEI SEHR KLEINEN LBM-DE-POLYGONEN ZU BAUMBEDECKUNGSANTEILEN �BER 100 PROZENT
# DESWEGEN WIRD UNTERSUCHT, OB DIE ELIMINIERUNG (EINGLIEDERUNG VON FL�CHEN GR�SSER 100 KM2) DIESE FEHLER ETWAS BEHEBEN KANN

# EVENTUELL K�NNTE MAN DEN BERECHNETEN BAUMBEDECKUNGSANTEIL MIT DER MITGELIEFERTEN SPALTE ZUM VEGETATIONSANTEIL IM LBM-DE NOCHMAL ABGLEICHEN

# ERMITTLUNG DER FL�CHENGR�SSE �BER 2 HEKTAR / UNTER 2 HEKTAR
# Dies wird nur f�r unversiegelte Fl�chen gemacht (Offener Boden, heterogen, Wasser, Gras, Wald)  ---> soll hier "heterogen" wirklich mit reingenommen werden?

# 1) dissolven aller benachbarter Fl�chen, die nicht versiegelt sind, daraus eine Fl�chengr��e ermitteln und zuweisen, ob diese dissolvte Fl�che unter 2 ha (Wert 0) und �ber 2 ha (Wert 1) gro� ist
# 2) anschlie�end die Information �ber die (dissolvte)  Fl�chengr��e (0,1) den einzelnen (undissolvten Fl�chen) als neue Spalte anh�ngen (Spalte unter 2ha/�ber2ha)
# 3) anschlie�end �ber die Spalte unter 2ha/�ber2ha und  die Spalte des Baumanteils der einzelnen Fl�chen den CCA-Wert zuweisen �ber Funktion "UpdateCursor"

print("Extraktion der unversiegelten LBM-DE-Fl�chen")
BD_unversiegelt = output_gdb_2 + "\\BD_unversiegelt"
arcpy.Select_analysis(lbm_Stadt_Baumbed, BD_unversiegelt, "BD NOT IN ('V')")

print("Dissolven der unversiegelten Fl�chen")
BD_unversiegelt_dis = output_gdb_2 + "\\BD_unversiegelt_dis"
arcpy.analysis.PairwiseDissolve(BD_unversiegelt, BD_unversiegelt_dis, "BD", "", "SINGLE_PART")

# Feld hinzuf�gen mit der Information ob die Fl�che �ber 2 ha oder unter 2 ha gro� ist
print("Feld hinzuf�gen mit der Information ob �ber 2ha oder unter 2 ha")
if len(arcpy.ListFields(BD_unversiegelt_dis, "Ueber2ha_unter2ha")) > 0:
    print("Feld schon vorhanden")
else:
    arcpy.AddField_management(BD_unversiegelt_dis, "Ueber2ha_unter2ha", "LONG", "","", "", "", "NULLABLE", "", "")

with arcpy.da.UpdateCursor(BD_unversiegelt_dis, ['Shape_Area', 'Ueber2ha_unter2ha']) as cursorCLC:
    for rowCLC in cursorCLC:
        if rowCLC[0] < 20000:        # Fl�chen unter 2 ha (20.000 m�) erhalten Wert "0"
            rowCLC[1] = 0
        elif rowCLC[0] > 20000:      # Fl�chen �ber 2 ha (20.000 m�) erhalten Wert "1"
            rowCLC[1] = 1

        cursorCLC.updateRow(rowCLC)
    del rowCLC, cursorCLC

# Selektion von Fl�chen von Fl�chen �ber 2 ha in BD_unversiegelt_dis (Select-Funktion)
print("Selektion der dissolvten Fl�chen, die gr��er sind als 2 Hektar")
BD_unversiegelt_dis_2ha = output_gdb_2 + "\\BD_unversiegelt_2ha"
arcpy.Select_analysis(BD_unversiegelt_dis, BD_unversiegelt_dis_2ha, "Ueber2ha_unter2ha = 1")
arcpy.management.DeleteField(BD_unversiegelt_dis_2ha, "BD")

# �ber Identity die Spalten von Selektierten 2ha Fl�chen an lbm_Stadt_Baumbed anh�ngen
# wurde getestet, indem die durch die Identity-Funktion gekennzeichneten Fl�chen in lbm_Stadt_Baumbed mit der Fl�chengr��e
# der selektierten Fl�chen aus dem dissolven Feature verglichen wurden

lbm_Stadt_Baumbed_2ha = output_gdb_2 + "\\lbm_stadt_Baumbedeck_2ha"
arcpy.analysis.Identity(lbm_Stadt_Baumbed, BD_unversiegelt_dis_2ha, lbm_Stadt_Baumbed_2ha, "ALL", "", "NO_RELATIONSHIPS")

lbm_Stadt_Baumbed_2ha_sing = output_gdb_2 + "\\lbm_Stadt_Baumbedeck_2ha_sing"
arcpy.management.MultipartToSinglepart(lbm_Stadt_Baumbed_2ha, lbm_Stadt_Baumbed_2ha_sing)


# Versiegelten Fl�chen gr��er als 2 ha den Wert 1 zuordnen
with arcpy.da.UpdateCursor(lbm_Stadt_Baumbed_2ha_sing, ['Shape_Area', 'BD', 'Ueber2ha_unter2ha']) as cursorCLC:
    for rowCLC in cursorCLC:
        if rowCLC[0] < 20000 and rowCLC[1] == 'V':        # Fl�chen unter 2 ha (20.000 m�) erhalten Wert "0"
            rowCLC[2] = 0
        elif rowCLC[0] > 20000 and rowCLC[1] == 'V':      # Fl�chen �ber 2 ha (20.000 m�) erhalten Wert "1"
            rowCLC[2] = 1

        cursorCLC.updateRow(rowCLC)
    del rowCLC, cursorCLC

# Feld f�r K�hlkapazit�t anh�ngen (CCA)
print("Feld f�r Wert des Climate Cooling Assessments anh�ngen CCA")
if len(arcpy.ListFields(lbm_Stadt_Baumbed_2ha_sing, "CCA")) > 0:
    print("Feld schon vorhanden")
else:
    arcpy.AddField_management(lbm_Stadt_Baumbed_2ha_sing, "CCA", "LONG", "","", "", "", "NULLABLE", "", "")

# K�hlkapazit�tswerte zuweisen
# Abweichend von Zardo erhalten versiegelte Fl�chen mit 0-20 Prozent Baumbedeckung ungeachtet von ihrer Gr��e immer den Wert 11, statt 20

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

# Dissolven der Klassen �ber 80, diese erhalten einen Puffer von 100 METERN
CCA_groesser_80 = output_gdb_3 + "\\CCA_groesser_80"
arcpy.Select_analysis(lbm_Stadt_Baumbed_2ha_sing, CCA_groesser_80, "CCA > 80")

print("Dissolven der unversiegelten Fl�chen �ber 80")
CCA_groesser_80_dis = output_gdb_3 + "\\CCA_groesser_80_dis"
arcpy.analysis.PairwiseDissolve(CCA_groesser_80, CCA_groesser_80_dis, "", "", "SINGLE_PART")

print("Selektieren von Fl�chen gr�sser 2 ha")
CCA_groesser_80_2ha_dis = output_gdb_3 + "\\CCA_groesser_80_2ha_dis"
arcpy.Select_analysis(CCA_groesser_80_dis, CCA_groesser_80_2ha_dis, "Shape_Area >= 20000")

print("Puffern")
CCA_groesser_80_dis_puf = output_gdb_3 + "\\CCA_groesser_80_dis_puf_100"
arcpy.analysis.Buffer(CCA_groesser_80_2ha_dis, CCA_groesser_80_dis_puf, 100, "OUTSIDE_ONLY", "", "ALL", "", "PLANAR")

# Fl�chen innerhalb der Puffer selektieren
print("intersect")
lbm_Stadt_puf = output_gdb_3 + "\\lbm_Stadt_puf"
arcpy.analysis.Intersect([lbm_Stadt_Baumbed_2ha_sing, CCA_groesser_80_dis_puf], lbm_Stadt_puf, "ALL", "", "INPUT")

print("Repair")
arcpy.management.RepairGeometry(lbm_Stadt_puf, "DELETE_NULL", "")

print("Multipart to Singlepart")
lbm_Stadt_puf_sing = output_gdb_3 + "\\lbm_Stadt_puf_sing"
arcpy.management.MultipartToSinglepart(lbm_Stadt_puf, lbm_Stadt_puf_sing)

# Feld f�r K�hlkapazit�t anh�ngen (CCA)
print("Feld f�r Wert des Climate Cooling Assessments anh�ngen CCA")
if len(arcpy.ListFields(lbm_Stadt_puf_sing, "CCA_puf")) > 0:
    print("Feld schon vorhanden")
else:
    arcpy.AddField_management(lbm_Stadt_puf_sing, "CCA_puf", "LONG", "", "", "", "", "NULLABLE", "", "")

# Fl�chen im Bereich des Puffers mit CCA-Werten kleiner 81 erhalten eine Erh�hung des CCA-Wertes um 20 (der CCA-Wert verf�gt �ber keine Kommastelle)
# Fl�chen mit CCA-Werten �ber 81 im Bereich des Puffers wird kein neuer Wert zugewiesen, sie behalten ihren alten Wert
with arcpy.da.UpdateCursor(lbm_Stadt_puf_sing, ['CCA', 'CCA_puf']) as cursorCLC:
    for rowCLC_CCA80 in cursorCLC:
        if rowCLC_CCA80[0] < 81:
            rowCLC_CCA80[1] = rowCLC_CCA80[0] + 20
        else:
            rowCLC_CCA80[1] = rowCLC_CCA80[0]
        cursorCLC.updateRow(rowCLC_CCA80)
    #del rowCLC_CCA80, cursorCLC

# F�ge die gepufferten Fl�chen mit den Restfl�chen zusammen, radiere dazu die gepufferten Fl�chen aus dem Urpsrungsdatensatz weg (erase)
# F�ge anschlie�end das radierte Feature mit dem gepufferten Feature zusammen (merge)
# �bertrage dort, wo sich keine Pufferfl�chen befinden den CCA-Wert der urspr�nglichen Fl�chen in die CCA-Puf_Spalte

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

# Durchschnittlichen gewichteten Mittelwert der K�hlkapazit�t f�r jede Stadt berechnen
print("ID der St�dte anh�ngen")
lbm_Stadt_merge_AGS = output_gdb_3 + "\\lbm_Stadt_merge_AGS"
arcpy.analysis.Intersect([lbm_Stadt_merge_sing, vg_25_sel_Stadt_UA], lbm_Stadt_merge_AGS, "ALL", "", "INPUT")

lbm_Stadt_merge_AGS_sing = output_gdb_3 + "\\lbm_Stadt_merge_AGS_sing"
arcpy.management.MultipartToSinglepart(lbm_Stadt_merge_AGS, lbm_Stadt_merge_AGS_sing)

# Feld berechnen mit gewichteten CCA-Werten x Fl�che
print("Feld f�r nach Fl�chengr��e gewichtete CCA-Werte anh�ngen")
if len(arcpy.ListFields(lbm_Stadt_merge_AGS_sing, "CCA_Area")) > 0:
    print("Feld schon vorhanden")
else:
    arcpy.AddField_management(lbm_Stadt_merge_AGS_sing, "CCA_Area", "DOUBLE", "", "", "", "", "NULLABLE", "", "")
arcpy.management.CalculateField(lbm_Stadt_merge_AGS_sing, "CCA_Area", "(!CCA_puf!*!Shape_Area!)", "PYTHON3")

print("f�r jede Stadt die Summe der gewichteten CCA-Werte und der Fl�chengr��e zusammen addieren ")
tab_CCA_gew_Area = output_gdb_3 + "\\tab_CCA_gew_Area"
stat_fields_1 = [['CCA_Area', 'Sum'], ['Shape_Area', 'Sum']]
case_fields_1 = ['GEN']               # 'GEN':  ID-Feld der St�dte aus VG 25
arcpy.Statistics_analysis(lbm_Stadt_merge_AGS_sing, tab_CCA_gew_Area, stat_fields_1, case_fields_1)

# Feld berechnen mit gewichteten Mittelwert der CCA-Werte je Stadt
print("Feld berechnen mit gewichteten Mittelwerten der CCA-Werte je Stadt")
if len(arcpy.ListFields(tab_CCA_gew_Area, "CCA_Mean_gew")) > 0:
    print("Feld schon vorhanden")
else:
    arcpy.AddField_management(tab_CCA_gew_Area, "CCA_Mean_gew", "DOUBLE", "", "", "", "", "NULLABLE", "", "")
arcpy.management.CalculateField(tab_CCA_gew_Area, "CCA_Mean_gew", "(!SUM_CCA_Area!/!SUM_Shape_Area!)", "PYTHON3")

print("die Ergebnistabelle mit den gewichteten CCA-Werten werden an das Feature mit den Gemeindegrenzen anh�ngen (VG25), um das Ergebnis grafisch darzustellen")
arcpy.management.JoinField(vg_25_sel_Stadt_UA, "GEN", tab_CCA_gew_Area, "GEN")
CCA_gew_Area_vg25_GEM_Selektion_Stadt = output_gdb_3 + "\\CCA_gew_Area_vg25_GEM"
arcpy.CopyFeatures_management(vg_25_sel_Stadt_UA, CCA_gew_Area_vg25_GEM_Selektion_Stadt)

# ANGEH�NGTE FELDER WERDEN IM DATENSATZ VG_25_sel_Stadt_UA WIEDER ENTFERNT, DAMIT NICHT BEI JEDEM DURCHGANG DES SKRIPTES MEHR UND MEHR ZUS�TZLICHE SPALTEN ANGEH�NGT WERDEN
print("angeh�ngte Felder im urspr�nglichen VG_25_sel_Stadt_UA-Datensatz wieder l�schen")
FCfields = [f.name for f in arcpy.ListFields(vg_25_sel_Stadt_UA)]
nicht_loeschen = ['ADE', 'GF', 'BSG', 'RS', 'AGS', 'SDV_RS', 'GEN', 'BEZ', 'IBZ', 'BEM', 'NBD', 'SN_L', 'SN_R', 'SN_K', 'SN_V1', 'SN_V2', 'SN_G','FK_S3', 'NUTS', 'RS_0', 'AGS_0', 'WSK', 'Shape_Length', 'Shape_Area', 'Shape', 'OBJECTID_1']
Felder_loeschen = list(set(FCfields) - set(nicht_loeschen))
arcpy.DeleteField_management(vg_25_sel_Stadt_UA, Felder_loeschen)


# EINWOHNERANZAHL MIT EINBEZIEHEN
    # Zusammenfassung der Berechnung:
    # Verschneiden des Einwohnergrids mit dem K�hlkapazit�tsdatensatz
    # Einwohneranzahl innerhalb der durch die Verschneidung zerteilten Grid-Zellen neu ermitteln
    # Berechnung der Einwohneranteile, die in oder im 200 m Pufferumkreis von Fl�chen mit guter bis sehr guter K�hlung leben
    # Fl�chen mit guter bis sehr guter K�hlung z�hlen zu der CCA-Klasse 80-100, dies entspricht den CCA-Werten 61-100 )
    # die Berechnung der Einwohneranteile geschieht f�r jede Stadt seperat

lbm_Stadt_EW = output_gdb_3 + "\\lbm_Stadt_EW"
arcpy.analysis.Intersect([lbm_Stadt_merge_sing, Einwohnergrid], lbm_Stadt_EW, "ALL", "", "INPUT")

lbm_Stadt_EW_sing = output_gdb_3 + "\\lbm_Stadt_EW_sing"
arcpy.management.MultipartToSinglepart(lbm_Stadt_EW, lbm_Stadt_EW_sing)

# Feld f�r korrigierte Einwohneranzahl anh�ngen
print("Feld f�r korrgierte Anzahl der Einwohner anh�ngen, da Gridzellen aus Einwohnerraster durch intersect mit LBM-DE in kleinere Einheiten zerteilt wurde")
if len(arcpy.ListFields(lbm_Stadt_EW_sing, "EW_kor")) > 0:
    print("Feld schon vorhanden")
else:
    arcpy.AddField_management(lbm_Stadt_EW_sing, "EW_kor", "DOUBLE", "","", "", "", "NULLABLE", "", "")

# Berechnung des Anteils der Bev�lkerung innerhalb der kleineren Einheiten der Gridzellen
# 10.000 steht f�r die Gr��e der Gridzelle (100x100m)
# Die urspr�ngliche Einwohnerzahl innerhalb der 100x100m Zellen steht in Zelle "grid_code"
arcpy.CalculateField_management(lbm_Stadt_EW_sing, "EW_kor", "(!Shape_Area!/10000)*!grid_code!", "PYTHON3")

# Feld f�r CCA-Klasse anlegen
print("Feld f�r CCA-Klasse anlegen")
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

# die Berechnung der Einwohneranteile innerhalb der jeweiligen CCA-Klassen wird f�r jede Stadt separat ausgerechnet
# daher wird eine ID f�r jede Stadt an jedes Feature angehangen (Feld 'GEN' aus VG 25)
print("ID der St�dte anh�ngen")
lbm_Stadt_EW_AGS = output_gdb_3 + "\\lbm_Stadt_EW_AGS"
arcpy.analysis.Intersect([lbm_Stadt_EW_sing, vg_25_sel_Stadt_UA], lbm_Stadt_EW_AGS, "ALL", "", "INPUT")

print("f�r jede Stadt die Summe der Einwohner je CCA-Klasse zusammen addieren ")
tab_EW_CCA = output_gdb_3 + "\\tab_EW_CCA"
stat_fields_1 = [['EW_kor', 'Sum']]
case_fields_1 = ['GEN', 'CCA_Klasse']               # 'GEN':  ID-Feld der St�dte aus VG 25
arcpy.Statistics_analysis(lbm_Stadt_EW_AGS, tab_EW_CCA, stat_fields_1, case_fields_1)

print("f�r jede Stadt insgesamt die Summe des Einwohner, ungeachtet der CCA-Klasse, zusammen addieren")
tab_EW_AGS = output_gdb_3 + "\\tab_EW_AGS"
stat_fields_2 = [['EW_kor', 'Sum']]
case_field_2 = ['GEN']
arcpy.Statistics_analysis(lbm_Stadt_EW_AGS, tab_EW_AGS, stat_fields_2, case_field_2)

print("das Feld mit der 'Einwohneranzahl je CCA-Stufe je Stadt'  mit dem Feld zur 'Gesamteinwohnerzahl insgesamt' in einen Datensatz zusammenf�hren")
arcpy.management.JoinField(tab_EW_CCA, "GEN", tab_EW_AGS, "GEN")
tab_EW_CCA_AGS = output_gdb_3 + "\\tab_EW_CCA_AGS"
arcpy.conversion.TableToTable(tab_EW_CCA, output_gdb_3, "tab_EW_CCA_AGS", "", "", "")

print("Feld f�r ANTEIL DER EINWOHNER f�r jede CCA-Klasse erzeugen")
if len(arcpy.ListFields(tab_EW_CCA_AGS, "EW_Ant_CCA")) > 0:
    print("Feld schon vorhanden")
else:
    arcpy.AddField_management(tab_EW_CCA_AGS, "EW_Ant_CCA", "DOUBLE", "","", "", "", "NULLABLE", "", "")

# FELD "SUM_EW_kor": SUMME DER EINWOHNER AUS DEN KLASSEN
# FELD "SUM_EW_kor_1": SUMME DER EINWOHNER INSGESAMT IN DER STADT
arcpy.CalculateField_management(tab_EW_CCA_AGS, "EW_Ant_CCA", "(!SUM_EW_kor!/!SUM_EW_kor_1!)*100", "PYTHON3")

# Selektion der Einwohner, die sich in gut bis sehr gut gek�hlten Gebieten aufhalten (entpricht Klasse 80 und Klasse 100, das sind die K�hlkapazit�tswerte von 61 bis 100)
print("nur die Fl�chen selektieren, denen eine K�hlkapazit�ts-Klasse von 61 - 100 zugewiesen wurde (entspricht gut bis sehr gut gek�hlten Fl�chen)")
tab_EW_Ant_CCA_AGS_CCA_80_und_mehr = output_gdb_3 + "\\tab_EW_Ant_AGS_CCA_80_und_mehr"
arcpy.analysis.TableSelect(tab_EW_CCA_AGS, tab_EW_Ant_CCA_AGS_CCA_80_und_mehr, "CCA_Klasse >= 80")

print("die Einwohneranteile der CCA-Klassen 80 und 100 zusammen addieren, jeweils f�r jede Stadt")
tab_EW_CCA_80_und_mehr = output_gdb_3 + "\\tab_EW_CCA_80_und_mehr"
stat_fields_3 = [['EW_Ant_CCA', 'Sum']]
case_field_3 = ['GEN']                                  # 'GEN':  ID-Feld der St�dte aus VG 25
arcpy.Statistics_analysis(tab_EW_Ant_CCA_AGS_CCA_80_und_mehr, tab_EW_CCA_80_und_mehr, stat_fields_3, case_field_3)

print("die Ergebnistabelle mit den Einwohneranteilen an das Feature mit den Gemeindegrenzen anh�ngen (VG25), um das Ergebnis grafisch darzustellen")
arcpy.management.JoinField(vg_25_sel_Stadt_UA, "GEN", tab_EW_CCA_80_und_mehr, "GEN")
CCA_80_u_mehr_Ant_EW_vg25_GEM_Selektion_Stadt = output_gdb_3 + "\\CCA_80_u_mehr_Ant_EW_vg25_GEM"
arcpy.CopyFeatures_management(vg_25_sel_Stadt_UA, CCA_80_u_mehr_Ant_EW_vg25_GEM_Selektion_Stadt)

# ANGEH�NGTE FELDER WERDEN IM DATENSATZ VG_25_sel_Stadt_UA WIEDER ENTFERNT, DAMIT NICHT BEI JEDEM DURCHGANG DES SKRIPTES MEHR UND MEHR ZUS�TZLICHE SPALTEN ANGEH�NGT WERDEN
print("angeh�ngte Felder im urspr�nglichen VG_25_sel_Stadt_UA-Datensatz wieder l�schen")
FCfields = [f.name for f in arcpy.ListFields(vg_25_sel_Stadt_UA)]
nicht_loeschen = ['ADE', 'GF', 'BSG', 'RS', 'AGS', 'SDV_RS', 'GEN', 'BEZ', 'IBZ', 'BEM', 'NBD', 'SN_L', 'SN_R', 'SN_K', 'SN_V1', 'SN_V2', 'SN_G','FK_S3', 'NUTS', 'RS_0', 'AGS_0', 'WSK', 'Shape_Length', 'Shape_Area', 'Shape', 'OBJECTID_1']
Felder_loeschen = list(set(FCfields) - set(nicht_loeschen))
arcpy.DeleteField_management(vg_25_sel_Stadt_UA, Felder_loeschen)

print("Berechnung abgeschlossen")
