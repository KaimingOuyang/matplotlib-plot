
import re
import sys
import math

import matplotlib as mpl
import matplotlib.pyplot as plt

########################################################################################################################
# Utils
########################################################################################################################

def cm2in(cm):
    return cm / 2.54

def get_default_colors(index):
    colors = []
    colors.append((0.266, 0.447, 0.768))
    colors.append((0.929, 0.490, 0.192))
    colors.append((0.647, 0.647, 0.647))
    colors.append((1.000, 0.752, 0.000))
    colors.append((0.356, 0.607, 0.835))
    colors.append((0.439, 0.678, 0.278))
    colors.append((0.149, 0.266, 0.470))
    colors.append((0.619, 0.282, 0.054))
    return colors[index % len(colors)]

def get_default_markers(index):
    markers = []
    markers.append("o")
    markers.append("x")
    markers.append("+")
    markers.append("^")
    markers.append("s")
    markers.append("2")
    markers.append("v")
    markers.append("1")
    markers.append("D")
    markers.append("s")
    markers.append("<")
    markers.append(">")
    markers.append("*")
    markers.append("d")
    return markers[index]

def get_default_hatches(index):
    hatches = []
    density = 8
    hatches.append("\\" * (density + 2))
    hatches.append("/" * (density + 2))
    hatches.append("+" * density)
    hatches.append("x" * density)
    hatches.append("-" * (density + 2))
    hatches.append("|" * (density + 2) + "x" * density)
    hatches.append("-" * (density + 2) + "x" * density)
    hatches.append("-" * density + "/" * density)
    hatches.append("-" * density + "\\" * density)
    hatches.append("|" * (density + 2) + "/" * density)
    hatches.append("|" * (density + 2) + "\\" * density)
    hatches.append("x" * density + "+" * density)
    hatches.append("****")
    hatches.append("o")
    hatches.append("O")
    hatches.append(".")
    return hatches[index]

def get_default_fontsize():
    return 6.5

########################################################################################################################
# Line Chart
########################################################################################################################

class LineFormat:
    def __init__(self, color, width, style, marker):
        # color : (0.0~1.0, 0.0~1.0, 0.0~1.0)
        self.color = color
        # width : 0.0~
        self.width = width
        # style : "solid" | "dotted" | 'dashed' | 'dashdot'
        self.style = style
        # marker : "string" (see https://matplotlib.org/api/markers_api.html#module-matplotlib.markers)
        self.marker = marker

        self.linewidth = 0.5
        self.markersize = 3.0
        self.errorbar_width = 0.3
        self.errorbar_capsize = 1
        self.errorbar_capthick = 0.3
        return

    def get_linestyle(self):
        return self.style

    @staticmethod
    def get_default(index):
        return LineFormat(get_default_colors(index), 0.5, "solid", get_default_markers(index))

    @staticmethod
    def get_ideal(index):
        ideal_styles = ['--', ':', '-.']
        return LineFormat((1.0, 0.0, 0.0), 0.5, ideal_styles[index % 3], "")

class AxisFormat:
    def __init__(self, label, min_value, max_value, mode, tick):
        # label : "string" | None
        self.label = label
        # min_value : 0.0~ (< max_value)
        self.min_value = min_value
        # max_value : 0.0~ (> min_value)
        self.max_value = max_value
        # mode : "log" | "linear" | "label"
        self.mode = mode
        # tick : 0.0~ (ignored if axis_format == "label" | "log")
        self.tick = tick
        # minortick : 0.0~ (ignored if axis_format == "label" | "log")
        self.minortick = tick / 2.0

        self.labelpad = 1.0 # distance between label and axis.
        self.font_size = get_default_fontsize()
        return

class DataPoint:
    def __init__(self, label, xvalue, yvalue, yvalue_err):
        # label : "string"
        self.label = label
        # xvalue : value | "xlabel"
        self.xvalue = xvalue
        # yvalue : value
        self.yvalue = yvalue
        # yvalue : value
        self.yvalue_err = yvalue_err
        return

class DataBar:
    def __init__(self, label, yvalue, yvalue_err):
        # label : "string"
        self.label = label
        # yvalue : value
        self.yvalue = yvalue
        # yvalue : value
        self.yvalue_err = yvalue_err
        return

class DataCategoryBar:
    def __init__(self, label, category, yvalue, yvalue_err):
        # label : "string"
        self.label = label
        # category : "string"
        self.category = category
        # yvalue : value
        self.yvalue = yvalue
        # yvalue : value
        self.yvalue_err = yvalue_err
        return

