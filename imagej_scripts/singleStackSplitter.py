import os #for making directories
from glob2 import glob
import Tkinter, tkFileDialog
from tqdm import tqdm


#this is just a dialog to choose a folder
root = Tkinter.Tk()
root.withdraw()
root.update()
tempName = tkFileDialog.askopenfilename()
root.update()
root.destroy()


#this kludges to be able to handle spaces in the path
tempName = tempName.replace(' ','\ ')
os.system('/Applications/Fiji.app/Contents/MacOS/ImageJ-macosx --headless /Users/Matt/Documents/python/imageJ\ scripts/stackSplitter.py ' + tempName)