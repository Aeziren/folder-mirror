import os
from filecmp import cmp
from sys import exit
import argparse
import time
import shutil

def main():
    # Argument handling
    parser = argparse.ArgumentParser(description='Create a folder replica')
    parser.add_argument('path_source', type=str, help='Path to source folder')
    parser.add_argument('--path_replica', type=str, help='Path to replica folder (optional)')
    parser.add_argument('--interval', type=float, help='Interval in seconds between scans (optional)')
    args = parser.parse_args()

    if not args.interval:
        # Need attention here
        interval = 5

    while True:
        mirror(args.path_source, args.path_replica)
        time.sleep(args.interval)

def mirror(path_source, path_replica=None):
    # Check folders names
    if os.path.exists(path_source):
        source_files = os.listdir(path_source)
    else:
        exit("Source folder does not exists")

    if path_replica and os.path.exists(path_replica):
        replica_files = os.listdir(path_replica)
        print(f"Mirroring to {path_replica}...")
    else:
        path_replica = os.getcwd()
        replica_files = os.listdir(path_replica)
        print("Mirroring to current working directory...")

    # Add or update files on current folder
    for file in source_files:
        origin_file_path = f"{path_source}\{file}"
        destination_file_path = f"{path_replica}\{file}"

        try:
            if file not in replica_files:
                shutil.copy(origin_file_path, destination_file_path)
            elif not cmp(origin_file_path, destination_file_path):
                shutil.copy(origin_file_path, destination_file_path)
        except PermissionError:
            try:
                os.mkdir(destination_file_path)
            except FileExistsError:
                pass
            mirror(origin_file_path, destination_file_path)



    # Remove files from current folder
    for file in replica_files:
        if file not in source_files:
            file_path = f"{path_replica}\{file}"
            try:
                os.remove(file_path)
            except PermissionError:
                shutil.rmtree(file_path)

if __name__ == "__main__":
    main()
