import os
import pandas as pd
import re
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
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
                for i in range(5):
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
                        "Output_cov": ["no data"],
                        "total_outputs": ["no data"],
                        "covered_outputs": ["no data"],
                    })

                    newRow.Project = input.Project[i]
                    newRow.Bug = input.Bug[i]
                    newRow.Criterion = input.criterion[i]
                    newRow.Branch_Cov = input.BranchCoverage[i]
                    newRow.Output_cov = input.OutputCoverage[i]
                    newRow.total_outputs = input.Total_OutputGoals[i]
                    newRow.covered_outputs = input.Covered_OutputGoals[i]

                    if str(input.BranchCoverage[i]) != "no data":
                        log_path = str(foldername+"/generationData/"+str(input.criterion[i])+"/1-EvoTranscription.log")
                        log_path = log_path.replace(":", "_")
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
    numeric_cols = ['Failing_tests', 'Branch_Cov', 'covered_outputs', 'Output_cov', 'total_outputs', 'Test_suite_length',
                    'Private_Method_Covered', 'Trial', 'Private_Methods','Execution_Time', 'Exception_thrown',
                    'Nr_test_cases', 'Generation_success', 'Bug', 'Class_nr', 'Budget']
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
    return df


def is_id_in_filter(project_id, bug_id, class_nr):
    # Load the list of existing project, bug, and class_nr combinations from the CSV file
    existing_projects_bugs = pd.read_csv('/Users/afonsofo/Desktop/defects4j/framework/test/Experiments/bugs_list.csv')

    # Ensure that the bug_id and class_nr are integers, as they are likely to be stored as integers in the CSV
    bug_id = int(bug_id)
    class_nr = int(class_nr)

    # Check if the combination exists in the list
    return not existing_projects_bugs[(existing_projects_bugs['Project'] == project_id) &
                                      (existing_projects_bugs['Bug'] == bug_id) &
                                      (existing_projects_bugs['Class_nr'] == class_nr)].empty