class LineChartData:
    def __init__(self, points, line_formats, xaxis_format, yaxis_format, size):
        # points : [DataPoint, ... ]
        self.points = points
        self.labels = []
        for point in points:
             if not point.label in self.labels:
                self.labels.append(point.label)
        # line_formats : {label: LineFormat, ... }
        self.line_formats = line_formats
        # xaxis_format : AxisFormat
        self.xaxis_format = xaxis_format
        # yaxis_format : AxisFormat
        self.yaxis_format = yaxis_format
        # size : (width, height)
        self.size = size
        self.legend_labelspacing = 0
        self.legend_fontsize = 0.85 * get_default_fontsize()
        self.legend_location = "upper left" # "best"
        self.legend_ncolumns = 2
        self.legend_border_width = 0.3
        self.figure_border_width = 0.6
        self.frame_border_width = 0.5
        self.major_grid_linewidth = 0.2
        self.major_grid_dashes = (0.5, 0.5)
        self.minor_grid_linewidth = 0.1
        self.minor_grid_dashes = (0.25, 0.75)
        self.font_name = 'Latin Modern Roman'
        self.font_size = get_default_fontsize()
        return

class BarChartData:
    def __init__(self, bars, xaxis_format, yaxis_format, size):
        # points : [DataBar, ... ]
        self.bars = bars
        # xaxis_format : AxisFormat
        self.xaxis_format = xaxis_format
        # yaxis_format : AxisFormat
        self.yaxis_format = yaxis_format
        # size : (width, height)
        self.size = size
        self.figure_border_width = 0.6
        self.frame_border_width = 0.5
        self.major_grid_linewidth = 0.2
        self.major_grid_dashes = (0.5, 0.5)
        self.minor_grid_linewidth = 0.1
        self.minor_grid_dashes = (0.25, 0.75)
        self.errorbar_width = 0.3
        self.errorbar_capsize = 1
        self.errorbar_capthick = 0.3
        self.errorbar_color = 'black'
        self.barwidth = 0.5
        self.font_name = 'Latin Modern Roman'
        self.font_size = get_default_fontsize()
        self.xaxis_rotation = 'vertical'
        return


class CategoryBarChartData:
    def __init__(self, bars, xaxis_format, yaxis_format, size):
        # points : [DataBar, ... ]
        self.bars = bars
        # xaxis_format : AxisFormat
        self.xaxis_format = xaxis_format
        # yaxis_format : AxisFormat
        self.yaxis_format = yaxis_format
        # size : (width, height)
        self.size = size
        self.legend_labelspacing = 0
        self.legend_fontsize = 0.85 * get_default_fontsize()
        self.legend_location = "upper left" # "best"
        self.legend_border_width = 0.3
        self.legend_ncolumns = 1
        self.figure_border_width = 0.6
        self.frame_border_width = 0.5
        self.major_grid_linewidth = 0.2
        self.major_grid_dashes = (0.5, 0.5)
        self.minor_grid_linewidth = 0.1
        self.minor_grid_dashes = (0.25, 0.75)
        self.errorbar_width = 0.3
        self.errorbar_capsize = 1
        self.errorbar_capthick = 0.3
        self.errorbar_color = 'black'
        self.barwidth = 0.5
        self.barlinewidth = 0.3
        self.font_name = 'Latin Modern Roman'
        self.font_size = get_default_fontsize()
        self.xaxis_rotation = 'horizontal'
        self.color_indices = range(0, 20)
        self.hatch_indices = range(0, 20)
        return

