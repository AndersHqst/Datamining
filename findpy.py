from __future__ import print_function
import os
import fnmatch

rootPath = os.getcwd()
pattern = '*.py'
 
lines = []
for root, dirs, files in os.walk(rootPath):
    for filename in fnmatch.filter(files, pattern):
        output = os.path.join(root, filename).replace(rootPath, '..')
        lines.append(output)

with open('pythonfiles.txt', 'w') as f:
    for line in lines:
        print(line, file=f)