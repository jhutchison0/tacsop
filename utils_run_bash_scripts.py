# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 14:50:41 2020

@author: jhutchison


"""

import os
import subprocess

os.chdir(r'C:\Users\johnk\OneDrive\Documents\Python Scripts\Stanford\XCS224N-A5-master')

#subprocess.run([r'C:\cygwin64\cygwin.bat','run.sh','vocab'])

#subprocess.run(['python','python_sanity_check.py', '1d'])

subprocess.run([r'C:\Users\johnk\cygwin\bin\bash.exe', 
                r'C:\Users\johnk\OneDrive\Documents\Python Scripts\Stanford\XCS224N-A5-master\collect_submission.sh'],
               check=True, stdout=subprocess.PIPE, universal_newlines=True)
subprocess.run([r'C:\Users\johnk\cygwin\cygwin.bat', 
                r'C:\Users\johnk\OneDrive\Documents\Python Scripts\Stanford\XCS224N-A5-master\collect_submission.sh'],
               check=True, stdout=subprocess.PIPE, universal_newlines=True)
subprocess.run([r'C:\Users\johnk\cygwin\cygwin.bat','collect_submission.sh'], check=True, stdout=subprocess.PIPE, universal_newlines=True)
