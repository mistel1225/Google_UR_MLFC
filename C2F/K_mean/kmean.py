from nltk import cluster
from nltk.cluster import euclidean_distance, cosine_distance
import pandas as pd
import numpy as np

#df = pd.read_csv('BP.csv')
#print(df['embedding'])
#_ = df['embedding'].to_numpy(dtype=pd.arrays.FloatingArray)
file_list = ['Battery and Power', 'Camera', 'Connectivity, Network, Bluetooth', 'Contacts, Calls, Voicemail', 'Google Assistant and Voice Actions']

for f in file_list:
    _ = np.load(f+'.npy')
    #print(type(_[0]))
    
    clusterer = cluster.KMeansClusterer(5, cosine_distance, repeats=35)
    #clusterer = cluster.KMeansClusterer(3, euclidean_distance, repeats=35)
    clusters = clusterer.cluster(_, True, trace=True)
    #print(clusterer.means())
    #np.save('BP_means.npy', clusterer.means())
    np.save(f+'_clusters.npy', clusters)
'''
for v in _:
    print(clusterer.classify(v))
'''
