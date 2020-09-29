#!/usr/bin/env python3
"""
bulkrename.py is written to ease up renaming many files at once. You have to 
supply a directory (-d) where the files are, or as a default, current directory 
is used. 
You can verbose (-v) or quiet (-q) the output. By default . files are not renamed, 
you can add them with (-a). Renaming is done by following the pattern. All the 
occurences of the first character will be changed to the second, all of the third 
to fourth, fifth to sixth etc. If instead of changing, you want to delete a character, 
use / as the character to be changed.

    Copyright (C) 2020 Exforge exforge@x386.xyz

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


import argparse
import os

def ren(ins, ddict):
    """ Renames in and returns the result by using the ddict dictionary.
    Every character existing as a key in dict is changed to that key's val.
    Changing must be done one by one to avoid multiple changes.
    """
    outs = ""
    for i in range(len(ins)):
        if ins[i] in ddict:
            outs = outs + ddict[ins[i]]
        else:
            outs = outs + ins[i]
    return outs

# A somewhat long program description, also can be considered as a comment

desc = "This program is written to ease up renaming many files at once. "  + \
    "You have to supply a directory (-d) where the files are, or as a default, " + \
    "current directory is used. You can verbose (-v) or quiet (-q) the output. " + \
    "By default . files are not renamed, you can add them with (-a). " + \
    "Renaming is done by following the pattern. All the occurences of the first " + \
    "character will be changed to the second, all of the third to fourth, fifth " + \
    "to sixth etc. If instead of changing, you want to delete a character, use / " + \
    "as the character to be changed." 

# Start parser
parser = argparse.ArgumentParser(description="Bulk Rename", epilog=desc)

# Add 2 mutually exclusive options
#  verbose or quiet, one or none can be selected
group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", help = "verbose output",
        action="store_true")
group.add_argument("-q", "--quiet", help = "quiet mode, no output",
        action="store_true")

# Optional argument for directory of the files to be renames
parser.add_argument("-d", "--directory", default="./",
                    help="directory of the files to be renamed")

parser.add_argument("-a", "--all", 
                    help="do not ignore entries starting with .", action="store_true")



# Positional argument for the renaming pattern
"""Rename pattern is a string containing character to change and 
   character to be changed one by one. Thus RrAaCc means, R-->r, A-->a C-->c
   To remove a character instead of changing it, it must be followed by /
   Thus RrAaCcD/ means the same as above except all Ds will be removed.
   For repeated characters, only the last one will be used.
   """
parser.add_argument("pattern", 
        help = "Rename pattern. RrSs./  / is used to remove the char")

args = parser.parse_args()

# If given directory of files does not exist, leave the program with error code
if not os.path.isdir(args.directory):
    print("Directory", args.directory, "Does not exists. Exiting...")
    exit(1)


""" If there is an excess character, that is there are odd number of
    characters in the pattern, remove the last character
"""
ipattern = args.pattern
lenp = len(ipattern)
if lenp % 2 == 1:
    ipattern = ipattern[0:lenp-1]
lenp = len(ipattern)

""" Create a dict from the pattern, key --> char to be replaced
    val --> char to replace
"""
dpattern = dict()
for i in range(lenp//2):
    pat = ipattern[i*2+1]
    # / means char to be deleted, so null is assigned
    if pat == "/":
        pat = ""
    dpattern[ipattern[i*2]] = pat


# Get the directory of the files, 
#  put a / at the end if not already exists
path = args.directory
if path[-1] != "/":
    path = path + "/"

# Get the list of the items in the directory
files1 = os.listdir(path)        # List of everything in the directory
files1.sort()                    # It is easy to sort, so why not
files2 = list()                  # Only files will be added here
other_files = list()             # All others will be added here

# From all items (files, dirs) get only the files in a new list
#   All other items will be put the other_files list
for ffile in files1:
    if os.path.isfile(path + ffile):
        if ffile[0] == ".":
            if args.all:
                files2.append(ffile)
            else:
                other_files.append(ffile)
        else:
            files2.append(ffile)
    else:
        other_files.append(ffile)


# From the new list, remove the unchanging files and make a new list
#  move unchanging files to other_files list
files3 = list()

for ffile in files2:
    if ffile != ren(ffile, dpattern):
        files3.append(ffile)
    else:
        other_files.append(ffile)

# Now, all files to rename are in files3, all other files and dirs are in other_files

# Find the files that would cause a name conflict and put them in a skip list
#   if the new name of a file is already a name of other files, it will be skipped
skip_files = list()         # The list of skipped files because of the name conflict
files4 = list()             # Almost final list of files to be renamed

for ffile in files3:
    if ren(ffile, dpattern) in other_files:
        skip_files.append(ffile)
    else:
        files4.append(ffile)

""" Two (or more) of the files can be renamed to the same name in the list. 
    They will be found and put into the skip list.
    """
files5 = list()             # Final list of files to be renamed
skip2_files = list()        # Temporary place to keep renamed file name
for ffile in files4:
    # if the files renamed state would already be in the list
    #   put the file to the skip list
    if ren(ffile, dpattern) in skip2_files:
        skip_files.append(ffile)
    # Otherwise, file is OK, put its renamed state to the temporary list
    #   to check the other files with
    else:
        files5.append(ffile)
        skip2_files.append(ren(ffile, dpattern))


# If not quiet mode, display the skipped files.
if len(skip_files) != 0:
    if not args.quiet:
        print("The following files cause a name conflict.")
        print("So they will not be renamed:")
        for ffile in skip_files:
            print(path + ffile)

# If there are no files to rename, give a message and quit
if len(files5) == 0:
    if not args.quiet:
        print("No files to rename, exiting")
    exit(0)

""" In quiet mode do nothing. 
    In verbose mode, display the pattern, list all the files to rename and their renamed state. 
    In verbose and standart mode, ask user to continue.
    """

if args.verbose:
    print("Rename pattern:")
    for key in dpattern:
        print(key, "-->", dpattern[key])
    print()
    print("The following file renames will be processed:")
    for ffile in files5:
        print(path+ffile, "-->",  path + ren(ffile, dpattern))
    print()
if not args.quiet:
    print("!!!This process is irreversible!!!")         # I mean I cannot reverse it
    ans = input("Type Yes or Y to continue, any other to exit:")
    if ans not in ["Yes", "yes", "Y", "y"]:
        print("Exiting...")
        exit(2)
    print()

if not args.quiet:
    print("Renaming processing started...")

error_flag = False                  # Keep track of any rename error
error_files = list()                # Files with rename error

# Rename process
for ffile in files5:
    source = path + ffile
    dest = path + ren(ffile, dpattern)
    if args.verbose:
        print("Renaming", source, "to", dest)
    # try renaming
    try: 
        t = os.rename(source, dest)
    # error occured, put the file in error list
    except:
        error_flag = True
        error_files.append(ffile)
        if args.verbose:
            print("Rename is not successfull, possibly a name conflict")
    # rename successfull
    else:
        if args.verbose:
            print("Rename is successfull")

# Display finishing message, for verbose mode display renaming errors too   
message1 = "Rename process complete. "
message2 = "Some files couldn't be renamed."
message3 = "Following files also couldn't be renamed."
finish_message = message1
if error_flag:
    if args.verbose:
        finish_message = message1 + message3
    else:
        finish_message = message1 + message2

if not args.quiet:
    print(finish_message)

if args.verbose and error_flag:
    for ffile in error_files:
        print(path + ffile)

# This is the end