def data_complementar(complementaryFolder, everyTrialReport):
    project_identifiers = [
        'Chart', 'Cli', 'Closure', 'Codec', 'Collections', 'Compress', 'Csv',
        'Gson', 'JacksonCore', 'JacksonDatabind', 'JacksonXml', 'Jsoup',
        'JxPath', 'Lang', 'Math', 'Mockito', 'Time'
    ]
    appended_data = []
    for foldername, subfolders, filenames in os.walk(complementaryFolder):
        for filename in filenames:
            if foldername != "logs" and ".csv" in filename and "statistics" not in filename and "Class" in filename:

                project = "no data"
                bug = "no data"
                classNr = "no data"
                budget = "no data"
                trial = "no data"
                generation_success = "no data"
                criterion = "no data"
                failing_tests = "no data"
                branchCoverage = "no data"
                nr_test_cases = "no data"
                private_Methods = "no data"
                private_Method_Covered = "no data"
                exception_thrown = "no data"
                execution_Time = "no data"
                test_suite_length = "no data"
                output_cov = "no data"
                total_outputs = "no data"
                covered_outputs = "no data"
                BranchCoverageBitString = "no data"
                Total_Branches = "no data"
                Covered_Branches = "no data"
                BranchCoverageTimeline = "no data"
                BranchBitStringTimeline = "no data"

                # Loop through project_identifiers to find the project in foldername
                for identifier in project_identifiers:
                    if identifier in foldername:
                        project = identifier
                        break

                #print(foldername)
                bug = foldername.replace(complementaryFolder,'').split("/")[1]
                #bug = foldername.replace(complementaryFolder,'').split("/")[2]
                budget = foldername.replace(complementaryFolder, '').split("/")[2].replace("budget_", "")
                trial = int((foldername.replace(complementaryFolder, '').split("/")[3].replace("trial_", "")))+10
                #budget = foldername.replace(complementaryFolder, '').split("/")[3].replace("budget_", "")
                #trial = int((foldername.replace(complementaryFolder, '').split("/")[4].replace("trial_", "")))+10
                classNr = int((filename.replace("results-Class_", "").replace(".csv", ""))) + 1
                if is_id_in_filter(str(project), str(bug), str(classNr)):
                    print(project)
                    print(bug)
                    print("--")
                    file_path = os.path.join(foldername, filename)
                    results = pd.read_csv(file_path)
                    row = 0

                    for i in range(5):
                        if str(results.BranchCoverage[i]) != "no data":
                            branchCoverage = results.BranchCoverage[i]
                            criterion = str(results.criterion[i])
                            row = i
                            break
                    if criterion != "no data":
                        log_path_et = str(foldername+"/generationData/"+criterion+"/bug_detection_log/"+project+"/run_bug_detection.pl.log")
                        log_path_et = log_path_et.replace(":", "_")
                        execution_Time = extract_execution_time(log_path_et)
                    if "no data" not in str(execution_Time):
                        if float(execution_Time) > 0:
                            generation_success = str(1)
                        else:
                            generation_success = str(0)
                    else:
                        generation_success = str(0)
                    if float(generation_success) > 0:
                        failing_tests = results.Bug_Detection[row]
                    if criterion != "no data":
                        log_path = str(foldername+"/generationData/"+criterion+"/1-EvoTranscription.log")
                        log_path = log_path.replace(":", "_")
                        nr_test_cases, test_suite_length = extract_test_info(log_path)
                    private_Methods = (results.Total_PrivateMethods[row])
                    private_Method_Covered = results.Covered_PrivateMethods[row]
                    Total_Branches = results.Total_Branches[row]
                    Covered_Branches = results.Covered_Branches[row]
                    exception_thrown = results.ExceptionsCovered[row]
                    output_cov = results.OutputCoverage[row]
                    total_outputs = results.Total_OutputGoals[row]
                    covered_outputs = results.Covered_OutputGoals[row]
                    BranchCoverageBitString = results.BranchCoverageBitString[row]
                    BranchCoverageTimeline = results.BranchCoverageTimeline[row]
                    BranchBitstringTimeline = results.BranchBitstringTimeline[row]


                    newRow = pd.DataFrame({
                        "Project": [project],
                        "Bug": [int(bug)],
                        "Class_nr": [classNr],
                        "Budget": [budget],
                        "Trial": [trial],
                        "Generation_success": [generation_success],
                        "Criterion": [criterion],
                        "Failing_tests": [failing_tests],
                        "Branch_Cov": [branchCoverage],
                        "Total_Branches": [Total_Branches],
                        "Covered_Branches": [Covered_Branches],
                        "Nr_test_cases": [nr_test_cases],
                        "Private_Methods": [private_Methods],
                        "Private_Method_Covered": [private_Method_Covered],
                        "Exception_thrown": [exception_thrown],
                        "Execution_Time": [execution_Time],
                        "Test_suite_length": [test_suite_length],
                        "Output_cov": [output_cov],
                        "total_outputs": [total_outputs],
                        "covered_outputs": [covered_outputs],
                        "BranchCoverageBitString": [BranchCoverageBitString],
                        "BranchCoverageTimeline": [BranchCoverageTimeline],
                        "BranchBitstringTimeline": [BranchBitstringTimeline],
                    })
                    appended_data.append(newRow)
    # Combine the newly created rows with the existing DataFrame
    if appended_data:
        appended_data = pd.concat(appended_data, ignore_index=True)
        everyTrialReport = pd.concat([everyTrialReport, appended_data], ignore_index=True)
        appended_data.to_csv("/Users/afonsofo/Desktop/defects4j/framework/test/Experiments/1-complement_data_wave_2.csv", index=False)
        return everyTrialReport
    else:
        return

