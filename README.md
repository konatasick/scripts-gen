ScriptsGen
====================

Overview
--------------------
The script is aiming for a handy tool when you need to test your algorithm with different combinations of parameters. It helps to generate a text file (usually a piece of script) for each parameter combination according to a template file.

Usage
--------------------
    $ scripts_gen.py --help
    usage: scripts_gen.py [-h] --template FILE --save-to FOLDER --param DICT
                          --format STRING [--open TOKEN] [--close TOKEN]
                          [--comment TOKEN] [--delete]
    
    Generate scripts from a template, by enumerating combinations of parameters.
    
    arguments:
      -h, --help        show this help message and exit
      --template FILE   The location of the template file.
      --save-to FOLDER  The destination folder for the scripts.
      --param DICT      All the parameters with their values as a dictionary,
                        where a value can be a list, or a file name that refers to
                        a file containing one parameter value per line. See
                        Python's dictionary literals
                        (http://docs.python.org/3/reference/expressions.html
                        #dictionary-displays).
      --format STRING   The format string for the file names of the scripts. See
                        Python's format string syntax
                        (http://docs.python.org/3/library/string.html#format-
                        string-syntax).
      --open TOKEN      The token that indicates the start of a template
                        identifier. (default: <%)
      --close TOKEN     The token that indicates the end of a template identifier.
                        (default: %>)
      --comment TOKEN   The token placed at the beginning of a certain line in the
                        template file that treats the line, which will be removed
                        in the scripts, as a comment. (default: ###)
      --delete          Delete the contents in the destination folder.


Also, see `example/template.txt` for the built-in template identifiers.

Files
--------------------
- `scripts_gen.py`: the script for Python 3.x users
- `scripts_gen_3to2.py`: the script for Python 2.x users, where probably x>=6
- `example/command-line.sh`: an example of command line that shows how to invoke the script
- `example/template.txt`: an example of template file
- `example/datasets.txt`: an example of parameter input file for the example parameter `data`
