import matplotlib.pyplot as pyplot
from LineChart import LineChartObj
from LineChart import LineFormat
from matplotlib.ticker import MultipleLocator as mtlocator
import matplotlib.ticker as ticker
import numpy as np
import sys

def clean_head_tail_line(strline):
    if strline == "":
        return strline
    while strline[0] == "\t" or strline[0] == " ":
        strline = strline[1:]
    while strline[-1] == "\n" or strline[-1] == "\t" or strline[-1] == " ":
        strline = strline[:-1]
    return strline

def get_default_fontsize():
    return 6.5

def cm2in(cm):
    return cm / 2.54

def get_default_colors(index):
    colors = []
    colors.append((0.266, 0.447, 0.768))
    colors.append((0.929, 0.490, 0.192))
    colors.append((0.619, 0.282, 0.054))
    colors.append((1.000, 0.752, 0.000))
    colors.append((0.356, 0.607, 0.835))
    colors.append((0.439, 0.678, 0.278))
    colors.append((0.149, 0.266, 0.470))
    colors.append((0.647, 0.647, 0.647))
    
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

class AxisFormat:
    def __init__(self):
        # label : "string" | None
        self.axis_label = ""
        # scale : "log" | "linear" | "label"
        self.scale = "linear"

        # min_value : 0.0~ (< max_value)
        self.min_value = 0.0
        # max_value : 0.0~ (> min_value)
        self.max_value = 0.0
        self.tick_label = ""
        self.tick_num = 8
        self.font_size = 6.5
        self.rotation = 0
        self.minorticks_on = True
        self.grid_on = True
        self.label_on = True

        # for key, value in kargs.items():
        #     if key == "rotation":
        #         self.rotation = value
        #     elif key == "minorticks_on":
        #         self.minorticks_on = value
        #     elif key == "grid_on":
        #         self.grid_on = value
        #     elif key == "tick_num":
        #         self.tick_num = value
        #     elif key == "tick_label":
        #         self.tick_label = tick_label
        #     elif key == "min_value":
        #         self.min_value = value
        #     elif key == "max_value":
        #         self.max_value = value
        #     elif key == "label_on":
        #         self.label_on = value
        return

