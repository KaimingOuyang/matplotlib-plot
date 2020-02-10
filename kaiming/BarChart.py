import math
import numpy as np
from matplotlib.ticker import AutoMinorLocator

def point_to_inch(point):
    return float(point) / 72.0

def get_default_hatches(index):
    hatches = []
    density = 6
    hatches.append("\\" * density)
    hatches.append("/" * density)
    hatches.append("." * density)
    hatches.append("+" * density)
    hatches.append("x" * density)
    hatches.append("-" * density)
    hatches.append("|" * density)
    hatches.append("o" * density)
    hatches.append("O" * density)
    hatches.append("****" * density)
    return hatches[index % len(hatches)]

# def get_color_list():
#     colors = []
#     colors.append("#5B9BD5") # blue
#     colors.append("#ED7D31") # orange
#     colors.append("#FFDE03") # yellow
#     colors.append("#70AD47") # green
#     colors.append("#FFC000") # brown
#     colors.append("#800080") # purple
#     colors.append("#FF0266") # red
#     colors.append("#F08080") # pink
#     colors.append("#59B8CC") # light blue
#     colors.append("#E59400") # dark orange
#     colors.append("#DAA520") # dark yellow
#     return colors

def get_default_colors(index):
    colors = []
    colors.append((0.266, 0.447, 0.768))
    colors.append((0.929, 0.490, 0.192))
    colors.append((1.000, 0.752, 0.000))
    colors.append((0.356, 0.607, 0.835))
    colors.append((0.439, 0.678, 0.278))
    colors.append((0.149, 0.266, 0.470))
    colors.append((0.619, 0.282, 0.054))
    colors.append((0.647, 0.647, 0.647))
    return colors[index % len(colors)]

class BarData:
    def __init__(self, data, barlabel):
        self.data = data
        self.barlabel = barlabel

class BarChart:
    def __init__(self):
        self.bar_cnt = 0
        self.grid_linewidth = 0.2
        self.grid_dashes = (0.5, 0.5)
        self.barwidth = 0.4
        self.linewidth = 0.8
        self.legends = []

    def plot(self, databars, xformat, yformat, ax, **kwargs):
        num_bars = len(databars)
        # set x axis
        ax.set_xticks(range(0, len(xformat.tick_label)))
        ax.set_xticklabels(xformat.tick_label)
        for tick in ax.get_xticklabels():
            tick.set_rotation(xformat.rotation)
        if xformat.label_on == True:
            ax.set_xlabel(xformat.axis_label)

        # set y axis
        if yformat.grid_on == True:
            ax.yaxis.grid(which = 'major', linestyle = '--', linewidth = self.grid_linewidth, dashes = self.grid_dashes)
        if yformat.minorticks_on == True:
            ax.yaxis.set_minor_locator(AutoMinorLocator())
        if yformat.scale == "log":
            ax.set_yscale('log')
        if yformat.label_on == True:
            ax.set_ylabel(yformat.axis_label)
        if yformat.min_value != yformat.max_value:
            ax.set_ylim(yformat.min_value, yformat.max_value)
            
        if num_bars % 2 == 0:
            shift_base = self.barwidth / 2 + point_to_inch(self.linewidth) / 2.0
        else:
            shift_base = 0
        for i in range(0, num_bars):
            shift = (i - int(num_bars / 2)) * (self.barwidth + point_to_inch(self.linewidth)) + shift_base
            for j in range(0, len(databars[i].data)):
                if j == 0:
                    self.legends.append(ax.bar(np.arange(len(databars[i].data[j])) + shift, databars[i].data[j], width = self.barwidth, align="center", linewidth = self.linewidth, label = databars[i].barlabel[j], hatch = get_default_hatches(self.bar_cnt), color = "w", edgecolor=get_default_colors(self.bar_cnt)))
                else:
                    self.legends.append(ax.bar(np.arange(len(databars[i].data[j])) + shift, databars[i].data[j], width = self.barwidth, align="center", linewidth = self.linewidth, label = databars[i].barlabel[j], hatch = get_default_hatches(self.bar_cnt), color = "w", edgecolor=get_default_colors(self.bar_cnt), bottom = databars[i].data[j - 1]))
                self.bar_cnt += 1
        return self.legends