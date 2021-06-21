def CreateSubtypeAveragePlotSources(df_p_subtype_average,df_p_subtype_sd,df_m_subtype_average,df_m_subtype_sd,subtypes,gene_plot):
  from pdb import set_trace

  # Collect the data to be displayed initially
  # Initialize protein lists
  x_data_subtype_p = list()
  y_data_subtype_p = list()
  upper_p = list()
  lower_p = list()
  LegendGroup_p = list()
  # Initialize mRNA lists
  x_data_subtype_m = list()
  y_data_subtype_m = list()
  upper_m = list()
  lower_m = list()
  LegendGroup_m = list()

  # Populate protein and mRNA lists
  for subtype in subtypes:
      for gene in gene_plot:
          # Protein lists
          x_data_subtype_p.append((gene,subtype))
          y_data_subtype_p.append((df_p_subtype_average.loc[gene,subtype]))
          upper_p.append(df_p_subtype_average.loc[gene,subtype] + df_p_subtype_sd.loc[gene,subtype])
          lower_p.append(df_p_subtype_average.loc[gene,subtype] - df_p_subtype_sd.loc[gene,subtype])
          LegendGroup_p.append(subtype)
          # mRNA lists
          x_data_subtype_m.append((gene,subtype))
          y_data_subtype_m.append((df_m_subtype_average.loc[gene,subtype]))
          upper_m.append(df_m_subtype_average.loc[gene,subtype] + df_m_subtype_sd.loc[gene,subtype])
          lower_m.append(df_m_subtype_average.loc[gene,subtype] - df_m_subtype_sd.loc[gene,subtype])
          LegendGroup_m.append(subtype)

  # Create the dictionaries for the protein and mRNA data and fill them with the initial values
  # Protein
  source_dict_subtype_p = {}
  source_dict_subtype_p['x'] = x_data_subtype_p
  source_dict_subtype_p['y'] = y_data_subtype_p
  source_dict_subtype_p['upper'] = upper_p
  source_dict_subtype_p['lower'] = lower_p
  source_dict_subtype_p['LegendGroup'] = LegendGroup_p
  # mRNA
  source_dict_subtype_m = {}
  source_dict_subtype_m['x'] = x_data_subtype_m
  source_dict_subtype_m['y'] = y_data_subtype_m
  source_dict_subtype_m['upper'] = upper_m
  source_dict_subtype_m['lower'] = lower_m
  source_dict_subtype_m['LegendGroup'] = LegendGroup_m

  return(source_dict_subtype_p, source_dict_subtype_m)
