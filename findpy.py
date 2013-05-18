from __future__ import print_function
import os
import fnmatch

rootPath = os.getcwd()
pattern = '*.py'

lines = []
for root, dirs, files in os.walk(rootPath):
    for filename in fnmatch.filter(files, pattern):
        relativePath = os.path.join(root, filename).replace(
            rootPath, '').replace('\\', '/')
        title = '\\subsection{File: \\texttt{%s}}' % relativePath.replace(
            '_', '\\_')
        output = '\pythonfile{..' + relativePath + '}'
        lines.append(title)
        lines.append(output)

with open('pythonfiles.txt', 'w') as f:
    for line in lines:
        print(line, file=f)
