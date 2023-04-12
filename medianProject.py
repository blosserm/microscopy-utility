# Setup Instructions
# -----
# pip install bottleneck
# pip install scikit-image
# pip install pims
# pip install jpype1
# pip install tifffile
# pip install tqdm

# Example Useage
# -----
#python MIW_imageaverager.py --median --running --filterwindow 50 2PEG5us10short.cine
#python MIW_imageaverager.py --median --grouped --filterwindow 50 'test/*.tif'
#python MIW_imageaverager.py --median --grouped --filterwindow 50 percsim_f_0.1.tif

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
parser.add_argument('filename', help='Name of input file, or the directory containing images')
args = parser.parse_args()
filename = args.filename

subLen = 1000


# open the file using the magic of PIMS.
input_images = pims.Bioformats(args.filename)
iter = len(input_images)/subLen

    #io.imsave(filename + '.output.tif',im_out)
subStack = input_images[1:len(input_images):iter]

median = np.nanmedian(subStack, axis=0)


io.imsave(filename + '.medProj.tif',median)
print 'Saved', filename + '.medProj.tif'


#Notes for potential parallelizing this
#from joblib import Parallel, delayed #easy parallel processing
# Under Windows, it is important to protect the main loop of code to avoid recursive spawning of subprocesses when using joblib.
# No code should run outside of the "if __name__ == '__main__'" blocks, only imports and definitions.
    #im_out = np.empty((len(input_images)/filterwindow,input_images[0].shape[0],input_images[0].shape[1]))
    #Parallel(n_jobs=2)(delayed(sqrt)(i ** 2) for i in range(10))
    #Parallel(n_jobs=2)(delayed(sqrt)(i ** 2) for i in range(10))
    #for n in tqdm(range(0,len(input_images)/filterwindow)):
    #im_out[n] = Parallel(n_jobs=2) bn.delayed(nanmean)(input_images[n*filterwindow:(n+1)*filterwindow], axis=0) for n in range(0,len(input_images)/filterwindow)
