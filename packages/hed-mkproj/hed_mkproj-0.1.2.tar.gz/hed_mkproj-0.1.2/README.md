# hed_mkproj

Vanilla project skeleton generator.


## Description

Installs the 'mkproj' CLI command:
    
    usage: mkproj [-h] [-v] [-p PACKAGE_NAME] project_name
    
    Vanilla project skeleton generator.
    
    positional arguments:
      project_name     desired project name.
    
    optional arguments:
      -h, --help       show this help message and exit
      -v               verbose (debug-level) logging. (info by default)
      -p PACKAGE_NAME  root package name. (defaults to project name)
    
    NOTE: Project is created in cwd (...) !

---

Creates the following project structure:

path                                        | type 
-----                                       | -----
.\project_name                              | folder 
.\project_name\setup.py                     | file 
.\project_name\README.md                    | file 
.\project_name\MANIFEST.in                  | file 
.\project_name\Docs                         | folder 
.\project_name\tests                        | folder 
.\project_name\package_name                 | folder 
.\project_name\package_name\\\_\_init__.py  | file 


## Installation / Upgrade

- Windows

    pip install --user --upgrade --force hed_mkproj
    
- Linux / Mac

    pip3 install --user --upgrade --force hed_mkproj

