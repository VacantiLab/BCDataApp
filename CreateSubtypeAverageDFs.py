def CreateSubtypeAverageDFs(df_p,df_m,subtypes):
    import numpy as np
    import pandas as pd


    # create protein average and standard deviation data frames
    df_p_subtype_average = pd.DataFrame(index=df_p.index, columns=subtypes)
    df_p_subtype_average.loc[:,'Basal'] = np.mean(df_p.iloc[:,0:9].T)
    df_p_subtype_average.loc[:,'LumA'] = np.mean(df_p.iloc[:,9:18].T)
    df_p_subtype_average.loc[:,'LumB'] = np.mean(df_p.iloc[:,18:27].T)
    df_p_subtype_average.loc[:,'Her2'] = np.mean(df_p.iloc[:,27:36].T)
    df_p_subtype_average.loc[:,'Norm'] = np.mean(df_p.iloc[:,36:45].T)

    df_p_subtype_sd = pd.DataFrame(index=df_p.index, columns=subtypes)
    df_p_subtype_sd.loc[:,'Basal'] = np.std(df_p.iloc[:,0:9].T)
    df_p_subtype_sd.loc[:,'LumA'] = np.std(df_p.iloc[:,9:18].T)
    df_p_subtype_sd.loc[:,'LumB'] = np.std(df_p.iloc[:,18:27].T)
    df_p_subtype_sd.loc[:,'Her2'] = np.std(df_p.iloc[:,27:36].T)
    df_p_subtype_sd.loc[:,'Norm'] = np.std(df_p.iloc[:,36:45].T)

    # create mRNA average and standard deviation data frames
    df_m_subtype_average = pd.DataFrame(index=df_m.index, columns=subtypes)
    df_m_subtype_average.loc[:,'Basal'] = np.mean(df_m.iloc[:,0:9].T)
    df_m_subtype_average.loc[:,'LumA'] = np.mean(df_m.iloc[:,9:18].T)
    df_m_subtype_average.loc[:,'LumB'] = np.mean(df_m.iloc[:,18:27].T)
    df_m_subtype_average.loc[:,'Her2'] = np.mean(df_m.iloc[:,27:36].T)
    df_m_subtype_average.loc[:,'Norm'] = np.mean(df_m.iloc[:,36:45].T)

    df_m_subtype_sd = pd.DataFrame(index=df_m.index, columns=subtypes)
    df_m_subtype_sd.loc[:,'Basal'] = np.std(df_m.iloc[:,0:9].T)
    df_m_subtype_sd.loc[:,'LumA'] = np.std(df_m.iloc[:,9:18].T)
    df_m_subtype_sd.loc[:,'LumB'] = np.std(df_m.iloc[:,18:27].T)
    df_m_subtype_sd.loc[:,'Her2'] = np.std(df_m.iloc[:,27:36].T)
    df_m_subtype_sd.loc[:,'Norm'] = np.std(df_m.iloc[:,36:45].T)

    # create an entry for a "blank" gene
    zero_data = np.zeros(len(subtypes))
    df_p_subtype_average.loc['blank',:] = zero_data
    df_p_subtype_sd.loc['blank',:] = zero_data
    df_m_subtype_average.loc['blank',:] = zero_data
    df_m_subtype_sd.loc['blank',:] = zero_data

    return(df_p_subtype_average,df_p_subtype_sd,df_m_subtype_average,df_m_subtype_sd)
