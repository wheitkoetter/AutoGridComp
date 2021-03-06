import qgis
import PyQt4
from PyQt4 import QtGui
from qgis.gui import *
from qgis.core import *

# Prepare processing import (source: https://gis.stackexchange.com/questions/129513/accessing-processing-with-python/129974#129974) 
import sys 
sys.path.append('/usr/share/qgis/python/plugins') # command for avoiding errors at importing function below
from processing.core.Processing import Processing

import glob
import os

from PyQt4 import QtCore

import csv

QgsMapLayerRegistry.instance().removeAllMapLayers()

path=ui_path
sys.path.append(path) # command for avoiding errors at importing function below
from mathematical_characterisation import mathematical_characterisation
#from plot_both_graphs_in_one_figure import plot_both_graphs_in_one_figure # commented out, because function uses pandas and this can lead to an error (https://github.com/qgis/QGIS/issues/30446)


####################################
######### input parameters #########
####################################

# booleans from checkboxes in GUI
check_onl_charac_sing=ui_check_onl_charac_sing
check_two_grids=ui_check_two_grids
check_visual=ui_check_visual
check_mathematical=ui_check_mathematical
check_electrical=ui_check_electrical

input_network_name=ui_input_network_name#'scigrid_germany_15012017'
target_network_name=ui_target_network_name

### vertices file
dist_input_file=ui_dist_input_file # needed for "open" commands
dist_input_file_ext=''+dist_input_file+'?delimiter=%s&quote=%s&crs=epsg:3857&wktField=%s' % (",","'",ui_input_vertices_geom) # needed for "create vector layer" commands
dist_input_file_name='vertices_'+input_network_name+''
dist_input_field=ui_dist_input_field#unique id of input layer from which distances shall be calculated
join_inputField=dist_input_field
input_vert_volt_colu=ui_input_vert_volt_colu
input_vert_freq_colu=ui_input_vert_freq_colu

dist_target_file=ui_dist_target_file
dist_target_file_ext=''+dist_target_file+'?delimiter=%s&quote=%s&crs=epsg:3857&wktField=%s' % (",","'",ui_target_vertices_geom)
dist_target_file_name='vertices_'+target_network_name+''
dist_target_field=ui_dist_target_field #id of target layer to which distances shall be calculated
targ_vert_volt_colu=ui_target_vert_volt_colu
targ_vert_freq_colu=ui_target_vert_freq_colu

#matrix options
dist_matrix_type=0
dist_nearest_points=1

#join matrix
dist_matrix_file="/dist.csv"
dist_matrix_file_equiv_nodes="/dist_equiv_nodes.csv"
dist_matrix_name="dist"


### links
input_link_wkt=ui_input_link_wkt
links_input_file=ui_links_input_file
links_input_file_ext=''+links_input_file+'?delimiter=%s&quote=%s&crs=epsg:3857&wktField=%s' % (",","'",input_link_wkt)
links_input_file_name='links_'+input_network_name+''
input_link_volt_colu=ui_input_link_volt_colu
input_link_cable_colu=ui_input_link_cable_colu
input_link_wire_colu=ui_input_link_wire_colu
input_link_freq_colu=ui_input_link_freq_colu
input_link_l_id_colu=ui_input_link_l_id_colu
input_link_v_id1_colu=ui_input_link_v_id1_colu
input_link_v_id2_colu=ui_input_link_v_id2_colu
input_link_length=ui_input_link_length


links_target_wkt=ui_target_link_wkt
links_target_file=ui_links_target_file
links_target_file_ext=''+links_target_file+'?delimiter=%s&quote=%s&crs=epsg:3857&wktField=%s' % (",","'",links_target_wkt)
links_target_file_name='links_'+target_network_name+''
targ_link_volt_colu=ui_target_link_volt_colu
targ_link_cable_colu=ui_target_link_cable_colu
targ_link_wire_colu='wires'
targ_link_freq_colu=ui_target_link_freq_colu
targ_link_l_id_colu=ui_target_link_l_id_colu
targ_link_v_id1_colu=ui_target_link_v_id1_colu
targ_link_v_id2_colu=ui_target_link_v_id2_colu
targ_link_length=ui_target_link_length


###############################################
####### visual comparison #####################
###############################################

