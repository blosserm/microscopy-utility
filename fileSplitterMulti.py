import os #for making directories
from glob2 import glob

#.cine to your file type
paths = glob('**/*.cine')
#print paths

for i in paths:
 os.system("python fileSplitter.py --quicksave --newlength 500 " + i)
