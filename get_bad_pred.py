import h5py
import numpy as np
from tqdm import tqdm
import cc3d

f = h5py.File('seg_64nm.h5', 'r')
print("Layers: %s" % f.keys())

dset = f['main']
print(dset.shape)

n1 = np.array(dset)

indices = np.random.randint(374, size=(5))
cnt = 0


for i in tqdm(range(len(indices))):
    for j in range(dset.shape[1]):
        for k in range(dset.shape[2]):
	    n1[indices[i]][j][k] = 0
	    cnt += 1

print(cnt)

connectivity = 26 # only 4,8 (2D) and 26, 18, and 6 (3D) are allowed
labels_out, N = cc3d.connected_components(n1, connectivity=connectivity, return_N=True)
print(N)
print(labels_out.shape)
