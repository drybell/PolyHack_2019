import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn import preprocessing
from matplotlib import pyplot as plt


X_df = pd.read_csv('test3.csv')
new_df = X_df[['links', 'month', 'day', 'time']].copy()
months = {
		  'Jan': 1,
		  'Feb': 2,
		  'Mar': 3,
		  'Apr': 4,
		  'May': 5,
		  'Jun': 6,
		  'Jul': 7,
		  'Aug': 8,
		  'Sep': 9,
		  'Oct': 10,
		  'Nov': 11,
		  'Dec': 12,
		 }
new_month_col = []
for mon in new_df['month']:
	new_month_col.append(months[mon])

m_df = pd.DataFrame({'month_num': new_month_col})
new_df = pd.concat([new_df, m_df], axis=1)
new_df.drop(['month'],axis=1, inplace=True)


# distortions = []
# for i in range(1, 11):
#     km = KMeans(
#         n_clusters=i, init='random',
#         n_init=10, max_iter=300,
#         tol=1e-04, random_state=0
#     )
#     km.fit(new_df)
#     distortions.append(km.inertia_)

# #plot
# plt.plot(range(1, 11), distortions, marker='o')
# plt.xlabel('Number of clusters')
# plt.ylabel('Distortion')
# plt.show()
# exit(1)
clusters = 5 #CHANGE THIS 


km = KMeans(
    n_clusters=clusters, init='random',
    n_init=10, max_iter=300, 
    tol=1e-04, random_state=0
)
y_km = km.fit_predict(new_df)
y_df = pd.DataFrame({'Cluster': y_km})
X_df = pd.concat([X_df, y_df], axis=1)
X = new_df['links']
Y = new_df['time']

plt.scatter(
    X[y_km == 0], Y[y_km == 0],
    label='cluster 1'
)

plt.scatter(
    X[y_km == 1], Y[y_km == 1],
    label='cluster 2'
)

plt.scatter(
    X[y_km == 2], Y[y_km == 2],
    label='cluster 3'
)

plt.scatter(
    X[y_km == 3], Y[y_km == 3],
    label='cluster 4'
)

plt.scatter(
    X[y_km == 4], Y[y_km == 4],
    label='cluster 5'
)



# for row in X_np[y_km==3]:
# 	print(row)
# plt.legend()
# plt.grid()
# plt.show()


