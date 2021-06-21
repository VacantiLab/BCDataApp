# The call to this is:
#     bokeh serve --show BCDataApp
#     the call must be made in the terminal (not in python)

# import python packages
import numpy as np
import pandas as pd
from pdb import set_trace

# import necessary bokeh packages
from bokeh.io import curdoc
from bokeh.layouts import column, row, layout, widgetbox
from bokeh.models import ColumnDataSource, Slider, TextInput, FactorRange, Select, Whisker
from bokeh.models.widgets.markups import Div
from bokeh.plotting import figure, output_file
from bokeh.events import DoubleTap
from bokeh.transform import factor_cmap
from copy import copy

from ImportData import ImportData
from GetCorrelationSourceDicts import GetCorrelationSourceDicts
from StylePlot import StylePlot
from CreateSubtypeAverageDFs import CreateSubtypeAverageDFs
from CreateSubtypeAveragePlotSources import CreateSubtypeAveragePlotSources
from CreateMetSubAverageDFs import CreateMetSubAverageDFs

# Import the data
[df_p,df_m,x_data,genes,subtypes,subtype_colors] = ImportData()

# Create the correlation plots
[source_dict1,source_dict2,source_dict3,source_dict4,gene_plot] = GetCorrelationSourceDicts(df_p,df_m,x_data,genes,subtypes)

# create the plot data source objects from the above dictionaries for each gene
source1 = ColumnDataSource(data=source_dict1) #for bokeh widgets it is stored in a ColmnDataSource object
source2 = ColumnDataSource(data=source_dict2) #for bokeh widgets it is stored in a ColmnDataSource object
source3 = ColumnDataSource(data=source_dict3) #for bokeh widgets it is stored in a ColmnDataSource object
source4 = ColumnDataSource(data=source_dict4) #for bokeh widgets it is stored in a ColmnDataSource object
SourceList = [source1,source2,source3,source4]

# In itialize the figure object
plot_p=figure(x_range=FactorRange(*x_data), title='', x_axis_label='',y_axis_label='protein z-score',plot_width=350,plot_height=200)
plot_m=figure(x_range=FactorRange(*x_data), title='', x_axis_label='',y_axis_label='mRNA z-score',plot_width=350,plot_height=200)
#     x_range specifies that the data is categorical

################################################################################
################################################################################
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

# Define the function that updates the data in the figure object
def update_prot_trace(attrname, old, new):
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
    source_subtype_m.data = dict(x=x_data_subtype_m,y=y_data_subtype_m,upper=upper_m,lower=lower_m)
################################################################################
################################################################################

SpecifyBoxNumberFunctionList = [SpecifyBoxNumber1,SpecifyBoxNumber2,SpecifyBoxNumber3,SpecifyBoxNumber4]

# Create the lines that are displayed on the figure object
source_list = [source1,source2,source3,source4]

# set the colors of the corresponding lines
gene_colors = ['red','blue','green','purple']

gene_text = {}
options_array = ['blank'] + genes
GeneNumbers = ['Gene 1', 'Gene 2', 'Gene 3', 'Gene 4']
for j in [0,1,2,3]:
    plot_p.line('x','py',source=source_list[j],color=gene_colors[j],legend_group='gene') #update the plot object for the current mz
    plot_p.circle('x','py',source=source_list[j],color=gene_colors[j],size=4)
    plot_m.line('x','my',source=source_list[j],color=gene_colors[j],legend_group='gene') #update the plot object for the current mz
    plot_m.circle('x','my',source=source_list[j],color=gene_colors[j],size=4)
    gene_text[j] = Select(title=GeneNumbers[j], value=str(gene_plot[j]),width=150,options=options_array) #the textbox widget, the value must be a string
    gene_text[j].on_change('value',SpecifyBoxNumberFunctionList[j])
    gene_text[j].on_change('value',update_prot_trace)
plot_p = StylePlot(plot_p)
plot_m = StylePlot(plot_m)

# Line-Bar Plot for Subtypes ##########################################################
# create protein average and standard deviation data frames
[df_p_subtype_average,df_p_subtype_sd,df_m_subtype_average,df_m_subtype_sd] = CreateSubtypeAverageDFs(df_p,df_m,subtypes)

# Create the subtype average plot sources
[source_dict_subtype_p, source_dict_subtype_m] = CreateSubtypeAveragePlotSources(df_p_subtype_average,df_p_subtype_sd,df_m_subtype_average,df_m_subtype_sd,subtypes,gene_plot)

