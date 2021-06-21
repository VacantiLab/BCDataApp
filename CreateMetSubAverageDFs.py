def CreateMetSubAverageDFs(df_p,df_m):
    import numpy as np
    import pandas as pd
    from pdb import set_trace

    tumors = np.array(df_p.columns)
    SubtypeCategory = 'metabolites_core_prot'
    MetSubtypes = ['LP','HP']

    file_name_read = 'group_key.txt'
    Annotation = pd.read_csv('BCDataApp/DataFiles/group_key.txt',sep='\t',header='infer')

    # Reorder the columns for plotting
    #     The columns must be ordered with all of the low-proliferating tumors first and the high-proliferating tumors next
    tumors = np.asarray(Annotation.loc[:,'Patient'])
    OrderedTumors = np.array([])
    for i in MetSubtypes:
        SubtypeIndices = Annotation.loc[:,SubtypeCategory] == i
        SubtypeTumors = tumors[SubtypeIndices.tolist()]
        OrderedTumors = np.append(OrderedTumors,SubtypeTumors)
    df_p_met = df_p[OrderedTumors]
    df_m_met = df_m[OrderedTumors]

    x_data_met = list()
    for i in np.arange(0,len(OrderedTumors)):
            Subtype_Index = Annotation.loc[:,'Patient'] == OrderedTumors[i]
            Subtype_Assignment = Annotation.loc[:,SubtypeCategory][Subtype_Index]
            Subtype_Assignment = Subtype_Assignment.to_string().split()[1]
            x_data_met.append((Subtype_Assignment,OrderedTumors[i]))

    # create protein average and standard deviation data frames
    df_p_metsub_average = pd.DataFrame(index=df_p.index, columns=MetSubtypes)
    df_p_metsub_average.loc[:,'LP'] = np.mean(df_p.iloc[:,0:14].T)
    df_p_metsub_average.loc[:,'HP'] = np.mean(df_p.iloc[:,14:26].T)

    df_p_metsub_sd = pd.DataFrame(index=df_p.index, columns=MetSubtypes)
    df_p_metsub_sd.loc[:,'LP'] = np.std(df_p.iloc[:,0:14].T)
    df_p_metsub_sd.loc[:,'HP'] = np.std(df_p.iloc[:,14:26].T)

    # create mRNA average and standard deviation data frames
    df_m_metsub_average = pd.DataFrame(index=df_m.index, columns=MetSubtypes)
    df_m_metsub_average.loc[:,'LP'] = np.mean(df_m.iloc[:,0:14].T)
    df_m_metsub_average.loc[:,'HP'] = np.mean(df_m.iloc[:,14:26].T)

    df_m_metsub_sd = pd.DataFrame(index=df_m.index, columns=MetSubtypes)
    df_m_metsub_sd.loc[:,'LP'] = np.std(df_m.iloc[:,0:14].T)
    df_m_metsub_sd.loc[:,'HP'] = np.std(df_m.iloc[:,14:26].T)

    # create an entry for a "blank" gene
    zero_data = np.zeros(len(MetSubtypes))
    df_p_metsub_average.loc['blank',:] = zero_data
    df_p_metsub_sd.loc['blank',:] = zero_data
    df_m_metsub_average.loc['blank',:] = zero_data
    df_m_metsub_sd.loc['blank',:] = zero_data

    # return required values
    return(x_data_met,df_p_metsub_average,df_p_metsub_sd,df_m_metsub_average,df_m_metsub_sd)
