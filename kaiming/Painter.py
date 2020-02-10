import sys
import numpy as np
import matplotlib.pyplot as pyplot
from LineChart import LineChart
from LineChart import LineData
from BarChart import BarChart
from BarChart import BarData


def clean_head_tail_line(strline):
    while strline != "" and (strline[0] == "\t" or strline[0] == " "):
        strline = strline[1:]

    while strline != "" and (strline[-1] == "\n" or strline[-1] == "\t" or strline[-1] == " "):
        strline = strline[:-1]
    return strline

def get_default_fontsize():
    return 6.5

def cm2in(cm):
    return cm / 2.54

class AxisFormat:
    def __init__(self, **kargs):
        # label : "string" | ""
        self.axis_label = ""
        # scale : "log" | "linear"
        self.scale = "linear"

        # ylim low boundary
        self.min_value = 0.0
        # ylim low boundary
        self.max_value = 0.0

        self.tick_label = ""
        self.font_size = 6.5
        self.rotation = 0
        self.label_on = True

        self.minorticks_on = False
        self.grid_on = True

        for key, value in kargs.items():
            if key == "rotation":
                self.rotation = value
            elif key == "minorticks_on":
                self.minorticks_on = value
            elif key == "grid_on":
                self.grid_on = value
            elif key == "tick_num":
                self.tick_num = value
            elif key == "tick_label":
                self.tick_label = tick_label
            elif key == "min_value":
                self.min_value = value
            elif key == "max_value":
                self.max_value = value
            elif key == "label_on":
                self.label_on = value
        return

