# Script:   get_links.py
# Desc:     Parses out all hyperlinks from the page content
# Author:   Chaw Thiri Soe
# Created:  June 22, 2020
""" This is get_links python file which can be used
    for searching the hyperlinks from page content
    and for separating the absoulute and relative links """


import sys
import re
import urllib.parse


def print_links(wpcontent):
    """ This function is to find all hyperlinks from page content and return it """
    # Search all the hyperlinks
    links = re.findall(r"\b(?:href)=[\"\'](.*?)[\"\']", wpcontent)

    # sort and return the links
    links.sort()
    return links


def absolute_link(links):
    """ This function is to extract the absoulte link from all links """
    # Search the absoulte links
    alink = []
    for link in links:
        match = re.search(r"^(https|http|ftp|mailto)\:.+", link)
        # Append the links to the list
        if match:
            alink.append(link)
    return alink


def relative_link(alinks, links):
    """ This function is to extract the relative link from all links """
    fullpath = []
    # Remove the absoulte links from all links
    for re_link in alinks:
        links.remove(re_link)
    # Add the full url to the relative links
    for link in links:
        fpath = urllib.parse.urljoin(sys.argv[1], link)
        fullpath.append(fpath)
    return fullpath
