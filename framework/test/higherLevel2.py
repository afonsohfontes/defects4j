import os
import pandas as pd
import datetime

def process_folders(root_dir, output_file):
    output = pd.read_csv(output_file)

    newRow = pd.DataFrame({
        "Project": ["no data"],
        "Bug": ["no data"],
        "Class_nr": ["no data"],
        "Budget": ["no data"],
        "Trial": ["no data"],
        "Criterion": ["no data"],
        "Failing_tests": ["no data"],
        "Branch_Cov": ["no data"],
        "Nr_test_cases": ["no data"],
        "Private_Methods": ["no data"],
        "Private_Method_Covered": ["no data"],
        "Exception_thrown": ["no data"],
        "Execution_Time": ["no data"],
    })
    for foldername, subfolders, filenames in os.walk(root_dir):
        now = datetime.datetime.now()
        for filename in filenames:
            if foldername != "logs" and ".csv" in filename and "statistics" not in filename and "Class" in filename:
                #print("file name: ", filename)
                # print("folder name:", foldername.replace(root_dir,'').split("/"))
                # project = foldername.replace(root_dir,'').split("/")[0]
                # bug = foldername.replace(root_dir,'').split("/")[1]
                budget = foldername.replace(root_dir, '').split("/")[2].replace("budget_", "")
                trial = foldername.replace(root_dir, '').split("/")[3].replace("trial_", "")
                classNr = int(filename.replace("results-Class_", "").replace(".csv", "")) + 1
                file_path = os.path.join(foldername, filename)
                input = pd.read_csv(file_path)
                row_count, column_count = output.shape
                for i in range(3):
                    newRow.Project = input.Project[i]
                    newRow.Bug = input.Bug[i]
                    newRow.Criterion = input.criterion[i]
                    newRow.Class_nr = classNr
                    newRow.Budget = budget
                    newRow.Trial = trial
                    newRow.Failing_tests = input.Bug_Detection[i]
                    newRow.Branch_Cov = input.BranchCoverage[i]
                    newRow.Private_Methods = input.Total_PrivateMethods[0]
                    newRow.Failing_tests = input.Bug_Detection[i]
                    newRow.Private_Method_Covered = input.Covered_PrivateMethods[i]
                    newRow.Exception_thrown = input.ExceptionsCovered[i]
                    print(newRow)
                    output = pd.concat([output, newRow])

    # print(now.year, now.month, now.day, now.hour, now.minute, now.second)
    str2 = " - "+str(now.year)+str(now.month)+str(now.day)+" - "+str(now.hour)+":"+str(now.minute)+".csv"
    str3 = output_file.replace("MODEL_","").replace(".csv",str2)
    print(str3, "saved in ", root_dir)
    output.to_csv(root_dir+str3, index=False)
    return output
if __name__ == "__main__":
    project_root = "/Users/afonsofo/Desktop/defects4j/framework/test/Experiments/data/"
    output_csv_format = "MODEL_everyTrialReport.csv"
    # rawOutput = process_folders(project_root, output_csv_format)
    rawOutput = pd.read_csv("/Users/afonsofo/Desktop/defects4j/framework/test/Experiments/data/everyTrialReport_2023727_14h59m.csv")
    rawOutput.replace("no data", pd.NA, inplace=True)
    grouped_df = rawOutput.groupby(['Project', 'Bug', 'Budget', 'Criterion', 'Class_nr']).median()
    print(grouped_df)
    grouped_df.to_csv("/Users/afonsofo/Desktop/defects4j/framework/test/Experiments/aa.csv", index=True)