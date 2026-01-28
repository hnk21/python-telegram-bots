from utility.variables import *

# Finds the target folder and returns its path
def find_folder(folder: str):
    print(">> directory.py > find_folder")
    for root, dirs, files in os.walk(os.getcwd()):
        if folder in root:
            print(f"> Found target folder '{folder}' in '{root}'")
            return root

# Checks if file exists, creates a new one if it does not, and returns its path
def check_file(file: str, path: str):
    print(">> directory.py > check_file")
    file_path = path + "/" + file
    if not os.path.exists(file_path):
        with open(file_path, "w") as log:
            pass
        print(f"> Created '{file}' in '{path}'")
    else:
        print(f"> Found '{file}' in '{path}'")
    return file_path

# Checks if file needs to be created/updated 
# depending on whether it was last modified more than specified hours ago
# Returns boolean value indicating whether it needs to be created/updated, and its path
def check_file_update(file: str, path: str, hours: int):
    print(">> directory.py > check_file_update")
    file_path = path + "/" + file
    to_update = True
    if os.path.exists(file_path):
        last_modified = datetime.fromtimestamp(os.path.getmtime(file_path))
        hours_ago = (datetime.now() - last_modified).seconds / 3600
        if hours_ago > hours:
            to_update = True
        else:
            to_update = False
        print(f"> Found '{file}', last modified {round(hours_ago, 0)} hours ago")
    else:
        print(f"> '{file}' not found in target folder '{path}'")
        to_update = True
    return to_update, file_path