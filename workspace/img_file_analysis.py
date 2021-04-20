# Script:   img_file_analysis.py
# Desc:     Parsing out images and files from the page content
# Author:   Chaw Thiri Soe
# Created:  June 28, 2020
""" This is img_file_analysis python file which can be used
    to pull out all the links of images and files from page content """


import re
import get_links


def get_image(wpcontent):
    """ This function is to parse out the images from the page content """
    # Extract images from <img> tages
    imgs = re.findall(r"\b(?:src)=[\"\'](.*?)[\"\']", wpcontent)

    # Extract images from background images of inline CSS
    imgs.extend(
        re.findall(r"\b(?:background-image):url\([\"\'](.*?)[\"\']\)", wpcontent)
    )

    # Extract images from <form> tages
    imgs.extend(
        re.findall(r"\b(?:action)=[\"\'](.*[jpg|jpeg|bmp|gif|png])[\"\']", wpcontent)
    )
    return imgs


def get_file(wpcontent):
    """ This function is to search the document
        or pdf files from the page content """
    # Get all hyperlinks list from print_links function
    link = get_links.print_links(wpcontent)

    # Extract the pdf or docx files
    files = []
    for i in link:
        match = re.search(r".*(pdf|PDF|docx|DOCX)$", i)
        if match:
            files.append(i)
    return files
