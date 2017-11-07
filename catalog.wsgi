#!/usr/bin/env python3.5
activator = '/var/www/catalog/venv/bin/activate_this.py'  
# Looted from virtualenv; should not require modification, since it's defined relatively

with open(activator) as f:
    exec(f.read(), {'__file__': activator})

import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/catalog/")

from application import app as application
