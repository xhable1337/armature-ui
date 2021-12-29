from dataclasses import dataclass
import os
import sys


# Define function to import external files when using PyInstaller.
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


@dataclass
class Values:
    a: float
    b: float
    h: float
    M: float
    N: float
    As_: float
    concrete_type: str
    armature_type: str