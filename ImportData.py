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
    df_p.set_index('Gene', inplace=True)
    tumors = np.array(df_p.columns)
    genes = sorted(list(df_p.index))

    #import the mRNA data
    data_m_file = 'data_m.txt'
    df_m = pd.read_csv('BCDataApp/DataFiles/' + data_m_file,sep='\t')
    df_m.set_index('Gene', inplace=True)

    # Specify subtypes and associated colors
    #     Subtypes have to agree with what is in the annotation file
    subtypes = ['Basal','LumA','LumB','Her2','Norm']
    subtype_colors = ['#E31A1C','#1F78B4','#A6CEE3','#FB9A99','#33A02C']

    # Reorder the columns for plotting
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
