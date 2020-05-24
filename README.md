# PythonMaterial
Some Python Material, might be used for testing or educational purposes.

ComplexClass.py consist a simple Complex Number class with some methods and operator overloads like +,-,/,* etc. 
It is written to implement (actually learn) Python Object Oriented Programming. Suggesstions are well welcome.

bulkrename.py is written to ease up renaming many files at once. You have to supply a directory (-d) where the files are, or as a default, current directory is used. You can verbose (-v) or quiet (-q) the output. By default . files are not renamed, you can add them with (-a). Renaming is done by following the pattern. All the occurences of the first     character will be changed to the second, all of the third to fourth, fifth to sixth etc. If instead of changing, you want to delete a character, use / as the character to be changed.

helptext2html.py is a converter from txt to html. Input file consists of sections containing section header and details. Section headers start with one of the followings: #---, ---, /---, //--- . Section headers may contain only one line. Section details follow the section header and ends when: 1.An empty line comes or 2. Another new section starts. In the html file; section headers display as a link. All section details are hidden at the beginning. When you click the section header, its details become visible, click it again to hide the details.
Details are displayed as code, that is in a proportional font. input_text_file name and output_html_file names can be given as command arguments. if they are skipped, program asks for them as input. There will be a javacript function, named myFunction to hide and display section details. Every new section will be named as Div+section_ctr, the function will be called for each section to hide them initially.


sample.txt is a sample input file for helptext2html.py program.

sample.html is a sample output file for helptext2html.py program.

