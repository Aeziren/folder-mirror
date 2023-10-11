# Folder Mirror
#### Video Demo:  https://youtu.be/769DdzG_GBw
### Description:
This program implemment a folder mirror. Every change that happens on the source folder will be mirrored to the replica
folder while the program keeps running. Also, the changes will be logged in the terminal and in a especified log.txt file.
#### Usage:
The program usage is pretty objective:
1. Download project.py
1. Setup the folders
1. Execute the programm per the instructions below:

The programm must be executed followed by 4 parameters.
1. Path to the folder you want to track.
1. Path to where your replica folder is located.
1. Path to where you want the log file to be created.
1. Interval in seconds between each update.
(Lower intervals and big source folder may decrease performance)

Example:
```bash
python mirror.py "C:\\path\\to\\source\\folder\\" "C:\\path\\to\\replica\\folder" "C:\\path\\to\\log\\file\\" "interval(seconds)"
```

```bash
python mirror.py "C:\\Users\\Miguel\\Desktop\\Demonstration\\Source Folder\\" "C:\\Users\\Miguel\\Desktop\\Demonstration\\Replica Folder\\" "C:\\Users\\Miguel\\Desktop\\Demonstration\\" 0.1
```

### How it works:
#### Getting parameters and executing (main)
The main function is responsible for two things:
1. Get user input and escaping it in the case there is a space in any of the folder paths.
1. Execute the mirror function in the interval provided by the user.

#### Mirror Function:
The mirror function is the core of the programm. When called it will search for every file on the source folder, checking
if it already exists in the replica folder.

Case it don't exists, mirror will create a copy of the respective file. Otherwise, it will check again, now looking for modifications.
Since it is not possible to compare two folders directly, in the case that mirror confirm that some file is a folder, it will call itself to run through that folder.

Mirror is capable of keeping track of and handling:
1. Folder creation/deletion
1. Folder modification
1. File creatio/deletion
1. File modification

Mirror will raise and expection case is trying copy an entire app. Since it can't handle the installation proccess.

#### Log Changes function:
Log changes will automatically take care of writing the logs of every change made by mirror. It takes an action as key to formulate a string:
For consistency, the action string should be an verb.

#### Check Path Function:
Check paths takes as many arguments as the user wants.
Obs.: Check paths will raise an exception FileNotFoundError in case any of the arguments cannot be found in the OS.

#### Error Handling:
The program currently has handling for invalid inputs. Such as files or folders not found.

### Future Improvements:
#### Improve Stability:
Some actions that a user can take while running the app can cause it to raise an exception. Such as:
1. Changing any of the file paths.
1. Replica folder be the same as source folder.
1. Moving installable apps.
1. Moving files that should not be moved.
