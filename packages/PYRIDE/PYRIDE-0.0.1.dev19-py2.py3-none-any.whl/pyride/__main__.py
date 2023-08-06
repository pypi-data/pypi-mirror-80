
"""
This module is the console entry point when setup.py was used to install pyride.
This module is also run with the -m option from the terminal
"""

import sys
from .core import App

try:
    import requests
except (ImportError, ModuleNotFoundError):
    raise ValueError("Must have 'requests' installed: 'pip install requests' -> CMD line")


def main(*args, **kwargs):
    if args is None:
        args = sys.argv[1:]
    
    app = App()
    app.mainloop()

if __name__ == '__main__':
    main()
