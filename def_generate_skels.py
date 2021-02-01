from biologicalgraphs.transforms import seg2seg
from biologicalgraphs.skeletonization import generate_skeletons
from biologicalgraphs.utilities import dataIO
from biologicalgraphs.utilities.dataIO import ReadSkeletons

import pickle
import os
import h5py
import numpy as np

"""
    prefix (type string) 
	-> corresponds to the name of dataset, a meta file is created as meta/{PREFIX}.meta
    output_file_path (type string)
	-> the path to the file where the skeletons are to be stored
    segmentation_file_path (type string)
	-> complete path to the segmentation file (file must be in .h5 format)
    resolution (type array)
	-> array of size 3 having resolution(in nm) of segmentation
"""

def generate_skels(prefix, output_file_path, segmentation_file_path, resolution):
 
    if not os.path.exists("../meta"):
        os.mkdir("../meta")

    meta_path = "../meta/" + prefix + ".meta"

    segmentation = dataIO.ReadH5File(segmentation_file_path, "main").astype(np.int64)

    grid = [len(segmentation), len(segmentation[0]), len(segmentation[0][0])]
	
    with open(meta_path, "w") as meta_file:
        meta_file.write("# resolution in nm\n")
        meta_file.write(f"{resolution[0]}x{resolution[1]}x{resolution[2]}\n")
        meta_file.write("# segmentation filename\n")
        meta_file.write(f"{segmentation_file_path} main\n")
        meta_file.write("# grid size\n")
        meta_file.write(f"{grid[0]}x{grid[1]}x{grid[2]}\n")

    seg2seg.DownsampleMapping(prefix, segmentation)
    generate_skeletons.TopologicalThinning(prefix, segmentation)
    generate_skeletons.FindEndpointVectors(prefix)
    skeletons = ReadSkeletons(prefix)
    
    with open(output_file_path, 'wb') as fp:
        pickle.dump(skeletons, fp)
