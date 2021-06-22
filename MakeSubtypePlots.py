def MakeSubtypePlots(source_subtype_p,source_subtype_m,subtype_colors,subtypes,PlotID):
    # import necessary bokeh packages
    from bokeh.io import curdoc
    from bokeh.layouts import column, row, layout, widgetbox
    from bokeh.models import ColumnDataSource, Slider, TextInput, FactorRange, Select, Whisker
    from bokeh.models.widgets.markups import Div
    from bokeh.plotting import figure, output_file
    from bokeh.events import DoubleTap
    from bokeh.transform import factor_cmap

    from pdb import set_trace

    SubtypePlotWidth = 350
    SubtypePlotHeight = 200
    if PlotID == 'MetSubtype':
        SubtypePlotWidth = 200
        SubtypePlotHeight = 288

    # In itialize the figure object
    plot_subtype_p=figure(x_range=FactorRange(*source_subtype_p.data['x']), title='', x_axis_label='',y_axis_label='protein z-score',plot_width=SubtypePlotWidth,plot_height=SubtypePlotHeight)
    plot_subtype_m=figure(x_range=FactorRange(*source_subtype_m.data['x']), title='', x_axis_label='',y_axis_label='mRNA z-score',plot_width=SubtypePlotWidth,plot_height=SubtypePlotHeight)
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

    return(plot_subtype_p,plot_subtype_m)
