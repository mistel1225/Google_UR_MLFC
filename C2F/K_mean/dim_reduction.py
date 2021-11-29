from sklearn import manifold
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
data = np.load('BP.npy')
#means = np.load('BP_means.npy')
clusters = np.load('BP_clusters.npy')
print(clusters)
#print(means)
data_tsne = manifold.TSNE(n_components=2, init='random', random_state=15, verbose=1).fit_transform(data)
#print(data_tsne)
data_tsne_x = [i[0] for i in data_tsne]
data_tsne_y = [i[1] for i in data_tsne]
print(data_tsne_x[0])
print(data_tsne_y[0])
print(data_tsne)
df = pd.DataFrame(dict(x=data_tsne_x, y=data_tsne_y, label=clusters))
groups = df.groupby('label')

fig, ax = plt.subplots()
ax.margins(0.05)
for name, group in groups:
    ax.plot(group.x, group.y, marker='o', linestyle='', ms=3, label=name)
ax.legend()
plt.savefig('BP.png')
