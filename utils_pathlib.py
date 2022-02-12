# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 23:25:03 2021

@author: johnk
"""

from pathlib import Path

p = Path('.')
[x for x in p.iterdir() if x.is_dir()]
list(p.glob('**/*.py'))
