import os
import shutil

def delete_branch_folders(root_folder):
    for current_folder, subfolders, _ in os.walk(root_folder, topdown=False):
        for folder in subfolders:
            if folder == "BRANCH_PRIVATEMETHOD":
                folder_path = os.path.join(current_folder, folder)
                try:
                    shutil.rmtree(folder_path)
                    print(f"Deleted folder and its contents: {folder_path}")
                except OSError as e:
                    print(f"Error deleting folder {folder_path}: {e}")

def rename_onlybranch_folders(root_folder):
    for current_folder, subfolders, _ in os.walk(root_folder, topdown=False):
        for folder in subfolders:
            if folder == "ONLYBRANCH_PRIVATEMETHOD":
                old_folder_path = os.path.join(current_folder, folder)
                new_folder_path = os.path.join(current_folder, "BRANCH_PRIVATEMETHOD")
                try:
                    os.rename(old_folder_path, new_folder_path)
                    print(f"Renamed folder: {old_folder_path} -> {new_folder_path}")
                except OSError as e:
                    print(f"Error renaming folder {old_folder_path}: {e}")

if __name__ == "__main__":
    root_directory = "/Users/afonsofo/Desktop/defects4j/framework/test/Experiments/data/"
    delete_branch_folders(root_directory)
    rename_onlybranch_folders(root_directory)