class Painter:
    def __init__(self, inputfiles, outputfile, **kargs):
        self.figure = None
        self.paint_funcs = {}
        self.legend_ncol = 1
        self.legend_border_width = 0.2
        self.setup_paint_funcs()
        self.parse_inputfiles(inputfiles)
        self.outputfile = outputfile
        self.delimiter = "\t"
        for key, value in kargs.items():
            if key == "delimiter":
                self.delimiter = value
        # self.figsize=(11, 5.5) # minighost figure size
        # self.figsize=(20, 4) # multiple figure size
        # self.figsize=(5, 3.5) # line figure size
        # self.figsize=(5, 4) # line figure size
        
        # self.figure, self.axes = pyplot.subplots(nrows=2, ncols=2)

        # self.figure, self.axes = pyplot.subplots(nrows=1, ncols=self.file_num)
        # self.figure.
        # self.axes = self.figure.add_axes()
        # self.line_cnt = 0
        # self.bar_cnt = 0
        # self.bar_width = 0.35
        # pyplot.axes().yaxis.set_major_locator(mtlocator(2))
        # pyplot.axes().set_yscale("log", basey=2)
        # pyplot.minorticks_on()
        # pyplot.axes().yaxis.set_minor_locator(ticker.AutoMinorLocator())
        # pyplot.grid(axis='y', which = 'major', linestyle = '--', linewidth = 0.2, dashes = (0.5, 0.5)) 

    def set_xtick(self):
        self.xformat.tick_label = clean_head_tail_line(self.file.readline()).split("\t")
    def set_xlabel(self):
        self.xformat.axis_label = clean_head_tail_line(self.file.readline())
    def set_ylabel(self):
        self.yformat.axis_label = clean_head_tail_line(self.file.readline())
    def set_ylim(self):
        ylim = [int(y) for y in clean_head_tail_line(self.file.readline()).split("\t")]
        self.yformat.min_value = ylim[0]
        self.yformat.max_value = ylim[1]
    def assign_title(self):
        self.title = clean_head_tail_line(self.file.readline())
    def assign_position(self):
        # x, y, index
        pos = [int(n) for n in clean_head_tail_line(self.file.readline()).split("\t")]
        if self.figure == None:
            if pos[0] == 1 and pos[1] == 1:
                self.figsize = (6, 3.5)
            else:
                self.figsize = (5.0 * pos[0], 4 * pos[1])
            self.figure = pyplot.figure(figsize=self.figsize, dpi = 160, facecolor = 'w', edgecolor = 'k')
        if pos[0] != 1 or pos[1] != 1:
            pyplot.subplot(pos[0], pos[1], pos[2])
        self.ax = pyplot.gca()

    def set_legend_ncol(self):
        self.legend_ncol = int(clean_head_tail_line(self.file.readline()))

    def create_chart(self):
        self.chart_type = clean_head_tail_line(self.file.readline())
        if self.chart_type == "LineChart":
            self.chart = LineChartObj()
        elif self.chart_type == "BarChart": 
            self.chart = None

    def add_line(self):
        linelabel = clean_head_tail_line(self.file.readline())
        data = [float(x) for x in clean_head_tail_line(self.file.readline()).split("\t")]
        line = LineFormat(data, linelabel)
        self.datalines.append(line)

    def setup_paint_funcs(self):
        self.paint_funcs["xticks"] = self.set_xtick
        self.paint_funcs["xlabel"] = self.set_xlabel
        self.paint_funcs["ylabel"] = self.set_ylabel
        self.paint_funcs["title"] = self.assign_title
        self.paint_funcs["position"] = self.assign_position
        self.paint_funcs["ylim"] = self.set_ylim
        self.paint_funcs["line"] = self.add_line
        self.paint_funcs["chart"] = self.create_chart
        self.paint_funcs["legend_ncol"] = self.set_legend_ncol

    def parse_inputfiles(self, inputfiles):
        for filename in inputfiles:
            self.xformat = AxisFormat()
            self.yformat = AxisFormat()
            self.title = ""
            self.chart = None
            self.secondary = False
            self.legends = []
            self.datalines = []
            self.file = open(filename, "r")
            while True:
                command = clean_head_tail_line(self.file.readline())
                if command != "":
                    self.paint_funcs[command]()
                else:
                    break

            # plot figure
            self.legends = self.chart.plot(self.datalines, self.xformat, self.yformat, self.ax)
            # self.lgd = self.ax.legend(self.legends, [legend.get_label() for legend in self.legends], fancybox=True, fontsize = 1.2 * get_default_fontsize(), ncol = self.legend_ncol, framealpha=1)
            self.lgd = self.ax.legend(fancybox=True, fontsize = 1.2 * get_default_fontsize(), ncol = self.legend_ncol, framealpha=1)
            self.lgd.get_frame().set_linewidth(self.legend_border_width)
            self.ax.set_title(self.title)

            # release obj
            del self.xformat
            del self.yformat
            del self.chart
            self.file.close()
        # while True:
        #     command = data_file.readline()[:-1]
        #     if command != "":
        #         elif command == "line":
        #             label = data_file.readline()[1:-1]
        #             data = [float(v) for v in data_file.readline()[1:-1].split()]
        #             # print(data)
        #             marker = get_default_markers(self.line_cnt)
        #             color = get_default_colors(self.line_cnt)
        #             self.line_cnt += 1
        #             pyplot.subplot(x, y, index)

        #             # pyplot.yscale("log", basey=2)
        #             pyplot.plot(data, label = label, marker = marker, linewidth = 0.2, markersize = 3.0, color = color)
        #             axes = pyplot.gca()
        #             axes.set_xticks(np.arange(len(self.xticks)));
        #             # axes.tick_params(axis='y', which='minor', direction='out')
        #             # axes.yaxis.set_minor_formatter(ticker.FormatStrFormatter("%.1f"))
        #             # axes.yaxis.set_minor_locator(ticker.AutoMinorLocator());
        #             axes.set_xticklabels(self.xticks)
        #             for tick in axes.get_xticklabels():
        #                 tick.set_rotation(45)
        #             axes.yaxis.grid(which = 'major', linestyle = '--', linewidth = 0.2, dashes = (0.5, 0.5))
        #             if self.title != "":
        #                 axes.set_xlabel(self.xtitle)
        #             axes.set_title(self.title)
        #             # if index % y == 1:
        #             pyplot.ylabel(self.ytitle);

        #             # axes.set_title(self.title);
        #             # axes.plot(data, label = label, marker = marker, linewidth = 0.2, markersize = 3.0, color = color)
        #             pyplot.ylim(ylim[0], ylim[1])
        #         elif command == "stackbar":
        #             stack_num = int(data_file.readline()[1:-1])
        #             data = []
        #             for i in range(0, stack_num):
        #                 label = data_file.readline()[1:-1]
        #                 data.append([float(yvalue) for yvalue in data_file.readline()[1:-1].split()])
        #                 hatch = get_default_hatches(self.line_cnt)
        #                 color = get_default_colors(self.line_cnt)
        #                 self.line_cnt += 1
        #                 # print(data[i], len(data[i]))
        #                 if i == 0:
        #                     pyplot.bar(range(0, len(data[i])), data[i], width = self.bar_width, align = 'center', linewidth = 1, label = label, hatch = hatch, color = "w", edgecolor=color)
        #                 else:
        #                     pyplot.bar(range(0, len(data[i])), data[i], width = self.bar_width, align = 'center', linewidth = 1, bottom = data[i - 1], label = label, hatch = hatch, color = "w", edgecolor=color)
        #             # pyplot.axhline(y=828.676, color='r', linestyle='--')
        #             pyplot.legend(loc = (.0,1.01), fancybox=True, fontsize = 1.8 * get_default_fontsize(), ncol = 2, framealpha=0.0)
        #         elif command == "bar":
        #             data = [float(yvalue) for yvalue in data_file.readline()[1:-1].split()]
        #             # print(np.arange(len(data)) + shift,", data=",data)
        #             pyplot.bar(np.arange(len(data)), data, width = self.bar_width, align="center", linewidth = 0.1)
        #         elif command == "groupbars":
        #             pyplot.xticks(np.arange(len(self.xticks)), self.xticks)
        #             pyplot.xlabel(self.xtitle)
        #             pyplot.ylabel(self.ytitle)
        #             bar_num = int(data_file.readline()[1:-1])
        #             shift_base = 0
        #             if bar_num % 2 == 0:
        #                 shift_base = self.bar_width / 2
        #             for i in range(0, bar_num):
        #                 shift = (i - int(bar_num / 2)) * self.bar_width + shift_base
        #                 label = data_file.readline()[1:-1]
        #                 color = get_default_colors(self.bar_cnt)
        #                 hatch = get_default_hatches(self.bar_cnt)
        #                 self.bar_cnt += 1
        #                 data = [float(yvalue) for yvalue in data_file.readline()[1:-1].split()]
        #                 # print(np.arange(len(data)) + shift,", data=",data)
        #                 pyplot.bar(np.arange(len(data)) + shift, data, width = self.bar_width, align="center", linewidth = 0.0, label = label, hatch = hatch, color = "w", edgecolor=color)
        #         elif command == "ysecondary":
        #             ysec_axis = pyplot.twinx()
        #             line_num = int(data_file.readline()[1:-1])
        #             for i in range(0, line_num):
        #                 command = data_file.readline()[1:-1]
        #                 if command == "line":
        #                     label = data_file.readline()[2:-1]
        #                     data = [float(yvalue) for yvalue in data_file.readline()[2:-1].split()]
        #                     marker = get_default_markers(self.line_cnt)
        #                     color = get_default_colors(self.line_cnt)
        #                     self.line_cnt += 1
        #                     ysec_axis.plot(data, label = label, marker = marker, linewidth = 1.5, markersize = 3.0, color = color)
        #                 elif command == "ytitle":
        #                     ysec_axis.set_ylabel(data_file.readline()[2:-1])
        #             ysec_axis.legend(loc = (.38, 1.01), fancybox=True, fontsize = 1.8 * get_default_fontsize(), ncol = 2, framealpha=0.0)
        #         else:
        #             print("Command %s is not defined yet" % command)
        #     else:
        #         break

    def print_figure(self):
        # for i in range(0, self.file_num):
        #     self.line_cnt = 0
        #     data_file = open(sys.argv[i + 1], "r")
        #     self.parse_data_file(data_file, 1, self.file_num, i + 1)
        #     data_file.close()
        # axes = pyplot.gca()
        # handles, labels = axes.get_legend_handles_labels()
        # self.figure()
        # self.figure.legend(handles, labels, loc='best', bbox_to_anchor=(0.5, 1.1), fancybox=True, shadow=True, fontsize = 1.6 * get_default_fontsize(), ncol = 4, framealpha=1)
        # pyplot.legend(loc='lower center', bbox_to_anchor=(-1.35, -0.33), fancybox=True, shadow=True, fontsize = 1.6 * get_default_fontsize(), ncol = 4, framealpha=1)
        # legend = pyplot.legend(fancybox=True, fontsize = 1.2 * get_default_fontsize(), ncol = self.legend_ncol, framealpha=1)
        # legend.get_frame().set_linewidth(self.legend_border_width)
        pyplot.savefig(self.outputfile + ".pdf", bbox_inches='tight', pad_inches = cm2in(0.1), dpi = 160, transparent = True)
        pyplot.close(self.figure)

    


