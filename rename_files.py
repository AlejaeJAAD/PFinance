import os

def rename_files(folder_path):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        new_file_name = file_name.upper()
        new_file_path = os.path.join(folder_path, new_file_name)
        os.rename(file_path, new_file_path)

rename_files("./files")