def plot_linechart(data, filename):
    # data : LineChartData
    assert (data.yaxis_format.mode != "label"), 'yaxis may not be "label".'
    assert (data.xaxis_format.mode != "label"), 'xaxis_format + "label" is not supported.'

    mpl.rc('font', family = data.font_name, size = data.font_size)

    fig = plt.figure(figsize = (cm2in(data.size[0]), cm2in(data.size[1])), dpi = 160, facecolor = 'w', edgecolor = 'k')
    plt.minorticks_on()

    if data.xaxis_format.mode == "log":
        plt.xscale('log')
    elif data.xaxis_format.mode == "linear":
        plt.xticks([data.xaxis_format.min_value + x * data.xaxis_format.tick for x in range(0, int((data.xaxis_format.max_value - data.xaxis_format.min_value) / data.xaxis_format.tick + 1))])
    if data.yaxis_format.mode == "log":
        plt.yscale('log')
        plt.yticks([10 ** y  for y in range((int(math.ceil(math.log10(data.yaxis_format.min_value))) / data.yaxis_format.tick) * data.yaxis_format.tick, int(math.floor(math.log10(data.yaxis_format.max_value))) + 1, data.yaxis_format.tick)])
    elif data.yaxis_format.mode == "linear":
        plt.yticks([data.yaxis_format.min_value + y * data.yaxis_format.tick for y in range(0, int((data.yaxis_format.max_value - data.yaxis_format.min_value) / data.yaxis_format.tick + 1))])
    # fig.get_frame().set_linewidth(data.figure_border_width)
    plt.xlim(xmin = data.xaxis_format.min_value, xmax = data.xaxis_format.max_value)
    plt.ylim(ymin = data.yaxis_format.min_value, ymax = data.yaxis_format.max_value)

    if data.yaxis_format.mode == "linear":
        plt.axes().yaxis.set_minor_locator(plt.MultipleLocator(base = data.yaxis_format.minortick))

    plt.grid(which = 'major', linestyle = '--', linewidth = data.major_grid_linewidth, dashes = data.major_grid_dashes, color = 'black')
    plt.grid(which = 'minor', linestyle = '--', linewidth = data.minor_grid_linewidth, dashes = data.minor_grid_dashes, color = 'black')
    for axis in ['top','bottom','left','right']:
        plt.gca().spines[axis].set_linewidth(data.frame_border_width)

    # get all labels
    line_index = 0
    ideal_index = 0
    for label in data.labels:
        xvalues = [point.xvalue for point in data.points if point.label == label]
        yvalues = [point.yvalue for point in data.points if point.label == label]
        yvalue_errs = [point.yvalue_err for point in data.points if point.label == label]
        if not label in data.line_formats:
            if "ideal" in label or "Ideal" in label:
                line_format = LineFormat.get_ideal(ideal_index)
                ideal_index += 1
            else:
                line_format = LineFormat.get_default(line_index)
                line_index += 1
        else:
            line_format = data.line_formats[label]
        plt.plot(xvalues, yvalues, label = label, marker = line_format.marker, fillstyle = "none", color = line_format.color, markersize = line_format.markersize, linewidth = line_format.linewidth, linestyle = line_format.get_linestyle())
        if any([(yvalue_err != None and yvalue_err != 0.0) for yvalue_err in yvalue_errs]):
            plt.errorbar(xvalues, yvalues, yerr = [yvalue_errs, yvalue_errs], fmt = "none", ecolor = line_format.color, elinewidth = line_format.errorbar_width, capsize = line_format.errorbar_capsize, capthick = line_format.errorbar_capthick)
    if data.xaxis_format.label != None and data.xaxis_format.label != "":
        plt.xlabel(data.xaxis_format.label, fontsize = data.xaxis_format.font_size, labelpad = data.xaxis_format.labelpad)
    if data.yaxis_format.label != None and data.yaxis_format.label != "":
        plt.ylabel(data.yaxis_format.label, fontsize = data.yaxis_format.font_size, labelpad = data.yaxis_format.labelpad)
    legend = plt.legend(loc = data.legend_location, frameon=True, fontsize = data.legend_fontsize, labelspacing = data.legend_labelspacing, ncol = data.legend_ncolumns)
    legend.get_frame().set_linewidth(data.legend_border_width)
    plt.savefig(filename, bbox_inches = 'tight', pad_inches = cm2in(0.1), dpi = 100)
    plt.close(fig)

