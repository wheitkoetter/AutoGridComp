# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 16:17:29 2019

@author: wilkohe
"""
from matplotlib import pyplot as plt
import pandas as pd

def plot_both_graphs_in_one_figure(path,nw_name):
    
    plt.ioff()
    path_mat_crit_tabs=(path+'/results/mathematical_criteria/mathematical_criteria_tables/')
    mat_crit=['degree','clustering_coefficient_nodes','betweenness_centrality_edges']   
    mat_crit_file_name=['degree','clustering_coefficient','bce']
    distribution_type=['_PDF_','_CDF_']
    x_labels=['Degree (d)', 'Clustering coefficient (c)','Betweenness centrality (bce)']
    y_labels=[['Pr(d)','Pr(x>=d)'],['Pr(c)','Pr(x<=c)'],['Pr(bce)','Pr(x<=bce)']]
    
    for s in range(len(mat_crit)):
        for t in range(len(distribution_type)):
            df_list=[]    
            plt.close('all')
            fig, ax = plt.subplots()    
            for i in range(len(nw_name)):    
                df_list.append(pd.read_csv(
                (path_mat_crit_tabs+mat_crit[s]+
                '/'+mat_crit_file_name[s]+distribution_type[t]+nw_name[i]+'.csv'),index_col=0))
                ax.plot(df_list[i],label=nw_name[i])
            ax.legend(fancybox=True,framealpha=0.5)
            ax.set_xlabel(x_labels[s])
            ax.set_ylabel(y_labels[s][t])
            plt.savefig(path_mat_crit_tabs+mat_crit[s]+'/'+mat_crit_file_name[s]+distribution_type[t]+nw_name[0]+'_'+nw_name[1]+'.pdf') 
            
    plt.close('all')
    fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, figsize=(11, 15))
    
    ax_list=[[ax1, ax2],[ax3,ax4],[ax5,ax6]]
        
    for s in range(len(mat_crit)):
        for t in range(len(distribution_type)):
            df_list=[]    
                
            for i in range(len(nw_name)):    
                df_list.append(pd.read_csv(
                (path_mat_crit_tabs+mat_crit[s]+
                '/'+mat_crit_file_name[s]+distribution_type[t]+nw_name[i]+'.csv'),index_col=0))

                ax=ax_list[s][t]    
                ax.plot(df_list[i],label=nw_name[i], marker='o', markersize=3)
                
                ax.legend(fancybox=True,framealpha=0.5)            
            ax.set_title(mat_crit[s]+distribution_type[t])
            ax.set_xlabel(x_labels[s])
            ax.set_ylabel(y_labels[s][t])
            

    plt.savefig(path_mat_crit_tabs+'/all_network_criteria_distributions_overview.pdf')  
    plt.close('all')       