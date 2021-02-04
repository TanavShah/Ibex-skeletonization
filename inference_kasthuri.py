from biologicalgraphs.utilities import dataIO
from biologicalgraphs.graphs.biological import node_generation, edge_generation
from biologicalgraphs.evaluation import comparestacks
#from biologicalgraphs.cnns.biological import nodes, edges
from biologicalgraphs.cnns.biological.nodes import forward
#from biologicalgraphs.cnns.biological.edges import forward
from biologicalgraphs.transforms import seg2seg, seg2gold
from biologicalgraphs.skeletonization import generate_skeletons
from biologicalgraphs.algorithms import lifted_multicut



# the prefix name corresponds to the meta file in meta/{PREFIX}.meta
prefix = 'Kasthuri-test'

# read the ground truth for this data
gold = dataIO.ReadGoldData(prefix)

# read the input segmentation data
segmentation = dataIO.ReadSegmentationData(prefix)

# subset is either training, validation, or testing
subset = 'testing'

# remove the singleton slices
node_generation.RemoveSingletons(prefix, segmentation)
print("Step 1 done")
# need to update the prefix and segmentation
# removesingletons writes a new h5 file to disk
prefix = '{}-segmentation-wos'.format(prefix)
segmentation = dataIO.ReadSegmentationData(prefix)
# need to rerun seg2gold mapping since segmentation changed
seg2gold_mapping = seg2gold.Mapping(prefix, segmentation, gold)
print("Step 2 done")

# generate locations for segments that are too small
node_generation.GenerateNodes(prefix, segmentation, subset, seg2gold_mapping)
print("Step 3 done")

# run inference for node network
node_model_prefix = '/n/home03/tanav/axonem/biologicalgraphs/neuronseg/architectures/nodes-400nm-3x20x60x60-Kasthuri/nodes'
forward.Forward(prefix, node_model_prefix, segmentation, subset, seg2gold_mapping, evaluate=True)

print("Step 4 done")
"""
edge_generation.GenerateEdges(prefix, segmentation, subset, seg2gold_mapping)
print("Step 5 done")
# run inference for edge network
edge_model_prefix = '/n/home03/tanav/axonem/biologicalgraphs/neuronse/garchitectures/edges-600nm-3x18x52x52-Kasthuri/edges'
forward.Forward(prefix, edge_model_prefix, subset)
"""
print("Step 6 done")