def plot_linecharts(data_list, filename):
    data = data_list[0]
    # data : LineChartData
    assert (data.yaxis_format.mode != "label"), 'yaxis may not be "label".'
    assert (data.xaxis_format.mode != "label"), 'xaxis_format + "label" is not supported.'

    mpl.rc('font', family = data.font_name, size = data.font_size)

    fig = plt.figure(figsize = (cm2in(data.size[0]), cm2in(data.size[1])), dpi = 160, facecolor = 'w', edgecolor = 'k')
    # fig = plt.figure(1)
    plt.minorticks_on()

    for data_index in range(0, 9):
        data = data_list[data_index]
        data_index_y = data_index / 3
        data_index_x = data_index % 3
        ax = plt.subplot(331 + data_index)
        # plt.plot(t, s1)

        if data.xaxis_format.mode == "log":
            plt.xscale('log')
            if data_index_y != 2:
                plt.xticks([1, 10, 100], " ")
            else:
                plt.xticks([1, 10, 100])
        elif data.xaxis_format.mode == "linear":
            if data_index_y != 2:
                plt.xticks([data.xaxis_format.min_value + x * data.xaxis_format.tick for x in range(0, int((data.xaxis_format.max_value - data.xaxis_format.min_value) / data.xaxis_format.tick + 1))], " ")
            else:
                plt.xticks([data.xaxis_format.min_value + x * data.xaxis_format.tick for x in range(0, int((data.xaxis_format.max_value - data.xaxis_format.min_value) / data.xaxis_format.tick + 1))])
        if data.yaxis_format.mode == "log":
            plt.yscale('log')
            if data_index_x != 0:
                plt.yticks([10 ** y  for y in range((int(math.ceil(math.log10(data.yaxis_format.min_value))) / data.yaxis_format.tick) * data.yaxis_format.tick, int(math.floor(math.log10(data.yaxis_format.max_value))) + 1, data.yaxis_format.tick)], " ")
            else:
                plt.yticks([10 ** y  for y in range((int(math.ceil(math.log10(data.yaxis_format.min_value))) / data.yaxis_format.tick) * data.yaxis_format.tick, int(math.floor(math.log10(data.yaxis_format.max_value))) + 1, data.yaxis_format.tick)])
        elif data.yaxis_format.mode == "linear":
            if data_index_x != 0:
                plt.yticks([data.yaxis_format.min_value + y * data.yaxis_format.tick for y in range(0, int((data.yaxis_format.max_value - data.yaxis_format.min_value) / data.yaxis_format.tick + 1))], " ")
            else:
                plt.yticks([data.yaxis_format.min_value + y * data.yaxis_format.tick for y in range(0, int((data.yaxis_format.max_value - data.yaxis_format.min_value) / data.yaxis_format.tick + 1))])

        # fig.get_frame().set_linewidth(data.figure_border_width)
        [i.set_linewidth(data.figure_border_width) for i in ax.spines.itervalues()]
        # ax.get_frame().set_linewidth()
        plt.xlim(xmin = data.xaxis_format.min_value, xmax = data.xaxis_format.max_value)
        plt.ylim(ymin = data.yaxis_format.min_value, ymax = data.yaxis_format.max_value)

        if data.yaxis_format.mode == "linear":
            ax.yaxis.set_minor_locator(plt.MultipleLocator(base = data.yaxis_format.minortick))

        plt.grid(which = 'major', linestyle = '--', linewidth = data.major_grid_linewidth, dashes = data.major_grid_dashes, color = 'black')
        plt.grid(which = 'minor', linestyle = '--', linewidth = data.minor_grid_linewidth, dashes = data.minor_grid_dashes, color = 'black')

        # for axis in ['top','bottom','left','right']:
        #     plt.gca().spines[axis].set_linewidth(data.frame_border_width)

        # get all labels
        line_index = 0
        ideal_index = 0
        for label in data.labels:
            xvalues = [point.xvalue for point in data.points if point.label == label]
            yvalues = [point.yvalue for point in data.points if point.label == label]
            yvalue_errs = [point.yvalue_err for point in data.points if point.label == label]
            if not label in data.line_formats:
                if "ideal" in label or "Ideal" in label:
                    line_format = LineFormat.get_ideal(ideal_index)
                    ideal_index += 1
                else:
                    line_format = LineFormat.get_default(line_index)
                    line_index += 1
            else:
                line_format = data.line_formats[label]
            plt.plot(xvalues, yvalues, label = label, marker = line_format.marker, fillstyle = "none", color = line_format.color, markersize = line_format.markersize, linewidth = line_format.linewidth, linestyle = line_format.get_linestyle())
            if any([(yvalue_err != None and yvalue_err != 0.0) for yvalue_err in yvalue_errs]):
                plt.errorbar(xvalues, yvalues, yerr = [yvalue_errs, yvalue_errs], fmt = "none", ecolor = line_format.color, elinewidth = line_format.errorbar_width, capsize = line_format.errorbar_capsize, capthick = line_format.errorbar_capthick)
        if data_index_y == 2 and data.xaxis_format.label != None and data.xaxis_format.label != "":
            plt.xlabel(data.xaxis_format.label, fontsize = data.xaxis_format.font_size, labelpad = data.xaxis_format.labelpad)
        plt.title(data.title, fontweight='bold', fontsize = data.xaxis_format.font_size * 0.9, position=(0.5, 0.78), bbox=dict(facecolor='white', alpha=1.0, lw=0.0, pad=1.5))

        if data_index_x == 0 and data_index_y == 1 and data.yaxis_format.label != None and data.yaxis_format.label != "":
            plt.ylabel(data.yaxis_format.label.replace("\n", " "), fontsize = data.yaxis_format.font_size, labelpad = data.yaxis_format.labelpad)

    data = data_list[data_index]

    legend = plt.legend(bbox_to_anchor=(1.5, 2.0), frameon=True, fontsize = data.legend_fontsize, labelspacing = data.legend_labelspacing + 1,  ncol = 1)
    legend.get_frame().set_linewidth(data.legend_border_width)

    plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.05, wspace=0.10)

    plt.savefig(filename, bbox_inches = 'tight', pad_inches = cm2in(0.1), dpi = 100)
    plt.close(fig)

