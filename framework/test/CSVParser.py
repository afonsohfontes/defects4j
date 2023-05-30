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

        for class_i in range(int(arg_i)):
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
            elif arg_c=="BRANCH:EXECUTIONTIME":
                row=5
            elif arg_c=="EXECUTIONTIME":
                row=6
            if row<7 and int(arg_b) > 0:
                str1 = arg_o
                str2 = "{}.csv".format(class_i)
                df2 = pd.read_csv(str1 + str2)
                df2.Bug_Detection[row] = int(arg_b)
                str3 = str1 + str2
                df2.to_csv(str3, index=False)




    if str(arg_file) != "":
        df = pd.read_csv(arg_file)
        for class_i in range(int(arg_i)):
            BranchBitstringTimeline = [0]
            BranchBitstringTimeline_x = [0]
            BranchBitstringTimeline_i = 0

            OnlyBranchBitstringTimeline = [0]
            OnlyBranchBitstringTimeline_x = [0]
            OnlyBranchBitstringTimeline_i = 0

            PrivateMethodBitstringTimeline = [0]
            PrivateMethodBitstringTimeline_x = [0]
            PrivateMethodBitstringTimeline_i = 0

            PrivateMethodCoverageTimeline = [0]
            PrivateMethodCoverageTimeline_x = [0]
            PrivateMethodCoverageTimeline_i = 0

            ExceptionBitstringTimeline = [0]
            ExceptionBitstringTimeline_x = [0]
            ExceptionBitstringTimeline_i = 0

            BranchCoverageBitString = "no data"
            PrivateMethodCoverage = "no data"
            PrivateMethodCoverageBitString = "no data"
            ExceptionCoverage = "no data"
            ExceptionCoverageBitString = "no data"

            #ExecutionTimeFitnessTimeline = [0]
            #ExecutionTimeFitnessTimeline_x = [0]
            #ExecutionTimeFitnessTimeline_i = 0
            ExecutionTimeCoverage = "no data"

            for (columnName, columnData) in df.items():
                if columnName == "BranchCoverageBitString":
                    BranchCoverageBitString = str(columnData[class_i])
                if columnName == "OnlyBranchCoverageBitString":
                    OnlyBranchCoverageBitString = str(columnData[class_i])
                if columnName == "ExecutionTimeCoverage":
                    ExecutionTimeCoverage = float(columnData[class_i])
                if columnName == "PrivateMethodCoverageBitString":
                    PrivateMethodCoverageBitString = str(columnData[class_i])
                if columnName == "PrivateMethodCoverage":
                    PrivateMethodCoverage = float(columnData[class_i])
                if columnName == "ExceptionCoverage":
                    ExceptionCoverage = float(columnData[class_i])
                if columnName == "ExceptionCoverageBitString":
                    ExceptionCoverageBitString = str(columnData[class_i])
                if "BranchBitstringTimeline" in columnName and not ("Only" in columnName):
                    BranchBitstringTimeline_i = BranchBitstringTimeline_i + 1
                    BranchBitstringTimeline = np.append(BranchBitstringTimeline, str(columnData[class_i]))
                    BranchBitstringTimeline_x = np.append(BranchBitstringTimeline_x, BranchBitstringTimeline_i)
                if "OnlyBranchBitstringTimeline" in columnName:
                    OnlyBranchBitstringTimeline_i = OnlyBranchBitstringTimeline_i + 1
                    OnlyBranchBitstringTimeline = np.append(OnlyBranchBitstringTimeline, str(columnData[class_i]))
                    OnlyBranchBitstringTimeline_x = np.append(OnlyBranchBitstringTimeline_x, OnlyBranchBitstringTimeline_i)
                #if "ExecutionTimeTimeline" in columnName:
                #    ExecutionTimeFitnessTimeline_i = ExecutionTimeFitnessTimeline_i + 1
                #    ExecutionTimeFitnessTimeline = np.append(ExecutionTimeFitnessTimeline, float(columnData[class_i]))
                #    ExecutionTimeFitnessTimeline_x = np.append(ExecutionTimeFitnessTimeline_x, ExecutionTimeFitnessTimeline_i)
                if "ExceptionBitstringTimeline" in columnName:
                    ExceptionBitstringTimeline_i = ExceptionBitstringTimeline_i + 1
                    ExceptionBitstringTimeline = np.append(ExceptionBitstringTimeline, float(columnData[class_i]))
                    ExceptionBitstringTimeline_x = np.append(ExceptionBitstringTimeline_x, ExceptionBitstringTimeline_i)
                if "PrivateMethodBitstringTimeline" in columnName:
                    PrivateMethodBitstringTimeline_i = PrivateMethodBitstringTimeline_i + 1
                    PrivateMethodBitstringTimeline = np.append(PrivateMethodBitstringTimeline, str(columnData[class_i]))
                    PrivateMethodBitstringTimeline_x = np.append(PrivateMethodBitstringTimeline_x,
                                                                 PrivateMethodBitstringTimeline_i )
                if "PrivateMethodCoverageTimeline" in columnName:
                    PrivateMethodCoverageTimeline_i = PrivateMethodCoverageTimeline_i + 1
                    PrivateMethodCoverageTimeline = np.append(PrivateMethodCoverageTimeline, float(columnData[class_i]))
                    PrivateMethodCoverageTimeline_x = np.append(PrivateMethodCoverageTimeline_x,
                                                                PrivateMethodCoverageTimeline_i)

            BranchCoverageTimeline = [0]
            BranchCoverageTimeline_x = [0]
            BranchCoverageTimeline_i = 0
            for j in range(0, BranchBitstringTimeline_i):
                BranchCoverageTimeline_i = BranchCoverageTimeline_i + 1
                try:
                    totalBranches = len(str(BranchBitstringTimeline[j]))
                    s = str(BranchBitstringTimeline[j])
                    coveredBranches = sum(float(ii) for ii in s)
                    BranchCoverageTimeline = np.append(BranchCoverageTimeline, float(coveredBranches)
                                                       / float(totalBranches))
                except:
                    BranchCoverageTimeline = np.append(BranchCoverageTimeline, 0)
                BranchCoverageTimeline_x = np.append(BranchCoverageTimeline_x, BranchCoverageTimeline_i)
            BranchCoverageTimeline = [BranchCoverageTimeline_x, BranchCoverageTimeline]

            OnlyBranchCoverageTimeline = [0]
            OnlyBranchCoverageTimeline_x = [0]
            OnlyBranchCoverageTimeline_i = 0
            for j in range(0, OnlyBranchBitstringTimeline_i):
                OnlyBranchCoverageTimeline_i = OnlyBranchCoverageTimeline_i + 1
                try:
                    totalOnlyBranches = len(str(OnlyBranchBitstringTimeline[j]))
                    s = str(OnlyBranchBitstringTimeline[j])
                    coveredOnlyBranches = sum(float(ii) for ii in s)
                    OnlyBranchCoverageTimeline = np.append(OnlyBranchCoverageTimeline, float(coveredOnlyBranches)
                                                       / float(totalOnlyBranches))
                except:
                    OnlyBranchCoverageTimeline = np.append(OnlyBranchCoverageTimeline, 0)
                OnlyBranchCoverageTimeline_x = np.append(OnlyBranchCoverageTimeline_x, OnlyBranchCoverageTimeline_i)
            OnlyBranchCoverageTimeline = [OnlyBranchCoverageTimeline_x, OnlyBranchCoverageTimeline]

            try:
                if (int(PrivateMethodCoverageBitString)>0):
                    n = str((PrivateMethodCoverageBitString))
                    private_cov_methods = 0
                    private_total_methods = 0
                    for i in n:
                        private_total_methods+=1
                        if i == "1":
                            private_cov_methods+=1
                else:
                    private_cov_methods = 0
                    private_total_methods = 0
            except:
                private_cov_methods = 0
                private_total_methods = 0

            ''' ExceptionCoverageTimeline = [0]
            ExceptionCoverageTimeline_x = [0]
            ExceptionCoverageTimeline_i = 0
            exceptionsFound = 0
            if int(ExceptionCoverageBitString)>0:
                exceptionsFound = len(str(ExceptionCoverageBitString))
            if exceptionsFound == 0:
                for j in range(0, ExceptionBitstringTimeline_i):
                    ExceptionCoverageTimeline_i = ExceptionCoverageTimeline_i + 1
                    ExceptionCoverageTimeline = np.append(ExceptionCoverageTimeline, 0)
                    ExceptionCoverageTimeline_x = np.append(ExceptionBitstringTimeline_x, ExceptionBitstringTimeline_i)
            else:
                for j in range(0, ExceptionBitstringTimeline_i):
                    ExceptionCoverageTimeline_i = ExceptionCoverageTimeline_i + 1
                    s = str(ExceptionCoverageBitString)
                    ExceptionsCovered = sum(float(ii) for ii in s)
                    ExceptionCoverageTimeline = np.append(ExceptionCoverageTimeline, ExceptionsCovered/exceptionsFound)
                    ExceptionCoverageTimeline_x = np.append(ExceptionBitstringTimeline_x, ExceptionBitstringTimeline_i)

            ExceptionCoverageTimeline = [ExceptionCoverageTimeline_x, ExceptionCoverageTimeline]
            ExecutionTimeFitnessTimeline = [ExecutionTimeFitnessTimeline_x, ExecutionTimeFitnessTimeline]
            '''
            PrivateMethodCoverageTimeline = [PrivateMethodCoverageTimeline_x, PrivateMethodCoverageTimeline]
            PrivateMethodBitstringTimeline = [PrivateMethodBitstringTimeline_x, PrivateMethodBitstringTimeline]
            BranchBitstringTimeline = [BranchBitstringTimeline_x, BranchBitstringTimeline]
            OnlyBranchBitstringTimeline = [OnlyBranchBitstringTimeline_x, OnlyBranchBitstringTimeline]

            str1 = arg_o
            str2 = "{}.csv".format(class_i)
            print(str1)
            print(str2)
            df2 = pd.read_csv(str1 + str2)
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
            elif arg_c=="BRANCH:EXECUTIONTIME":
                row=5
            elif arg_c=="EXECUTIONTIME":
                row=6
            if row<7:

                try:
                    n = str(BranchCoverageBitString)
                    branch_cov_methods = 0
                    branch_total_methods = 0
                    for i in n:
                        branch_total_methods+=1
                        if i == "1":
                            branch_cov_methods+=1
                except:
                    branch_cov_methods = 0
                    branch_total_methods = 0
                branch_cov = 0
                if branch_total_methods>0:
                    branch_cov = float(branch_cov_methods) / float(branch_total_methods)

                try:
                    n = str(OnlyBranchCoverageBitString)
                    Onlybranch_cov_methods = 0
                    Onlybranch_total_methods = 0
                    for i in n:
                        Onlybranch_total_methods+=1
                        if i == "1":
                            Onlybranch_cov_methods+=1
                except:
                    Onlybranch_cov_methods = 0
                    Onlybranch_total_methods = 0
                Onlybranch_cov = 0
                if Onlybranch_total_methods>0:
                    Onlybranch_cov = float(Onlybranch_cov_methods) / float(Onlybranch_total_methods)

                df2.ExecutionTimeCoverage[row] = ExecutionTimeCoverage
                df2.Total_PrivateMethods[row] = private_total_methods
                df2.Covered_PrivateMethods[row] = private_cov_methods
                df2.BranchCoverage[row] = branch_cov
                df2.Total_Branches[row] = branch_total_methods
                df2.Covered_Branches[row] = branch_cov_methods
                df2.OnlyBranchCoverage[row] = Onlybranch_cov
                df2.Total_OnlyBranches[row] = Onlybranch_total_methods
                df2.Covered_OnlyBranches[row] = Onlybranch_cov_methods
                df2.BranchCoverageBitString[row] = BranchCoverageBitString
                df2.OnlyBranchCoverageBitString[row] = OnlyBranchCoverageBitString
                df2.PrivateMethodCoverage[row] = PrivateMethodCoverage
                df2.PrivateMethodCoverageBitString[row] = PrivateMethodCoverageBitString
                df2.ExceptionCoverage[row] = ExceptionCoverage
                df2.ExceptionCoverageBitString[row] = ExceptionCoverageBitString
                df2.OnlyBranchCoverageTimeline[row] = OnlyBranchCoverageTimeline
                df2.BranchCoverageTimeline[row] = BranchCoverageTimeline
                #df2.ExceptionCoverageTimeline[row] = ExceptionCoverageTimeline
                #df2.ExecutionTimeFitnessTimeline[row] = ExecutionTimeFitnessTimeline
                df2.PrivateMethodCoverageTimeline[row] = PrivateMethodCoverageTimeline
                df2.PrivateMethodBitstringTimeline[row] = PrivateMethodBitstringTimeline
                df2.BranchBitstringTimeline[row] = BranchBitstringTimeline
                df2.OnlyBranchBitstringTimeline[row] = OnlyBranchBitstringTimeline

                str3 = str1 + str2
                a = str3.replace(".csv", "-" + arg_c + ".txt")
                a = a.replace("results","summaries/summary")
                f = open(a, 'w')
                f.write('\n')
                f.write("-- TEST SUITE STATISTICS --")
                f.write('\n')
                f.write("BRANCH Coverage: {}".format(branch_cov))
                f.write('\n')
                f.write("Total BRANCHES: {}".format(branch_total_methods))
                f.write('\n')
                f.write("Covered BRANCHES: {}".format(branch_cov_methods))
                f.write('\n')
                f.write('\n')
                f.write("ONLYBRANCH Coverage: {}".format(Onlybranch_cov))
                f.write('\n')
                f.write("Total ONLYBRANCHES: {}".format(Onlybranch_total_methods))
                f.write('\n')
                f.write("Covered ONLYBRANCHES: {}".format(Onlybranch_cov_methods))
                f.write('\n')
                f.write('\n')
                f.write("PRIVATE METHOD Coverage: {}".format(PrivateMethodCoverage))
                f.write('\n')
                f.write("Total PRIVATE METHODS: {}".format(private_total_methods))
                f.write('\n')
                f.write("Covered PRIVATE METHODS: {}".format(private_cov_methods))
                f.write('\n')
                f.write('\n')
                ExceptionsFound = 0
                ExceptionsCovered = 0
                if math.isnan(float(ExceptionCoverageBitString)):
                    f.write("EXCEPTION Coverage: N/A")
                    f.write('\n')
                    f.write("EXCEPTION found: none")
                    f.write('\n')
                    f.write("EXCEPTION covered: N/A")
                    f.write('\n')
                else:
                    s = str(ExceptionCoverageBitString)
                    ExceptionsCovered = sum(float(ii) for ii in s)
                    ExceptionsFound = len(str(ExceptionCoverageBitString))
                    if ExceptionsFound>0:
                        f.write("EXCEPTION Coverage: {}".format(ExceptionsCovered/ExceptionsFound))
                    else:
                        f.write("EXCEPTION Coverage: N/A")
                    f.write('\n')
                    f.write("EXCEPTION found: {}".format(ExceptionsFound))
                    f.write('\n')
                    f.write("EXCEPTION covered: {}".format(ExceptionsCovered))
                df2.ExceptionsFound[row] = ExceptionsFound
                df2.ExceptionsCovered[row] = ExceptionsCovered
                f.write('\n')
                f.write('\n')
                f.write("Test EXECUTION TIME final coverage: {}".format(ExecutionTimeCoverage))
                f.close()

                str3 = str1 + str2
                df2.to_csv(str3, index=False)

                plt.title('Cov evolution using: {}'.format(arg_c))
                plt.rcParams["figure.autolayout"] = True

                #ExceptionCoverageTimeline_i = ExceptionCoverageTimeline_i + 1
                #ExceptionCoverageTimeline[0] = np.append(ExceptionCoverageTimeline[0],  ExceptionCoverageTimeline_i)
                #if ExceptionsFound > 0:
                #    expC = ExceptionsCovered/ExceptionsFound
                #else:
                #    expC = 0
                #ExceptionCoverageTimeline[1] = np.append(ExceptionCoverageTimeline[1],  expC)

                #ExecutionTimeFitnessTimeline_i = ExecutionTimeFitnessTimeline_i + 1
                #ExecutionTimeFitnessTimeline[0] = np.append(ExecutionTimeFitnessTimeline[0],  ExecutionTimeFitnessTimeline_i)

                #ExecutionTimeFitnessTimeline[1] = np.append(ExecutionTimeFitnessTimeline[1],  ExecutionTimeCoverage)

                PrivateMethodCoverageTimeline_i = PrivateMethodCoverageTimeline_i + 1
                PrivateMethodCoverageTimeline[0] = np.append(PrivateMethodCoverageTimeline[0],
                                                             PrivateMethodCoverageTimeline_i)
                if private_total_methods > 0:
                    pCov = private_cov_methods/private_total_methods
                else:
                    pCov = 0
                PrivateMethodCoverageTimeline[1] = np.append(PrivateMethodCoverageTimeline[1],  pCov)

                BranchCoverageTimeline_i = BranchCoverageTimeline_i + 1
                BranchCoverageTimeline[0] = np.append(BranchCoverageTimeline[0], BranchCoverageTimeline_i)
                BranchCoverageTimeline[1] = np.append(BranchCoverageTimeline[1], branch_cov)

                OnlyBranchCoverageTimeline_i = OnlyBranchCoverageTimeline_i + 1
                OnlyBranchCoverageTimeline[0] = np.append(OnlyBranchCoverageTimeline[0], OnlyBranchCoverageTimeline_i)
                OnlyBranchCoverageTimeline[1] = np.append(OnlyBranchCoverageTimeline[1], Onlybranch_cov)


                plt.plot(BranchCoverageTimeline[0], BranchCoverageTimeline[1], color="black", label="Branch",
                         linestyle="-")
                plt.plot(OnlyBranchCoverageTimeline[0], OnlyBranchCoverageTimeline[1], color="green", label="OnlyBranch",
                         linestyle="--")
                #plt.plot(PrivateMethodCoverageTimeline[0], PrivateMethodCoverageTimeline[1], color="cyan",
                #         label="Private Method", linestyle="--")
                #plt.plot(ExceptionCoverageTimeline[0], ExceptionCoverageTimeline[1], color="red", label="Exception",
                #         linestyle=":")
                #plt.plot(ExecutionTimeFitnessTimeline[0], ExecutionTimeFitnessTimeline[1], color="magenta", label="Execution Time",
                #         linestyle=":")
                plt.legend()
                b = "-{}-CoverageTimelines(w-OB).png".format(arg_c)
                a = str3.replace(".csv", b)
                a = a.replace("results-", "images/")
                plt.savefig(a)
                #plt.show()
                plt.clf()

                plt.plot(BranchCoverageTimeline[0], BranchCoverageTimeline[1], color="black", label="Branch",
                         linestyle="-")
                #plt.plot(PrivateMethodCoverageTimeline[0], PrivateMethodCoverageTimeline[1], color="cyan",
                #         label="Private Method", linestyle="--")
                #plt.plot(ExceptionCoverageTimeline[0], ExceptionCoverageTimeline[1], color="red", label="Exception",
                #         linestyle=":")
                #plt.plot(ExecutionTimeFitnessTimeline[0], ExecutionTimeFitnessTimeline[1], color="magenta", label="Execution Time",
                #         linestyle=":")
                #plt.legend()
                b = "-{}-BRANCHTimeline.png".format(arg_c)
                a = str3.replace(".csv", b)
                a = a.replace("results-", "images/")
                plt.savefig(a)
                #plt.show()
                plt.clf()


                # plt.style.use('_mpl-gallery')
                # make data:
                x = []
                z = []
                d = []
                for i in range(1, BranchBitstringTimeline_i):
                    d.append([])
                    z.append([])
                    x.append(len(x))
                    for k in range(0, len(str(BranchCoverageBitString))):
                        z[i - 1].append((k + 1))
                    for j in range(0, len(str(BranchBitstringTimeline[1][i]))):
                        # print((j+1)*int(BranchBitstringTimeline[1][i][j]))
                        try:
                            if int(str(BranchBitstringTimeline[1][i][j])) > 0:
                                d[i - 1].append(((j + 1) * int(str(BranchBitstringTimeline[1][i][j]))))
                            #else:
                                #z[i - 1].append((j + 1))
                        except:
                            if int(str(BranchBitstringTimeline[1][i])) > 0:
                                d[i - 1].append(((j + 1) * int(str(BranchBitstringTimeline[1][i]))))
                            #else:
                                #z[i - 1].append((j + 1))

                d.append([])
                z.append([])
                x.append(len(x))
                #print(BranchCoverageBitString)

                for j in range(0, len(str(BranchCoverageBitString))):
                    try:
                        if int(str(BranchCoverageBitString[j])) > 0:
                            d[i].append(((j + 1) * int(str(BranchCoverageBitString[j]))))
                        else:
                            z[i].append((j + 1))
                    except:
                        if int(str(BranchBitstringTimeline)) > 0:
                            d[i].append(((j + 1) * int(str(BranchBitstringTimeline))))
                        else:
                            z[i].append((j + 1))

                plt.rcParams["figure.autolayout"] = True
                fig, ax = plt.subplots()
                ax.set_title('Branch evolution using: {}'.format(arg_c))
                ax.eventplot(z, color="red", orientation="horizontal", lineoffsets=x, linewidth=0.3, linelength=0.3)
                ax.eventplot(d, color="blue", orientation="horizontal", lineoffsets=x, linewidth=2.8, linelength=0.8)
                b = "-{}-BranchBitstringTimeline.png".format(arg_c)
                a = str3.replace(".csv", b)
                a = a.replace("results-","images/")
                plt.savefig(a)
                #plt.show()
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
