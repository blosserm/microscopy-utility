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
from scipy import signal
import csv

# Get some variables from command line (nb switch raw_input for input in python v3 here it's v2.7)
parser = argparse.ArgumentParser()
parser.add_argument('filename', help='Name of input file, or the directory containing images')
parser.add_argument('--subtractMedian', action='store_true', help='subtract off the median value' )
parser.add_argument('--flatfield', help='subtract off the median value' )
args = parser.parse_args()
filename = args.filename
#constants
timeStep = 0.01 #in seconds
channelPos1 = 424 #left channel left edge, in pixels
channelPos2 = 214 #right channel left edge, in pixels
channelPos3 = 0
channelW = 88 #channel width in pixels
medFilt = 61 #number of frames for rolling median filter, must be odd

print 'opening file'
# open the file using the magic of PIMS.
input_images = pims.Bioformats(filename)
print 'file open'
#input_images = np.float32(input_images)

if args.flatfield:
    print 'flat field correcting'
    backgroundFile = args.flatfield
    background = pims.Bioformats(backgroundFile)
    background = background/np.average(background)
    background = background[0]
else:
    input_images = input_images[0]


if args.subtractMedian:
    print 'subtracting the median background'
    subLen = 1000
    iter = len(input_images)/subLen
    subStack = input_images[1:len(input_images):iter]
    median = np.nanmedian(subStack, axis=0)
    input_images = input_images - median




int1 = np.float32(np.ones(len(input_images)))
int2 = np.float32(np.ones(len(input_images)))
times = np.uint32(range(len(input_images)))*timeStep

for i in tqdm(range(len(input_images))):
#for i in tqdm([1,2,3,4,5,6,7,8,9,10]):

    frame = input_images[i]
    frame = np.float32(frame)
    if args.flatfield:
        frame = frame/background
    #else:
        #frame = frame[0]
        #frame = frame[0]
    int1[i] = sum(sum(frame[:, channelPos1:channelPos1+channelW]))
    int2[i] = sum(sum(frame[:, channelPos2:channelPos2+channelW]))
    print int1[i]
filt1 = signal.medfilt(int1, medFilt)
filt2 = signal.medfilt(int2, medFilt)

peaks1 = int1 - filt1
peaks2 = int2 - filt2

#finds off set to line up traces of each channel
corr = signal.correlate(peaks2, peaks1, 'same')
maxCorr = np.where(corr == max(corr))
offset = maxCorr[0][0]-len(input_images)/2

#identifies peaks
stdev = np.std(peaks1)
peakLoc1 = signal.find_peaks(peaks1, stdev, None, 20, None)
peakLoc2 = signal.find_peaks(peaks2, stdev, None, 20, None)


filenameprefix = os.path.splitext(filename)[0]
with open(filenameprefix+'/'+filename +'intensity.csv', 'wb') as csvfile:
    wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
    wr.writerows(zip(*[['raw Int 1'], ['raw Int2'], ['median filter1'], ['median filter 2'], ['filtered Int 1'], ['filtered Int 2']]))
    wr.writerows(zip(*[int1, int2, filt1, filt2, peaks1, peaks2]))

####plots####
fig1 = plt.figure(1)
plt.plot(times, int1)
plt.plot(times, int2)

fig2 = plt.figure(2)
plt.plot(times, filt1)
plt.plot(times, filt2)

fig3 = plt.figure(3)
plt.plot(times, peaks1)
plt.plot(times, peaks2)

fig4 = plt.figure(4)
plt.plot(times, peaks1+max(peaks2))
plt.plot(times - offset*timeStep, peaks2)

fig5 = plt.figure(5)
plt.plot(times, peaks1)
plt.plot(times - offset*timeStep, peaks2)

eventFig1 = plt.figure(6)
for i in range(len(peakLoc1[0])):
    sub = eventFig1.add_subplot(1, len(peakLoc1[0]), i + 1)
    sub.imshow(input_images[peakLoc1[0][i]], interpolation='nearest')

eventFig2 = plt.figure(7)
for i in range(len(peakLoc2[0])):
    sub = eventFig2.add_subplot(1, len(peakLoc2[0]), i + 1)
    sub.imshow(input_images[peakLoc2[0][i]], interpolation='nearest')
plt.show()

        #io.imsave(filename + '.output.tif',im_out)

#    if args.normalise :
#        overall_median = bn.nanmedian(im_out, axis=0)
#        im_out = np.float32(im_out / overall_median)
        #print "overall_median", overall_median
