# The call to this is:
#     bokeh serve --show BCDataApp
#     the call must be made in the terminal (not in python)

# import python packages
import numpy as np
import pandas as pd
from pdb import set_trace

# import necessary bokeh packages
from bokeh.io import curdoc
from bokeh.layouts import column, row, layout, widgetbox, Spacer
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
from MakeSubtypePlots import MakeSubtypePlots
from Get_mRNA_Prot_CorrelationSourceDicts import Get_mRNA_Prot_CorrelationSourceDicts

# Create Widget Responding Functions
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
    # correlation line plots
    gene = new
    if gene in list(df_p.index):
        py = df_p.loc[gene]
    if gene not in list(df_p.index):
        py = df_p.loc['blank']

    if gene in list(df_m.index):
        my = df_m.loc[gene]
    if gene not in list(df_m.index):
        my = df_m.loc['blank']
    GeneListRepeat = np.repeat(gene,len(x_data))
    SourceList[select_box_index].data = dict(x=x_data, py=py, my=my, gene=GeneListRepeat)

    # correlation scatter plots
    gene = new
    if gene in list(df_p.index):
        cor_y = df_p.loc[gene]
    if gene not in list(df_p.index):
        cor_y = df_p.loc['blank']

    if gene in list(df_m.index):
        cor_x = df_m.loc[gene]
    if gene not in list(df_m.index):
        cor_x = df_m.loc['blank']
    x_to_change = mRNA_prot_xList[select_box_index]
    y_to_change = mRNA_prot_yList[select_box_index]
    source_mRNA_prot.data[x_to_change] = cor_x
    source_mRNA_prot.data[y_to_change] = cor_y

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
    if gene not in gene_plot_subtypes:
        gene_plot_subtypes[select_box_index] = gene
    for subtype in subtypes:
        for gene_to_plot in gene_plot_subtypes:
            gene_to_plot_original = copy(gene_to_plot)
            # Subtype Plot
            # protein
            x_data_subtype_p.append((gene_to_plot,subtype))
            if gene_to_plot not in list(df_p.index):
                gene_to_plot = 'blank'
            y_data_subtype_p.append((df_p_subtype_average.loc[gene_to_plot,subtype]))
            upper_p.append(df_p_subtype_average.loc[gene_to_plot,subtype] + df_p_subtype_sd.loc[gene_to_plot,subtype])
            lower_p.append(df_p_subtype_average.loc[gene_to_plot,subtype] - df_p_subtype_sd.loc[gene_to_plot,subtype])
            # mRNA
            gene_to_plot = copy(gene_to_plot_original)
            x_data_subtype_m.append((gene_to_plot,subtype))
            if gene_to_plot not in list(df_m.index):
                gene_to_plot = 'blank'
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


    # MetSubtype bar-scatter plots
    # initialize lists
    # protein
    x_data_metsub_p = list()
    y_data_metsub_p = list()
    upper_metsub_p = list()
    lower_metsub_p = list()
    # mRNA
    x_data_metsub_m = list()
    y_data_metsub_m = list()
    upper_metsub_m = list()
    lower_metsub_m = list()

    # Populate the x and y axis data lists
    # You cannot have the same thing twice on the x-axis
    if gene not in gene_plot_metsub:
        gene_plot_metsub[select_box_index] = gene
    for MetSubtype in MetSubtypes:
        for gene_to_plot in gene_plot_metsub:
            gene_to_plot_original = copy(gene_to_plot)
            # Subtype Plot
            # protein
            x_data_metsub_p.append((gene_to_plot,MetSubtype))
            if gene_to_plot not in list(df_p.index):
                gene_to_plot = 'blank'
            y_data_metsub_p.append((df_p_metsub_average.loc[gene_to_plot,MetSubtype]))
            upper_metsub_p.append(df_p_metsub_average.loc[gene_to_plot,MetSubtype] + df_p_metsub_sd.loc[gene_to_plot,MetSubtype])
            lower_metsub_p.append(df_p_metsub_average.loc[gene_to_plot,MetSubtype] - df_p_metsub_sd.loc[gene_to_plot,MetSubtype])
            # mRNA
            gene_to_plot = copy(gene_to_plot_original)
            x_data_metsub_m.append((gene_to_plot,MetSubtype))
            if gene_to_plot not in list(df_m.index):
                gene_to_plot = 'blank'
            y_data_metsub_m.append((df_m_metsub_average.loc[gene_to_plot,MetSubtype]))
            upper_metsub_m.append(df_m_metsub_average.loc[gene_to_plot,MetSubtype] + df_m_metsub_sd.loc[gene_to_plot,MetSubtype])
            lower_metsub_m.append(df_m_metsub_average.loc[gene_to_plot,MetSubtype] - df_m_metsub_sd.loc[gene_to_plot,MetSubtype])

    # update the plot data
    # protein
    plot_metsub_p.x_range.factors = x_data_metsub_p
    source_metsub_p.data = dict(x=x_data_metsub_p,y=y_data_metsub_p,upper=upper_metsub_p,lower=lower_metsub_p)
    # mRNA
    plot_metsub_m.x_range.factors = x_data_metsub_m
    source_metsub_m.data = dict(x=x_data_metsub_m,y=y_data_metsub_m,upper=upper_metsub_m,lower=lower_metsub_m)
