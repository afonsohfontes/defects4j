import math

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys
import getopt

from scipy.stats import wilcoxon
from numpy import mean, std  # version >= 1.7.1 && <= 1.9.1
from math import sqrt

pd.options.mode.chained_assignment = None


def myfunc(argv):
    arg_file = ""
    arg_help = "{0} -f <path to results> -o <path to output> -c <criterion>".format(argv[0])

    try:
        opts, args = getopt.getopt(argv[1:], "f:o:c:i:b:", ["f=", "o=", "c=", "i="])
    except:
        print(arg_help)
        print("failed to get opt")
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-f", "--file"):
            arg_file = arg
        elif opt in ("-o"):
            arg_o = arg
        elif opt in ("-c"):
            arg_c = arg
        elif opt in ("-i"):
            arg_i = arg
        elif opt in ("-b"):
            arg_b = arg

    # if str(arg_file)=="":
    #    print("A file path is needed.")
    #    print(arg_help)
    #    sys.exit(2)
    if str(arg_o) == "":
        print("An output path is needed.")
        print(arg_help)
        sys.exit(2)
    if str(arg_c) == "":
        print("A criterion path is needed.")
        print(arg_help)
        sys.exit(2)


    if str(arg_file) == "":

        for i in range(int(arg_i)):
            row = 99
            if arg_c == "BRANCH":
                row = 0
            elif arg_c == "PRIVATEMETHOD":
                row = 1
            elif arg_c == "EXCEPTION":
                row = 2
            elif arg_c == "BRANCH:PRIVATEMETHOD":
                row = 3
            elif arg_c == "BRANCH:EXCEPTION":
                row = 4
            if row < 5 and int(arg_b) > 0:
                str1 = arg_o
                str2 = "{}.csv".format(i)
                df2 = pd.read_csv(str1 + str2)
                df2.Bug_Detection[row] = int(arg_b)
                str3 = str1 + str2
                df2.to_csv(str3, index=False)

    if str(arg_file) != "":
        df = pd.read_csv(arg_file)
        for i in range(int(arg_i)):
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
                if columnName == "Coverage":
                    Coverage = float(columnData[i])
                if columnName == "Total_Goals":
                    Total_Goals = float(columnData[i])
                if columnName == "Covered_Goals":
                    Covered_Goals = float(columnData[i])
                if columnName == "BranchCoverage":
                    BranchCoverage = float(columnData[i])
                if columnName == "Total_Branches":
                    Total_Branches = float(columnData[i])
                if columnName == "Covered_Branches":
                    Covered_Branches = float(columnData[i])
                if columnName == "BranchCoverageBitString":
                    BranchCoverageBitString = (columnData[i])
                if columnName == "PrivateMethodCoverage":
                    PrivateMethodCoverage = float(columnData[i])
                if columnName == "PrivateMethodCoverageBitString":
                    PrivateMethodCoverageBitString = (columnData[i])
                if columnName == "ExceptionCoverage":
                    ExceptionCoverage = float(columnData[i])
                if columnName == "ExceptionCoverageBitString":
                    ExceptionCoverageBitString = (columnData[i])
                if "BranchCoverageTimeline" in columnName:
                    BranchCoverageTimeline_i = BranchCoverageTimeline_i + 1
                    BranchCoverageTimeline = np.append(BranchCoverageTimeline, float(columnData[i]))
                    BranchCoverageTimeline_x = np.append(BranchCoverageTimeline_x, BranchCoverageTimeline_i * 0.5)
                if "CoverageTimeline" in columnName:
                    CoverageTimeline_i = CoverageTimeline_i + 1
                    # if CoverageTimeline_i>1 and float(columnData)==0.0:
                    #     CoverageTimeline = np.append(CoverageTimeline, CoverageTimeline[CoverageTimeline_i -1])
                    # else:
                    CoverageTimeline = np.append(CoverageTimeline, float(columnData[i]))
                    CoverageTimeline_x = np.append(CoverageTimeline_x, CoverageTimeline_i * 0.5)
                if "BranchBitstringTimeline" in columnName:
                    BranchBitstringTimeline_i = BranchBitstringTimeline_i + 1
                    BranchBitstringTimeline = np.append(BranchBitstringTimeline, (columnData[i]))
                    BranchBitstringTimeline_x = np.append(BranchBitstringTimeline_x, BranchBitstringTimeline_i * 0.5)
                if "PrivateMethodBitstringTimeline" in columnName:
                    PrivateMethodBitstringTimeline_i = PrivateMethodBitstringTimeline_i + 1
                    PrivateMethodBitstringTimeline = np.append(PrivateMethodBitstringTimeline, (columnData[i]))
                    PrivateMethodBitstringTimeline_x = np.append(PrivateMethodBitstringTimeline_x,
                                                                 PrivateMethodBitstringTimeline_i * 0.5)
                if "PrivateMethodCoverageTimeline" in columnName:
                    PrivateMethodCoverageTimeline_i = PrivateMethodCoverageTimeline_i + 1
                    PrivateMethodCoverageTimeline = np.append(PrivateMethodCoverageTimeline, (columnData[i]))
                    PrivateMethodCoverageTimeline_x = np.append(PrivateMethodCoverageTimeline_x,
                                                                PrivateMethodCoverageTimeline_i * 0.5)
                if "ExceptionCoverageTimeline" in columnName:
                    ExceptionCoverageTimeline_i = ExceptionCoverageTimeline_i + 1
                    ExceptionCoverageTimeline = np.append(ExceptionCoverageTimeline, (columnData[i]))
                    ExceptionCoverageTimeline_x = np.append(ExceptionCoverageTimeline_x,
                                                            ExceptionCoverageTimeline_i * 0.5)

            BranchCoverageTimeline = [BranchCoverageTimeline_x, BranchCoverageTimeline]
            ExceptionCoverageTimeline = [ExceptionCoverageTimeline_x, ExceptionCoverageTimeline]
            PrivateMethodCoverageTimeline = [PrivateMethodCoverageTimeline_x, PrivateMethodCoverageTimeline]
            PrivateMethodBitstringTimeline = [PrivateMethodBitstringTimeline_x, PrivateMethodBitstringTimeline]
            BranchBitstringTimeline = [BranchBitstringTimeline_x, BranchBitstringTimeline]
            CoverageTimeline = [CoverageTimeline_x, CoverageTimeline]

            CoverageTimeline_i = BranchCoverageTimeline_i
            CoverageTimeline[0] = CoverageTimeline[0][:CoverageTimeline_i + 1]
            CoverageTimeline[1] = CoverageTimeline[1][:CoverageTimeline_i + 1]

            # dest=$name$PID-bug_$bid-budget_$budget-trial_$trial/results-Class_
            str1 = arg_o
            str2 = "{}.csv".format(i)
            df2 = pd.read_csv(str1 + str2)
            row = 99
            if arg_c == "BRANCH":
                row = 0
            elif arg_c == "PRIVATEMETHOD":
                row = 1
            elif arg_c == "EXCEPTION":
                row = 2
            elif arg_c == "BRANCH:PRIVATEMETHOD":
                row = 3
            elif arg_c == "BRANCH:EXCEPTION":
                row = 4
            if row < 5:

                df2.Coverage[row] = Coverage
                df2.Total_Goals[row] = Total_Goals
                df2.Covered_Goals[row] = Covered_Goals
                df2.BranchCoverage[row] = BranchCoverage
                df2.Total_Branches[row] = Total_Branches
                df2.Covered_Branches[row] = Covered_Branches
                df2.BranchCoverageBitString[row] = BranchCoverageBitString
                df2.PrivateMethodCoverage[row] = PrivateMethodCoverage
                df2.PrivateMethodCoverageBitString[row] = PrivateMethodCoverageBitString
                df2.ExceptionCoverage[row] = ExceptionCoverage
                df2.ExceptionCoverageBitString[row] = ExceptionCoverageBitString

                df2.BranchCoverageTimeline[row] = BranchCoverageTimeline
                df2.ExceptionCoverageTimeline[row] = ExceptionCoverageTimeline
                df2.PrivateMethodCoverageTimeline[row] = PrivateMethodCoverageTimeline
                df2.PrivateMethodBitstringTimeline[row] = PrivateMethodBitstringTimeline
                df2.BranchBitstringTimeline[row] = BranchBitstringTimeline
                df2.CoverageTimeline[row] = CoverageTimeline
                str3 = str1 + str2
                df2.to_csv(str3, index=False)

                a = str3.replace(".csv", "-" + arg_c + ".txt")
                a = a.replace("results","summaries/summary")
                f = open(a, 'w')
                f.write('\n')

                f.write("-- VALUES ON THE FINAL TEST SUITE --")
                f.write('\n')
                f.write("COVERAGE (SELECTED CRITERIA)")
                f.write('\n')
                # "-{}-CoverageTimelines.png".format(arg_c)
                if float(Total_Goals) != 0:
                    f.write("Coverage: {}".format(float(Covered_Goals) / float(Total_Goals)))
                else:
                    f.write("Coverage: 0.0 (or no data acquired).")
                f.write('\n')
                f.write("Total goals: {}".format(Total_Goals))
                f.write('\n')
                f.write("Covered goals: {}".format(Covered_Goals))
                f.write('\n')
                f.write("BRANCH")
                f.write('\n')
                f.write("Coverage: {}".format(float(Covered_Branches) / float(Total_Branches)))
                f.write('\n')
                f.write("Total goals: {}".format(Total_Branches))
                f.write('\n')
                f.write("Covered goals: {}".format(Covered_Branches))
                f.write('\n')
                f.write("PRIVATE METHOD")
                f.write('\n')
                f.write("Coverage: {}".format(PrivateMethodCoverage))
                f.write('\n')
                f.write("EXCEPTION")
                f.write('\n')
                if math.isnan(float(ExceptionCoverageBitString)):
                    f.write("Coverage: N/A")
                    f.write('\n')
                    f.write("Exceptions found: none")
                    f.write('\n')
                    f.write("Exceptions covered: N/A")
                    f.write('\n')
                else:
                    f.write("Coverage: {}".format(ExceptionCoverage))
                    f.write('\n')
                    f.write("Exceptions found: {}".format(len(str(ExceptionCoverageBitString))))
                    f.write('\n')
                    s = str(ExceptionCoverageBitString)
                    f.write("Exceptions covered: {}".format(sum(float(i) for i in s)))
                f.close()

                plt.title("Coverage evolution")
                plt.rcParams["figure.autolayout"] = True
                plt.plot(CoverageTimeline[0], CoverageTimeline[1], color="red", label="Selected Criteria",
                         linestyle="-")
                plt.plot(BranchCoverageTimeline[0], BranchCoverageTimeline[1], color="cyan", label="Branch",
                         linestyle="--")
                plt.plot(PrivateMethodCoverageTimeline[0], PrivateMethodCoverageTimeline[1], color="blue",
                         label="Private Method", linestyle="-.")
                plt.plot(ExceptionCoverageTimeline[0], ExceptionCoverageTimeline[1], color="green", label="Exception",
                         linestyle=":")
                plt.legend()
                b = "-{}-CoverageTimelines.png".format(arg_c)
                a = str3.replace(".csv", b)
                a = a.replace("results-","images/")
                plt.savefig(a)
                # plt.show()
                plt.clf()

                # plt.style.use('_mpl-gallery')
                # make data:
                x = []

                d = []
                for i in range(1, BranchBitstringTimeline_i):
                    d.append([])
                    x.append(len(x))
                    for j in range(0, len(str(BranchBitstringTimeline[1][i]))):
                        # print((j+1)*int(BranchBitstringTimeline[1][i][j]))
                        try:
                            if int(str(BranchBitstringTimeline[1][i][j])) > 0:
                                d[i - 1].append(((j + 1) * int(str(BranchBitstringTimeline[1][i][j]))))
                        except:
                            if int(str(BranchBitstringTimeline[1][i])) > 0:
                                d[i - 1].append(((j + 1) * int(str(BranchBitstringTimeline[1][i]))))
                    # print(BranchBitstringTimeline[1][i])
                # print("terminou -------------------------------------------------------")
                # print(d)
                D = (d)

                plt.rcParams["figure.autolayout"] = True
                fig, ax = plt.subplots()
                ax.set_title('Branch goals covered over the evolution.')
                ax.eventplot(D, orientation="horizontal", lineoffsets=x, linewidth=2.8, linelength=0.8)
                b = "-{}-BranchBitstringTimeline.png".format(arg_c)
                a = str3.replace(".csv", b)
                a = a.replace("results-","images/")
                plt.savefig(a)
                plt.clf()


# WHAT WE NEED
# Coverage	Total_Goals	Covered_Goals	CoverageTimeline
# BranchCoverage	Total_Branches	Covered_Branches	BranchCoverageBitString	BranchCoverageTimeline
# BranchBitstringTimeline	PrivateMethodCoverage	PrivateMethodCoverageBitString
# PrivateMethodBitstringTimeline	PrivateMethodCoverageTimeline	ExceptionCoverage
# ExceptionCoverageBitString	ExceptionCoverageTimeline

# WHAT WE HAVE
# "Coverage,Total_Goals,Covered_Goals,CoverageTimeline,BranchCoverage,Total_Branches,
# Covered_Branches,BranchCoverageBitString,BranchCoverageTimeline,BranchBitstringTimeline,
# PrivateMethodCoverage,PrivateMethodCoverageBitString,PrivateMethodBitstringTimeline,
# PrivateMethodCoverageTimeline,ExceptionCoverage,ExceptionCoverageBitString,ExceptionCoverageTimeline";


if __name__ == "__main__":
    myfunc(sys.argv)
