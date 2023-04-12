import os #for making directories
from glob2 import glob
import Tkinter, tkFileDialog
from tqdm import tqdm
import time

#this is just a dialog to choose a folder
root = Tkinter.Tk()
root.withdraw()
root.update()
file_path = tkFileDialog.askdirectory()
root.update()
root.destroy()

#.cine to your file type
paths = glob(file_path+'**/*convolved.tif')
#print paths
#time.sleep(7200)
for i in tqdm(paths):
 tempName = i
 #print tempName
 #this kludges to be able to handle spaces in the path
 tempName = tempName.replace(' ','\ ')
 os.system('/Applications/Fiji.app/Contents/MacOS/ImageJ-macosx  --headless /Users/Matt/Documents/python/imageJ\ scripts/headlessTrackerTemp.py ' + tempName)
