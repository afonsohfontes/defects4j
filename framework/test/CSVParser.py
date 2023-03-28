import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys
import getopt

from scipy.stats import wilcoxon
from numpy import mean, std # version >= 1.7.1 && <= 1.9.1
from math import sqrt

pd.options.mode.chained_assignment = None

def myfunc(argv):
    arg_file = ""
    arg_help = "{0} -f <path to results> -o <path to output> -c <criterion>".format(argv[0])

    try:
        opts, args = getopt.getopt(argv[1:], "f:o:c:", ["f=","o=","c="])
    except:
        print(arg_help)
        print("failed to get opt")
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-f", "--file"):
            arg_file= arg
        elif opt in ("-o"):
            arg_o= arg
        elif opt in ("-c"):
            arg_c = arg

    if str(arg_file)=="":
        print("A file path is needed.")
        print(arg_help)
        sys.exit(2)
    if str(arg_o)=="":
        print("An output path is needed.")
        print(arg_help)
        sys.exit(2)
    if str(arg_c)=="":
        print("A criterion path is needed.")
        print(arg_help)
        sys.exit(2)

    df = pd.read_csv(arg_file)
    BranchCoverageTimeline = [0]
    x = [0]
    i = 0
    for (columnName, columnData) in df.items():
        if "BranchCoverageTimeline" in columnName:
            i=i+1
            BranchCoverageTimeline = np.append(BranchCoverageTimeline, columnData)
            x = np.append(x, i*0.5)


    #plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True

    plt.title("Branch Coverage Timeline - Evolution")
    plt.plot(x, BranchCoverageTimeline, color="red")
    BranchCoverageTimeline = [x,BranchCoverageTimeline]
    plt.show()

    ExceptionCoverageTimeline = [0]
    x = [0]
    i = 0
    for (columnName, columnData) in df.items():
        if "ExceptionCoverageTimeline" in columnName:
            i=i+1
            ExceptionCoverageTimeline = np.append(ExceptionCoverageTimeline, columnData)
            x = np.append(x, i*0.5)


    plt.title("ExceptionCoverageTimeline - Evolution")
    plt.plot(x, ExceptionCoverageTimeline, color="red")
    ExceptionCoverageTimeline = [x,ExceptionCoverageTimeline]
    plt.show()


    df = pd.read_csv(arg_o)
    row = 99
    if arg_c=="BRANCH":
        row=0
    elif arg_c=="PRIVATEMETHOD":
        row=1
    elif arg_c=="EXCEPTION":
        row=2
    elif arg_c=="BRANCH:PRIVATEMETHOD":
        row=3
    elif arg_c=="BRANCH:EXCEPTION":
        row=4
    if row<5:
        df.BranchCoverageTimeline[row] = BranchCoverageTimeline
        df.ExceptionCoverageTimeline[row] = ExceptionCoverageTimeline
        df.to_csv(arg_o)
        print(df)


if __name__ == "__main__":
    myfunc(sys.argv)