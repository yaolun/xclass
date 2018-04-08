In the starting script for using XCLASS outside of CASA (Sec. 1.5)
* inconsistent variable definition for `NewModulePath`.  It seems to me that there should be only one module path for XCLASS.  `NewModulePath` seems more reasonable for me.  
* Too many iterations performed for adding the module path to the system path.
    ```python
    # extend sys.path variable
    already_included_flag = False
    for entries in sys.path:  
        if (entries == NewModulesPath):
            already_included_flag = True
            break  
        if (not already_included_flag):
            sys.path.append(NewModulesPath)  
    ```
    update:
    ```python
    # extend sys.path variable
    if NewModulesPath not in sys.path:
        sys.path.append(NewModulesPath)
    ```
* Need to `import os` first in order to use the `os.environ` function.
