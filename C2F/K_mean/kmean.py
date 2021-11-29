from nltk import cluster
from nltk.cluster import euclidean_distance, cosine_distance
import pandas as pd
import numpy as np

#df = pd.read_csv('BP.csv')
#print(df['embedding'])
#_ = df['embedding'].to_numpy(dtype=pd.arrays.FloatingArray)
_ = np.load('BP.npy')
#print(type(_[0]))

clusterer = cluster.KMeansClusterer(3, cosine_distance, repeats=5)
#clusterer = cluster.KMeansClusterer(3, euclidean_distance)
clusters = clusterer.cluster(_, True, trace=True)
print(clusterer.means())
np.save('BP_means.npy', clusterer.means())
np.save('BP_clurters.npy', clusters)
'''
for v in _:
    print(clusterer.classify(v))
'''
