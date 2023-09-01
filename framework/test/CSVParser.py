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
            elif arg_c=="BRANCH:PRIVATEMETHOD":
                row=1
            elif arg_c=="BRANCH:EXCEPTION":
                row=2
            elif arg_c=="BRANCH:EXECUTIONTIME":
                row=3
            elif arg_c=="BRANCH:OUTPUT":
                row=4

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

            BranchCoverageBitString = "no data"
            PrivateMethodCoverage = "no data"
            PrivateMethodCoverageBitString = "no data"
            ExceptionCoverage = "no data"
            ExceptionCoverageBitString = "no data"
            OutputCoverageBitString = "no data"
            for (columnName, columnData) in df.items():
                if columnName == "BranchCoverageBitString":
                    BranchCoverageBitString = str(columnData[class_i])
                if columnName == "OutputCoverageBitString":
                    OutputCoverageBitString = str(columnData[class_i])
                if columnName == "PrivateMethodCoverageBitString":
                    PrivateMethodCoverageBitString = str(columnData[class_i])
                if columnName == "ExceptionCoverageBitString":
                    ExceptionCoverageBitString = str(columnData[class_i])
                if "BranchBitstringTimeline" in columnName and not ("Only" in columnName):
                    BranchBitstringTimeline_i = BranchBitstringTimeline_i + 1
                    BranchBitstringTimeline = np.append(BranchBitstringTimeline, str(columnData[class_i]))
                    BranchBitstringTimeline_x = np.append(BranchBitstringTimeline_x, BranchBitstringTimeline_i)

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
            pm_cov = 0
            if private_total_methods>0:
                pm_cov = float(private_cov_methods) / float(private_total_methods)

            try:
                if (int(OutputCoverageBitString)>0):
                    n = str((OutputCoverageBitString))
                    output_cov_goals = 0
                    output_total_goals = 0
                    for i in n:
                        output_total_goals+=1
                        if i == "1":
                            output_cov_goals+=1
                else:
                    output_cov_goals = 0
                    output_total_goals = 0
            except:
                output_cov_goals = 0
                output_total_goals = 0
            output_cov = 0
            if output_total_goals>0:
                output_cov = float(output_cov_goals) / float(output_total_goals)

            BranchBitstringTimeline = [BranchBitstringTimeline_x, BranchBitstringTimeline]

            str1 = arg_o
            str2 = "{}.csv".format(class_i)
            df2 = pd.read_csv(str1 + str2)
            row = 99

            if arg_c=="BRANCH":
                row=0
            elif arg_c=="BRANCH:PRIVATEMETHOD":
                row=1
            elif arg_c=="BRANCH:EXCEPTION":
                row=2
            elif arg_c=="BRANCH:EXECUTIONTIME":
                row=3
            elif arg_c=="BRANCH:OUTPUT":
                row=4
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
                    n = str(ExceptionCoverageBitString)
                    exp_t = 0
                    exp_c = 0
                    for i in n:
                        exp_t+=1
                        if i == "1":
                            exp_c+=1
                except:
                    exp_c = 0
                    exp_t = 0
                exp_cov = 0
                if exp_t>0:
                    exp_cov = float(exp_c) / float(exp_t)

                df2.Total_PrivateMethods[row] = private_total_methods
                df2.Covered_PrivateMethods[row] = private_cov_methods
                df2.Total_OutputGoals[row] = output_total_goals
                df2.Covered_OutputGoals[row] = output_cov_goals
                df2.BranchCoverage[row] = branch_cov
                df2.Total_Branches[row] = branch_total_methods
                df2.Covered_Branches[row] = branch_cov_methods
                if branch_total_methods>0:
                    df2.BranchCoverageBitString[row] = BranchCoverageBitString
                else:
                    df2.BranchCoverageBitString[row] = "no data"
                if output_total_goals>0:
                    df2.OutputCoverageBitString[row] = OutputCoverageBitString
                else:
                    df2.OutputCoverageBitString[row] = "no data"
                df2.PrivateMethodCoverage[row] = pm_cov
                df2.OutputCoverage[row] = output_cov
                if private_total_methods>0:
                    df2.PrivateMethodCoverageBitString[row] = PrivateMethodCoverageBitString
                else:
                    df2.PrivateMethodCoverageBitString[row] = "no data"
                df2.ExceptionCoverage[row] = exp_cov
                df2.ExceptionsFound[row] = exp_t
                df2.ExceptionsCovered[row] = exp_c
                if exp_t>0:
                    df2.ExceptionCoverageBitString[row] = ExceptionCoverageBitString
                else:
                    df2.ExceptionCoverageBitString[row] = "no data"
                df2.BranchCoverageTimeline[row] = BranchCoverageTimeline
                df2.BranchBitstringTimeline[row] = BranchBitstringTimeline

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
                f.write("PRIVATE METHOD Coverage: {}".format(pm_cov))
                f.write('\n')
                f.write("Total PRIVATE METHODS: {}".format(private_total_methods))
                f.write('\n')
                f.write("Covered PRIVATE METHODS: {}".format(private_cov_methods))
                f.write('\n')
                f.write('\n')
                f.write("EXCEPTION Coverage: {}".format(exp_cov))
                f.write('\n')
                f.write("EXCEPTION found: {}".format(exp_t))
                f.write('\n')
                f.write("EXCEPTION covered: {}".format(exp_c))
                f.write('\n')
                f.write('\n')
                f.write("Test EXECUTION TIME: To be fetched from D4J execution")
                f.write('\n')
                f.write('\n')
                f.write("OUTPUT Coverage: {}".format(output_cov))
                f.write('\n')
                f.write("OUTPUT goals (total): {}".format(output_total_goals))
                f.write('\n')
                f.write("OUTPUT goals (covered): {}".format(output_cov_goals))
                f.write('\n')
                f.close()

                str3 = str1 + str2
                df2.to_csv(str3, index=False)

                plt.title('Cov evolution using: {}'.format(arg_c))
                plt.rcParams["figure.autolayout"] = True

                BranchCoverageTimeline_i = BranchCoverageTimeline_i + 1
                BranchCoverageTimeline[0] = np.append(BranchCoverageTimeline[0], BranchCoverageTimeline_i)
                BranchCoverageTimeline[1] = np.append(BranchCoverageTimeline[1], branch_cov)

                plt.plot(BranchCoverageTimeline[0], BranchCoverageTimeline[1], color="black", label="Branch",
                         linestyle="-")

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

if __name__ == "__main__":
    myfunc(sys.argv)
