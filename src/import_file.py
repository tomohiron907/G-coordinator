'''
import_file

import_file is meant to import a python script from a normal file path.
Relative (dotted) imports are complicated, and fixing sys.path just feels wrong.

Usage examples::

    >>>from import_file import import_file
    >>>mylib = import_file('c:\\mylib.py')
    >>>another = import_file('relative_subdir/another.py')
    
    
So now you aren't limited to importing only within your package or trail of
__init__.py files.

This should work for python 2.5-3.2 and it's public domain, have fun.


 - http://uberpython.wordpress.com
 - http://code.google.com/p/import-file/
 - http://pypi.python.org/pypi/import_file
 - ubershmekel at gmail
 
'''

import imp as _imp
import os as _os


def import_file(fpath):
    '''
    fpath - the relative or absolute path to the .py file which is imported.
    
    Returns the imported module.
    
    NOTE: if import_file is called twice with the same module, the module is reloaded.
    '''
    if hasattr(_os, 'getcwdu'):
        # python 2 returns question marks in os.path.realpath for
        # ascii input (eg '.').
        original_path = _os.path.realpath(_os.getcwdu())
    else:
        original_path = _os.path.realpath(_os.path.curdir)
    dst_path = _os.path.dirname(fpath)
    if dst_path == '':
        dst_path = '.'
    
    # remove the .py suffix
    script_name = _os.path.basename(fpath)
    if script_name.endswith('.py'):
        mod_name = script_name[:-3]
    else:
        # packages for example.
        mod_name = script_name
    
    _os.chdir(dst_path)
    fhandle = None
    try:
        tup = _imp.find_module(mod_name, ['.'])
        module = _imp.load_module(mod_name, *tup)
        fhandle = tup[0]
    finally:
        _os.chdir(original_path)
        if fhandle is not None:
            fhandle.close()
    
    return module



