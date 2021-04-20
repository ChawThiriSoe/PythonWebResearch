# Script:   scraper.py
# Desc:     Print all the output
# Author:   Chaw Thiri Soe
# Created:  June 30, 2020
""" This is scraper python file which is used
    for printing out all the results """

# One third party module 'wget' is used for downloading files.
# So, if the code will be run, 'wget' module must be installed.

import sys
import re
import os
import urllib.error
import webpage_get
import email_phone_analysis
import img_file_analysis
import get_links
import link_download
import hash_crack
import file_analysis


def main():
    # All the hardcoded filepath or URL (if you want to change filepath, you can change here)

    sys.argv.append("http://soc-web-prd-01.napier.ac.uk/staff/petra/cw/")  # For URL
    filepath = "../download/"  # For 'download' folder
    output_file = "../output.txt"  # For 'output' text file which is for saving all results
    badfilepath = "../badfiles.txt"  # For 'badfile' text file which is for checking badfiles
    wordfile = "../wordlist.txt"  # For 'wordlist' text file which is for cracking

    try:
        print("The program is running!! Please Wait!!\n.\n.\n.")

        #### Open output file to save all print statements
        # modified from https://stackoverflow.com/questions/7152762/how-to-redirect-print-output-to-a-file-using-python (Gringo Suave, 22/8/2011)
        stdoutOrigin = sys.stdout
        with open(output_file, "w") as f:
            sys.stdout = f

            # Check args
            if len(sys.argv) != 2:
                print("[-] Usage: Scraper URL")
                return

            # Get webpage
            wpcontent = webpage_get.getcontent(sys.argv[1])
            print(f"[*] {sys.argv[1]} : This url is using ....\n")

            #### Start of printing the hyperlinks
            try:
                links = get_links.print_links(wpcontent)

                print("[*] Usage: get_links")
                print(f"[+] The number of hyperLinks which are found: {len(links)}")

                # Print absolute hyperlinks
                alinks = get_links.absolute_link(links)
                print("\n[+] The following are the absolute links of hyperlinks: ")
                alinks.sort()
                email_phone_analysis.counting(alinks)

                # Print relative hyperlinks
                rlinks = get_links.relative_link(alinks, links)
                print("\n[+] The following are the relative links of hyperlinks: ")
                rlinks.sort()
                email_phone_analysis.counting(rlinks)
            except Exception as exc:
                print(f"[-] Exception({exc.__class__.__name__}): {exc}")
            ##### End of printing the hyperlinks

            print(
                "\n***********************************************************************************************************************************************************************"
            )

            #### Start of printing the result of img_file_analysis
            try:
                # Get the images
                imgs = img_file_analysis.get_image(wpcontent)

                # Print the images
                print("\n[*] Usage: img_file_analysis.get_image")
                print(f"[+] The number of images which are found: {len(imgs)}")

                # Print absolute links of images
                aimg = get_links.absolute_link(imgs)
                print("\n[+] The following are the absolute links of images: ")
                aimg.sort()
                email_phone_analysis.counting(aimg)

                # Print relative links of images
                reimg = get_links.relative_link(aimg, imgs)
                print("\n[+] The following are the relative links of images: ")
                reimg.sort()
                email_phone_analysis.counting(reimg)
            except Exception as exc:
                print(f"[-] Exception({exc.__class__.__name__}): {exc}")

            print(
                "\n***********************************************************************************************************************************************************************"
            )

            try:
                # Get the files
                files = img_file_analysis.get_file(wpcontent)

                # Print the files
                print("\n[*] Usage: img_file_analysis.get_file")
                print(f"[+] The number of files which are found: {len(files)}")

                # Print absolute links of files
                afile = get_links.absolute_link(files)
                print("\n[+] The following are the absolute links of files: ")
                afile.sort()
                email_phone_analysis.counting(afile)

                # Print relative links of files
                refile = get_links.relative_link(afile, files)
                print("\n[+] The following are the relative links of files: ")
                refile.sort()
                email_phone_analysis.counting(refile)
            except Exception as exc:
                print(f"[-] Exception({exc.__class__.__name__}): {exc}")

            #### End of printing the result of img_file_analysis

            print(
                "\n***********************************************************************************************************************************************************************"
            )

            #### Start of printing the result of email_phone_analysis
            try:
                param = re.search("^https|http", sys.argv[1])
                if param:
                    content = wpcontent
                else:
                    content = email_phone_analysis.txtget(sys.argv[1])

                # Print email addresses
                try:
                    print("\n[*] Usage: email_phone_analysis.findemail")
                    getemails, mail_to = email_phone_analysis.findemail(content)
                    print(
                        f"\n[+] The number of email addresses which are found: {len(getemails)}"
                    )
                    email_phone_analysis.counting(getemails)
                    print(
                        f"\n[+] The following {len(mail_to)} is(are) the mailto email!!!"
                    )
                    email_phone_analysis.counting(mail_to)
                except Exception as exc:
                    print(f"[-] Exception({exc.__class__.__name__}): {exc}")

                print(
                    "\n***********************************************************************************************************************************************************************"
                )

                # Print phone numbers
                try:
                    print("\n[*] Usage: email_phone_analysis.getphone")
                    getphone = email_phone_analysis.findphone(content)
                    print(
                        f"\n[+] The number of phone numbers which are found: {len(getphone)}"
                    )
                    email_phone_analysis.counting(getphone)
                except Exception as exc:
                    print(f"[-] Exception({exc.__class__.__name__}): {exc}")

            except urllib.error.HTTPError as exc:
                print(f"[-] Exception({exc.__class__.__name__}): {exc}")
            #### End of printing the result of email_phone_analysis

            print(
                "\n***********************************************************************************************************************************************************************"
            )

            #### Start of printing the result of dict_crack
            try:
                # Get md5 hash
                hashs = hash_crack.get_hash(wpcontent)
                # Print md5 hash
                print("\n[*] Usage: hash_crack.get_hash")
                print(f"\n[+] The number of hash which are found: {len(hashs)}")
                pdict = email_phone_analysis.counting(hashs)
            except Exception as exc:
                print(f"[-] Exception({exc.__class__.__name__}): {exc}")

            print(
                "\n***********************************************************************************************************************************************************************"
            )

            # Print the cracked md5 hash
            try:
                print("\n[*] Usage: hash_crack.crack_hash")
                for i in pdict.keys():
                    print(f"\n[+] {i} is cracking...")
                    passwd = hash_crack.crack_hash(i, wordfile)
                    if passwd != None:
                        print("     The hash is cracked!!!")
                        print(f"     The password of the hash is ----------> {passwd}")
                    else:
                        print("[-] The hash cannot be cracked!!")
            except Exception as exc:
                print(f"[-] Exception({exc.__class__.__name__}): {exc}")
            #### End of printing the result of dict_crack

            print(
                "\n***********************************************************************************************************************************************************************"
            )

            #### Start of downloading the files
            try:
                # Get the image links
                imgs = img_file_analysis.get_image(wpcontent)
                # Get the file links
                file = img_file_analysis.get_file(wpcontent)
                all_file = imgs + file
                all_file.sort()
                # Print download successful or not
                print("\n[*] Usage: link_download.file_download")
                print(
                    f"[+] The number of downloading files which are found: {len(all_file)}\n"
                )
                # Download the files and get number of succeeded and failed files
                success, unsuccess = link_download.file_download(all_file, filepath)
                # Print numbers of succeeded and failed files
                print(f"\n[+] The number of files which are downloaded: {len(success)}")
                print(
                    f"[-] The number of file which are failed to download: {unsuccess}"
                )
            except Exception as exc:
                print(f"[-] Exception({exc.__class__.__name__}): {exc}")
            #### End of downloading the files

            print(
                "\n***********************************************************************************************************************************************************************"
            )

            #### Start of searching duplicated files
            try:
                print("\n[*] Usage: link_download.check_duplicate")
                file_dir = os.listdir(filepath)
                file1 = ""
                file2 = ""
                for x in success:
                    # Check if there is same name files or not
                    if success.count(x) > 1:
                        file1 = x
                        success.remove(x)
                        # Check the same name files in the download folder
                        for fp in file_dir:
                            if fp.startswith(os.path.splitext(x)[0]) and fp != x:
                                file2 = fp
                                break
                        # Search the duplicated files
                        first, second, file1_hashsig = link_download.check_duplicate(
                            file1, file2, filepath
                        )
                        # Print the result
                        if file1_hashsig != None:
                            print(
                                f"\n--> {first} has the same name with {second}\n     And, they also have the same content"
                            )
                        else:
                            print(
                                f"\n--> {first} has the same name with {second}\n     But, they do not have the same content"
                            )
            except ValueError as exc:
                print(
                    f"[-] Error : the value error is occurred!! Please check the value in codes"
                )
            except Exception as exc:
                print(f"[-] Exception({exc.__class__.__name__}): {exc}")
            #### End of searching duplicated files

            print(
                "\n***********************************************************************************************************************************************************************"
            )

            #### Start of analysising files
            try:
                print("\n[*] Usage: file_analysis.check_type")
                # Set the file to analyse
                file_dir = os.listdir(filepath)
                match = 0
                unmatch = 0
                for i in file_dir:
                    fp = filepath + "/" + i
                    print(f"\n--> Checking file extension of {i} ...")
                    # Check the file type extension
                    real_type = file_analysis.check_type(fp)
                    # Print the matched or not result
                    if real_type != None:
                        print(
                            f"      Its file type ----------> {os.path.splitext(fp)[1][1:]}"
                        )
                        print(
                            f"      Its actual file extension ----------> {real_type}"
                        )
                        print(
                            "      Its file type and real file extensions are matched!"
                        )
                        match += 1
                    else:
                        print(
                            f"      Its file type ----------> {os.path.splitext(fp)[1][1:]}"
                        )
                        print("[-]  Its actual file extension cannot be identified!!!")
                        unmatch += 1

                # Print the number of matched and unmatched files
                print(
                    f"\n[+]  The number of files which are match with its actual extension: {match}"
                )
                print(
                    f"[-]  The number of file which are not match with its actual extension: {unmatch}"
                )
            except ValueError as exc:
                print(
                    f"[-] Error : the value error is occurred!! Please check the value in codes"
                )
            except Exception as exc:
                print(f"[-] Exception({exc.__class__.__name__}): {exc}")

            print(
                "\n***********************************************************************************************************************************************************************"
            )

            try:
                print("\n[*] Usage: file_analysis.find_badfile\n")
                count = 0
                for files in file_dir:
                    # Check the bad files
                    same = file_analysis.find_badfile(files, badfilepath, filepath)
                    # Print the bad files result
                    if same != None:
                        print(
                            f"--> {files} is matched with **{same}** So, It is the bad file!!!"
                        )
                        count += 1

                # Print the number of found bad files
                print(f"\n[+] The numbers of bad files which are found: {count}")
            except ValueError as exc:
                print(
                    f"[-] Error : the value error is occurred!! Please check the value in codes"
                )
            except Exception as exc:
                print(f"[-] Exception({exc.__class__.__name__}): {exc}")
            #### End of analysising files

            print(
                "\n***********************************************************************************************************************************************************************"
            )

            #### Close output file
        sys.stdout = stdoutOrigin

        print(
            "The program is finished!! All printed outputs are saved in output.txt file!!"
        )
    except NameError as exc:
        print(
            f"[-] Error : {exc} ----------> !!!Your file path may be wrong or it is not defined!!!"
        )
    except Exception as exc:
        print(f"[-] Exception({exc.__class__.__name__}): {exc}")


if __name__ == "__main__":
    main()
