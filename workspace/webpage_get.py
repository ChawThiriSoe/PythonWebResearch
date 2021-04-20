# Script:   webpage_get.py
# Desc:     Fetch data from the URL
# Author:   Chaw Thiri Soe
# Created:  June 20, 2020
""" This is webpage_get python file which can be used
    to get the page content from the URL """


import urllib.request


def getcontent(url):
    """ Retrieve webpage through URL, and return its page content """
    try:
        # Get the page content of URL
        webpage = urllib.request.urlopen(url)
        # Read the page content and decode it
        page_contents = webpage.read().decode()
        # Return the decoded page content
        return page_contents
    except:
        print(f"[-] {url} : This url is not existed!! Please check it again!!")