if check_visual:
    ############# distance matrix #################

    # open input csv
    dist_input_layer_intermediate=QgsVectorLayer(''+path+''+dist_input_file_ext+'', dist_input_file_name,"delimitedtext")

    # write to shp and open again, when vector layer build from csv --> error in alg qgis:distancematrix
    QgsVectorFileWriter.writeAsVectorFormat(dist_input_layer_intermediate,r''+path+'/intermediate_data/power_grid_1_vertices_auto_saved.shp',"utf-8",None,"ESRI Shapefile")    
    uri_input = ''+path+'/intermediate_data/power_grid_1_vertices_auto_saved.shp'
    dist_input_layer=QgsVectorLayer(uri_input, dist_input_file_name,"ogr")

    if check_two_grids:
        # open target csv, write to shp and open again
        dist_target_layer_intermediate=QgsVectorLayer(''+path+''+dist_target_file_ext+'', dist_target_file_name,"delimitedtext")
        QgsVectorFileWriter.writeAsVectorFormat(dist_target_layer_intermediate,r"/home/wilkohe/01_promo/08_model/06_autogridcomp/AutoGridComp_working_folder/intermediate_data/power_grid_2_vertices_auto_saved.shp","utf-8",None,"ESRI Shapefile")
        uri_target = ''+path+'/intermediate_data/power_grid_2_vertices_auto_saved.shp'
        dist_target_layer=QgsVectorLayer(uri_target, dist_target_file_name,'ogr')

        ### distance matrix
        processing.runalg('qgis:distancematrix', dist_input_layer, dist_input_field, dist_target_layer, dist_target_field, dist_matrix_type, dist_nearest_points, ''+path+''+dist_matrix_file+'')

        ### join distance matrix and input layer, from: http://gis.stackexchange.com/questions/133573/join-table-field-with-shapefile-programatically-via-pyqgis
        dist_matrix_file_modified='/dist_modified.csv'
        with open(''+path+''+dist_matrix_file+'','r') as csvinput:
            with open(''+path+''+dist_matrix_file_modified+'', 'w+') as csvoutput:
                writer = csv.writer(csvoutput, lineterminator='\n')
                reader = csv.reader(csvinput)
                
                row=next(reader)
                writer.writerow(row)
                for row in reader:
                    out_row=[]
                    if float(row[2])>=10:
                        out_row.append(row[0])
                        out_row.append(row[1])
                        out_row.append("{0:.0f}".format(float(row[2])))
                        #str("{0:.4f}".format(tot_length/1000))
                    else:
                        out_row.append(row[0])
                        out_row.append(row[1])                
                    writer.writerow(out_row)
        dist = QgsVectorLayer(''+path+''+dist_matrix_file_modified+'', dist_matrix_name, 'ogr')


        join_csvField='InputID'

        # add layers to registry for showing them on canvas
        QgsMapLayerRegistry.instance().addMapLayer(dist)
        QgsMapLayerRegistry.instance().addMapLayer(dist_input_layer)
        QgsMapLayerRegistry.instance().addMapLayer(dist_target_layer)
        
        
        # Set properties for the join
        joinObject = QgsVectorJoinInfo()
        joinObject.joinLayerId = dist.id()
        joinObject.joinFieldName = join_csvField
        joinObject.targetFieldName = join_inputField
        joinObject.memoryCache = True
        dist_input_layer.addJoin(joinObject)


        ### visualisation, from http://gis.stackexchange.com/questions/136526/how-to-add-label-to-qgsvectorlayer-by-python
        # adding labels
        qgis.utils.iface.setActiveLayer(dist_input_layer)
        dist_input_layer.setCustomProperty("labeling", "pal")
        dist_input_layer.setCustomProperty("labeling/enabled", "true")
        dist_input_layer.setCustomProperty("labeling/fontFamily", "Arial")
        dist_input_layer.setCustomProperty("labeling/fontSize", "10")
        dist_input_layer.setCustomProperty("labeling/fieldName", 'dist_Distance')
        dist_input_layer.setCustomProperty("labeling/placement", "2")
        dist_input_layer.setCustomProperty("labeling/decimals", 1)

    else:
        # show vertices of power grid 1, if no comparison to a second network is conducted
        QgsMapLayerRegistry.instance().addMapLayer(dist_input_layer)
        


    ### find equivalent paths in both networks
    if check_two_grids:
        # table with equal node ids
        with open(''+path+''+dist_matrix_file+'','r') as csvinput:
            with open(''+path+''+dist_matrix_file_equiv_nodes+'', 'w+') as csvoutput:
                writer = csv.writer(csvoutput, lineterminator='\n')
                reader = csv.reader(csvinput)
                all = []
                row = next(reader)
                row.append('equal_node_id')
                all.append(row)
                buffer=1000
                i=0
                for row in reader:
                    i=i+1
                    if float(row[2])<buffer:
                        row.append(row[0])
                        all.append(row)
                writer.writerows(all)
                
        # create table INPUT network nodes with equal node ids
        with open(''+path+''+dist_matrix_file_equiv_nodes+'', 'r') as csvoutput:
            with open(''+path+'/intermediate_data/input_eqno_id.csv', 'w+') as input_eqno_id_file:
                writer = csv.writer(input_eqno_id_file, lineterminator='\n')
                reader = csv.reader(csvoutput)
                all = []
                counter = next(reader)

                for row in reader:                
                    fields=[]
                    fields.append(row[0])
                    fields.append(row[3])
                    all.append(fields)
                writer.writerows(all)
                
        # create table TARGET network nodes with equal node ids        
        with open(''+path+''+dist_matrix_file_equiv_nodes+'', 'r') as csvoutput:    
            with open(''+path+'/intermediate_data/target_eqno_id.csv', 'w+') as input_eqno_id_file:
                writer = csv.writer(input_eqno_id_file, lineterminator='\n')
                reader = csv.reader(csvoutput)
                all = []
                counter = next(reader)

                for row in reader:                
                    fields=[]
                    fields.append(row[1])
                    fields.append(row[3])
                    all.append(fields)
                writer.writerows(all)
                

        # create table INPUT network links with equal node ids 
        with open(''+path+''+links_input_file+'','r') as edge_list:
            with open(''+path+'/intermediate_data/input_eqno_id.csv', 'r') as input_eqno_id_file:
                with open(''+path+'/intermediate_data/input_links_eqno_id.csv', 'w+') as input_links_eqno_id_file:
                    writer = csv.writer(input_links_eqno_id_file, lineterminator='\n',delimiter=',', quotechar="'")
                    reader1 = csv.DictReader(edge_list,delimiter=',', quotechar="'")
                    reader2 = csv.reader(input_eqno_id_file,delimiter=',', quotechar="'")

                    v_id1=9999999
                    eq_no_id1=999999
                    v_id2=9999999
                    eq_no_id2=999999

                    all = []

                    writer.writerow(['l_id','v_id1','eq_no_id1','v_id2','eq_no_id2','wkt_srid_3857'])
                    
                    reader2_dict = dict((reader2))
                    
                    for row1 in reader1:
                        fields=[]
                        l_id=row1[input_link_l_id_colu]
                        if str(row1[input_link_v_id1_colu]) in reader2_dict:
                            v_id1=row1[input_link_v_id1_colu]
                            eq_no_id1=int(reader2_dict[row1[input_link_v_id1_colu]])
                        else:
                            v_id1=row1[input_link_v_id1_colu]
                            eq_no_id1='no equal node id'
                            
                        if str(row1[input_link_v_id2_colu]) in reader2_dict:
                            v_id2=row1[input_link_v_id2_colu]
                            eq_no_id2=int(reader2_dict[row1[input_link_v_id2_colu]])
                        else:
                            v_id2=row1[input_link_v_id2_colu]
                            eq_no_id2='no equal node id'
                        
                        fields.append(l_id)
                        fields.append(v_id1)
                        fields.append(eq_no_id1)
                        fields.append(v_id2)
                        fields.append(eq_no_id2)
                        fields.append(row1[input_link_wkt])
                        all.append(fields)
                    writer.writerows(all)

        # create table TARGET network links with equal node ids 
        with open(''+path+''+links_target_file+'','r') as edge_list:
            with open(''+path+'/intermediate_data/target_eqno_id.csv', 'r') as target_eqno_id_file:
                with open(''+path+'/intermediate_data/target_links_eqno_id.csv', 'w+') as target_links_eqno_id_file:
                    writer = csv.writer(target_links_eqno_id_file, lineterminator='\n',delimiter=',', quotechar="'")
                    reader1 = csv.DictReader(edge_list,delimiter=',', quotechar="'")
                    reader2 = csv.reader(target_eqno_id_file,delimiter=',', quotechar="'")
                    v_id1=9999999
                    eq_no_id1=999999
                    v_id2=9999999
                    eq_no_id2=999999
                    all = []

                    writer.writerow(['branch_id','v_id1','eq_no_id1','v_id2','eq_no_id2','wkt_srid_3857'])
                    reader2_dict = dict((reader2))

                    
                    for row1 in reader1:
                        fields=[]
                        branch_id=row1[targ_link_l_id_colu]

                        if str(row1[targ_link_v_id1_colu]) in reader2_dict:
                            v_id1=row1[targ_link_v_id1_colu]
                            eq_no_id1=int(reader2_dict[row1[targ_link_v_id1_colu]])
                        else:
                            v_id1=row1[targ_link_v_id1_colu]
                            eq_no_id1='no equal node id'

                        if str(row1[targ_link_v_id2_colu]) in reader2_dict:
                            v_id2=row1[targ_link_v_id2_colu]
                            eq_no_id2=int(reader2_dict[row1[targ_link_v_id2_colu]])
                        else:
                            v_id2=row1[targ_link_v_id2_colu]
                            eq_no_id2='no equal node id'
                        fields.append(branch_id)
                        fields.append(v_id1)
                        fields.append(eq_no_id1)
                        fields.append(v_id2)
                        fields.append(eq_no_id2)
                        fields.append(row1[links_target_wkt])
                        all.append(fields)
                    writer.writerows(all)

        # find equal links
        buffer_string=str(buffer)
        with open(''+path+'/intermediate_data/target_links_eqno_id.csv', 'r') as target_links_eqno_id_file:
            with open(''+path+'/intermediate_data/input_links_eqno_id.csv', 'r') as input_links_eqno_id_file:
                with open(''+path+'/results/equal_links_buffer_'+buffer_string+'m_'+input_network_name+'_'+target_network_name+'.csv', 'w+') as equal_links:
                    writer = csv.writer(equal_links, lineterminator='\n',delimiter=',', quotechar="'")
                    reader1 = csv.reader(target_links_eqno_id_file,delimiter=',', quotechar="'")
                    reader2 = csv.reader(input_links_eqno_id_file,delimiter=',', quotechar="'")
                    row=next(reader1)
                    target_eqn=dict()
                    writer.writerow(['equal_node_id_1','equal_node_id_2','link_id_input','link_id_target', 'input_wkt_srid_3857', 'target_wkt_srid_3857'])
                    
                    for row1 in reader1: # building dictionary of dictionaries with equal nodes of target file for faster query
                        new_key=(row1[2],row1[4])
                        new_value={'l_id':row1[0],'wkt_srid_3857':row1[5]}
                        target_eqn[new_key]=new_value
                        fields.append(target_eqn[new_key]['wkt_srid_3857'])
                    all=[]
                    for row2 in reader2: # check whether links of input grid are included in target
                        new_key=(row2[2],row2[4])
                        new_key_inv=(row2[4],row2[2])
                        new_value=(row2[0])
                        if (new_key in target_eqn and row2[2] != 'no equal node id' and row2[4] != 'no equal node id'): # equal links and nodes with same order
                            fields=[]
                            fields.append(row2[2])
                            fields.append(row2[4])
                            fields.append(new_value)
                            fields.append(target_eqn[new_key]['l_id'])
                            fields.append(row2[5])
                            fields.append(target_eqn[new_key]['wkt_srid_3857'])
                            all.append(fields)
                        if (new_key_inv in target_eqn and row2[2] != 'no equal node id' and row2[4] != 'no equal node id'): # equal links but inverted order of nodes
                            fields=[]
                            fields.append(row2[2])
                            fields.append(row2[4])
                            fields.append(new_value)
                            fields.append(target_eqn[new_key_inv]['l_id'])
                            fields.append(row2[5])
                            fields.append(target_eqn[new_key_inv]['wkt_srid_3857'])
                            all.append(fields)
                    writer.writerows(all)

    ############# length calculation ######## http://gis.stackexchange.com/questions/168871/calculate-line-lengths-with-python-in-qgis

    length_layer_input=QgsVectorLayer(''+path+''+links_input_file_ext+'', links_input_file_name,'delimitedtext')
    QgsMapLayerRegistry.instance().addMapLayer(length_layer_input)
    qgis.utils.iface.setActiveLayer(length_layer_input)
    
    if check_two_grids:
        length_layer_target=QgsVectorLayer(''+path+''+links_target_file_ext+'', links_target_file_name,'delimitedtext')
        QgsMapLayerRegistry.instance().addMapLayer(length_layer_target)
        qgis.utils.iface.setActiveLayer(length_layer_target)

