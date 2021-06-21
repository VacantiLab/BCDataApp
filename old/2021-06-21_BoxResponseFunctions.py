# Define the functions that keep track of what input box is being modified
#     These are fun before the update_prot_trace function because they are added first using on_change() below
def SpecifyBoxNumber1(attrname, old, new):
    global select_box_index
    select_box_index = 0

def SpecifyBoxNumber2(attrname, old, new):
    global select_box_index
    select_box_index = 1

def SpecifyBoxNumber3(attrname, old, new):
    global select_box_index
    select_box_index = 2

def SpecifyBoxNumber4(attrname, old, new):
    global select_box_index
    select_box_index = 3

SpecifyBoxNumberFunctionList = [SpecifyBoxNumber1,SpecifyBoxNumber2,SpecifyBoxNumber3,SpecifyBoxNumber4]

# Define the function that updates the data in the figure object
def update_prot_trace(attrname, old, new):
    from pdb import set_trace
    import numpy as np
    from main import df_p, df_m, SourceList, x_data, gene_plot, subtypes, df_p_subtype_average, df_p_subtype_sd, df_m_subtype_average, df_m_subtype_sd, plot_subtype_p, source_subtype_p, plot_subtype_m, source_subtype_m

    print(select_box_index)
    # correlation plots
    gene = new
    py = df_p.loc[gene]
    my = df_m.loc[gene]
    GeneListRepeat = np.repeat(gene,len(x_data))
    SourceList[select_box_index].data = dict(x=x_data, py=py, my=my, gene=GeneListRepeat)

    # subtype bar-scatter plots
    # initialize lists
    # protein
    x_data_subtype_p = list()
    y_data_subtype_p = list()
    upper_p = list()
    lower_p = list()
    # mRNA
    x_data_subtype_m = list()
    y_data_subtype_m = list()
    upper_m = list()
    lower_m = list()

    # Populate the x and y axis data lists
    # You cannot have the same thing twice on the x-axis
    if gene not in gene_plot:
        gene_plot[select_box_index] = gene
    for subtype in subtypes:
        for gene_to_plot in gene_plot:
            # protein
            x_data_subtype_p.append((gene_to_plot,subtype))
            y_data_subtype_p.append((df_p_subtype_average.loc[gene_to_plot,subtype]))
            upper_p.append(df_p_subtype_average.loc[gene_to_plot,subtype] + df_p_subtype_sd.loc[gene_to_plot,subtype])
            lower_p.append(df_p_subtype_average.loc[gene_to_plot,subtype] - df_p_subtype_sd.loc[gene_to_plot,subtype])
            # mRNA
            x_data_subtype_m.append((gene_to_plot,subtype))
            y_data_subtype_m.append((df_m_subtype_average.loc[gene_to_plot,subtype]))
            upper_m.append(df_m_subtype_average.loc[gene_to_plot,subtype] + df_m_subtype_sd.loc[gene_to_plot,subtype])
            lower_m.append(df_m_subtype_average.loc[gene_to_plot,subtype] - df_m_subtype_sd.loc[gene_to_plot,subtype])

    # update the plot data
    # protein
    plot_subtype_p.x_range.factors = x_data_subtype_p
    source_subtype_p.data = dict(x=x_data_subtype_p,y=y_data_subtype_p,upper=upper_p,lower=lower_p)
    # mRNA
    plot_subtype_m.x_range.factors = x_data_subtype_m
    #source_subtype_m.data = dict(x=x_data_subtype_m,y=y_data_subtype_m,upper=upper_m,lower=lower_m)
