# hed_mkproj

Vanilla project skeleton generator.


## Description

Installs the 'mkproj' CLI command:
    
    usage: mkproj [-h] [-v] -n NAME [-d DESCRIPTION] [-p PACKAGE]
    
    Vanilla project skeleton generator.
    
    optional arguments:
      -h, --help      show this help message and exit
      -v              set logging level to debug (default: info)
      -n NAME         project name
      -d DESCRIPTION  project description
      -p PACKAGE      project package (default: project name)
    
    NOTE: Project is created in cwd (...) !

---

Creates the following project structure:

path                                        | type 
-----                                       | -----
.\project_name                              | folder 
.\project_name\build.sh                     | file 
.\project_name\setup.py                     | file 
.\project_name\README.md                    | file 
.\project_name\LICENSE.txt                  | file 
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

