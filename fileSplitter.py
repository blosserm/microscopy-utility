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
parser.add_argument('--normalise', action='store_true', help='normalise the data?' )
parser.add_argument('--newlength', type=int, help='save output as this many TIF stacks' )
args = parser.parse_args()
filename = args.filename

# open the file using the magic of PIMS.
input_images = pims.Bioformats(args.filename)


im_out = np.uint32(input_images)
    #io.imsave(filename + '.output.tif',im_out)

if args.normalise :
    overall_median = bn.nanmedian(im_out, axis=0)
    im_out = np.float32(im_out / overall_median)
    #print "overall_median", overall_median

if args.newlength  :
    print len(im_out)
    print args.newlength
    filenameprefix = os.path.splitext(filename)[0]
    #os.makedirs(str(filenameprefix)+str(args.newlength)+'files')
    for n in tqdm(range(0,len(im_out)/args.newlength)):
        #io.imsave(filenameprefix+str(args.newlength)+'files/'+ filename + '.' + str(filterwindow) + '.output.' + str(n) +'.tif',im_out[n*args.newlength:(n+1)*args.newlength])
        io.imsave(filename + '.output.' + str(n) +'.tif',im_out[n*args.newlength:(n+1)*args.newlength])
else :
    io.imsave(filename + '.output.tif',im_out)
    print 'Saved', filename + '.output.tif'


#Notes for potential parallelizing this
#from joblib import Parallel, delayed #easy parallel processing
# Under Windows, it is important to protect the main loop of code to avoid recursive spawning of subprocesses when using joblib.
# No code should run outside of the "if __name__ == '__main__'" blocks, only imports and definitions.
    #im_out = np.empty((len(input_images)/filterwindow,input_images[0].shape[0],input_images[0].shape[1]))
    #Parallel(n_jobs=2)(delayed(sqrt)(i ** 2) for i in range(10))
    #Parallel(n_jobs=2)(delayed(sqrt)(i ** 2) for i in range(10))
    #for n in tqdm(range(0,len(input_images)/filterwindow)):
    #im_out[n] = Parallel(n_jobs=2) bn.delayed(nanmean)(input_images[n*filterwindow:(n+1)*filterwindow], axis=0) for n in range(0,len(input_images)/filterwindow)
