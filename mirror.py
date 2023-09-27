from filecmp import cmp, dircmp
from sys import exit
from time import sleep
from datetime import datetime
import os
import argparse
import shutil

def main():
    # Argument handling
    parser = argparse.ArgumentParser(description="Create a replica folder based on a source folder and mirror its contents")
    parser.add_argument("path_source", type=str, help="Path to source folder")
    parser.add_argument("path_replica", type=str, help="Path to replica folder")
    parser.add_argument("path_log", type=str, help="Path to log file")
    parser.add_argument("interval", type=float, help="Interval in seconds between scans")
    args = parser.parse_args()

    # Escaping arguments
    path_source = os.path.normpath(args.path_source)
    path_replica = os.path.normpath(args.path_replica)
    path_log = os.path.normpath(args.path_log)

    # Working
    print("Mirroring...")
    while True:
        try:
            mirror(path_source, path_replica, path_log)
            sleep(args.interval)
        except KeyboardInterrupt:
            exit("Interrupted")

def mirror(path_source, path_replica, path_log):
    # Check folders names
    if os.path.exists(path_source):
        source_files = os.listdir(path_source)
    else:
        exit("Source folder not located")

    if os.path.exists(path_replica):
        replica_files = os.listdir(path_replica)
    else:
        exit("Replica folder not located")

    # Access log
    current_time = datetime.now()
    log_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

    if not path_log.endswith("log.txt"):
        path_log = os.path.join(path_log, "log.txt")
    log = open(path_log, "a")

    # Add or update files on current folder
    for file in source_files:
        source_file_path = f"{path_source}\{file}"
        destination_file_path = f"{path_replica}\{file}"

        if os.path.isfile(source_file_path):
            # Add new files
            if file not in replica_files:
                shutil.copy(source_file_path, destination_file_path)
                print(f"{log_time} - Creating {file}...")
                log.write(f"{log_time} - Creating {file}...\n")
            # Update files
            elif not cmp(source_file_path, destination_file_path):
                shutil.copy(source_file_path, destination_file_path)
                print(f"{log_time} - Updating {file}...")
                log.write(f"{log_time} - Updating {file}...\n")
        elif os.path.isdir(source_file_path):
            # Create subdirectories and recursively call mirror to run through them
            if file not in replica_files:
                os.mkdir(destination_file_path)
                print(f"{log_time} - Creating folder {file}...")
                log.write(f"{log_time} - Creating folder {file}...\n")

            mirror(source_file_path, destination_file_path, path_log)


    # Remove files from current folder
    for file in replica_files:
        if file not in source_files:
            file_path = f"{path_replica}\{file}"
            # Remove files
            try:
                os.remove(file_path)
                print(f"{log_time} - Removing {file}...")
                log.write(f"{log_time} - Removing {file}...\n")
            # Remove folders
            except PermissionError:
                shutil.rmtree(file_path)
                print(f"{log_time} - Removing folder {file}...")
                log.write(f"{log_time} - Removing folder {file}...\n")

    log.close()

if __name__ == "__main__":
    main()