##############################################
## completeness of electrical properties #####
##############################################
if check_electrical:
	### input grid

    with open(''+path+'/results/electrical_properties_'+input_network_name+'.csv', 'w+') as elec_output:
        with open(''+path+''+links_input_file+'','r') as edge_list:
            with open(''+path+''+dist_input_file+'','r') as vertices_list:
                reader1 = csv.DictReader(edge_list,delimiter=',', quotechar="'")
                reader2 = csv.DictReader(vertices_list,delimiter=',', quotechar="'")
                writer = csv.writer(elec_output, lineterminator='\n',delimiter=',',quotechar="'")
    
                # links
                counter=0            
                voltage_counter=0
                cables_counter=0
                wires_counter=0
                freq_counter=0
                complete_counter=0
                for row in reader1:
                    counter=counter+1
                    if row[input_link_volt_colu] not in (None,""):
                        voltage_counter=voltage_counter+1
                    if row[input_link_cable_colu] not in (None,""):
                        cables_counter=cables_counter+1
                    if row[input_link_wire_colu] not in (None,""):
                        wires_counter=wires_counter+1
                    if row[input_link_freq_colu] not in (None,""):
                        freq_counter=freq_counter+1
                    if (row[input_link_volt_colu] not in (None,"")) and (row[input_link_cable_colu] not in (None,"")) and (row[input_link_wire_colu] not in (None,"")) and (row[input_link_freq_colu] not in (None,"")):
                        complete_counter=complete_counter+1
                        #"{0:.2f}".format(
                header=['electrical property','items holding this property [%]', 'items holding this property [absolute number]']
                voltage_percentage=['voltage (links)',"{0:.2f}".format(float(voltage_counter)/float(counter)*100), voltage_counter]
                cables_percentage=['cables (links)',"{0:.2f}".format(float(cables_counter)/float(counter)*100), cables_counter]
                wires_percentage=['wires (links)',"{0:.2f}".format(float(wires_counter)/float(counter)*100), wires_counter]
                freq_percentage=['frequency (links)',"{0:.2f}".format(float(freq_counter)/float(counter)*100), freq_counter]
                complete_percentage=['complete information (links)',"{0:.2f}".format(float(complete_counter)/float(counter)*100), complete_counter]
    
                writer.writerow(header)
                writer.writerow(voltage_percentage)
                writer.writerow(cables_percentage)
                writer.writerow(wires_percentage)
                writer.writerow(freq_percentage)
                writer.writerow(complete_percentage)
    
                # vertices
                counter=0            
                voltage_counter=0
                freq_counter=0
                complete_counter=0
                for row in reader2:
                    counter=counter+1
                    if row[input_vert_volt_colu] not in (None,""):
                        voltage_counter=voltage_counter+1
                    if row[input_vert_freq_colu] not in (None,""):
                        freq_counter=freq_counter+1
                    if (row[input_vert_volt_colu] not in (None,"")) and (row[input_vert_freq_colu] not in (None,"")):
                        complete_counter=complete_counter+1
                        
                voltage_percentage=['voltage (vertices)',"{0:.2f}".format(float(voltage_counter)/float(counter)*100), voltage_counter]
                freq_percentage=['frequency (vertices)',"{0:.2f}".format(float(freq_counter)/float(counter)*100), freq_counter]
                complete_percentage=['complete information (vertices)',"{0:.2f}".format(float(complete_counter)/float(counter)*100), complete_counter]
    
                writer.writerow([])
                writer.writerow(voltage_percentage)
                writer.writerow(freq_percentage)
                writer.writerow(complete_percentage)

	### target grid
        if check_two_grids:
            with open(''+path+'/results/electrical_properties_'+target_network_name+'.csv', 'w+') as elec_output:
                with open(''+path+''+links_target_file+'','r') as edge_list:
                    with open(''+path+''+dist_target_file+'','r') as vertices_list:
                        reader1 = csv.DictReader(edge_list,delimiter=',', quotechar="'")
                        reader2 = csv.DictReader(vertices_list,delimiter=',', quotechar="'")
                        writer = csv.writer(elec_output, lineterminator='\n',delimiter=',', quotechar="'")

                        # links
                        counter=0            
                        voltage_counter=0
                        cables_counter=0
                        wires_counter=0
                        freq_counter=0
                        complete_counter=0
                        for row in reader1:
                            counter=counter+1
                            if row[targ_link_volt_colu] not in (None,""):
                                voltage_counter=voltage_counter+1
                            if row[targ_link_cable_colu] not in (None,""):
                                cables_counter=cables_counter+1
                                if row[targ_link_wire_colu] not in (None,""):
                                    wires_counter=wires_counter+1
                            if row[targ_link_freq_colu] not in (None,""):
                                freq_counter=freq_counter+1
                            if (row[targ_link_volt_colu] not in (None,"")) and (row[targ_link_cable_colu] not in (None,"")) and (row[targ_link_freq_colu] not in (None,"")): #and (row[] not in (None,"")):
                                complete_counter=complete_counter+1

                        
                        header=['electrical property','items holding this property [%]', 'items holding this property [absolute number]']
                        voltage_percentage=['voltage (links)',"{0:.2f}".format(float(voltage_counter)/float(counter)*100), voltage_counter]
                        cables_percentage=['cables (links)',"{0:.2f}".format(float(cables_counter)/float(counter)*100), cables_counter]
                        wires_percentage=['wires (links)',"{0:.2f}".format(float(wires_counter)/float(counter)*100), wires_counter]
                        freq_percentage=['frequency (links)',"{0:.2f}".format(float(freq_counter)/float(counter)*100), freq_counter]
                        complete_percentage=['complete information (links)',"{0:.2f}".format(float(complete_counter)/float(counter)*100), complete_counter]
                        
                        writer.writerow(header)
                        writer.writerow(voltage_percentage)
                        writer.writerow(cables_percentage)
                        writer.writerow(wires_percentage)
                        writer.writerow(freq_percentage)
                        writer.writerow(complete_percentage)

                        # vertices
                        counter=0            
                        voltage_counter=0
                        freq_counter=0
                        complete_counter=0
                        for row in reader2:
                            counter=counter+1
                            if row[targ_vert_volt_colu] not in (None,""):
                                voltage_counter=voltage_counter+1
                            if row[targ_vert_freq_colu] not in (None,""):
                                freq_counter=freq_counter+1
                            if (row[targ_vert_volt_colu] not in (None,"")) and (row[targ_vert_freq_colu] not in (None,"")):
                                complete_counter=complete_counter+1
                                
                        voltage_percentage=['voltage (vertices)',"{0:.2f}".format(float(voltage_counter)/float(counter)*100), voltage_counter]
                        freq_percentage=['frequency (vertices)',"{0:.2f}".format(float(freq_counter)/float(counter)*100), freq_counter]
                        complete_percentage=['complete information (vertices)',"{0:.2f}".format(float(complete_counter)/float(counter)*100), complete_counter]
                        
                        writer.writerow([])
                        writer.writerow(voltage_percentage)
                        writer.writerow(freq_percentage)
                        writer.writerow(complete_percentage)

#############################################
######### mathematical criteria #############
#############################################

if check_mathematical:
    
    mathematical_characterisation(
    nw_name=input_network_name,
    nodes_list_file=dist_input_file,
    node_id_colu=dist_input_field,
    edges_list_file=links_input_file,
    input_link_v_id1_colu=input_link_v_id1_colu,
    input_link_v_id2_colu=input_link_v_id2_colu,
    input_link_length_colu=input_link_length,
    path=path)    
    
    
    if check_two_grids:
        
        mathematical_characterisation(
        nw_name=target_network_name,
        nodes_list_file=dist_target_file,
        node_id_colu=dist_target_field,
        edges_list_file=links_target_file,
        input_link_v_id1_colu=targ_link_v_id1_colu,
        input_link_v_id2_colu=targ_link_v_id2_colu,
        input_link_length_colu=targ_link_length,
        path=path)
        
        
#        plot_both_graphs_in_one_figure(path=path,nw_name=[input_network_name,target_network_name]) # commented out, because function uses pandas and this can lead to an error (https://github.com/qgis/QGIS/issues/30446)