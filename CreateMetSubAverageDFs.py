def CreateMetSubAverageDFs(df_p,df_m):
    import numpy as np
    import pandas as pd
    from pdb import set_trace

    tumors = np.array(df_p.columns)
    SubtypeCategory = 'vacanti_website_4'
    MetSubtypes = ['Glycolytic','Non Glycolytic']
    #     The Legend is presented in alphabetical order so these had to be named in a way to present the order as desired
    metsub_colors = ['#FF8C00','#51B20E']
    SubtypeSplitIndex = 6
    N_Tumors = 15

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
    df_p_metsub_average = pd.DataFrame(index=df_p_met.index, columns=MetSubtypes)
    df_p_metsub_average.loc[:,MetSubtypes[0]] = np.mean(df_p_met.iloc[:,0:SubtypeSplitIndex].T)
    df_p_metsub_average.loc[:,MetSubtypes[1]] = np.mean(df_p_met.iloc[:,SubtypeSplitIndex:N_Tumors].T)

    df_p_metsub_sd = pd.DataFrame(index=df_p_met.index, columns=MetSubtypes)
    df_p_metsub_sd.loc[:,MetSubtypes[0]] = np.std(df_p_met.iloc[:,0:SubtypeSplitIndex].T)
    df_p_metsub_sd.loc[:,MetSubtypes[1]] = np.std(df_p_met.iloc[:,SubtypeSplitIndex:N_Tumors].T)

    # create mRNA average and standard deviation data frames
    df_m_metsub_average = pd.DataFrame(index=df_m_met.index, columns=MetSubtypes)
    df_m_metsub_average.loc[:,MetSubtypes[0]] = np.mean(df_m_met.iloc[:,0:SubtypeSplitIndex].T)
    df_m_metsub_average.loc[:,MetSubtypes[1]] = np.mean(df_m_met.iloc[:,SubtypeSplitIndex:N_Tumors].T)

    df_m_metsub_sd = pd.DataFrame(index=df_m_met.index, columns=MetSubtypes)
    df_m_metsub_sd.loc[:,MetSubtypes[0]] = np.std(df_m_met.iloc[:,0:SubtypeSplitIndex].T)
    df_m_metsub_sd.loc[:,MetSubtypes[1]] = np.std(df_m_met.iloc[:,SubtypeSplitIndex:N_Tumors].T)

    # create an entry for a "blank" gene
    zero_data = np.zeros(len(MetSubtypes))
    df_p_metsub_average.loc['blank',:] = zero_data
    df_p_metsub_sd.loc['blank',:] = zero_data
    df_m_metsub_average.loc['blank',:] = zero_data
    df_m_metsub_sd.loc['blank',:] = zero_data

    # return required values
    return(x_data_met,df_p_metsub_average,df_p_metsub_sd,df_m_metsub_average,df_m_metsub_sd,MetSubtypes,metsub_colors)
