#!/usr/bin/env python3

"""
# helptext2html.py input_text_file output_html_file

A text file will be converted to an html file.
Input file consists of sections containing section header and details.
Section headers start with one of the followings:
    #---, /---, //---
Section headers may contain only one line.
Section details follow the section header and ends when:
    - An empty line comes or
    - Another new section starts
In section details, if a line starts with Link:, the remainder is considered as a link
Link:https://x386.xyz will be converted to 
<a href="https://x386.xyz" target="_blank">x386.xyz</a>
In the html file; section headers display as a link.
All section details are hidden at the beginning.
When you click the section header, its details become visible,
Click it again to hide the details.
Details are displayed as code, that is in a proportional font.
input_text_file name and output_html_file names can be given as command arguments.
if they are skipped, program asks for them as input.
There will be a javacript function, named myFunction to hide and display section details.
Every new section will be named as Div+section_ctr, the function will be called for each
section to hide them initially.
html_escape() method is used to translate escape sequences for <, >, &, [, and ]
A sample.txt file and a sample.html file are given as examples.
Exit Codes:
0  -> Everything is fine
11 -> Input text file does not exist
12 -> Output html file already exists, user chose not to overwrite


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

from sys import argv
import os
import html

# List of HTML Escape Characters to Convert
html_escape_table = {
    "&": "&amp;",
    ">": "&gt;",
    "<": "&lt;",
    "[":"&lsqb;",
    "]":"&rsqb;",
    }

# Taken from:
# https://stackoverflow.com/questions/2077283/escape-special-html-characters-in-python#2077321
def html_escape(text):
    # Convert HTML Escape Characters.
    return "".join(html_escape_table.get(c,c) for c in text)



# Start code for html
html_header = "<!DOCTYPE html> <html> <head> </head> <body>"
# end code for html
html_footer = "</body> </html>"
# Section header, section detail and number of section will be added dynamically
section_header1 = '<p> <a href="javascript:myFunction(\'Div'
section_header2 = '\')">'
section_header3 = '</a> <div id="Div'
section_header4 = '" style="margin-left:10%;"><pre><code>'
# Section footer
section_footer = '</code> </pre> </div> </p>\n'
# Script header, number of times to call the function will be added dynamically
script_header = '''<script>
function myFunction(divid) {
  var x = document.getElementById(divid);
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}
var i;
var str;

for (i=1; i<'''
# script footer, actually the second part of the script
script_footer = '''; i++) {
    str = "Div" + i.toString();
    myFunction(str);
}
</script>'''
# section counter
section_ctr = 0

# a line starting with a section_identifier defines a section header
section_identifier = ["#---", "/---", "//---"]

# start, mid and end of a link
link_start = '<a href="'
link_mid = '" target="_blank">' 
link_end = '</a>'

# a line starting with Link:, link:, or LINK: identifies a link
link_identifier = "Link:"

status = -1
# -1 -> just started, 
# 0 -> header is set, but there is no section yet
# 1 -> a new section header added, adding section details
# 2 -> section details ended

text_file = None
html_file = None

# if we have 1 or more arguments, 1 is input text file
if len(argv) >= 2:
    text_file = argv[1]
# if we have 2 or more arguments 2 is output html file
if len(argv) >= 3:
    html_file = argv[2]

# Input text file was not in the arguments, get it from the user
if text_file == None:
    text_file = input("Please enter input text file name: ")
# There is nothing to do if input text file does not exist
if not os.path.exists(text_file):
    print("Input text file does not exist. Exiting...")
    exit(11)

# Output html file was not in the arguments, get it from the user
if html_file == None:
    # prepare a default output file by changing input file's ext to html
    filename, file_extension = os.path.splitext(text_file)
    temp_html_file = filename + ".html"
    html_file = input(f"Please enter output html file name: ({temp_html_file}) ")
    # if user didnt type anything, use the default
    if html_file.strip() == "":
        html_file = temp_html_file
# If output html file already exists, warn the user to overwrite it
if os.path.exists(html_file):
    ans = input("Output html file already exists. Do you want to overwrite? (y,N) ")
    if ans not in ("y", "Y", "yes", "Yes", "YES"):
        print("Exiting...")
        exit(12)

with open(text_file) as in_file, open(html_file, "w") as out_file:
    out_file.write(html_header)
    for line in in_file:
        new_section = False
        # Process has just started, write Header Line
        if status == -1:
            if line.strip() == "":          # skip beginning empty lines
                continue        
            else:                           # write header line
                out_file.write("<H1>" + html.escape(line) + "</H1>")
                status = 0                  # Set status to expect sections
                continue
        # Check if a new section starting
        for start in section_identifier:
            if line.startswith(start):
                starts_with = start
                new_section = True
                break
        # We are starting a new section
        if new_section:
            # if previous section isnt ended, end it
            if status == 1:
                out_file.write(section_footer)
            section_ctr += 1
            # Add html code for the new section
            sheader_line = section_header1 + str(section_ctr) + section_header2 + \
                html.escape(line[len(starts_with):]) + section_header3 + str(section_ctr) + \
                section_header4
            out_file.write(sheader_line)
            status = 1              # set status to expect section details
            continue
        # An empty line means a section is ended (if not already has ended)
        if line.strip() == "":
            if status == 1:                 # section is ending now
                out_file.write(section_footer)
                status = 2                  # section is ended
            continue
        # if we are in the mode of adding section details
        if status == 1:
            # Check if it is a link line:
            if line.startswith(link_identifier):
                # Stripe link_identifier
                link_text = line[len(link_identifier):-1]
                # Convert the line to an href link
                # line = <a href="link_text" target="_blank">link_text</a>
                line = link_start + link_text + link_mid + link_text + link_end + "\n"
                # add the line                
                out_file.write(line)
            # otherwise, convert html escape characters and add the line
            else:
                out_file.write(html_escape(line))
    # EOF is reached, prepare bottom lines
    out_file.write(section_footer)          # end section
    out_file.write("<br /><br /><br />")    # put 3 empty lines
    # preparing the scripts
    out_file.write(script_header + str(section_ctr+1) + script_footer)
    out_file.write(html_footer)

print("Done")
exit(0)   