def data_complementar1(complementaryFolder, everyTrialReport):
    project_identifiers = [
        'Chart', 'Cli', 'Closure', 'Codec', 'Collections', 'Compress', 'Csv',
        'Gson', 'JacksonCore', 'JacksonDatabind', 'JacksonXml', 'Jsoup',
        'JxPath', 'Lang', 'Math', 'Mockito', 'Time'
    ]
    appended_data = []
    for foldername, subfolders, filenames in os.walk(complementaryFolder):
        for filename in filenames:
            if foldername != "logs" and ".csv" in filename and "statistics" not in filename and "Class" in filename:

                project = "no data"
                bug = "no data"
                classNr = "no data"
                budget = "no data"
                trial = "no data"
                generation_success = "no data"
                criterion = "no data"
                failing_tests = "no data"
                branchCoverage = "no data"
                nr_test_cases = "no data"
                private_Methods = "no data"
                private_Method_Covered = "no data"
                exception_thrown = "no data"
                execution_Time = "no data"
                test_suite_length = "no data"
                output_cov = "no data"
                total_outputs = "no data"
                covered_outputs = "no data"
                BranchCoverageBitString = "no data"
                Total_Branches = "no data"
                Covered_Branches = "no data"
                BranchCoverageTimeline = "no data"
                BranchBitStringTimeline = "no data"

                # Loop through project_identifiers to find the project in foldername
                for identifier in project_identifiers:
                    if identifier in foldername:
                        project = identifier
                        break

                #bug = foldername.replace(complementaryFolder,'').split("/")[1]
                bug = foldername.replace(complementaryFolder,'').split("/")[2]
                #budget = foldername.replace(complementaryFolder, '').split("/")[2].replace("budget_", "")
                #trial = int((foldername.replace(complementaryFolder, '').split("/")[3].replace("trial_", "")))+10
                budget = foldername.replace(complementaryFolder, '').split("/")[3].replace("budget_", "")
                trial = int((foldername.replace(complementaryFolder, '').split("/")[4].replace("trial_", "")))+10
                classNr = int((filename.replace("results-Class_", "").replace(".csv", ""))) + 1

                if is_id_in_filter(str(project), str(bug), str(classNr)):
                    print(project)
                    print(bug)
                    print("--")
                    file_path = os.path.join(foldername, filename)
                    results = pd.read_csv(file_path)
                    row = 0
                    for i in range(5):
                        if str(results.BranchCoverage[i]) != "no data":
                            branchCoverage = results.BranchCoverage[i]
                            criterion = str(results.criterion[i])
                            row = i
                            break
                    if criterion != "no data":
                        log_path_et = str(foldername+"/generationData/"+criterion+"/bug_detection_log/"+project+"/run_bug_detection.pl.log")
                        log_path_et = log_path_et.replace(":", "_")
                        execution_Time = extract_execution_time(log_path_et)
                    if "no data" not in str(execution_Time):
                        if float(execution_Time) > 0:
                            generation_success = str(1)
                        else:
                            generation_success = str(0)
                    else:
                        generation_success = str(0)
                    if float(generation_success) > 0:
                        failing_tests = results.Bug_Detection[row]
                    if criterion != "no data":
                        log_path = str(foldername+"/generationData/"+criterion+"/1-EvoTranscription.log")
                        log_path = log_path.replace(":", "_")
                        nr_test_cases, test_suite_length = extract_test_info(log_path)
                    private_Methods = (results.Total_PrivateMethods[row])
                    private_Method_Covered = results.Covered_PrivateMethods[row]
                    Total_Branches = results.Total_Branches[row]
                    Covered_Branches = results.Covered_Branches[row]
                    exception_thrown = results.ExceptionsCovered[row]
                    output_cov = results.OutputCoverage[row]
                    total_outputs = results.Total_OutputGoals[row]
                    covered_outputs = results.Covered_OutputGoals[row]
                    BranchCoverageBitString = results.BranchCoverageBitString[row]
                    BranchCoverageTimeline = results.BranchCoverageTimeline[row]
                    BranchBitstringTimeline = results.BranchBitstringTimeline[row]


                    newRow = pd.DataFrame({
                        "Project": [project],
                        "Bug": [int(bug)],
                        "Class_nr": [classNr],
                        "Budget": [budget],
                        "Trial": [trial],
                        "Generation_success": [generation_success],
                        "Criterion": [criterion],
                        "Failing_tests": [failing_tests],
                        "Branch_Cov": [branchCoverage],
                        "Total_Branches": [Total_Branches],
                        "Covered_Branches": [Covered_Branches],
                        "Nr_test_cases": [nr_test_cases],
                        "Private_Methods": [private_Methods],
                        "Private_Method_Covered": [private_Method_Covered],
                        "Exception_thrown": [exception_thrown],
                        "Execution_Time": [execution_Time],
                        "Test_suite_length": [test_suite_length],
                        "Output_cov": [output_cov],
                        "total_outputs": [total_outputs],
                        "covered_outputs": [covered_outputs],
                        "BranchCoverageBitString": [BranchCoverageBitString],
                        "BranchCoverageTimeline": [BranchCoverageTimeline],
                        "BranchBitstringTimeline": [BranchBitstringTimeline],
                    })
                    appended_data.append(newRow)
    # Combine the newly created rows with the existing DataFrame
    if appended_data:
        appended_data = pd.concat(appended_data, ignore_index=True)
        everyTrialReport = pd.concat([everyTrialReport, appended_data], ignore_index=True)
        appended_data.to_csv("/Users/afonsofo/Desktop/defects4j/framework/test/Experiments/1-complement_data_wave_1.csv", index=False)
        return everyTrialReport
    else:
        return

