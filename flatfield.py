#just divides one image by another

# Example Useage
# -----
#python flatfield.py 'background.tif' 'filename.tif'

import pims
import argparse
import bottleneck as bn
from skimage import io
import numpy as np
from tqdm import tqdm # adds a taskbar to any loop, e.g. for i in tqdm(range(10000)):
from matplotlib import pyplot as plt # for plotting
import os #for making directories

# Get some variables from command line (nb switch raw_input for input in python v3 here it's v2.7)
parser = argparse.ArgumentParser()
parser.add_argument('--background', help='median flatfield background')
parser.add_argument('--darkCurrent', help = 'dark current, make sure median is already dark current corrected')
parser.add_argument('filename', help='Name of input file, or the directory containing images')
args = parser.parse_args()
backgroundFile = args.background
filename = args.filename

# open the file using the magic of PIMS.
input_images = np.float32(pims.Bioformats(filename))
background = np.float32(pims.Bioformats(backgroundFile))
if args.darkCurrent:
    darkCurrent = np.float32(pims.Bioformats(args.darkCurrent))
    input_images = input_images-darkCurrent


im_out = np.float32(input_images/background)
        #io.imsave(filename + '.output.tif',im_out)

#    if args.normalise :
#        overall_median = bn.nanmedian(im_out, axis=0)
#        im_out = np.float32(im_out / overall_median)
        #print "overall_median", overall_median


io.imsave(filename + '.flatfield.tif',im_out)
print 'Saved', filename + '.flatfield.tif'


#Notes for potential parallelizing this
#from joblib import Parallel, delayed #easy parallel processing
# Under Windows, it is important to protect the main loop of code to avoid recursive spawning of subprocesses when using joblib.
# No code should run outside of the "if __name__ == '__main__'" blocks, only imports and definitions.
    #im_out = np.empty((len(input_images)/filterwindow,input_images[0].shape[0],input_images[0].shape[1]))
    #Parallel(n_jobs=2)(delayed(sqrt)(i ** 2) for i in range(10))
    #Parallel(n_jobs=2)(delayed(sqrt)(i ** 2) for i in range(10))
    #for n in tqdm(range(0,len(input_images)/filterwindow)):
    #im_out[n] = Parallel(n_jobs=2) bn.delayed(nanmean)(input_images[n*filterwindow:(n+1)*filterwindow], axis=0) for n in range(0,len(input_images)/filterwindow)
