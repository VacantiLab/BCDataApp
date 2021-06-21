def CreateMetSubAverageDFs(df_p,df_m):
    import numpy as np
    import pandas as pd

    tumors = np.array(df_p.columns)
    SubtypeCategory = 'metabolites_core_prot'
    MetSubtypes = ['LP','HP']

    file_name_read = 'group_key.txt'
    Annotation = pd.read_csv('BCDataApp/DataFiles/group_key.txt',sep='\t',header='infer')

    df_mp =

    # Reorder the columns for plotting
    OrderedTumors = np.array([])
    for i in MetSubtypes:
        SubtypeIndices = Annotation.loc[:,SubtypeCategory] == i
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
