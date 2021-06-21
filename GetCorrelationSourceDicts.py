def GetCorrelationSourceDicts(df_p,df_m,x_data,genes,subtypes):
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
    source_dict2 = {}
    source_dict3 = {}
    source_dict4 = {}

    source_dict1['x'] = x_data
    source_dict1['py'] = df_p.loc[gene_plot[0]]
    source_dict1['my'] = df_m.loc[gene_plot[0]]
    source_dict1['gene'] = np.repeat('Gene 1',len(x_data))

    source_dict2['x'] = x_data
    source_dict2['py'] = df_p.loc[gene_plot[1]]
    source_dict2['my'] = df_m.loc[gene_plot[1]]
    source_dict2['gene'] = np.repeat('Gene 2',len(x_data))

    source_dict3['x'] = x_data
    source_dict3['py'] = df_p.loc[gene_plot[2]]
    source_dict3['my'] = df_m.loc[gene_plot[2]]
    source_dict3['gene'] = np.repeat('Gene 3',len(x_data))

    source_dict4['x'] = x_data
    source_dict4['py'] = df_p.loc[gene_plot[3]]
    source_dict4['my'] = df_m.loc[gene_plot[3]]
    source_dict4['gene'] = np.repeat('Gene 4',len(x_data))

    return(source_dict1,source_dict2,source_dict3,source_dict4,gene_plot)
