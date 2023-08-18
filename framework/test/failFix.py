import os
import pandas as pd

import os
import pandas as pd

def fix_csv_error(file_path):
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Extract the Bug_Detection column
        bug_detection_column = df['Bug_Detection']

        # Calculate the number of rows to shift
        num_rows = len(df)
        shift_amount = num_rows // 2

        # Check if the CSV was already fixed (by looking at the first row of Bug_Detection)
        if bug_detection_column[4] != "no data":
            df.Bug_Detection[1] = df.Bug_Detection[3]
            df.Bug_Detection[2] = df.Bug_Detection[4]
            df.Bug_Detection[3] = df.Bug_Detection[5]
            df.Bug_Detection[4] = "no data"

            '''elif arg_c=="BRANCH:PRIVATEMETHOD":
                row=1 #3
            elif arg_c=="BRANCH:EXCEPTION":
                row=2 #4
            elif arg_c=="BRANCH:EXECUTIONTIME":
                row=3 #5'''

            # Save the corrected DataFrame back to the CSV file
            df.to_csv(file_path, index=False)

            print(f"Fixed error in {file_path}")
        else:
            print(f"CSV file {file_path} is already fixed")

    except Exception as e:
        print(f"Error fixing {file_path}: {e}")

def iterate_folders(root_folder):
    for root, _, files in os.walk(root_folder):
        for file in files:
            if file.startswith("results-Class_") and file.endswith(".csv"):
                file_path = os.path.join(root, file)
                fix_csv_error(file_path)

if __name__ == "__main__":
    root_folder = "/Users/afonsofo/Desktop/defects4j/framework/test/Experiments/"
    iterate_folders(root_folder)
    print("fixed!")