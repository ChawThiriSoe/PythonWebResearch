# Script:   hash_crack.py
# Desc:     Extract the md5 hashes of passwords from the page content
#           Crack the password hash using the wordlist file
# Author:   Chaw Thiri Soe
# Created:  July 4, 2020
""" This is hash_crack python file which can be used
    for getting the hash code from page content and
    for cracking them """


import re
import hashlib


def get_hash(wpcontent):
    """ This function is to extract hash code
        from page content and return it """
    # Find md5 hashes from page content
    hash_found = re.findall(r"(?=(\b[A-Fa-f0-9]{32}\b))", wpcontent)
    return hash_found


def crack_hash(hashs, filename):
    """ This function is to crack hash code to readable words """
    try:
        # Get the possible words from the wordlist text file
        pwd_list = []
        with open(filename, "r") as pwd_file:
            for pwd in pwd_file:
                pwd_list.append(pwd.strip())

        # Check against the md5 hashes to the possible words
        for passwd in pwd_list:
            pwd = hashlib.md5(passwd.encode()).hexdigest()
            if pwd == hashs:
                return passwd
        return None
    except ValueError as exc:
        print(
            "[-] Error : the value error is occurred!! Please check the value in codes"
        )
    except Exception as exc:
        print(f"[-] Exception({exc.__class__.__name__}): {exc}")
