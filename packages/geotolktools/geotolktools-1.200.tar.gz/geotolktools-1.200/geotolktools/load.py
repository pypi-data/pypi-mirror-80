from collections import defaultdict
import sys
import os
import re
from typing import List
from .parser import parse_snd_file, parse_tlk_file, parse_prv_file, path_to_lines

_VALID_FILETYPES = [".snd", ".tlk", ".prv"]
_PR_PATTERN = re.compile(".*PR([^\-]).*(SND|snd)")


if sys.platform == "linux" or sys.platform == "linux2":
    _os = "linux"
    _SEPARATOR = "/"
elif sys.platform == "win32":
    _os = "win"
    _SEPARATOR = "\\"


def _find_filenames_in_folder(path: str) -> List[str]:
    return os.listdir(path)


def _remove_filenames_without_snd_file(files: List[str]) -> List[str]:
    # If none of the files ends with .snd, ignore the rest of the files
    for filename in files:
        if filename[-4:].lower() == ".snd":
            return files
    return []

def _prune_filetypes(files: List[str]) -> List[str]:
    # Remove files with invalid filetypes from the list
    return [f for f in files if f[-4:].lower() in _VALID_FILETYPES]

def _remove_incomplete_files(files: List[str]) -> List[str]:
    # Remove files containing PR.SND (except PR-*.SND for some reason...)
    return [f for f in files if not _PR_PATTERN.match(f)]

def _remove_CPTU_files(files: List[str]) -> List[str]:
    # Remove CPTU files. They can be found by having CPTU in their name
    return [f for f in files if "cptu" not in f.lower()]


def _get_oppdragsnr(oppdragsnr: str) -> int:
    return int(oppdragsnr.split("_")[-1])

def _sanitize_filename(filename: str) -> str:
    # First remove file ending
    prefix = filename[:-4]
    # Then remove special filename conventions from old versions
    for code in ["cpt", "prv", "pr", "tot"]:
        if code in prefix.lower():
            # remove special characters 
            prefix = "".join(e for e in prefix if e.isalnum())
            # remove upper and lower case versions of the code
            prefix = prefix.replace(code.lower(), "")
            prefix = prefix.replace(code.upper(), "")
    return prefix

def _create_id(path: str) -> dict:
    split_str = path.split(_SEPARATOR)
    filename = split_str[-1]
    oppdragsnr_raw = split_str[-3]
    oppdragsnr = _get_oppdragsnr(oppdragsnr_raw)
    borehole_id = _sanitize_filename(filename)
    return {"oppdragsnr": oppdragsnr, "borehole_id": borehole_id, "filename": filename}

_FILEPARSER = {
    "snd": parse_snd_file,
    "prv": parse_prv_file,
    "tlk": parse_tlk_file
}

def load_folder(folder_path: str) -> dict:
    # Find all filenams in the folder
    filenames = _find_filenames_in_folder(folder_path)

    # Remove unwanted files
    filenames = _remove_CPTU_files(filenames)
    filenames = _prune_filetypes(filenames)
    filenames = _remove_incomplete_files(filenames)
    # Initialize dict to hold all files with a defaultdict with lists
    folder_data = defaultdict(list)

    # Loop through each file
    for file in filenames:
        # Get absolute path
        abspath = os.path.join(folder_path, file)
        # Create ID
        _id = _create_id(abspath)
        # Create unique identifier by joining oppdragsnr and borehole id
        uid = f"{_id['oppdragsnr']}_{_id['borehole_id']}"
        # Read the lines
        lines = path_to_lines(abspath)
        # Get filetype
        file_type = file[-3:].lower()
        # Use the defined file parser for the specific file type
        parsed = _FILEPARSER[file_type](lines)
        parsed = {**_id, **parsed}
        folder_data[uid].append(parsed)
    return folder_data

