import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys
import getopt
pd.options.mode.chained_assignment = None

def myfunc(argv):
    arg_value = ""
    arg_file = ""
    arg_c = ""
    arg_r = ""
    arg_p = ""
    arg_b = ""
    arg_help = "{0} -f <path to file> -c <column name> -v <value> -r <row (criterion)> -p <project name> -b <bug name>".format(argv[0])

    try:
        opts, args = getopt.getopt(argv[1:], "hf:c:v:r:p:b:", ["help", "f=",
                                                         "c=", "v=","r=","b=","p="])
    except:
        print(arg_help)
        print("failed to get opt")
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)  # print the help message
            sys.exit(2)
        elif opt in ("-f", "--file"):
            arg_file= arg
        elif opt in ("-c", "--column"):
            arg_c = arg
        elif opt in ("-v", "--value"):
            arg_value = arg
        elif opt in ("-r", "--row", "--criterion"):
            arg_r = arg
        elif opt in ("-p"):
            arg_p = arg
        elif opt in ("-b"):
            arg_b = arg




    if str(arg_file)=="":
        print("A file path is needed.")
        print(arg_help)
        sys.exit(2)

    df = pd.read_csv(arg_file)
    if str(arg_p)!="":
        df.Project[0] = arg_p
        df.Project[1] = arg_p
        df.Project[2] = arg_p
        df.Project[3] = arg_p
        df.Project[4] = arg_p
        df.Project[5] = arg_p
        df.Project[6] = arg_p
    if str(arg_b)!="":
        df.Bug[0] = arg_b
        df.Bug[1] = arg_b
        df.Bug[2] = arg_b
        df.Bug[3] = arg_b
        df.Bug[4] = arg_b
        df.Bug[5] = arg_b
        df.Bug[6] = arg_b

    row = 99
    if arg_c=="BRANCH":
        row=0
    elif arg_c=="BRANCH:PRIVATEMETHOD":
        row=1
    elif arg_c=="BRANCH:EXCEPTION":
        row=2
    elif arg_c=="BRANCH:EXECUTIONTIME":
        row=3
    #elif arg_c=="EXECUTIONTIME":
    #    row=4
    #elif arg_c=="PRIVATEMETHOD":
    #    row=5
    #elif arg_c=="EXCEPTION":
    #    row=6
    if row < 7:
        if arg_r=="Bug_Detection":
            df.Bug_Detection[row] = arg_value
        if arg_r=="Total_Banches":
            df.Total_Banches[row] = arg_value
        if arg_r=="Covered_Banches":
            df.Covered_Banches[row] = arg_value
        if arg_r=="Total_Methods":
            df.Total_Methods[row] = arg_value
        if arg_r=="Covered_Methods":
            df.Covered_Methods[row] = arg_value
        if arg_r=="CoverageBitString":
            df.CoverageBitString[row] = arg_value

    df.to_csv(arg_file,index=False)

if __name__ == "__main__":
    myfunc(sys.argv)