def plot_barchart(data, filename):
    assert (data.yaxis_format.mode != "label"), 'yaxis may not be "label".'

    mpl.rc('font', family = data.font_name, size = data.font_size)

    fig = plt.figure(figsize = (cm2in(data.size[0]), cm2in(data.size[1])), dpi = 160, facecolor = 'w', edgecolor = 'k')
    if data.yaxis_format.mode == "log":
        plt.yscale('log')
        plt.yticks([10 ** y  for y in range((int(math.ceil(math.log10(data.yaxis_format.min_value))) / data.yaxis_format.tick) * data.yaxis_format.tick, int(math.floor(math.log10(data.yaxis_format.max_value))) + 1, data.yaxis_format.tick)])
    elif data.yaxis_format.mode == "linear":
        plt.yticks([data.yaxis_format.min_value + y * data.yaxis_format.tick for y in range(0, int((data.yaxis_format.max_value - data.yaxis_format.min_value) / data.yaxis_format.tick + 1))])
    # fig.get_frame().set_linewidth(data.figure_border_width)
    plt.ylim(ymin = data.yaxis_format.min_value, ymax = data.yaxis_format.max_value)
    plt.minorticks_on()
    plt.gca().yaxis.grid(which = 'major', linestyle = '--', linewidth = data.major_grid_linewidth, dashes = data.major_grid_dashes, color = 'black')
    plt.gca().yaxis.grid(which = 'minor', linestyle = '--', linewidth = data.minor_grid_linewidth, dashes = data.minor_grid_dashes, color = 'black')
    for axis in ['top','bottom','left','right']:
        plt.gca().spines[axis].set_linewidth(data.frame_border_width)

    # get all bars
    plt_bars = plt.bar(range(0, len(data.bars)), [bar.yvalue for bar in data.bars], width = data.barwidth, align = 'center', linewidth = 0)
    plt.errorbar([bar_index for bar_index in range(0, len(data.bars))], [bar.yvalue for bar in data.bars], yerr = [[bar.yvalue_err for bar in data.bars], [bar.yvalue_err for bar in data.bars]], fmt = "none", ecolor = data.errorbar_color, elinewidth = data.errorbar_width, capsize = data.errorbar_capsize, capthick = data.errorbar_capthick)
    for bar_index in range(0, len(data.bars)):
        plt_bars[bar_index].set_color(get_default_colors(bar_index))
    plt.xticks([bar_index for bar_index in range(0, len(data.bars))], [bar.label for bar in data.bars], rotation = data.xaxis_rotation)

    if data.yaxis_format.label != None and data.yaxis_format.label != "":
        plt.ylabel(data.yaxis_format.label, fontsize = data.yaxis_format.font_size, labelpad = data.yaxis_format.labelpad)
    plt.savefig(filename, bbox_inches = 'tight', pad_inches = cm2in(0.1), dpi = 100)
    plt.close(fig)

