# utils.file_utils.py : Hanterar filhantering
import os
import shutil

def save_file(file_path, destination_dir):
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    shutil.copy(file_path, destination_dir)

def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        raise FileNotFoundError(f"Filen '{file_path}' finns inte.")

def read_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return file.read()
    else:
        raise FileNotFoundError(f"Filen '{file_path}' finns inte.")
