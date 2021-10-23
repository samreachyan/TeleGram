from sys import argv
from os.path import isfile
import os
import sys

arg = sys.argv[1]
# image = sys.argv[2]

# extract text from file
with open(arg, 'r') as f:
    text = f.read()


print("hello world")
print(arg)

print(text)

if os.path.isfile(sys.argv[2]):
    print("file exists")
else:
    print("file does not exist")