def plot_categorybarchart(data, filename):
    assert (data.yaxis_format.mode != "label"), 'yaxis may not be "label".'

    mpl.rc('font', family = data.font_name, size = data.font_size)

    fig = plt.figure(figsize = (cm2in(data.size[0]), cm2in(data.size[1])), dpi = 160, facecolor = 'w', edgecolor = 'k')
    if data.yaxis_format.mode == "log":
        plt.yscale('log')
        plt.yticks([10 ** y  for y in range((int(math.ceil(math.log10(data.yaxis_format.min_value))) / data.yaxis_format.tick) * data.yaxis_format.tick, int(math.floor(math.log10(data.yaxis_format.max_value))) + 1, data.yaxis_format.tick)])
    elif data.yaxis_format.mode == "linear":
        plt.yticks([data.yaxis_format.min_value + y * data.yaxis_format.tick for y in range(0, int((data.yaxis_format.max_value - data.yaxis_format.min_value) / data.yaxis_format.tick + 1))])

    # fig.get_frame().set_linewidth(data.figure_border_width)
    plt.ylim(ymin = data.yaxis_format.min_value, ymax = data.yaxis_format.max_value)
    plt.minorticks_on()
    plt.gca().yaxis.grid(which = 'major', linestyle = '--', linewidth = data.major_grid_linewidth, dashes = data.major_grid_dashes, color = 'black', zorder = -100)
    plt.gca().yaxis.grid(which = 'minor', linestyle = '--', linewidth = data.minor_grid_linewidth, dashes = data.minor_grid_dashes, color = 'black', zorder = -100)
    for axis in ['top','bottom','left','right']:
        plt.gca().spines[axis].set_linewidth(data.frame_border_width)

    # get all categories
    categories = []
    labels = []
    bar_dicts = {}
    for bar in data.bars:
        if not bar.category in categories:
            categories.append(bar.category) # keep the order.
        if not bar.label in labels:
            labels.append(bar.label)
            bar_dicts[bar.label] = {}
        bar_dicts[bar.label][bar.category] = bar
    # get all yvalue data
    yvalues_labeled = []
    yvalues_err_labeled = []
    for label_index in range(0, len(labels)):
        yvalues_labeled.append([bar_dicts[labels[label_index]][category].yvalue if category in bar_dicts[labels[label_index]] else 0.0 for category in categories])
        yvalues_err_labeled.append([bar_dicts[labels[label_index]][category].yvalue_err if category in bar_dicts[labels[label_index]] else 0.0 for category in categories])

    # count valid yvalues in each category
    xvalues_labeled = [[] for label_index in range(0, len(labels))]
    for category_index in range(0, len(categories)):
        values_in_category = 0
        for label_index in range(0, len(labels)):
            if yvalues_labeled[label_index][category_index] > 1.0e-11:
                values_in_category += 1
        xvalue_offset = (len(labels) - values_in_category) * 0.5
        valid_label_index = 0
        for label_index in range(0, len(labels)):
            xvalues_labeled[label_index].append(valid_label_index + xvalue_offset + category_index * len(labels))
            if yvalues_labeled[label_index][category_index] > 1.0e-11:
                valid_label_index += 1

    for label_index in range(0, len(labels)):
        yvalues = yvalues_labeled[label_index]
        yvalues_err = yvalues_err_labeled[label_index]
        xvalues = xvalues_labeled[label_index]
        plt_bars = plt.bar(xvalues, yvalues, width = data.barwidth, align = 'center', linewidth = data.barlinewidth, label = labels[label_index], color = 'white', edgecolor = get_default_colors(data.color_indices[label_index]), hatch = get_default_hatches(data.hatch_indices[label_index]), zorder = 10)
        plt.errorbar(xvalues, yvalues, yerr = [yvalues_err, yvalues_err], fmt = "none", ecolor = data.errorbar_color, elinewidth = data.errorbar_width, capsize = data.errorbar_capsize, capthick = data.errorbar_capthick, zorder = 20)
        # for bar_index in range(0, len(categories)):
        #     plt_bars[bar_index].set_color()

    plt.xlim(xmin = -1, xmax = len(categories) * len(labels))
    # print xaxis
    plt.xticks([(i + (len(labels) - 1.0) / (2.0 * len(labels))) * len(labels) for i in range(0, len(categories))], categories, rotation = data.xaxis_rotation)
    # print yaxis
    if data.yaxis_format.label != None and data.yaxis_format.label != "":
        plt.ylabel(data.yaxis_format.label, fontsize = data.yaxis_format.font_size, labelpad = data.yaxis_format.labelpad)
    # print legends
    legend = plt.legend(loc = data.legend_location, frameon=True, fontsize = data.legend_fontsize, labelspacing = data.legend_labelspacing, ncol = data.legend_ncolumns)
    legend.get_frame().set_linewidth(data.legend_border_width)

    plt.savefig(filename, bbox_inches = 'tight', pad_inches = cm2in(0.1), dpi = 100)
    plt.close(fig)

# points = [DataPoint("a", 0, 1, 0.2), DataPoint("a", 1, 2, 0.5), DataPoint("a", 2, 2.4, 0.3), DataPoint("a", 3, 1.8, 0.3), DataPoint("b", 0, 4, 1.2), DataPoint("b", 1.2, 3, 0.3), DataPoint("b", 2.6, 2.1, 0.1)]
# line_formats = {}
# xaxis_format = AxisFormat("time", 0, 4, "linear", 1)
# yaxis_format = AxisFormat("amount", 0, 5, "linear", 2)
# size = (7, 10)
# plot_linechart(LineChartData(points, line_formats, xaxis_format, yaxis_format, size))

