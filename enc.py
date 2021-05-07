#!/usr/bin/env python3
"""
enc -a -r [-v -q] -c chipper -d directory file1 file2 ..

Encode a file or group of files by given chipper. All arguments are
optional. If you omit the chipper, you'll be asked when the program 
begins. Encoding a file twice reverts it to the original status.

-c --chipper chipper encoding chipper value
-d --directory directory encode contents of the directory
-a --all encode hidden files too
-r --recursive traverse subdirectories too
-v --verbose verbose mode
-q --quiet quiet mode
file1 file2 .. encode given files

Return Codes:
0  : Everything is fine
11 : Empty file list, no files to encode

   ---Copyright (C) Exforge exforge@karasite.com
   This document is free text: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   any later version.
   This document is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.
   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <https://www.gnu.org/licenses/>.


"""
import os
import argparse
import sys
import getpass

def decen(filename):
   """
   Decode a file with chippers

   filename: string of filename

   Return Codes:
   0 : OK
   11: File not exists or not a file
   12: Encode error
   """
   
   if not os.path.isfile(filename):
      return(11)     # file not exists or not a file, file error
   filelength = os.path.getsize(filename)
   lchippers = len(chippers)
   ckb = 1024              # 1 KB
   cmb = ckb * ckb         # 1 MB
   cgb = cmb * ckb         # 1 GB
   # Give percentage of completion at every MB
   breaker = cmb
   # Display file size
   if filelength > cgb:
      filesize = filelength // cgb 
      cfilesize = str(filesize) + " GB"
   elif filelength > cmb:
      filesize = filelength // cmb 
      cfilesize = str(filesize) + " MB"
   elif filelength > ckb:
      filesize = filelength // ckb 
      cfilesize = str(filesize) + " KB"
   else:
      cfilesize = str(filelength) + " B"
   # try opening and encoding file
   try:
      with open(filename, "r+b") as fio:
         if verbose:
            sys.stdout.write("Encoding " + filename + " " + cfilesize + "...........")
            sys.stdout.flush()
         indata = fio.read(filelength)
         outdata = bytearray(filelength)
         # XOR of bytes in file with the chipper bytes
         for i in range(filelength):
            chipper = chippers[i % lchippers]
            outdata[i] = indata[i] ^ chipper
            if verbose and (i>0) and (i % breaker == 0):
               percent = i / filelength
               b = ""
               if percent < 0.1:
                  b = " "
               sys.stdout.write(f"\b\b\b\b\b\b" + b+ "{:.2%}".format(percent))
               sys.stdout.flush()
         fio.seek(0)
         fio.write(outdata)
   except:
      return(12)
   if verbose:
      sys.stdout.write("\b\b\b\b\b\b done \n")
      sys.stdout.flush() 
   # Actually it means, (not verbose) and (not quiet)
   # In normal mode, display the name of the file encoded
   if not (verbose or quiet):
      sys.stdout.write(filename + "\n")
      sys.stdout.flush()
   return(0)

def traverse(path):
   """
   Traverse a given path, full files list with the filenames.
   If recursive flag is set, traverse subdirectories too.
   """
   cpath = path
   # if there is no / at the end of the directory, add it
   if path[-1] != "/":
      cpath = cpath + "/"
   # Get list of files in that dir
   files = os.listdir(cpath)
   files.sort()      # I love to sort
   # I really love to sort when it is that easy. I wrote so many sort routines
   #    in Pascal and C when I was a student. Now it is really easy. 
   for filename in files:
      # if the item is a directory, traverse it too (if recursive)
      if os.path.isdir(cpath + filename):
         if recursive:
            traverse(cpath + filename)
      # if the item is a file, depending if it is hidden or not, checking all flag
      elif os.path.isfile(cpath + filename):
         if (filename[0] == ".") and not all:
            continue
         allfiles.append(cpath + filename)
      

def getchipper():
   while True:
      print("Enter chipper (password), Ctrl-C to abort:")
      chipper1 = getpass.getpass()
      print("Enter chipper (password) again:")
      chipper2 = getpass.getpass()
      if chipper1 != chipper2:
         print("Passwords do not math, try again...")
         print()
         continue
      if chipper1 == "":
         print("Empty chipper is not allowed, try again...")
         print()
         continue
      break
   return(chipper1)

# Reset all parameters to False, "" or []
all = recursive = verbose = quiet = False
chipper = ""
directory = ""
files = []
allfiles = []

# Process arguments, I love argparse
desc = "This program encodes a file with a chipper. To decode it, you have to " + \
   "encode it again with the same chipper. A very simple encoding mechanism is " + \
   "used, so it can be broken easily, so do not trust it so much. But it " + \
   "might be used to hide documents on your computer\n" + \
   "You can supply a directory with -d option to include all files in it, " + \
   "add -r to traverse subdirectories, use -a to include hidden files. -v and" + \
   " -q are used for verbose and quite modes. With -c you can give you chipper " + \
   "eg. password at the command line, if you omit it you'll be asked for it by " + \
   "the program. Finally you can add filenames to encode"

# Start parser
parser = argparse.ArgumentParser(description="Encode", epilog=desc)

# Add 2 mutually exclusive options
#  verbose or quiet, one or none can be selected
group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", help = "verbose output",
        action="store_true")
group.add_argument("-q", "--quiet", help = "quiet mode, no output",
        action="store_true")

# Optional argument for directory of the files to be renames
parser.add_argument("-d", "--directory", default="",
                    help="directory of the files to be renamed")
parser.add_argument("-c", "--chipper", default="",
                    help="chipper (password) for encoding")
parser.add_argument("-a", "--all", 
                    help="do not ignore entries starting with .", action="store_true")
parser.add_argument("-r", "--recursive", 
                    help="recurse subdirectories", action="store_true")

# Positional argument for the files to encode
parser.add_argument("files", nargs ="*",
        help = "Files to encode")

args = parser.parse_args()

directory = args.directory
chipper = args.chipper
all = args.all 
recursive = args.recursive
quiet = args.quiet
verbose = args.verbose
files = args.files

# Fill the file list from the given directory
if directory != "":
   traverse(directory)
# Add given files to the list
if files != []:
   for filename in files:
      if not os.path.isfile(filename):
         if not quiet:
            print(f"{filename} does not exist, skipping it")
      else:
         allfiles.append(filename)
# No files, nothing to do
if allfiles == []:
   print("No files to process, exiting...")
   exit(11)

# Number of files to process
if not quiet:
   print("Total ", len(allfiles), "files to process...")

# Chipper not given in arguments, ask it
if chipper == "":
   chipper = getchipper()

# Convert chipper text to bytes
chippers = bytearray(chipper, "utf-8")

# Encode all files
for filename in allfiles:
   ret = decen(filename)
   if not quiet:
      if ret == 11:
         sys.stdout.write("File " + filename + "does not exist or is not a file")
         sys.stdout.flush()
      elif ret == 12:
         sys.stdout.write("Unknown encode error on " + filename)
         sys.stdout.flush()
if not quiet:
   print("Done")