################################################################################
################################################################################

# Import the data
[df_p,df_m,x_data,genes,subtypes,subtype_colors] = ImportData()

# Protein Complex Subunit Correlation Plot
###########################################
# Create the protein complex correlation plot data source dictionaries
[source_dict1,source_dict2,source_dict3,source_dict4,gene_plot] = GetCorrelationSourceDicts(df_p,df_m,x_data,genes,subtypes)

# Create the plot data source objects from the above dictionaries for each gene
source1 = ColumnDataSource(data=source_dict1) #for bokeh widgets it is stored in a ColmnDataSource object
source2 = ColumnDataSource(data=source_dict2) #for bokeh widgets it is stored in a ColmnDataSource object
source3 = ColumnDataSource(data=source_dict3) #for bokeh widgets it is stored in a ColmnDataSource object
source4 = ColumnDataSource(data=source_dict4) #for bokeh widgets it is stored in a ColmnDataSource object
SourceList = [source1,source2,source3,source4]

# In itialize the figure object
plot_p=figure(x_range=FactorRange(*x_data), title='', x_axis_label='',y_axis_label='protein z-score',plot_width=350,plot_height=200)
plot_m=figure(x_range=FactorRange(*x_data), title='', x_axis_label='',y_axis_label='mRNA z-score',plot_width=350,plot_height=200)
#     x_range specifies that the data is categorical

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

# mRNA-Protein Correlation Plots
##################################
# Create the mRNA-protein correlation plot data source dictionaries
[source_dict1,gene_plot] = Get_mRNA_Prot_CorrelationSourceDicts(df_p,df_m,x_data,genes,subtypes)

# Create the plot data source objects from the above dictionaries for each gene
source_mRNA_prot = ColumnDataSource(data=source_dict1) #for bokeh widgets it is stored in a ColmnDataSource object

mRNA_prot_xList = ['x1','x2','x3','x4']
mRNA_prot_yList = ['y1','y2','y3','y4']

# In itialize the figure object
plot_mRNA_prot1 = figure(title='Gene 1', x_axis_label='mRNA z-score',y_axis_label='protein z-score',plot_width=200,plot_height=200)
plot_mRNA_prot1.circle('x1','y1',source=source_mRNA_prot)
plot_mRNA_prot1 = StylePlot(plot_mRNA_prot1,PlotID='mRNA-Prot')

plot_mRNA_prot2 = figure(title='Gene 2', x_axis_label='mRNA z-score',y_axis_label='protein z-score',plot_width=200,plot_height=200)
plot_mRNA_prot2.circle('x2','y2',source=source_mRNA_prot)
plot_mRNA_prot2 = StylePlot(plot_mRNA_prot2,PlotID='mRNA-Prot')

plot_mRNA_prot3 = figure(title='Gene 3', x_axis_label='mRNA z-score',y_axis_label='protein z-score',plot_width=200,plot_height=200)
plot_mRNA_prot3.circle('x3','y3',source=source_mRNA_prot)
plot_mRNA_prot3 = StylePlot(plot_mRNA_prot3,PlotID='mRNA-Prot')

