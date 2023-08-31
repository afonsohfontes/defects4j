import os
import pandas as pd
import re
from datetime import datetime, timedelta

def extract_test_info(file_path):
    if not os.path.exists(file_path):
        return "no data", "no data"
    # Define the regex pattern to find the desired text
    pattern = r"Generated (\d+) tests with total length (\d+)"
    pattern2 = r'-criterion=([^ \n]+)'
    # Initialize variables to store the results
    tests_generated_list = []
    total_length_list = []
    # Read the log file
    with open(file_path, 'r') as file:
        for line in file:
            # Search for the pattern in each line
            matches = re.findall(pattern, line)
            for match in matches:
                tests_generated_list.append(int(match[0]))
                total_length_list.append(int(match[1]))
            matches = re.findall(pattern2, line)


    tests_average = "no data"
    length_average = "no data"
    if len(tests_generated_list) > 0:
        tests_average = sum(tests_generated_list) / len(tests_generated_list)
    if len(total_length_list) > 0 and tests_average > 0:
        length_average = sum(total_length_list) / len(total_length_list)

    return tests_average, length_average

def extract_execution_time(file_path):

    if not os.path.exists(file_path):
        return "no data"

    with open(file_path, "r") as log_file:
        lines = log_file.readlines()

    # Find lines containing the relevant timestamps and failing tests count
    start_line = ""
    end_line = ""
    failing_tests_count = 0  # Initialize the variable to track failing tests

    for line in lines:
        if "run_bug_detection.pl" in line:
            if "Start executing" in line:
                start_line = line
            elif "End executing" in line:
                end_line = line
            elif "- Found" in line and "failing tests" in line and "on buggy version" in line:
                match = re.search(r'(\d+) failing tests', line)
                if match:
                    failing_tests_count = int(match.group(1))

            if start_line and end_line:
                break

    start_timestamp_str = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', start_line).group()
    end_timestamp_str = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', end_line).group()

    start_timestamp = datetime.strptime(start_timestamp_str, "%Y-%m-%d %H:%M:%S")
    end_timestamp = datetime.strptime(end_timestamp_str, "%Y-%m-%d %H:%M:%S")

    # Check if the day changed in between and adjust end_timestamp if needed
    # if start_timestamp.day != end_timestamp.day:
    #    end_timestamp += timedelta(days=1)

    # Calculate the time difference in seconds
    time_difference = (end_timestamp - start_timestamp).total_seconds()

    return time_difference

def process_folders(root_dir, output_file):
    output = pd.read_csv(output_file)

    for foldername, subfolders, filenames in os.walk(root_dir):
        for filename in filenames:
            if foldername != "logs" and ".csv" in filename and "statistics" not in filename and "Class" in filename:
                # print("folder name:", foldername.replace(root_dir,'').split("/"))
                project = foldername.replace(root_dir,'').split("/")[0]
                # bug = foldername.replace(root_dir,'').split("/")[1]
                budget = foldername.replace(root_dir, '').split("/")[2].replace("budget_", "")
                trial = foldername.replace(root_dir, '').split("/")[3].replace("trial_", "")
                classNr = int(filename.replace("results-Class_", "").replace(".csv", "")) + 1
                file_path = os.path.join(foldername, filename)
                input = pd.read_csv(file_path)
                for i in range(4):
                    newRow = pd.DataFrame({
                        "Project": ["no data"],
                        "Bug": ["no data"],
                        "Class_nr": ["no data"],
                        "Budget": ["no data"],
                        "Generation_success": [0],
                        "Trial": ["no data"],
                        "Criterion": ["no data"],
                        "Failing_tests": ["no data"],
                        "Branch_Cov": ["no data"],
                        "Nr_test_cases": ["no data"],
                        "Test_suite_length": ["no data"],
                        "Private_Methods": ["no data"],
                        "Private_Method_Covered": ["no data"],
                        "Exception_thrown": ["no data"],
                        "Execution_Time": ["no data"],
                    })
                    newRow.Project = input.Project[i]
                    newRow.Bug = input.Bug[i]
                    newRow.Criterion = input.criterion[i]
                    newRow.Branch_Cov = input.BranchCoverage[i]
                    if str(input.BranchCoverage[i]) != "no data":
                        log_path = str(foldername+"/generationData/"+str(input.criterion[i])+"/1-EvoTranscription.log")
                        log_path = log_path.replace(":", "_")
                        #log_path = log_path.replace("BRANCH", "ONLYBRANCH")
                        testsTemp, lengthTemp = extract_test_info(log_path)
                        newRow.Nr_test_cases = testsTemp
                        newRow.Test_suite_length = lengthTemp
                        if testsTemp == "no data":
                            #input.BranchCoverage[i] = "no data"
                            newRow.Branch_Cov = "no data"
                            #input.to_csv(file_path, index=False)
                            newRow.Private_Method_Covered = "no data"
                            newRow.Exception_thrown = "no data"
                        else:
                            newRow.Private_Method_Covered = input.Covered_PrivateMethods[i]
                            newRow.Exception_thrown = input.ExceptionsCovered[i]
                        log_path_et = str(foldername+"/generationData/"+str(input.criterion[i])+"/bug_detection_log/"+project+"/run_bug_detection.pl.log")
                        log_path_et = log_path_et.replace(":", "_")
                        newRow.Execution_Time = extract_execution_time(log_path_et)
                        if "no data" not in str(newRow.Execution_Time):
                            if float(newRow.Execution_Time) > 0:
                                newRow.Generation_success = str(1)
                                # print(log_path_et + '  --has--:  ' + str(input.BranchCoverage[i]))
                            else:
                                newRow.Generation_success = str(0)
                    else:
                        newRow.Private_Method_Covered = "no data"
                        newRow.Nr_test_cases = "no data"
                        newRow.Test_suite_length = "no data"
                        newRow.Exception_thrown = "no data"
                        newRow.Private_Methods = "no data"
                    newRow.Class_nr = classNr
                    newRow.Budget = budget
                    newRow.Trial = trial
                    if float(newRow.Generation_success) > 0:
                        newRow.Failing_tests = input.Bug_Detection[i]
                    b = 0
                    if input.Total_PrivateMethods[0] != "no data":
                        if b < int(input.Total_PrivateMethods[0]):
                            b = int(input.Total_PrivateMethods[0])
                    if input.Total_PrivateMethods[1] != "no data":
                        if b < int(input.Total_PrivateMethods[1]):
                            b = int(input.Total_PrivateMethods[1])
                    if input.Total_PrivateMethods[2] != "no data":
                        if b < int(input.Total_PrivateMethods[2]):
                            b = int(input.Total_PrivateMethods[2])
                    newRow.Private_Methods = str(b)
                    output = pd.concat([output, newRow])
    for foldername, subfolders, filenames in os.walk(root_dir):
        for filename in filenames:
            if "_old" not in foldername and "run_bug_detection.pl.log" in filename:
                file_path = os.path.join(foldername, filename)
                input = pd.read_csv(file_path)

    str3 = output_file.replace("MODEL_","1-")
    print(str3, "saved in ", root_dir.replace("/data", ""))
    output.to_csv(root_dir.replace("/data", "")+str3, index=False)
    return output