if __name__ == "__main__":

    everyTrialReport = pd.read_csv("/Users/afonsofo/Desktop/defects4j/framework/test/Experiments/1-everyTrialReport.csv")


    complementaryFolder = "/Users/afonsofo/Desktop/defects4j/framework/test/Experiments/data_comp_wave2/"
    everyTrialReport = data_complementar(complementaryFolder, everyTrialReport)

    complementaryFolder = "/Users/afonsofo/Desktop/defects4j/framework/test/Experiments/data_complementares"
    everyTrialReport = data_complementar1(complementaryFolder, everyTrialReport)









'''

    agg_functions = {
        'Trial': 'max',
        'Nr_test_cases': lambda x: round(x.mean(), 2),
        'Test_suite_length': lambda x: round(x.mean(), 2),
        'Failing_tests': lambda x: round(x.mean(), 2),
        'Branch_Cov': lambda x: round(x.mean(), 5),
        'Exception_thrown': lambda x: round(x.mean(), 2),
        'Private_Methods': 'max',
        'Private_Method_Covered': lambda x: round(x.mean(), 4),
        'Execution_Time': lambda x: round(x.mean(), 2),
        'Generation_success': lambda x: round(x.sum() / 10, 4),
        'Output_cov': lambda x: round(x.mean(), 4),
        'total_outputs': lambda x: round(x.mean(), 2),
        'covered_outputs': lambda x: round(x.mean(), 2),
    }
    grouped_df = filtered_rawOutput.groupby(['Project', 'Bug', 'Budget', 'Class_nr', 'Criterion']).agg(agg_functions)

    # Step 1: Identify unique combinations where 'Generation_success' is below 50% or is blank
    to_remove = grouped_df.reset_index()
    to_remove = to_remove[(to_remove['Generation_success'] < 0.5) | pd.isna(to_remove['Generation_success'])]
    to_remove = to_remove[['Project', 'Bug', 'Class_nr']].drop_duplicates()


    # Step 2: Remove all rows with these combinations
    if not to_remove.empty:
        for index, row in to_remove.iterrows():
            condition = (
                    (grouped_df.index.get_level_values('Project') == row['Project']) &
                    (grouped_df.index.get_level_values('Bug') == row['Bug']) &
                    (grouped_df.index.get_level_values('Class_nr') == row['Class_nr'])
            )
            grouped_df = grouped_df.drop(grouped_df[condition].index)

    filtered_df = grouped_df
    # Existing code where you calculate 'More_Trials_Needed'
    trial_data = grouped_df.groupby(['Project', 'Bug', 'Class_nr', 'Criterion', 'Budget'])['Generation_success'].mean().reset_index()
    trial_data['Successful_Trials'] = trial_data['Generation_success'] * 10
    trial_data['More_Trials_Needed'] = 10 - trial_data['Successful_Trials']
    # Convert 'More_Trials_Needed' to integer
    trial_data['More_Trials_Needed'] = trial_data['More_Trials_Needed'].astype(int)
    # Filter out the entries where no more trials are needed
    trial_data_needed = trial_data[trial_data['More_Trials_Needed'] > 0]

    # Write the filtered DataFrame to configurations_to_run.txt
    if not trial_data_needed.empty:
        trial_data_needed.to_csv('configurations_to_run.txt', columns=['Project', 'Bug', 'Criterion', 'Budget', 'More_Trials_Needed'], index=False)
    unique_proj_bug_final = grouped_df.reset_index().groupby(['Project', 'Bug']).size().reset_index().rename(columns={0:'count'})
    print("unique_proj_bug_final: ")
    print(unique_proj_bug_final)
    num_unique_proj_bug_final = unique_proj_bug_final.shape[0]
    print(f"Total number of unique Project/Bug combinations in the final dataset: {num_unique_proj_bug_final}")
    # Group by 'Project' and then list all 'Bug' numbers for each project
    grouped_by_project = unique_proj_bug_final.groupby('Project')['Bug'].apply(list).reset_index()

    # Print the result in a readable format
    print("List of Projects and Their Covered Bugs:")
    for index, row in grouped_by_project.iterrows():
        print(f"{row['Project']}: {row['Bug']}")


    new_column_names = {
        "Trial": "Trials",
        "Private_Method_Covered": "Private_Methods_Covered"
    }


    grouped_df = grouped_df.rename(columns=new_column_names)



    grouped_df.loc[grouped_df['Generation_success'] == 0, 'Generation_success'] = pd.NA
    grouped_df.to_csv("/Users/afonsofo/Desktop/defects4j/framework/test/Experiments/2-allTrialsCompiled_complemented.csv", index=True)
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
        'Nr_test_cases': lambda x: round(x.mean(), 2),
        'Test_suite_length': lambda x: round(x.mean(), 2),
        'Failing_tests': lambda x: round(x.mean(), 2),
        'Branch_Cov': lambda x: round(x.mean(), 5),
        'Exception_thrown': lambda x: round(x.mean(), 2),
        'Private_Methods': lambda x: round(x.mean(), 4),
        'Private_Methods_Covered': lambda x: round(x.mean(), 4),
        'Execution_Time': lambda x: round(x.mean(), 2),
        'Output_cov': lambda x: round(x.mean(), 4),
        'total_outputs': lambda x: round(x.mean(), 2),
        'covered_outputs': lambda x: round(x.mean(), 2),
        'Generation_success': lambda x: round(x.mean(), 4),
    }
    higher_df = grouped_df.groupby(['Budget', 'Criterion']).agg(agg_functions)
    column_to_exclude = 'Trials'
    higher_df = higher_df.drop(columns=column_to_exclude)
    higher_df.to_csv("/Users/afonsofo/Desktop/defects4j/framework/test/Experiments/3-experimentSummaryPerBudget_complemented.csv", index=True)

    average_branch_cov = grouped_df.groupby(['Project', 'Bug'])['Branch_Cov'].mean().reset_index()

    # Generate a distribution plot for average Branch Coverage
    plt.figure(figsize=(12, 6))
    sns.histplot(average_branch_cov['Branch_Cov'], kde=True, bins=30)
    plt.title('Average Branch Coverage Distribution Grouped by Project and Bug')
    plt.xlabel('Average Branch Coverage')
    plt.ylabel('Frequency')
    plt.show()

'''