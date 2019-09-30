import sys
import math
import numpy as np, scipy.stats as st
import plot
from dataframe import *

if len(sys.argv) != 2:
    print ("Usage: analysis.py LOG_PATH")
    exit(-1)

g_nskip = 0
g_nrepeats = 20
label = None

log = open(sys.argv[1])
df = dataframe()

alpha = 0
npts_per_box = 0
NP = 0
npts = 0
ndowns, nups, ntotals = (0, 0, 0)

for line in log:
    if line.startswith("### ") and " - MKL_NUM_THREADS=" in line:
        mode = line.split(" ")[1].strip()
        if "DY:" in mode:
            mkl_num_threads = 1
        else:
            mkl_num_threads = int(line.split("MKL_NUM_THREADS=")[1].split(" ")[0].strip())
        label = mode
    elif " ./fmmd--omp_sse_block " in line:
        npts = int(line.split("./fmmd--omp_sse_block ")[1].split(" ")[0])
        npts_per_box = int(line.split("./fmmd--omp_sse_block ")[1].split(" ")[2])
        NP = int(line.split("NP=")[1].split(" ")[0])
        alpha = int(line.split("PLUMMER_ALPHA=")[1].split(" ")[0])
        ndowns, nups, ntotals = (0, 0, 0)
    elif label is not None:
        dtype = "alpha" + str(alpha) + "_nptsbox" + str(npts_per_box) + "_NP" + str(NP) + "_npts" + str(npts)
        key = str(mkl_num_threads)
        if line.startswith("  Down  :"):
            ndowns += 1
            if ndowns <= g_nskip or ndowns > g_nskip + g_nrepeats:
                continue
            time = float("0" + line.split("Down  :")[1].strip().split("secs")[0])
            df.add(dtype + "_down", label, key, time)
        elif line.startswith("  Up    :"):
            nups += 1
            if nups <= g_nskip or nups > g_nskip + g_nrepeats:
                continue
            time = float("0" + line.split("Up    :")[1].strip().split("secs")[0])
            df.add(dtype + "_up", label, key, time)
        if "==> Total Execution Time:" in line:
            ntotals += 1
            if ntotals <= g_nskip or ntotals > g_nskip + g_nrepeats:
                continue
            time = float("0" + line.split("==> Total Execution Time:")[1].strip().split(" secs")[0].split("D")[0])
            df.add(dtype + "_total", label, key, time)

df.print_data(vtype = "ave")

label_rename = {}
labels = ["bolt:FJX:WPR:KH=2:CSAL:AFM=2050:", "icc:WPP:KH=2:", "icc:WPP:CT:KH=2:", "icc:WPP:CL:KH=2:", "icc:WPP:CS:KH=2:", "icc:WPP:DY:KH=2:"]
for label in labels:
    rename = ""
    descriptions = []
    if "gcc:" in label:
        rename = "GOMP"
    elif "icc:" in label:
        rename = "IOMP"
    elif "lcc:" in label:
        rename = "LOMP"
    if "CT:" in label:
        descriptions.append("true")
    elif "CS:" in label:
        descriptions.append("spread")
    elif "CL:" in label:
        descriptions.append("close")
    elif not "DY:" in label:
        descriptions.append("nobind")
    if "DY:" in label:
        descriptions.append("dyn")
    if "TL=" in label:
        TLval = label.split("TL=")[1].split(":")[0]
        descriptions.append("TL=" + TLval)
    # if "XB:" in label:
    #     descriptions.append("NB")
    if len(descriptions) >= 1:
        rename += " ("
        is_first = True
        for description in descriptions:
            if not is_first:
                rename += ", "
            is_first = False
            rename += description
        rename += ")"
    label_rename[label] = rename
    label_rename["bolt:FJX:WPR:KH=2:CSAL:AFM=2050:"] = "BOLT (opt)"

active_labels = []
active_label_dict = {}
for label in labels:
    if "icc:" in label and not "DY:" in label:
        active_label = label.replace(":WPP:", ":WPA:")
        active_labels.append(active_label)
        active_label_dict[active_label] = label


alpha = 100
NPs = [12 ,14, 16]
nptsbox_list = [4000]
npts_list = [100000, 200000, 500000]
time_kinds = ["up", "down"]

for time_kind in time_kinds:
    data_list = []
    for NP in NPs:
        for nptsbox in nptsbox_list:
            for npts in npts_list:
                dtype = "alpha" + str(alpha) + "_nptsbox" + str(nptsbox) + "_NP" + str(NP) + "_npts" + str(npts)
                data, unused, nths = df.extract("ave", dtype + "_" + time_kind, labels[:-1])
                data_err, unused, unused2 = df.extract("s95", dtype + "_" + time_kind, labels[:-1])
                # use active for 1
                active_data, unused, unused2 = df.extract("ave", dtype + "_" + time_kind, active_labels)
                active_data_err, unused, unused2 = df.extract("s95", dtype + "_" + time_kind, active_labels)
                for active_label_i in range(0, len(active_labels)):
                    active_label = active_labels[active_label_i]
                    label_i = labels[:-1].index(active_label_dict[active_label])
                    data[label_i][0] = active_data[active_label_i][0]
                    data_err[label_i][0] = active_data_err[active_label_i][0]

                points = []
                base_y = data[0][0]
                max_y = 1
                for label_i in range(0, len(labels[:-1])):
                    for nth_i in range(0, len(nths)):
                        x = nths[nth_i]
                        if data[label_i][nth_i] > 0.000001:
                            y = base_y / data[label_i][nth_i]
                            y_err = (data_err[label_i][nth_i] / data[label_i][nth_i]) * y
                        else:
                            y = 0
                            y_err = 0
                        if max_y < y:
                            max_y = y
                        newpoint = plot.DataPoint(label_rename[labels[label_i]], x, y, y_err)
                        points.append(newpoint)

                dyn_data_val = df.extract("ave", dtype + "_" + time_kind, [labels[-1]])[0][0][0]
                points.append(plot.DataPoint(label_rename[labels[-1]], -10, base_y / dyn_data_val, 0))
                points.append(plot.DataPoint(label_rename[labels[-1]], 10, base_y / dyn_data_val, 0))
                points.append(plot.DataPoint(label_rename[labels[-1]], 1000, base_y / dyn_data_val, 0))

                line_formats = {}
                xaxis_format = plot.AxisFormat("# of MKL threads", 1, 100, "log", 10)
                yaxis_format = plot.AxisFormat("Relative performance\n(BOLT+1thread = 1)", 0, 4.5, "linear", 1.0)

                size = (5.7, 3.0)
                linechart = plot.LineChartData(points, line_formats, xaxis_format, yaxis_format, size)
                linechart.legend_ncolumns = 2
                plot.plot_linechart(linechart, "pdfs/" + dtype + "_" + time_kind + ".pdf")

                yaxis_format = plot.AxisFormat("Relative performance\n(BOLT+1thread = 1)", 0, 3.7, "linear", 1.0)
                size = (18.0, 7.0)
                linechart = plot.LineChartData(points, line_formats, xaxis_format, yaxis_format, size)
                linechart.legend_ncolumns = 2
                linechart.title = "NP = " + str(NP) + " + " + str(npts / 1000) + ",000 points"
                data_list.append(linechart)
    plot.plot_linecharts(data_list, "pdfs/kifmm_" + time_kind + ".pdf")
