def StylePlot(plot,PlotID='NA'):

    from bokeh.plotting import figure
    from pdb import set_trace

    if PlotID != 'MetHeatMap':
        plot.y_range.range_padding = 0.25
        plot.toolbar_location = None
        plot.xaxis.major_label_orientation = 1.57079632679 #pi/2
        plot.border_fill_color = "#d0cbcb"
        plot.xaxis.major_label_text_font_size = '0pt'
        plot.xaxis.major_tick_line_color = None
        plot.xaxis.minor_tick_line_color = None
        plot.xgrid.grid_line_color = None
        plot.ygrid.grid_line_color = None
        plot.background_fill_color = "#F3F2F2"
        plot.legend.label_text_font_size = '8pt'
        plot.legend.location = "top_center"
        plot.legend.orientation = "horizontal"
        plot.legend.background_fill_alpha = 0
        plot.legend.border_line_alpha = 0
        plot.legend.spacing = 5
        plot.legend.margin = -14
        plot.legend.label_standoff = 3
        plot.legend.glyph_width = 10

    if (PlotID == 'Subtype') | (PlotID == 'MetSubtype'):
        plot.xaxis.separator_line_color = None
        plot.legend.label_standoff = 0

    if PlotID == 'MetSubtype':
        plot.xaxis.group_label_orientation = 1.57079632679 #pi/2

    if PlotID == 'MetHeatMap':
        plot.toolbar_location = None
        plot.xaxis.major_tick_line_color = None
        plot.xaxis.minor_tick_line_color = None
        plot.yaxis.major_tick_line_color = None
        plot.yaxis.minor_tick_line_color = None
        plot.xgrid.grid_line_color = None
        plot.ygrid.grid_line_color = None
        plot.xaxis.major_label_text_font_size = '0pt'
        plot.yaxis.major_label_text_font_size = '0pt'
        plot.border_fill_color = "#d0cbcb"
        plot.background_fill_color = "#d0cbcb"
        plot.outline_line_color = "#d0cbcb"
        plot.xaxis.axis_line_color = "#d0cbcb"
        plot.yaxis.axis_line_color = "#d0cbcb"
        plot.min_border = 0



    return(plot)
