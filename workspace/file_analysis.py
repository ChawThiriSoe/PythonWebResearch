# Script:   file_analysis.py
# Desc:     Check acutal file types and badfiles, and report them
# Author:   Chaw Thiri Soe
# Created:  July 5, 2020
""" This is link_download python file which can used to
    check against file extension types
    and check badfiles within downloaded files """


import os
import hashlib


def check_type(full_dir):
    """ This is for checking the file extension
        by using file type signature """
    # Add file extension signatures into dictionary
    sigs = {
        b"\xff\xd8\xff": ("JPG", "jpg", "JPEG", "jpeg"),
        b"\x42\x4d": ("BMP", "bmp"),
        b"GIF": ("GIF", "gif"),
        b"\x89PN": ("PNG", "png"),
        b"%PD": ("PDF", "pdf"),
        b"PK\x03": ("DOCX", "docx"),
    }

    try:
        # Get file type
        fread = open(full_dir, "rb")
        file_sig = fread.read(3)
        print("      Its hash signature:", file_sig)

        # Search actual file extension
        real_type = ""
        if file_sig in sigs:
            real_type = sigs[file_sig]
            for j in real_type:
                if j == os.path.splitext(full_dir)[1][1:]:
                    return j
        return None
    except Exception as exc:
        print(f"[-] Exception({exc.__class__.__name__}): {exc}")


def find_badfile(files, filename, downloadfolder):
    """ This function is to search bad files
        into files which is downloaded """
    # Get the bad file data from text file to dictionary
    try:
        badfiles = {}
        with open(filename, "r") as getbadfile:
            for line in getbadfile:
                dkey, dvalue = line.strip().replace("'", "").split(":")
                badfiles[dkey.strip()] = dvalue.strip()

        # Get the hash signature of downloaded file
        with open(downloadfolder + files, "rb") as gethashfile:
            fileread = gethashfile.read()
            fhash = hashlib.md5(fileread).hexdigest()

        # Check against the bad file dictionary
        for dkey, dvalue in badfiles.items():
            if dkey == fhash:
                return dvalue
        return None
    except FileNotFoundError as exc:
        print(
            f"[-] Error : {exc} ----------> !!!Your file path may be wrong or your file may not be located!!!"
        )
    except Exception as exc:
        print(f"[-] Exception({exc.__class__.__name__}): {exc}")