###
###import re
###import sys
###import argparse
###
###import numpy as np
###import matplotlib as mpl
###import matplotlib.pyplot as plt
###
###########################################################################################################################
#### Utils
###########################################################################################################################
###
#### Calculate error interval
#### alpha : [0, 1)
###def get_interval(values, alpha):
###    stats.t.interval(alpha, len(data)-1, loc=mean_val, scale=sem_val)
###
###def cm2in(cm):
###    return cm / 2.54
###
###def get_colors(index):
###    colors = []
###    colors.append((0.266, 0.447, 0.768))
###    colors.append((0.929, 0.490, 0.192))
###    colors.append((0.647, 0.647, 0.647))
###    colors.append((1.000, 0.752, 0.000))
###    colors.append((0.356, 0.607, 0.835))
###    colors.append((0.439, 0.678, 0.278))
###    colors.append((0.149, 0.266, 0.470))
###    colors.append((0.619, 0.282, 0.054))
###    return colors[index]
###
###########################################################################################################################
#### Kernel
###########################################################################################################################
###
###########################################################################################################################
#### Barchart
###########################################################################################################################
###
#### List of available fonts
#### import matplotlib.font_manager
#### flist = matplotlib.font_manager.get_fontconfig_fonts()
#### names = [matplotlib.font_manager.FontProperties(fname=fname).get_name() for fname in flist]
#### print names
###
###mpl.rc('font', family = 'Latin Modern Roman', size = '8')
###mpl.rc('axes', linewidth = '0.1')
###
###class PltBarCategory:
###    def __init__(self, label, data, color):
###        self.label = label
###        self.data = data
###        self.color = color
###    def get_label(self):
###        return self.label
###    def get_data(self, indices):
###        return [self.data[index] for index in indices]
###    def get_color(self):
###        return self.color
###
###def plot_barchart(original_categories, indices, ylabel, xlabels, ymin, ymax, ytick, figwidth, figheight):
###    width = 0.4
###    if len(indices) <= 2:
###        width = 0.3
###    label_fontsize = 8
###    value_fontsize = 8
###    legend_fontsize = 7.5
###    linewidth = 0.1
###    gridwidth = 0.6
###    gridcolor = (0.85, 0.85, 0.85)
###    subgridwidth = 0.1
###    subgridcolor = (0.9, 0.9, 0.9)
###    logflag = False
###
###    categories = []
###    for original_category in original_categories:
###        nonemptyflag = False
###        for data in original_category.get_data(indices):
###            if data != 0:
###                nonemptyflag = True
###                break
###        if nonemptyflag:
###            categories.append(original_category)
###
###    plt.figure(figsize = (cm2in(figwidth), cm2in(figheight)), dpi = 160, facecolor = 'w', edgecolor = 'k')
###    # margins
###    plt.subplots_adjust(left = 0.5, right = 0.9, top = 0.9, bottom = 0.1)
###    plt_bars = []
###    plt_bottom = [0.0 for d in categories[0].get_data(indices)]
###    for category in categories:
###        plt_bars.append(plt.bar(np.arange(len(indices)), category.get_data(indices), width, bottom = plt_bottom, yerr = None, align = 'center', color = category.get_color(), linewidth = 0, log = logflag, zorder = 4))
###        for index in range(0, len(indices)):
###            plt_bottom[index] += category.get_data(indices)[index]
###    # put labels above bars
###    for i in range(0, len(indices)):
###        barlabel_value = plt_bottom[i]
###        (barlabel_bottom, barlabel_top) = plt.gca().get_ylim()
###        barlabel_height = barlabel_top - barlabel_bottom
###        rect = plt_bars[-1][i]
###        barlabel_x = rect.get_x() + rect.get_width() / 2.0
###        barlabel_y = barlabel_value + 0.02 * barlabel_height
###        plt.text(barlabel_x, barlabel_y, '%d' % int(barlabel_value), ha = 'center', va = 'bottom', fontsize = value_fontsize)
###
###    plt.ylabel(ylabel, fontsize = label_fontsize)
###    plt.xticks(np.arange(len(indices)), [xlabels[index] for index in indices], fontsize = label_fontsize)
###    plt.yticks(np.arange(ymin, ymax + ytick / 10.0, ytick), fontsize = value_fontsize)
###    handles = ()
###    categorylabels = ()
###    for index in range(len(categories) - 1, -1, -1):
###        handles = handles + (plt_bars[index][0],)
###        categorylabels = categorylabels + (categories[index].get_label(),)
###    plt.tight_layout(rect = [0, 0, 0.75, 1])
###    plt.legend(handles, categorylabels, bbox_to_anchor = (1.01, 0.52), loc = "center left", frameon = False, fontsize = legend_fontsize, labelspacing  = 0)
###    # Y-axis (Major)
###    plt.gca().yaxis.grid(True, which = 'major', linestyle = "solid", linewidth = gridwidth, color = gridcolor, zorder = 0)
###    # Y-axis (Minor)
###    plt.minorticks_on()
###    plt.gca().yaxis.grid(True, which = 'minor', linestyle = "solid", linewidth = subgridwidth, color = subgridcolor, zorder = 0)
###    # Hide ticks.
###    plt.gca().xaxis.set_tick_params(size = 0, which = 'major')
###    plt.gca().xaxis.set_tick_params(size = 0, which = 'minor')
###    plt.gca().yaxis.set_tick_params(size = 0, which = 'major')
###    plt.gca().yaxis.set_tick_params(size = 0, which = 'minor')
###    # Hide spines
###    plt.gca().spines['top'].set_color('none')
###    plt.gca().spines['bottom'].set_color('none')
###    plt.gca().spines['left'].set_color('none')
###    plt.gca().spines['right'].set_color('none')
###    # plt.show()
###    plt.savefig("out.pdf", bbox_inches = 'tight', pad_inches = cm2in(0.1))
###    return
###
###########################################################################################################################
#### Barchart
###########################################################################################################################
###
###def plot_linechart(original_categories, indices, ylabel, xlabels, ymin, ymax, ytick, figwidth, figheight):
###    
###
###########################################################################################################################
#### Setup
###########################################################################################################################
###
###parser = argparse.ArgumentParser(description = "parse log files", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
###parser.add_argument('-v', '--verbose', action = 'store_true', help = 'print verbose messages')
###parser.add_argument('-d', '--develop', action = 'store_true', help = 'output developer data')
###parser.add_argument('-c', '--csv', action = 'store_false', help = 'output CSV file(s)')
###parser.add_argument('-p', '--pdf', action = 'store_false', help = 'output PDF file(s)')
###parser.add_argument('-e', '--error', action = 'store_false', help = 'output error bars')
###parser.add_argument('-a', '--alpha', nargs = '?', action = 'store', type = float, const = 0.95, default = 0.95, help = 'confidence level')
###parser.add_argument('-P', '--paper-format', action = 'store_true', help = 'use a paper format mode')
###parser.add_argument('-x', '--xmin', nargs = '?', action = 'store', type = float, const = None, default = None, help = 'minimum value of X axis')
###parser.add_argument('-X', '--xmax', nargs = '?', action = 'store', type = float, const = None, default = None, help = 'maximum value of X axis')
###parser.add_argument('-y', '--ymin', nargs = '?', action = 'store', type = float, const = None, default = None, help = 'minimum value of Y axis')
###parser.add_argument('-Y', '--ymax', nargs = '?', action = 'store', type = float, const = None, default = None, help = 'maximum value of Y axis')
###parser.add_argument('-W', '--width', nargs = '?', action = 'store', type = float, const = None, default = None, help = 'width of PDF files')
###parser.add_argument('-H', '--height', nargs = '?', action = 'store', type = float, const = None, default = None, help = 'height of PDF files')
###parser.add_argument('-f', '--filter', nargs = '?', action = 'store', type = str, const = None, default = None, help = 'filter string')
###parser.add_argument('input_path', action = 'store', nargs = None, const = None, default = None, type = str, choices = None, help = 'input log file', metavar = None)
###
###args = parser.parse_args()
###
###if args.verbose:
###    print args
###
###########################################################################################################################
#### Read data
###########################################################################################################################
###
###logfile = open(args.input_path)
###lineindex = 0
###categories = []
###for line in logfile:
###    elements = [x.strip() for x in line.split("\t")]
###    if (lineindex == 0):
###        xlabels = elements[1:]
###    else:
###        categorylabel = elements[0]
###        data = [float("0" + x) for x in elements[1:]]
###        color = get_colors(lineindex - 1)
###        categories.append(PltBarCategory(categorylabel, data, color))
###    lineindex += 1
###logfile.close()
###
###indices = [int(x.strip()) for x in args.filter.split(":")]
###ymin = args.ymin
###ymax = args.ymax
###ytick = (args.ymax - args.ymin) / 5
###ylabel = "# of instructions"
###figwidth = args.width
###figheight = args.height
###
###plot_barchart(categories, indices, ylabel, xlabels, ymin, ymax, ytick, figwidth, figheight)
###
###########################################################################################################################
#### Kernel
###########################################################################################################################