# create the plot data source objects from the above dictionaries for each gene
source_subtype_p = ColumnDataSource(data=source_dict_subtype_p)
source_subtype_m = ColumnDataSource(data=source_dict_subtype_m)

# In itialize the figure object
plot_subtype_p=figure(x_range=FactorRange(*source_subtype_p.data['x']), title='', x_axis_label='',y_axis_label='protein z-score',plot_width=350,plot_height=200)
plot_subtype_m=figure(x_range=FactorRange(*source_subtype_m.data['x']), title='', x_axis_label='',y_axis_label='mRNA z-score',plot_width=350,plot_height=200)
#     x_range specifies that the data is categorical

# make protein plots
plot_subtype_p.circle('x','y',source=source_subtype_p,fill_color=factor_cmap('x', palette=subtype_colors, factors=subtypes, start=1, end=2),line_color=factor_cmap('x', palette=subtype_colors, factors=subtypes, start=1, end=2),legend_group='LegendGroup')
plot_subtype_p.circle('x','upper',source=source_subtype_p,size=0) # invisible, here only to set initial visible range correctly
plot_subtype_p.circle('x','lower',source=source_subtype_p,size=0)# invisible, here only to set initial visible range correctly

# make mRNA plots
plot_subtype_m.circle('x','y',source=source_subtype_m,fill_color=factor_cmap('x', palette=subtype_colors, factors=subtypes, start=1, end=2),line_color=factor_cmap('x', palette=subtype_colors, factors=subtypes, start=1, end=2),legend_group='LegendGroup')
plot_subtype_m.circle('x','upper',source=source_subtype_m,size=0) # invisible, here only to set initial visible range correctly
plot_subtype_m.circle('x','lower',source=source_subtype_m,size=0)# invisible, here only to set initial visible range correctly

# Add error bars
# protein plot
W_p = Whisker(source=source_subtype_p, base="x", upper="upper", lower="lower",line_color=factor_cmap('x', palette=subtype_colors, factors=subtypes, start=1, end=2))
W_p.upper_head.line_color = factor_cmap('x', palette=subtype_colors, factors=subtypes, start=1, end=2)
W_p.lower_head.line_color = factor_cmap('x', palette=subtype_colors, factors=subtypes, start=1, end=2)
plot_subtype_p.add_layout(W_p)
# mRNA plot
W_m = Whisker(source=source_subtype_m, base="x", upper="upper", lower="lower",line_color=factor_cmap('x', palette=subtype_colors, factors=subtypes, start=1, end=2))
W_m.upper_head.line_color = factor_cmap('x', palette=subtype_colors, factors=subtypes, start=1, end=2)
W_m.lower_head.line_color = factor_cmap('x', palette=subtype_colors, factors=subtypes, start=1, end=2)
plot_subtype_m.add_layout(W_m)

# set aesthetic values
plot_subtype_p = StylePlot(plot_subtype_p,DotBar=True)
plot_subtype_m = StylePlot(plot_subtype_m,DotBar=True)

# Line-Bar Plot for Metabolite Subtypes #######################################
# create protein average and standard deviation data frames
[x_data_met,df_p_metsub_average,df_p_metsub_sd,df_m_metsub_average,df_m_metsub_sd] = CreateMetSubAverageDFs(df_p,df_m)



# Application Layout ###########################################################
ProteinTitle = Div(text="Protein", style={'font-size': '100%', 'color': 'black'},align='center')
mRNATitle = Div(text="mRNA", style={'font-size': '100%', 'color': 'black'},align='center')
MetHeatMap = Div(text="<img src='DataApp/static/met_heat_map1.png'>",width=350,width_policy='fixed')
RowSpacer = Div(height=100)
ColumnSpacer = Div(width=100)

TextBoxes = column(RowSpacer,gene_text[0],gene_text[1],gene_text[2],gene_text[3])
ProteinPlots = column(ProteinTitle,plot_p,RowSpacer,plot_subtype_p,RowSpacer,MetHeatMap)
mRNAPlots = column(mRNATitle,plot_m,RowSpacer,plot_subtype_m)
l = layout([
  [ProteinPlots,ColumnSpacer,mRNAPlots,TextBoxes],
], sizing_mode='fixed')

# Create the bokeh server application
curdoc().add_root(l)
