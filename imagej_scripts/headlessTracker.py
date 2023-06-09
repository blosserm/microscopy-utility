from fiji.plugin.trackmate import Model
from fiji.plugin.trackmate import Settings
from fiji.plugin.trackmate import TrackMate
from fiji.plugin.trackmate import SelectionModel
from fiji.plugin.trackmate import Logger
from fiji.plugin.trackmate.detection import LogDetectorFactory
from fiji.plugin.trackmate.detection import DogDetectorFactory
from fiji.plugin.trackmate.tracking.sparselap import SparseLAPTrackerFactory
from fiji.plugin.trackmate.tracking import LAPUtils
from ij import IJ
import fiji.plugin.trackmate.visualization.hyperstack.HyperStackDisplayer as HyperStackDisplayer
import fiji.plugin.trackmate.features.FeatureFilter as FeatureFilter
import sys
import fiji.plugin.trackmate.features.track.TrackDurationAnalyzer as TrackDurationAnalyzer
from ij.io import Opener
from ij import WindowManager
import fiji.plugin.trackmate.action.ExportTracksToXML as ExportTracksToXML
import fiji.plugin.trackmate.io.TmXmlWriter as TmXmlWriter
from java.io import File

opener = Opener()

imageName = sys.argv[1]
# Get currently selected image
#imp = WindowManager.getCurrentImage()
#imageName = '/Users/Matt/Documents/python/imageJ/scripts/testTrack.tif'
#imageName = '/Users/Matt/Documents/Data/2017-01-17_1-1_DiPhyPC_DPPC_OldGUV/A_1-1_DipHyPC-DPPC_133_0/A_1-1_DipHyPC-DPPC_133_0_040101_frame0.tif'
#imageName = '/Users/Matt/Documents/Data/temp/processing/scratch100us_Cam_17706_Cine8.cine.10.output.tif'
#imageName = '/Users/Matt/Documents/Data/2018-01-17_DiPhyPC-DPPC-Chol_glass_40nmAu/C_6k_samePlace/1-1-1_DiPhyPC-DPPC-Chol_40nmAu_6k_Cam_17706_Cine1.cine.2.output.tif'
#imageName = '/Users/Matt/Documents/Data/2018-01-17_DiPhyPC-DPPC-Chol_glass_40nmAu/testTrack.tif'
#imageName = 'http://fiji.sc/samples/FakeTracks.tif'
imp = opener.openImage(imageName)


#Swith the z and t dimensions, which you apparently always need to do.
dims = imp.getDimensions();
imp.setDimensions( dims[ 2 ], dims[ 4 ], dims[ 3 ] );
IJ.run(imp, "Bin...", "x=2 y=2 z=1 bin=Average");
#IJ.run(imp,"Duplicate...", "duplicate range=1")
#Invert the image, for tracking dark features
#IJ.run(imp, "Invert", "stack")

#imp.show()
#----------------------------
# Create the model object now
#----------------------------
    
# Some of the parameters we configure below need to have
# a reference to the model at creation. So we create an
# empty model now.
   
model = Model()
    
# Send all messages to ImageJ log window.
model.setLogger(Logger.IJ_LOGGER)
    
    
       
#------------------------
# Prepare settings object
#------------------------
       
settings = Settings()
settings.setFrom(imp)
##########################
##CHANGE STUFF HERE
#
#nb, all values must have a decimal point, to be interpreted as doubles
#
#
#****************************SPOT DETECTION SETTINGS HERE****************************
# Configure detector - We use the Strings for the keys
settings.detectorFactory = LogDetectorFactory()
settings.detectorSettings = { 
    'DO_SUBPIXEL_LOCALIZATION' : True,
    'RADIUS' : 3.0,
    'TARGET_CHANNEL' : 1,
    'THRESHOLD' : 0.005,
    'DO_MEDIAN_FILTERING' : False,
}  
    
# ****************************FILTER SPOT HERE****************************
#Configure spot filters - Classical filter on quality
#filter1 = FeatureFilter('QUALITY', 0.004, True)
#settings.addSpotFilter(filter1)
filterX1 = FeatureFilter('POSITION_X', 2, True)
settings.addSpotFilter(filterX1)

filterX2 = FeatureFilter('POSITION_X', 30, False)
settings.addSpotFilter(filterX2)

filterY1 = FeatureFilter('POSITION_Y', 2, True)
settings.addSpotFilter(filterY1)

filterY2 = FeatureFilter('POSITION_Y', 30, False)
settings.addSpotFilter(filterY2)
     
# Configure tracker - We want to allow merges and fusions
settings.trackerFactory = SparseLAPTrackerFactory()
settings.trackerSettings = LAPUtils.getDefaultLAPSettingsMap() # almost good enough
settings.trackerSettings['ALLOW_TRACK_SPLITTING'] = False
settings.trackerSettings['ALLOW_TRACK_MERGING'] = False
    
# Configure track analyzers - Later on we want to filter out tracks 
# based on their displacement, so we need to state that we want 
# track displacement to be calculated. By default, out of the GUI, 
# not features are calculated. 
settings.trackerFactory = SparseLAPTrackerFactory()
#settings.trackerSettings = LAPUtils.getDefaultLAPSettingsMap()
#****************************TRACK SETTINGS HERE****************************
settings.trackerSettings['LINKING_MAX_DISTANCE'] = 5.0
settings.trackerSettings['GAP_CLOSING_MAX_DISTANCE']=5.0
settings.trackerSettings['MAX_FRAME_GAP']= 1
# The displacement feature is provided by the TrackDurationAnalyzer.
#****************************TRACK FILTER HERE****************************    
settings.addTrackAnalyzer(TrackDurationAnalyzer())
filter2 = FeatureFilter('TRACK_DURATION', 1000, True)
#filter2 = FeatureFilter('NUM_SPOTS', 1000, True)
settings.addTrackFilter(filter2)
    
# Configure track filters - We want to get rid of the two immobile spots at 
# the bottom right of the image. Track displacement must be above 10 pixels.
    
#filter2 = FeatureFilter('TRACK_DISPLACEMENT', 10, True)
#settings.addTrackFilter(filter2)
    
    
#-------------------
# Instantiate plugin
#-------------------
    
trackmate = TrackMate(model, settings)
       
#--------
# Process
#--------
    
ok = trackmate.checkInput()
if not ok:
    sys.exit(str(trackmate.getErrorMessage()))
    
ok = trackmate.process()
if not ok:
    sys.exit(str(trackmate.getErrorMessage()))
    
       
#----------------
# Display results
#----------------
     
selectionModel = SelectionModel(model)
#displayer =  HyperStackDisplayer(model, selectionModel, imp)
#displayer.render()
#displayer.refresh()
    
# Echo results with the logger we set at start:
model.getLogger().log(str(model))

#outFilename = 'eagqreagfargAutoXML.XML'
outFilename = imageName.replace('.tif', '.xml')
#outputFolder = '/Users/Matt/Documents/Data/2018-01-17_DiPhyPC-DPPC-Chol_glass_40nmAu/'
print(outFilename)
#outFile =  File(outputFolder, outFilename)
outFile =  File(outFilename)
#outfile = File(imp, trackmate)
ExportTracksToXML.export(model, settings, outFile)
print('hello!')
#ExportTracksToXML.export(model, settings, outFile)
#Make a copy of the first frame, and close everything else
IJ.run(imp,"Duplicate...", "duplicate range=1-1")
imp.changes = False
imp.close()
