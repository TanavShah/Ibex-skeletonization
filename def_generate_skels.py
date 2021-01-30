from biologicalgraphs.transforms import seg2seg
from biologicalgraphs.skeletonization import generate_skeletons
from biologicalgraphs.utilities import dataIO
from biologicalgraphs.utilities.dataIO import ReadSkeletons

import pickle

"""
  the prefix name corresponds to the meta file in meta/{PREFIX}.meta
  output_file_path is the path to the file where the skeletons are stored
"""

def generate_skels(prefix, output_file_path):

#   read the input segmentation data
    segmentation = dataIO.ReadSegmentationData(prefix)

    seg2seg.DownsampleMapping(prefix, segmentation)
    generate_skeletons.TopologicalThinning(prefix, segmentation)
    generate_skeletons.FindEndpointVectors(prefix)
    skeletons = ReadSkeletons(prefix)

    with open(output_file_path, 'wb') as fp:
        pickle.dump(skeletons, fp)