class Painter:
    def __init__(self, inputfile, outputfile, **kargs):
        self.figsize = (5.7, 3.5)
        self.figure = pyplot.figure(figsize=self.figsize, dpi = 160, facecolor = 'w', edgecolor = 'k')
        self.ax = pyplot.gca()
        self.paint_funcs = {}
        self.legend_ncol = 2
        self.legend_border_width = 0.0
        self.setup_paint_funcs()
        self.outputfile = outputfile
        self.ysecondary = None
        self.chart = None
        self.next = None
        self.legends = []
        self.title = None
        self.xformat = AxisFormat(minorticks_on=False)
        self.yformat = AxisFormat(minorticks_on=True)
        self.delimiter = "\t"
        for key, value in kargs.items():
            if key == "delimiter":
                self.delimiter = value

        self.parse_inputfile(inputfile)

    def set_xtick(self):
        self.xformat.tick_label = clean_head_tail_line(self.file.readline()).split(self.delimiter)
    def set_xlabel(self):
        self.xformat.axis_label = clean_head_tail_line(self.file.readline())
    def set_ylabel(self):
        self.yformat.axis_label = clean_head_tail_line(self.file.readline())
    def set_ylim(self):
        ylim = [int(y) for y in clean_head_tail_line(self.file.readline()).split(self.delimiter)]
        self.yformat.min_value = ylim[0]
        self.yformat.max_value = ylim[1]
    def assign_title(self):
        self.title = clean_head_tail_line(self.file.readline())
    def assign_position(self):
        # x, y, index
        pos = [int(n) for n in clean_head_tail_line(self.file.readline()).split(self.delimiter)]
        if pos[0] != 1 or pos[1] != 1:
            pyplot.subplot(pos[0], pos[1], pos[2])
        self.ax = pyplot.gca()

    def set_figsize(self):
        self.figsize = (float(v) for v in clean_head_tail_line(self.file.readline()).split(self.delimiter))
        self.figure.set_size_inches(self.figsize)

    def set_legend_ncol(self):
        self.legend_ncol = int(clean_head_tail_line(self.file.readline()))

    def create_chart(self):
        self.chart_type = clean_head_tail_line(self.file.readline())
        if self.chart_type == "LineChart":
            self.chart = LineChart()
        elif self.chart_type == "BarChart":
            self.xformat.grid_on = False
            self.chart = BarChart()

    def add_line(self):
        linelabel = clean_head_tail_line(self.file.readline())
        data = [float(x) for x in clean_head_tail_line(self.file.readline()).split(self.delimiter)]
        line = LineData(data, linelabel)
        self.data.append(line)

    def add_bar(self):
        barlabel = [clean_head_tail_line(self.file.readline())]
        data = [[float(x) for x in clean_head_tail_line(self.file.readline()).split(self.delimiter)]]
        bar = BarData(data, barlabel)
        self.data.append(bar)

    def add_stackbar(self):
        barlabel = []
        data = []
        num_stack = int(clean_head_tail_line(self.file.readline()))
        for i in range(0, num_stack):
            barlabel.append(clean_head_tail_line(self.file.readline()))
            data.append([float(x) for x in clean_head_tail_line(self.file.readline()).split(self.delimiter)])
        bar = BarData(data, barlabel)
        self.data.append(bar)

    def set_barwidth(self):
        if self.chart == None:
            self.xformat.grid_on = False
            self.chart = BarChart()
        self.chart.barwidth = float(clean_head_tail_line(self.file.readline()))

    def set_ysecondary(self):
        self.ysecondary = clean_head_tail_line(self.file.readline())
    def set_next(self):
        self.next = clean_head_tail_line(self.file.readline())
    def set_yscale(self):
        self.yformat.scale = clean_head_tail_line(self.file.readline())

    def setup_paint_funcs(self):
        self.paint_funcs["xticks"] = self.set_xtick
        self.paint_funcs["xlabel"] = self.set_xlabel
        self.paint_funcs["ylabel"] = self.set_ylabel
        self.paint_funcs["yscale"] = self.set_yscale
        self.paint_funcs["title"] = self.assign_title
        self.paint_funcs["ylim"] = self.set_ylim

        self.paint_funcs["bar"] = self.add_bar
        self.paint_funcs["barwidth"] = self.set_barwidth
        self.paint_funcs["stackbar"] = self.add_stackbar

        self.paint_funcs["line"] = self.add_line
        self.paint_funcs["chart"] = self.create_chart
        self.paint_funcs["legend_ncol"] = self.set_legend_ncol

        self.paint_funcs["position"] = self.assign_position
        self.paint_funcs["figsize"] = self.set_figsize

        self.paint_funcs["ysecondary"] = self.set_ysecondary
        self.paint_funcs["next"] = self.set_next

    def show_legends(self, legends, ax):
        labels = [lgd.get_label() for lgd in legends]
        ax.legend(legends, labels, loc='best', fancybox=True, fontsize = 1.2 * get_default_fontsize(), ncol = self.legend_ncol, framealpha=1).get_frame().set_linewidth(0.0)
    def parse_inputfile(self, inputfile):
        filename = inputfile
        while True:
            # initialize
            self.data = []
            self.file = open(filename, "r")
            while True:
                command = clean_head_tail_line(self.file.readline())
                if command != "":
                    self.paint_funcs[command]()
                else:
                    break

            # plot figure
            if self.title != None:
                self.ax.set_title(self.title)
            self.legends = self.legends + self.chart.plot(self.data, self.xformat, self.yformat, self.ax)
        
            # release obj
            self.file.close()

            if self.next != None:
                filename = self.next
                del self.xformat
                del self.yformat
                del self.chart
                self.xformat = AxisFormat(minorticks_on=False)
                self.yformat = AxisFormat(minorticks_on=True)
                self.show_legends(self.legends, self.ax)
                self.legends = []
                self.next = None
                self.chart = None
                self.title = None
            elif self.ysecondary != None:
                filename = self.ysecondary
                del self.yformat
                self.ax = self.ax.twinx()
                self.yformat = AxisFormat(minorticks_on=True)
                self.ysecondary = None
                self.title = None
            else:
                break
        self.show_legends(self.legends, self.ax)

    def print_figure(self):
        pyplot.savefig(self.outputfile + ".pdf", bbox_inches='tight', pad_inches = cm2in(0.1), dpi = 160, transparent = True)
        pyplot.close(self.figure)


def help():
    print("Usage: python3 Painter.py inputfile outputfile")

if __name__ == "__main__":
    if sys.argv[1] == "help" or sys.argv[1] == "--help":
        help()
    else:
        # must have 3 parameters
        assert len(sys.argv) == 3
        painter = Painter(sys.argv[1], sys.argv[2])
        painter.print_figure()
