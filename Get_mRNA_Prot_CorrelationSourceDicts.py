def Get_mRNA_Prot_CorrelationSourceDicts(df_p,df_m,x_data,genes,subtypes):
    # import python packages
    import numpy as np
    import pandas as pd
    from pdb import set_trace

    # set the initial genes to be viewed
    gene_plot = ['NDUFS2','NDUFS3','NDUFS7','blank']

    # create an entry for a "blank" gene
    blank_data = np.zeros(len(x_data))
    for i in range(0,len(blank_data)):
        blank_data[i] = np.nan
    df_p.loc['blank'] = blank_data
    df_m.loc['blank'] = blank_data

    # Create the dictionaries for each line on the protein plot and fill them with the initial values
    source_dict1 = {}

    source_dict1['x1'] = df_m.loc[gene_plot[0]]
    source_dict1['y1'] = df_p.loc[gene_plot[0]]

    source_dict1['x2'] = df_m.loc[gene_plot[1]]
    source_dict1['y2'] = df_p.loc[gene_plot[1]]

    source_dict1['x3'] = df_m.loc[gene_plot[2]]
    source_dict1['y3'] = df_p.loc[gene_plot[2]]

    source_dict1['x4'] = df_m.loc[gene_plot[3]]
    source_dict1['y4'] = df_p.loc[gene_plot[3]]

    return(source_dict1,gene_plot)
