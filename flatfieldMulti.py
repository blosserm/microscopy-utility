import os #for making directories
from glob2 import glob
import tqdm
import Tkinter, tkFileDialog

root = Tkinter.Tk()
root.withdraw()
root.update()
file_path = tkFileDialog.askdirectory()
root.update()
root.destroy()

#print file_path

#.cine to your file type
#paths = glob('**/*405*.tif')
paths = glob(file_path+'**/**/*491*.tif')
#print paths

for i in paths:
    #print i
    tempName = i
    #this kludges to be able to handle spaces in the path
    tempName = tempName.replace(' ','\ ')

    os.system("python /Users/Matt/Documents/uscCode/gasTransport/flatfield.py --darkCurrent /Users/Matt/Documents/malmstadt\ lab/darkCurrent_nikon_491.tif --background /Users/Matt/Documents/malmstadt\ lab/flatfieldMinusDarkCurrent_nikon_491.tif " + tempName)
