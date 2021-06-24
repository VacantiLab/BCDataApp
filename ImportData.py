def ImportData():
    # import python packages
    import numpy as np
    import pandas as pd
    from pdb import set_trace

    # Import the sample annotations
    file_name_read = 'group_key.txt'
    Annotation = pd.read_csv('BCDataApp/DataFiles/group_key.txt',sep='\t',header='infer')

    #import the protein data
    data_p_file = 'data_p.txt'
    df_p = pd.read_csv('BCDataApp/DataFiles/' + data_p_file,sep='\t')
    df_p = ConvertDates(df_p) # Some gene symbols had been converted to dates at one point by excel. Convert them back.
    df_p.set_index('Gene', inplace=True)
    genes_p = sorted(list(df_p.index))

    #import the mRNA data
    data_m_file = 'data_m.txt'
    df_m = pd.read_csv('BCDataApp/DataFiles/' + data_m_file,sep='\t')
    df_m = ConvertDates(df_m) # Some gene symbols had been converted to dates at one point by excel. Convert them back.
    df_m.set_index('Gene', inplace=True)
    genes_m = sorted(list(df_m.index))

    #Get a list of the unique genes that are in the protein or mRNA sets
    genes = genes_p + genes_m
    genes = np.unique(genes)
    genes = np.ndarray.tolist(genes)

    # Specify subtypes and associated colors
    #     Subtypes have to agree with what is in the annotation file
    #subtypes = ['Basal','LumA','LumB','Her2','Norm']
    #subtype_colors = ['#E31A1C','#1F78B4','#A6CEE3','#FB9A99','#33A02C']
    subtypes = ['Basal','Her2','LumA','LumB','Norm']
    subtype_colors = ['#E31A1C','#FB9A99','#1F78B4','#A6CEE3','#33A02C']

    # Reorder the columns for plotting
    #     All basal columns, followed by all LumA columns, then all LumB colummns and so on in the order of the subtypes vector
    tumors = np.asarray(Annotation.loc[:,'Patient'])
    OrderedTumors = np.array([])
    for i in subtypes:
        SubtypeIndices = Annotation.loc[:,'Pam50'] == i
        SubtypeTumors = tumors[SubtypeIndices.tolist()]
        OrderedTumors = np.append(OrderedTumors,SubtypeTumors)
    df_p = df_p[OrderedTumors]
    df_m = df_m[OrderedTumors]

    tumors = list(df_m.columns)
    x_data = list()
    for i in np.arange(0,len(tumors)):
            PAM50_Index = Annotation.loc[:,'Patient'] == tumors[i]
            PAM50_Assignment = Annotation.loc[:,'Pam50'][PAM50_Index]
            PAM50_Assignment = PAM50_Assignment.to_string().split()[1]
            x_data.append((PAM50_Assignment,tumors[i]))

    return(df_p,df_m,x_data,genes,subtypes,subtype_colors)

################################################################################

def ConvertDates(DF):
    import pandas as pd
    from pdb import set_trace
    import numpy as np

    # Import the date-to-gene conversion file
    data_converstion_file = 'GeneDateConverstions.txt'
    df_conv = pd.read_csv('BCDataApp/DataFiles/' + data_converstion_file, sep='\t')
    df_conv.set_index('Date', inplace=True, drop=False)


    Dates = np.asarray(df_conv['Date'])
    Genes = np.asarray(DF['Gene'])

    for date in Dates:
        if date in Genes:
            DateIndex = np.where(Genes == date)[0]
            NewSymbol = df_conv.loc[date,'Current']
            Genes[DateIndex] = NewSymbol

    DF['Gene'] = Genes

    return(DF)
