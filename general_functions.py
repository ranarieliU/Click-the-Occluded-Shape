from os import listdir
from os.path import isfile, join
from os import getcwd

# debugging function - prints files in current directory
def print_files_in_dir():
    curr_path = getcwd()
    onlyfiles = [f for f in listdir(curr_path) if isfile(join(curr_path, f))]
    print(onlyfiles)


