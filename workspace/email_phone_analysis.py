# Script:   email_phone_analysis.py
# Desc:     Get email addresses and phone numbers from the page content
# Author:   Chaw Thiri Soe
# Created:  June 24, 2020
""" This is email_phone_analysis python file which can used to
    extract the email address and phone number from page content
    and counting function is for counting the duplicated links """


import re
import collections


def txtget(filename):
    """ This function is opening and reading the file content
        which is getting as a parameter, and returning it """
    txtfile = open(filename)
    file_content = txtfile.read()
    return file_content


def findemail(wpcontent):
    """ This function is to find email address and
        extract the mail_to email from page content """
    # Find emails from page content
    emails = re.findall(r"[a-zA-Z0-9_.+-:]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", wpcontent)

    # Extract and remove mail_to email
    mail_to = []
    for i in emails:
        match = re.search(r"^mailto:.*", i)
        if match:
            mail_to.append(i)
            emails.remove(i)

    return emails, mail_to


def findphone(wpcontent):
    """ This function is for searching phone numbers from page content """
    # Find phone numbers from page content
    phone = re.findall(r"(\+44[- ]*[(0)]*\d{3}[- ]*\d{3}[- ]*\d{4})", wpcontent)
    return phone


def counting(result):
    """ This function is to check duplication
        using counter method and print them """
    # Count duplication and get counting numbers as dictionary
    result_dict = collections.Counter(result)
    count = 1
    for dkey, dvalue in result_dict.items():
        print(f"     No({count}): {dkey} ----------> {dvalue} time(s) repeated")
        count += 1
    return result_dict
