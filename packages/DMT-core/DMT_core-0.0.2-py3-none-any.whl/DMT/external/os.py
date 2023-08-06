""" OS interaction of DMT
"""
import os
import shutil
from pathlib import Path

##MARKUS CONTEXT MANAGER AWESOMENESS ###############
# this is a cd command that support context_manager python commands.

class cd:
    """Context manager for changing the current working directory

    Usage::

    ```
        with cd(dir):
            pass
    ```

    """
    def __init__(self, newPath):
        self.savedPath = None
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

def recursive_copy(src, dst, force=False):
    """ Recursively copies a full directory to a new destination folder.

    Parameters:
    -------------
    src : str or os.Pathlike
        Path to the source folder
    dst : str or os.Pathlike
        Path to the destination folder
    force : bool, optional
        When true, all files are overwritten. Else, already existing ones are kept.
    """
    if not isinstance(src, Path):
        src = Path(src)
    if not isinstance(dst, Path):
        dst = Path(dst)
    for item_src in src.iterdir():
        item_dst = dst / item_src.name
        if item_src.is_file():
            if not item_dst.exists() or force:
                shutil.copy(item_src, dst)

        elif item_src.is_dir():
            item_dst.mkdir(exist_ok=True)
            recursive_copy(item_src, item_dst)
        else:
            raise ValueError("DMT->recursive_copy: I do not know this filettype.")