plot_mRNA_prot4 = figure(title='Gene 4', x_axis_label='mRNA z-score',y_axis_label='protein z-score',plot_width=200,plot_height=200)
plot_mRNA_prot4.circle('x4','y4',source=source_mRNA_prot)
plot_mRNA_prot4 = StylePlot(plot_mRNA_prot4,PlotID='mRNA-Prot')

# Line-Bar Plot for Subtypes ##########################################################
#######################################################################################
# create protein average and standard deviation data frames
[df_p_subtype_average,df_p_subtype_sd,df_m_subtype_average,df_m_subtype_sd] = CreateSubtypeAverageDFs(df_p,df_m,subtypes)

# Create the subtype plot sources
gene_plot_subtypes = ['ESR1','PGR','ERBB2','MKI67']
[source_subtype_p, source_subtype_m] = CreateSubtypeAveragePlotSources(df_p_subtype_average,df_p_subtype_sd,df_m_subtype_average,df_m_subtype_sd,subtypes,gene_plot_subtypes)

# Add the lines and dots to the subtype plot objects
[plot_subtype_p,plot_subtype_m] = MakeSubtypePlots(source_subtype_p,source_subtype_m,subtype_colors,subtypes,PlotID='Subtype')

# set aesthetic values
plot_subtype_p = StylePlot(plot_subtype_p,PlotID='Subtype')
plot_subtype_m = StylePlot(plot_subtype_m,PlotID='Subtype')


# Line-Bar Plot for Metabolite Subtypes ###############################################
#######################################################################################
# create protein average and standard deviation data frames
[x_data_met,df_p_metsub_average,df_p_metsub_sd,df_m_metsub_average,df_m_metsub_sd,MetSubtypes,metsub_colors] = CreateMetSubAverageDFs(df_p,df_m)

# Create the subtype average plot sources
gene_plot_metsub = ['MKI67','PCNA','PLK1','BUB1']
[source_metsub_p, source_metsub_m] = CreateSubtypeAveragePlotSources(df_p_metsub_average,df_p_metsub_sd,df_m_metsub_average,df_m_metsub_sd,MetSubtypes,gene_plot_metsub)

# Add the lines and dots to the subtype plot objects
[plot_metsub_p,plot_metsub_m] = MakeSubtypePlots(source_metsub_p,source_metsub_m,metsub_colors,MetSubtypes,PlotID='MetSubtype')

# set aesthetic values
plot_metsub_p = StylePlot(plot_metsub_p,PlotID='MetSubtype')
plot_metsub_m = StylePlot(plot_metsub_m,PlotID='MetSubtype')


# Application Layout ###########################################################
JohanssonStudyText = "Johansson et al., Nat. Commun. 10:1600, 2019"
JohanssonStudyTitleDiv = Div(text=JohanssonStudyText,style={'font-size':'150%', 'color':'black','font-style':'normal','font-weight':'bold'},width=900)

DescriptiveTextCorrelation = "Abundances of proteins that are part of the same complex are tightly correlated across breast tumors. "\
                             "This does not appear to be the case for the corresponing mRNA transcripts. "\
                             "The plots are initialized showing abundances of structural proteins of complex I of the electron transport chain."

CorrelationTextDiv = column(Div(text="Protein Complex Subunit Correlation:",style={'font-size':'100%', 'color':'black','font-style':'italic','font-weight':'bold'}),
                            Div(text=DescriptiveTextCorrelation,style={'font-size':'100%', 'color':'black','font-style':'italic'}),width=730)

DescriptiveText_mRNA_Prot_Cor = "Protein and transcript abundances often are not correlated; indicating substantial utilization of post-transcriptional regulatory mechanisms."

mRNA_Prot_TextDiv = column(Div(text="mRNA-Protein Correlation:",style={'font-size':'100%', 'color':'black','font-style':'italic','font-weight':'bold'}),
                           Div(text=DescriptiveText_mRNA_Prot_Cor,style={'font-size':'100%', 'color':'black','font-style':'italic'}),width=845)

DescriptiveTextSubtypes = "Breast cancer subtypes are defined by their gene expression profiles. " \
                          "The plots are initialized above showing abundances of ER (ESR1), PR (PGR), HER2 (ERBB2), and KI-67 (MKI67); "\
                          "four immunohistochemical markers commonly used in the clinic. "\
                          "Valeus are means +/- standard error of the mean (SEM). "\
                          "If data is not available for a gene, values will appear as all zeros with no SEMs."

