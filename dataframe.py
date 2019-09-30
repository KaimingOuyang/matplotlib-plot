
import re
import sys
import numpy as np
import scipy.stats as st

################################################################################
# data[dtype][label][key]
#
# dtype[0]
#          label[0]   label[1]   label[2]   ...
#  key[0]  value[0-0] value[0-1] value[0-2] ...
#  key[1]  value[1-0] value[1-1] value[1-2] ...
#  key[2]  value[2-0] value[2-1] value[2-2] ...
#  ...
#
# dtype[0]
# ...
################################################################################

class dataframe:
    @staticmethod
    def atoi(text):
        # https://stackoverflow.com/questions/5967500/how-to-correctly-sort-a-string-with-a-number-inslabele
        return int(text) if text.isdigit() else text

    @staticmethod
    def natural_keys(text):
        '''
        alist.sort(key=natural_keys) sorts in human order
        http://nedbatchelder.com/blog/200712/human_sorting.html
        (See Toothy's implementation in the comments)
        '''
        return [ dataframe.atoi(c) for c in re.split('(\d+)', text) ]

    def __init__(self):
        self.data = {}
        self.alldtypes = []
        self.alllabels = []
        self.allkeys = []

    def init_array(self, dtype, label, key):
        if not dtype in self.data:
            self.data[dtype] = {}
            self.alldtypes.append(dtype)
        if not label in self.data[dtype]:
            self.data[dtype][label] = {}
            if not label in self.alllabels:
                self.alllabels.append(label)
        if not key in self.data[dtype][label]:
            self.data[dtype][label][key] = []
            if not key in self.allkeys:
                self.allkeys.append(key)

    def add(self, dtype, label, key, value):
        self.init_array(dtype, label, key)
        self.data[dtype][label][key].append(value)

    def overwrite(self, dtype, label, key):
        self.init_array(dtype, label, key)
        self.data[dtype][label][key] = [value]

    def get_raw(self, dtype, label, key):
        self.init_array(dtype, label, key)
        return self.data[dtype][label][key]

    def get(self, dtype, label, key, vtype):
        values = self.get_raw(dtype, label, key)
        len_values = len(values)
        if len_values == 0:
            return 0.0
        if vtype == "ave":
            return np.mean(values)
        elif vtype == "med":
            return np.median(values)
        elif vtype == "bsd":
            return np.std(values, ddof = 0)
        elif vtype == "usd":
            # not strictly unbiased: https://en.wikipedia.org/wiki/Unbiased_estimation_of_standard_deviation
            return np.std(values, ddof = 1)
        elif vtype == "s95":
            interval = st.t.interval(0.95, len(values) - 1, loc = np.mean(values), scale = st.sem(values))
            return interval[1] - np.mean(values)
        elif vtype == "s99":
            interval = st.t.interval(0.99, len(values) - 1, loc = np.mean(values), scale = st.sem(values))
            return interval[1] - np.mean(values)
        elif vtype == "cnt":
            return len_values
        return 0

    def has_dtype(self, dtype):
        return dtype in self.data

    def print_data(self, vtype, dtypes = None, labels = None, keys = None):
        if dtypes is None:
            dtypes = sorted(self.alldtypes, key = dataframe.natural_keys)
        for dtype in dtypes:
            sys.stdout.write("## dtype = " + dtype + " : " + vtype + "\n")
            if labels is None:
                print_labels = sorted(self.data[dtype].keys(), key = dataframe.natural_keys)
            else:
                print_labels = labels
            for label in print_labels:
                sys.stdout.write("\t" + label)
            sys.stdout.write("\n")

            if keys is None:
                local_allkeys = []
                for label in print_labels:
                    if not label in self.data[dtype].keys():
                        continue
                    for key in self.data[dtype][label].keys():
                        if not key in local_allkeys:
                            local_allkeys.append(key)
                print_keys = sorted(local_allkeys, key = dataframe.natural_keys)
            else:
                print_keys = keys

            for key in print_keys:
                sys.stdout.write(str(key))
                for label in print_labels:
                    sys.stdout.write("\t" + str(self.get(dtype, label, key, vtype)))
                sys.stdout.write("\n")
            sys.stdout.write("\n")

    # dtype
    #              keys[0]     keys[1]     keys[2]    ...
    #  labels[0] [[value[0-0], value[1-0], value[2-0], ...],
    #  labels[1]  [value[0-1], value[1-1], value[2-1], ...],
    #  labels[2]  [value[0-2], value[1-2], value[2-2], ...], ... ]
    def extract(self, vtype, dtype, labels = None, keys = None):
        retvals = []
        if not dtype in self.alldtypes:
            retvals = [[0.0 for i in range(0, len(keys))] for j in range(0, len(labels))]
            return retvals

        if labels is None:
            labels = sorted(self.data[dtype].keys(), key = dataframe.natural_keys)
        if keys is None:
            local_allkeys = []
            for label in labels:
                if not label in self.data[dtype].keys():
                    continue
                for key in self.data[dtype][label].keys():
                    if not key in local_allkeys:
                        local_allkeys.append(key)
                keys = sorted(local_allkeys, key = dataframe.natural_keys)

        for label in labels:
            local_retval = []
            for key in keys:
                local_retval.append(self.get(dtype, label, key, vtype))
            retvals.append(local_retval)
        return retvals, labels, keys
