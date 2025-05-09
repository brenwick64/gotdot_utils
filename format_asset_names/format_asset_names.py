import os
import re
import shutil
import argparse

# constants
INPUT_DIR = "input"
OUTPUT_DIR = "output"
SUFFIX_WHITELIST = ["png", "PNG", "gif", "jpg"]

# global variables
global_path_list: list = []


def dump_dir_recursive(filename: str) -> None:
    for sub_dir in os.listdir(filename):
        # base case: file is not a directory
        if not os.path.isdir(os.path.join(filename, sub_dir)):
            global_path_list.append({
                "is_dir": False,
                "path": os.path.join(filename, sub_dir),
                "suffix": sub_dir.split(".")[-1] if "." in sub_dir else None
             })
             
        # recursive case: if the sub_dir is a directory, call the function again
        else:
            global_path_list.append({
                "is_dir": True,
                "path": os.path.join(filename, sub_dir),
                "suffix": None  
            })
            dump_dir_recursive(os.path.join(filename, sub_dir))
            
            
def extract_formatted_filepath(path: str) -> str:
    # remove input and output directory names from the path
    path = path.replace(INPUT_DIR, "")
    path = path.replace(OUTPUT_DIR, "")
    
    path = re.sub(r'-', '_', path) # replace dashes with underscores
    path = re.sub(r' ', '_', path) # remove spaces
    path = re.sub(r'_+', '_', path) # remove multiple underscores
    path = path.lower() # convert to lowercase
    return path


def main():
    # build list of all files and directories in input directory
    dump_dir_recursive(INPUT_DIR)

    # create all subdirectories
    for entry in global_path_list:
        if entry["is_dir"]:
            new_path = OUTPUT_DIR + extract_formatted_filepath(entry["path"])
            os.makedirs(new_path, exist_ok=True)
            
    # copy all files to the new directory structure
    for entry in global_path_list:    
        if not entry["is_dir"]:
            if not entry["suffix"] in SUFFIX_WHITELIST:
                continue
            new_path = OUTPUT_DIR + extract_formatted_filepath(entry["path"])
            shutil.copy2(entry["path"], new_path)
            
            
if __name__ == "__main__":
    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, default=INPUT_DIR, help="Input directory path")
    parser.add_argument("-o", "--output", type=str, default=OUTPUT_DIR, help="Output directory path")
    args = parser.parse_args()
    # set input and output directory paths
    if args.input:
        INPUT_DIR = args.input
        print(f"\nInput directory: {INPUT_DIR}")
    if args.output:
        print(f"Output directory: {args.output}\n")
        OUTPUT_DIR = args.output
    main()