SubtypesTextDiv = column(Div(text="Protein and mRNA Expression by Breast Cancer PAM50 Subtype:",style={'font-size':'100%', 'color':'black','font-style':'italic','font-weight':'bold'}),
                         Div(text=DescriptiveTextSubtypes,style={'font-size':'100%', 'color':'black','font-style':'italic'}),width=730)

SpacerWidth = 30
SpacerHeight = 30

RowSpacer1 = Spacer(height=30)
RowSpacer2 = Spacer(height=30)
RowSpacer3 = Spacer(height=30)

ColumnSpacer1 = Spacer(width=20)
ColumnSpacer2 = Spacer(width=20)
ColumnSpacer3 = Spacer(width=20)
ColumnSpacer4 = Spacer(width=20)
ColumnSpacer5 = Spacer(width=20)

DescriptiveTextMetSubtypes = "Tumors are clustered based on metabolite abundances (left) resulting in groupings designated as \"Glycolytic\" and \"Non-Glycolytic\". "\
                  "Glycolytic tumors are defined by low glucose and high lactate and alanine, i.e. they are using glucose to produce lactate/alanine via glycolysis. " \
                  "Non-Glycolytic tumors are defined by high glucose and low lactate and alanine, i.e. they are not using glucose to produce lactate/alanine via glycolysis. "\
                  "Plots are initialized to display markers of proliferation, " \
                  "of which, Glycolytic tumors appear to have higher protein and mRNA expression. "\
                  "Values are means +/- standard error of the mean (SEM). "\
                  "If data is not available for a gene, values will appear as all zeros with no SEMs."

MetaboliteSubtypeText = column(Div(text="Protein and mRNA Expression by Glycolytic Characterisitcs:",style={'font-size':'100%', 'color':'black','font-style':'italic','font-weight':'bold'}),
                               Div(text=DescriptiveTextMetSubtypes,style={'font-size':'100%', 'color':'black','font-style':'italic'}),width=850)

InstructionsText = "To view data for a different gene, click on a box and begin typing a HGNC gene symbol."
InstructionsDiv = Div(text=InstructionsText,style={'font-size':'100%', 'color':'red','font-style':'italic'},width=200)

HeatMapHeight = 288
HeatMapWidth = int(HeatMapHeight * 1120/900)
MetHeatMap = figure(x_range=(0,10), y_range=(0,10))
MetHeatMap.frame_height = HeatMapHeight
MetHeatMap.frame_width = HeatMapWidth
MetHeatMap.image_url(x=0, y=10, w=10, h=10, url=["http://44.194.104.183:5006/BCDataApp/static/met_heat_map3.png"])
MetHeatMap = StylePlot(MetHeatMap,PlotID='MetHeatMap')

TextBoxes = column(gene_text[0],gene_text[1],gene_text[2],gene_text[3])
GeneColumn = column(TextBoxes,InstructionsDiv)

CorrelationPlots = column(row(plot_p,ColumnSpacer1,plot_m),row(CorrelationTextDiv))
mRNA_Prot_Plots = column(row(plot_mRNA_prot1,Spacer(width=15),plot_mRNA_prot2,Spacer(width=15),plot_mRNA_prot3,Spacer(width=15),plot_mRNA_prot4),mRNA_Prot_TextDiv)
SubtypePlots = column(row(plot_subtype_p,ColumnSpacer2,plot_subtype_m),row(SubtypesTextDiv))
MetSubtypePlotRow = row(MetHeatMap,ColumnSpacer3,plot_metsub_p,ColumnSpacer4,plot_metsub_m)

MetaboliteColumn = column(MetSubtypePlotRow,MetaboliteSubtypeText)


l = layout([
  [JohanssonStudyTitleDiv],
  [Spacer(height=15)],
  [Spacer(width=20),CorrelationPlots,GeneColumn],
  [Spacer(width=20),RowSpacer1],
  [Spacer(width=20),mRNA_Prot_Plots],
  [Spacer(width=20),RowSpacer2],
  [Spacer(width=20),SubtypePlots],
  [Spacer(width=20),RowSpacer3],
  [Spacer(width=20),MetaboliteColumn],
], sizing_mode='fixed')

# Create the bokeh server application
curdoc().add_root(l)
