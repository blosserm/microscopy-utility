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
from loci.plugins import BF
from loci.common import Region
from loci.plugins.in import ImporterOptions
from ij.io import FileSaver

sliceNumber = 195328

#imageName = sys.argv[1]
# Get currently selected image
#imp = WindowManager.getCurrentImage()
#imageName = '/Users/Matt/Documents/python/imageJ/scripts/testTrack.tif'
#imageName = '/Users/Matt/Documents/Data/2017-01-17_1-1_DiPhyPC_DPPC_OldGUV/A_1-1_DipHyPC-DPPC_133_0/A_1-1_DipHyPC-DPPC_133_0_040101_frame0.tif'
#imageName = '/Users/Matt/Documents/Data/temp/processing/scratch100us_Cam_17706_Cine8.cine.10.output.tif'
#imageName = '/Users/Matt/Documents/Data/2018-01-17_DiPhyPC-DPPC-Chol_glass_40nmAu/C_6k_samePlace/1-1-1_DiPhyPC-DPPC-Chol_40nmAu_6k_Cam_17706_Cine1.cine.2.output.tif'
#imageName = '/Users/Matt/Documents/Data/2018-01-17_DiPhyPC-DPPC-Chol_glass_40nmAu/testTrack.tif'
#imageName = '/Volumes/Matt ext HD/2018-02-06_tieLineGUV_oldSplat_longIncubation/B_tielineGUV_fluor1041and1043_Ld/B_tielineGUV_fluor1041and1043_Ld_Cam_17706_Cine1.cine.1.outputhalf1.tif'
#imageName = 'http://fiji.sc/samples/FakeTracks.tif'
#imp = opener.openImage(imageName)
imageName = sys.argv[1]

newName1 = imageName.replace('.tif', 'Half1.tif')
newName2 = imageName.replace('.tif', 'Half2.tif')
options = ImporterOptions()
options.setWindowless(True);

options.setColorMode(ImporterOptions.COLOR_MODE_GRAYSCALE)

#options.setCBegin(0, 1); 
#options.setZBegin(0, 2); 
options.setTBegin(0, 0); 
#options.setCEnd(0, 4); 
#options.setZEnd(0, 5); 
options.setTEnd(0, sliceNumber/2); 

options.setSpecifyRanges(True)
#options.setCropRegion(0, Region(7, 8, 9, 10))
#options.setCrop(True)



options.setId(imageName)
imps = BF.openImagePlus(options)


for imp in imps:
    #imp.show()
	fs = FileSaver(imp)
	fs.saveAsTiff(newName1)

options.setTBegin(0, sliceNumber/2+1); 
#options.setCEnd(0, 4); 
#options.setZEnd(0, 5); 
options.setTEnd(0, sliceNumber-1); 
imps = BF.openImagePlus(options)
for imp in imps:
    #imp.show()
	fs = FileSaver(imp)
	fs.saveAsTiff(newName2)

#Swith the z and t dimensions, which you apparently always need to do.

#IJ.run(imp,"Duplicate...", "duplicate range=1")
#Invert the image, for tracking dark features
#IJ.run(imp, "Stack Splitter", "number=2")

#IJ.run(imp,"Slice Keeper", "first=1 last=50 increment=1");
#IJ.run("Bio-Formats (Windowless)", "open=[/Volumes/Matt ext HD/2018-02-06_tieLineGUV_oldSplat_longIncubation/B_tielineGUV_fluor1041and1043_Ld/B_tielineGUV_fluor1041and1043_Ld_Cam_17706_Cine1.cine.1.output.tif] color_mode=Default rois_import=[ROI manager] specify_range view=Hyperstack stack_order=XYCZT t_begin=1 t_end=20 t_step=1");
