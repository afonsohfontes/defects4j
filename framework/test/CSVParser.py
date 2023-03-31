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
    BranchCoverageTimeline_x = [0]
    BranchCoverageTimeline_i = 0

    CoverageTimeline = [0]
    CoverageTimeline_x = [0]
    CoverageTimeline_i = 0

    BranchBitstringTimeline = [0]
    BranchBitstringTimeline_x = [0]
    BranchBitstringTimeline_i = 0

    PrivateMethodBitstringTimeline = [0]
    PrivateMethodBitstringTimeline_x = [0]
    PrivateMethodBitstringTimeline_i = 0

    PrivateMethodCoverageTimeline = [0]
    PrivateMethodCoverageTimeline_x = [0]
    PrivateMethodCoverageTimeline_i = 0

    ExceptionCoverageTimeline = [0]
    ExceptionCoverageTimeline_x = [0]
    ExceptionCoverageTimeline_i = 0

    Coverage = "no data"
    Total_Goals = "no data"
    Covered_Goals = "no data"
    BranchCoverage = "no data"
    Total_Branches = "no data"
    Covered_Branches = "no data"
    BranchCoverageBitString = "no data"
    PrivateMethodCoverage = "no data"
    PrivateMethodCoverageBitString = "no data"
    ExceptionCoverage = "no data"
    ExceptionCoverageBitString = "no data"

    for (columnName, columnData) in df.items():
        if columnName=="Coverage":
            Coverage = columnData
        if columnName=="Total_Goals":
            Total_Goals = columnData
        if columnName=="Covered_Goals":
            Covered_Goals = columnData
        if columnName=="BranchCoverage":
            BranchCoverage = columnData
        if columnName=="Total_Branches":
            Total_Branches = columnData
        if columnName=="Covered_Branches":
            Covered_Branches = columnData
        if columnName=="BranchCoverageBitString":
            BranchCoverageBitString = columnData
        if columnName=="PrivateMethodCoverage":
            PrivateMethodCoverage = columnData
        if columnName=="PrivateMethodCoverageBitString":
            PrivateMethodCoverageBitString = columnData
        if columnName=="ExceptionCoverage":
            ExceptionCoverage = columnData
        if columnName=="ExceptionCoverageBitString":
            ExceptionCoverageBitString = columnData
        if "BranchCoverageTimeline" in columnName:
            BranchCoverageTimeline_i=BranchCoverageTimeline_i+1
            BranchCoverageTimeline = np.append(BranchCoverageTimeline, columnData)
            BranchCoverageTimeline_x = np.append(BranchCoverageTimeline_x, BranchCoverageTimeline_i*0.5)
        if "CoverageTimeline" in columnName:
            CoverageTimeline_i=CoverageTimeline_i+1
            if CoverageTimeline_i>1 and float(columnData)==0.0:
                CoverageTimeline = np.append(CoverageTimeline, CoverageTimeline[CoverageTimeline_i -1])
            else:
                CoverageTimeline = np.append(CoverageTimeline, float(columnData))
            CoverageTimeline_x = np.append(CoverageTimeline_x, CoverageTimeline_i*0.5)
        if "BranchBitstringTimeline" in columnName:
            BranchBitstringTimeline_i=BranchBitstringTimeline_i+1
            BranchBitstringTimeline = np.append(BranchBitstringTimeline, columnData)
            BranchBitstringTimeline_x = np.append(BranchBitstringTimeline_x, BranchBitstringTimeline_i*0.5)
        if "PrivateMethodBitstringTimeline" in columnName:
            PrivateMethodBitstringTimeline_i=PrivateMethodBitstringTimeline_i+1
            PrivateMethodBitstringTimeline = np.append(PrivateMethodBitstringTimeline, columnData)
            PrivateMethodBitstringTimeline_x = np.append(PrivateMethodBitstringTimeline_x, PrivateMethodBitstringTimeline_i*0.5)
        if "PrivateMethodCoverageTimeline" in columnName:
            PrivateMethodCoverageTimeline_i=PrivateMethodCoverageTimeline_i+1
            PrivateMethodCoverageTimeline = np.append(PrivateMethodCoverageTimeline, columnData)
            PrivateMethodCoverageTimeline_x = np.append(PrivateMethodCoverageTimeline_x, PrivateMethodCoverageTimeline_i*0.5)
        if "ExceptionCoverageTimeline" in columnName:
            ExceptionCoverageTimeline_i=ExceptionCoverageTimeline_i+1
            ExceptionCoverageTimeline = np.append(ExceptionCoverageTimeline, columnData)
            ExceptionCoverageTimeline_x = np.append(ExceptionCoverageTimeline_x, ExceptionCoverageTimeline_i*0.5)


    BranchCoverageTimeline = [BranchCoverageTimeline_x,BranchCoverageTimeline]
    ExceptionCoverageTimeline = [ExceptionCoverageTimeline_x,ExceptionCoverageTimeline]
    PrivateMethodCoverageTimeline = [PrivateMethodCoverageTimeline_x,PrivateMethodCoverageTimeline]
    PrivateMethodBitstringTimeline = [PrivateMethodBitstringTimeline_x,PrivateMethodBitstringTimeline]
    BranchBitstringTimeline = [BranchBitstringTimeline_x,BranchBitstringTimeline]
    CoverageTimeline = [CoverageTimeline_x,CoverageTimeline]


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
        df.Coverage[row] = Coverage
        df.Total_Goals[row] = Total_Goals
        df.Covered_Goals[row] = Covered_Goals
        df.BranchCoverage[row] = BranchCoverage
        df.Total_Branches[row] = Total_Branches
        df.Covered_Branches[row] = Covered_Branches
        df.BranchCoverageBitString[row] = BranchCoverageBitString
        df.PrivateMethodCoverage[row] = PrivateMethodCoverage
        df.PrivateMethodCoverageBitString[row] = PrivateMethodCoverageBitString
        df.ExceptionCoverage[row] = ExceptionCoverage
        df.ExceptionCoverageBitString[row] = ExceptionCoverageBitString

        df.BranchCoverageTimeline[row] = BranchCoverageTimeline
        df.ExceptionCoverageTimeline[row] = ExceptionCoverageTimeline
        df.PrivateMethodCoverageTimeline[row] = PrivateMethodCoverageTimeline
        df.PrivateMethodBitstringTimeline[row] = PrivateMethodBitstringTimeline
        df.BranchBitstringTimeline[row] = BranchBitstringTimeline
        df.CoverageTimeline[row] = CoverageTimeline
        df.to_csv(arg_o)

        print("--")
        print("COVERAGE VALUES ON THE FINAL TEST SUITE")
        print(df.Coverage[row])
        print(df.Total_Goals[row])
        print(df.Covered_Goals[row])
        plt.title("Coverage during generation.")
        plt.rcParams["figure.autolayout"] = True
        plt.plot(CoverageTimeline[0], CoverageTimeline[1], color="red")
        plt.show()


        print("--")
        print("BranchCoverage VALUES ON THE FINAL TEST SUITE")
        print(df.BranchCoverage[row])
        print(df.Total_Branches[row])
        print(df.Covered_Branches[row])
        plt.title("BranchCoverage during generation.")
        plt.rcParams["figure.autolayout"] = True
        plt.plot(BranchCoverageTimeline[0], BranchCoverageTimeline[1], color="red")
        plt.show()




# WHAT WE NEED
# Coverage	Total_Goals	Covered_Goals	CoverageTimeline
# BranchCoverage	Total_Branches	Covered_Branches	BranchCoverageBitString	BranchCoverageTimeline
# BranchBitstringTimeline	PrivateMethodCoverage	PrivateMethodCoverageBitString
# PrivateMethodBitstringTimeline	PrivateMethodCoverageTimeline	ExceptionCoverage
# ExceptionCoverageBitString	ExceptionCoverageTimeline

# WHAT WE HAVE
#"Coverage,Total_Goals,Covered_Goals,CoverageTimeline,BranchCoverage,Total_Branches,
# Covered_Branches,BranchCoverageBitString,BranchCoverageTimeline,BranchBitstringTimeline,
# PrivateMethodCoverage,PrivateMethodCoverageBitString,PrivateMethodBitstringTimeline,
# PrivateMethodCoverageTimeline,ExceptionCoverage,ExceptionCoverageBitString,ExceptionCoverageTimeline";


if __name__ == "__main__":
    myfunc(sys.argv)