def convert_to_numeric(df):
    # Convert columns to numeric data types
    numeric_cols = ['Failing_tests', 'Branch_Cov', 'Private_Method_Covered', 'Trial', 'Private_Methods',
                    'Execution_Time', 'Exception_thrown', 'Nr_test_cases', 'Generation_success']
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
    return df

if __name__ == "__main__":
    project_root = "/Users/afonsofo/Desktop/defects4j/framework/test/Experiments/data/"
    output_csv_format = "MODEL_everyTrialReport.csv"
    rawOutput = process_folders(project_root, output_csv_format)
    #rawOutput = pd.read_csv("/Users/afonsofo/Desktop/defects4j/framework/test/Experiments/data/everyTrialReport_2023731_12h44m.csv")
    rawOutput.replace("no data", pd.NA, inplace=True)
    rawOutput = convert_to_numeric(rawOutput)
    #print(rawOutput.tail())
    agg_functions = {
        'Trial': 'max',
        'Nr_test_cases': lambda x: round(x.mean(), 1),
        'Test_suite_length': lambda x: round(x.mean(), 1),
        'Failing_tests': lambda x: round(x.mean(), 1),
        'Branch_Cov': lambda x: round(x.mean(), 5),
        'Exception_thrown': lambda x: round(x.mean(), 1),
        'Private_Methods': 'max',
        'Private_Method_Covered': lambda x: round(x.mean(), 4),
        'Execution_Time': lambda x: round(x.mean(), 1),
        'Generation_success': lambda x: round(x.mean(), 4),
    }

    grouped_df = rawOutput.groupby(['Project', 'Bug', 'Budget', 'Class_nr', 'Criterion']).agg(agg_functions)
    new_column_names = {
        "Trial": "Trials",
        "Private_Method_Covered": "Private_Methods_Covered"
    }
    grouped_df = grouped_df.rename(columns=new_column_names)
    #grouped_df.Generation_success.replace("0", pd.NA, inplace=True)
    grouped_df.loc[grouped_df['Generation_success'] == 0, 'Generation_success'] = pd.NA
    grouped_df.to_csv("/Users/afonsofo/Desktop/defects4j/framework/test/Experiments/2-allTrialsCompiled.csv", index=True)
    agg_functions = {
        'Trials': ['max', 'median'],
       # 'Nr_test_cases': [lambda x: round(x.mean(), 1), lambda x: round(x.median(), 1)],
       # 'Test_suite_length': [lambda x: round(x.mean(), 1), lambda x: round(x.median(), 1)],
       # 'Failing_tests': [lambda x: round(x.mean(), 1), lambda x: round(x.median(), 1)],
       # 'Branch_Cov': [lambda x: round(x.mean(), 5), lambda x: round(x.median(), 5)],
       # 'Exception_thrown': [lambda x: round(x.mean(), 1), lambda x: round(x.median(), 1)],
       # 'Private_Methods': [lambda x: round(x.mean(), 4), lambda x: round(x.median(), 4)],
       # 'Private_Methods_Covered': [lambda x: round(x.mean(), 4), lambda x: round(x.median(), 4)],
       # 'Execution_Time': [lambda x: round(x.mean(), 1), lambda x: round(x.median(), 1)],
        'Nr_test_cases': lambda x: round(x.mean(), 1),
        'Test_suite_length': lambda x: round(x.mean(), 1),
        'Failing_tests': lambda x: round(x.mean(), 1),
        'Branch_Cov': lambda x: round(x.mean(), 5),
        'Exception_thrown': lambda x: round(x.mean(), 1),
        'Private_Methods': lambda x: round(x.mean(), 4),
        'Private_Methods_Covered': lambda x: round(x.mean(), 4),
        'Execution_Time': lambda x: round(x.mean(), 1),
        'Generation_success': lambda x: round(x.mean(), 4),
    }
    higher_df = grouped_df.groupby(['Budget', 'Criterion']).agg(agg_functions)
    column_to_exclude = 'Trials'
    higher_df = higher_df.drop(columns=column_to_exclude)
    higher_df.to_csv("/Users/afonsofo/Desktop/defects4j/framework/test/Experiments/3-experimentSummaryPerBudget.csv", index=True)