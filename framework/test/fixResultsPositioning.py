import os
import pandas as pd

def copy_column_data(source_df, dest_df):
    for column in source_df.columns:
        if "OnlyBranchCoverage" in column:
            dest_column = column.replace("OnlyBranchCoverage", "BranchCoverage")
            for i in range(len(source_df)):
                source_value = source_df.at[i, column]
                dest_value = dest_df.at[i, dest_column]
                if source_value != "no data" and dest_value == "no data":
                    print(f"Copying '{source_value}' from {column} to {dest_column} in row {i}")

                    # confirmation = input("Confirm overwrite? (yes/no): ")
                    if True: # confirmation.lower() == "yes":
                        dest_df.at[i, dest_column] = source_value
                        print("Data overwritten.")
                    else:
                        print("Skipped.")

    return dest_df

def iterate_folders(root_folder):
    for root, _, files in os.walk(root_folder):
        for file in files:
            if file.startswith("results-Class_") and file.endswith(".csv"):
                file_path = os.path.join(root, file)
                print(root)
                try:
                    df = pd.read_csv(file_path)
                    modified_df = copy_column_data(df, df.copy())

                    modified_df.to_csv(file_path, index=False)
                    print(f"Modified {file_path}")
                except Exception as e:
                    print(f"Error modifying {file_path}: {e}")

if __name__ == "__main__":
    root_folder = "/Users/afonsofo/Desktop/defects4j/framework/test/Experiments/data/"
    iterate_folders(root_folder)
    print("Data columns copied and modified!")
