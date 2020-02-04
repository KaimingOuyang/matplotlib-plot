import math
import matplotlib.pyplot as mtplot
import matplotlib.ticker as ticker
from matplotlib.ticker import MultipleLocator as mtlocator

def get_color_list():
    colors = []
    colors.append("#5B9BD5") # blue
    colors.append("#ED7D31") # orange
    colors.append("#FFDE03") # yellow
    colors.append("#70AD47") # green
    colors.append("#FFC000") # brown
    colors.append("#800080") # purple
    colors.append("#FF0266") # red
    colors.append("#F08080") # pink
    colors.append("#59B8CC") # light blue
    colors.append("#E59400") # dark orange
    colors.append("#DAA520") # dark yellow
    return colors

def get_marker_list():
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
    return markers

class LineFormat:
    line_index = 0
    def __init__(self, data, linelabel):
        self.data = data
        self.linelabel = linelabel
        self.linewidth = 0.3
        self.markersize = 3.0

class LineChartObj:
    def plot(self, datalines, xformat, yformat, ax, **kwargs):
        # set x axis
        ax.set_xticks(range(0, len(xformat.tick_label)))
        ax.set_xticklabels(xformat.tick_label)
        for tick in ax.get_xticklabels():
            tick.set_rotation(xformat.rotation)
        if xformat.grid_on == True:
            ax.xaxis.grid(which = 'major', linestyle = '--', linewidth = self.grid_linewidth, dashes = self.grid_dashes)
        if xformat.minorticks_on == True:
            ax.tick_params(axis = 'x', which = 'minor', bottom = False, top = False)
        if xformat.label_on == True:
            ax.set_xlabel(xformat.axis_label)

        # set y axis
        if yformat.grid_on == True:
            ax.yaxis.grid(which = 'major', linestyle = '--', linewidth = self.grid_linewidth, dashes = self.grid_dashes)
        if yformat.minorticks_on == True:
            ax.tick_params(axis = 'y', which = 'minor', left = False, right = False)

        if yformat.scale == "linear":
            ax.set_yticks([yformat.min_value + y * yformat.tick_num for y in range(0, int((yformat.max_value - yformat.min_value) / yformat.tick_num + 1))])
        elif yformat.scale == "log":
            ax.set_yicks([2 ** y  for y in range(int(math.floor(math.log2(yformat.min_value))), int(math.ceil(math.log2(data.yaxis_format.max_value))))])

        if yformat.label_on == True:
            ax.set_ylabel(yformat.axis_label)

        # draw the lines
        for i in range(0, len(datalines)):
            ax.plot(datalines[i].data, label = datalines[i].linelabel, marker = self.markers[i], linewidth = datalines[i].linewidth, markersize = datalines[i].markersize, color = self.colors[i])

    def __init__(self):
        # init line style
        self.colors = get_color_list()
        self.markers = get_marker_list()
        self.xformat = None
        self.yformat = None
        self.grid_linewidth = 0.2
        self.grid_dashes = (0.5, 0.5)
        # self.figure = mtplot.figure(figsize=self.figsize, dpi = 160, facecolor = 'w', edgecolor = 'k')
        # self.figure, self.axes = mtplot.subplots(nrows=2, ncols=2)

        # self.figure, self.axes = mtplot.subplots(nrows=1, ncols=self.file_num)
        # self.figure.
        # self.axes = self.figure.add_axes()
        
        # mtplot.axes().yaxis.set_major_locator(mtlocator(2))
        # mtplot.axes().set_yscale("log", basey=2)
        # mtplot.minorticks_on()
        # mtplot.axes().yaxis.set_minor_locator(ticker.AutoMinorLocator())
        mtplot.grid(axis='y', which = 'major', linestyle = '--', linewidth = 0.2, dashes = (0.5, 0.5)) 


    def parse_data_file(self, data_file, x, y, index):
        while True:
            command = data_file.readline()[:-1]
            if command != "":
                if command == "xtick":
                    self.xticks =data_file.readline()[1:-1].split("\t")
                    # print(self.xticks)
                    # axes.set_xticks(np.arange(len(self.xticks)), self.xticks)
                    # mtplot.xticks(np.arange(len(self.xticks)), self.xticks)
                elif command == "xtitle":
                    self.xtitle = data_file.readline()[1:-1]
                    # axes.set_xlabel(data_file.readline()[1:-1])
                    # mtplot.xlabel(data_file.readline()[1:-1])
                elif command == "ytitle":
                    self.ytitle = data_file.readline()[1:-1]
                    # axes.set_ylabel(data_file.readline()[1:-1])
                    # mtplot.ylabel(data_file.readline()[1:-1])
                elif command == "title":
                    self.title = data_file.readline()[1:-1]
                    # mtplot.title(data_file.readline()[1:-1])
                elif command == "line":
                    label = data_file.readline()[1:-1]
                    data = [float(v) for v in data_file.readline()[1:-1].split()]
                    # print(data)
                    marker = get_default_markers(self.line_cnt)
                    color = get_default_colors(self.line_cnt)
                    self.line_cnt += 1
                    mtplot.subplot(x, y, index)

                    # mtplot.yscale("log", basey=2)
                    mtplot.plot(data, label = label, marker = marker, linewidth = 0.2, markersize = 3.0, color = color)
                    axes = mtplot.gca()
                    axes.set_xticks(np.arange(len(self.xticks)));
                    # axes.tick_params(axis='y', which='minor', direction='out')
                    # axes.yaxis.set_minor_formatter(ticker.FormatStrFormatter("%.1f"))
                    # axes.yaxis.set_minor_locator(ticker.AutoMinorLocator());
                    axes.set_xticklabels(self.xticks)
                    for tick in axes.get_xticklabels():
                        tick.set_rotation(45)
                    axes.yaxis.grid(which = 'major', linestyle = '--', linewidth = 0.2, dashes = (0.5, 0.5))
                    if self.title != "":
                        axes.set_xlabel(self.xtitle)
                    axes.set_title(self.title)
                    # if index % y == 1:
                    mtplot.ylabel(self.ytitle);

                    # axes.set_title(self.title);
                    # axes.plot(data, label = label, marker = marker, linewidth = 0.2, markersize = 3.0, color = color)
                elif command == "ylim":
                    ylim = [float(lim) for lim in data_file.readline()[1:-1].split()]
                    mtplot.ylim(ylim[0], ylim[1])
                elif command == "stackbar":
                    stack_num = int(data_file.readline()[1:-1])
                    data = []
                    for i in range(0, stack_num):
                        label = data_file.readline()[1:-1]
                        data.append([float(yvalue) for yvalue in data_file.readline()[1:-1].split()])
                        hatch = get_default_hatches(self.line_cnt)
                        color = get_default_colors(self.line_cnt)
                        self.line_cnt += 1
                        # print(data[i], len(data[i]))
                        if i == 0:
                            mtplot.bar(range(0, len(data[i])), data[i], width = self.bar_width, align = 'center', linewidth = 1, label = label, hatch = hatch, color = "w", edgecolor=color)
                        else:
                            mtplot.bar(range(0, len(data[i])), data[i], width = self.bar_width, align = 'center', linewidth = 1, bottom = data[i - 1], label = label, hatch = hatch, color = "w", edgecolor=color)
                    # mtplot.axhline(y=828.676, color='r', linestyle='--')
                    mtplot.legend(loc = (.0,1.01), fancybox=True, fontsize = 1.8 * get_default_fontsize(), ncol = 2, framealpha=0.0)
                elif command == "bar":
                    data = [float(yvalue) for yvalue in data_file.readline()[1:-1].split()]
                    # print(np.arange(len(data)) + shift,", data=",data)
                    mtplot.bar(np.arange(len(data)), data, width = self.bar_width, align="center", linewidth = 0.1)
                elif command == "groupbars":
                    mtplot.xticks(np.arange(len(self.xticks)), self.xticks)
                    mtplot.xlabel(self.xtitle)
                    mtplot.ylabel(self.ytitle)
                    bar_num = int(data_file.readline()[1:-1])
                    shift_base = 0
                    if bar_num % 2 == 0:
                        shift_base = self.bar_width / 2
                    for i in range(0, bar_num):
                        shift = (i - int(bar_num / 2)) * self.bar_width + shift_base
                        label = data_file.readline()[1:-1]
                        color = get_default_colors(self.bar_cnt)
                        hatch = get_default_hatches(self.bar_cnt)
                        self.bar_cnt += 1
                        data = [float(yvalue) for yvalue in data_file.readline()[1:-1].split()]
                        # print(np.arange(len(data)) + shift,", data=",data)
                        mtplot.bar(np.arange(len(data)) + shift, data, width = self.bar_width, align="center", linewidth = 0.0, label = label, hatch = hatch, color = "w", edgecolor=color)
                elif command == "ysecondary":
                    ysec_axis = mtplot.twinx()
                    line_num = int(data_file.readline()[1:-1])
                    for i in range(0, line_num):
                        command = data_file.readline()[1:-1]
                        if command == "line":
                            label = data_file.readline()[2:-1]
                            data = [float(yvalue) for yvalue in data_file.readline()[2:-1].split()]
                            marker = get_default_markers(self.line_cnt)
                            color = get_default_colors(self.line_cnt)
                            self.line_cnt += 1
                            ysec_axis.plot(data, label = label, marker = marker, linewidth = 1.5, markersize = 3.0, color = color)
                        elif command == "ytitle":
                            ysec_axis.set_ylabel(data_file.readline()[2:-1])
                    ysec_axis.legend(loc = (.38, 1.01), fancybox=True, fontsize = 1.8 * get_default_fontsize(), ncol = 2, framealpha=0.0)
                else:
                    print("Command %s is not defined yet" % command)
            else:
                break





