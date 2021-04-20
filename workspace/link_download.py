# Script:   link_download.py
# Desc:     Download files and images from page content.
# Author:   Chaw Thiri Soe
# Created:  July 2, 2020
""" This is link_download python file which can be used
    to download images and files which are found
    from the page content and to check duplicated files
    within downloaded files """


import os
import sys
import urllib
import hashlib
import wget


def file_download(links, filepath):
    """ This function is to download images and files
        which are found into certain folder """
    try:
        if os.path.exists(filepath):
            file_dir = os.listdir(filepath)
            for f_path in file_dir:
                fullfp = filepath + f_path
                os.remove(fullfp)  # Remove the old files before downloading
        else:
            os.mkdir(filepath)
    except ValueError as exc:
        print(
            "[-] Error : the value error is occurred!! Please check the value in codes"
        )
    except Exception as exc:
        print(f"[-] Exception({exc.__class__.__name__}): {exc}")

    unsuccess = 0
    get = []

    # Downloading the files
    for down in links:
        try:
            # Download the files if the links starts with http or https
            if down.startswith("http://") or down.startswith("https://"):
                wget.download(
                    down, filepath
                )  # modified from https://stackabuse.com/download-files-with-python/ (Scott Robinson)
                print(f"     {down} ----------> Downloading successful\n")
                get.append(down)
            else:
                # Download the files if the links starts with subfolder
                if down.startswith("subfolder"):
                    down = down[down.index("/") + 1 :]
                    fpath = (sys.argv[1] + "subfolder/" + down)  # Add 'subfolder' at the link to download
                    wget.download(fpath, filepath)  # modified from https://stackabuse.com/download-files-with-python/ (Scott Robinson)
                    print(f"     {down} ----------> Downloading successful\n")
                    get.append(down)
                else:
                    # Download the files if the links is not matched with above conditions
                    # Add full path at the link to download
                    fpath = sys.argv[1] + down
                    wget.download(
                        fpath, filepath
                    )  # modified from https://stackabuse.com/download-files-with-python/ by Scott Robinson
                    print(f"     {down} ----------> Downloading successful\n")
                    get.append(down)
        except urllib.error.HTTPError as exc:
            unsuccess += 1
            # Except the 404 error
            if exc.code == 404:
                print(
                    f"[-] Error code : {exc.code} ----------> !!!**{down}** is the borken link which cannot find!!!\n"
                )
            # Except the 403 error
            elif exc.code == 403:
                print(
                    f"[-] Error code : {exc.code} ----------> !!!**{down}** is the forbidden link which is preventing!!!\n"
                )
            # Except other HTTP error
            else:
                print(
                    f"[-] Exception({exc.__class__.__name__}): {exc} ::: **{down}** cannot be downloaded!!!\n"
                )
        # Except other error
        except Exception as exc:
            unsuccess += 1
            print(
                f"[-] Exception({exc.__class__.__name__}): {exc} ::: **{down}** cannot be downloaded!!!\n"
            )
    return get, unsuccess


def check_duplicate(file1, file2, filepath):
    """ This function is to check the same or not
        of the file content of the same name files """
    try:
        # Get the hash of first file
        with open(filepath + file1, "rb") as f_file:
            file1_hashsig = hashlib.md5(f_file.read()).hexdigest()
        # Get the hash of second file
        with open(filepath + file2, "rb") as s_file:
            file2_hashsig = hashlib.md5(s_file.read()).hexdigest()

        # Check against the first and second files
        if file1_hashsig == file2_hashsig:
            return file1, file2, file1_hashsig
        return file1, file2, None
    except FileNotFoundError as exc:
        print(
            f"[-] Error : {exc} ----------> !!!Your file path may be wrong or your file may not be located!!!"
        )
    except Exception as exc:
        print(f"[-] Exception({exc.__class__.__name__}): {exc}")
