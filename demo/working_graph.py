import plotly.plotly as py
import plotly.graph_objs as go
import igraph as ig
import convert_to_dict as cd
import csv
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn import preprocessing



group = cd.determine_values("dict_test.txt")
data = cd.convert_to_dict(group)



# THIS IS MACHINE LEARNING
X_df = pd.read_csv('files.csv')

new_df = X_df[['links', 'month', 'time']].copy()
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

clusters = 3

km = KMeans(
    n_clusters=clusters, init='random',
    n_init=10, max_iter=300, 
    tol=1e-04, random_state=0
)
y_km = km.fit_predict(new_df)
y_df = pd.DataFrame({'Cluster': y_km})
X_df = pd.concat([X_df, y_df], axis=1)




for i in range(len(X_df['name'])):
    node_list = data['nodes']
    for node in node_list:
        if X_df.iloc[i]['name'] == node['name']:
            node['cluster'] = X_df.iloc[i]['Cluster']
print(data['nodes'])
# for node in data['nodes']:
#     print(node)

# for node_list in data['nodes']:
#     row = X_df.loc[X_df['name'] == node_list['name']]


# THIS IS THE END OF MACHINE LEARNIKNG



N=len(data['nodes'])
L=len(data['links'])
Edges=[(data['links'][k]['source'], data['links'][k]['target']) for k in range(L)]

G=ig.Graph(Edges, directed=False)

labels=[]
group=[]
cluster=[]
path=[]
for node in data['nodes']:
    labels.append(node['name'])
    group.append(node['group'])
    cluster.append(node['cluster'])
    # path.append(node['path'])

layt=G.layout('kk', dim=3)

Xn=[layt[k][0] for k in range(N)]# x-coordinates of nodes
Yn=[layt[k][1] for k in range(N)]# y-coordinates
Zn=[layt[k][2] for k in range(N)]# z-coordinates
Xe=[]
Ye=[]
Ze=[]
for e in Edges:
    Xe+=[layt[e[0]][0],layt[e[1]][0], None]# x-coordinates of edge ends
    Ye+=[layt[e[0]][1],layt[e[1]][1], None]
    Ze+=[layt[e[0]][2],layt[e[1]][2], None]

trace1=go.Scatter3d(x=Xe,
               y=Ye,
               z=Ze,
               mode='lines',
               line=dict(color='rgb(250,250,250)', width=2),
               hoverinfo='none',
               )

trace2=go.Scatter3d(x=Xn,
               y=Yn,
               z=Zn,
               mode='markers+text',
               name='files',
               marker=dict(symbol=group,
                             size=4,
                             color=cluster,
                             colorscale=[[0, 'rgb(250,250,250)'], [0.1, 'rgb(255,255,0)'], [1, 'rgb(255,0,0)']],
                             line=dict(color='rgb(50,50,50)', width=0.5)
                             ),
               text=labels,
               textposition="bottom center",
               textfont=dict(color='rgb(250,250,250)', size=10),
               hovertext=path,
               hoverinfo='text'
               )

axis=dict(showbackground=False,
          showline=False,
          zeroline=False,
          showgrid=False,
          showticklabels=False,
          title=''
          )

layout = go.Layout(
         title="/Desktop/Comp",
         template="plotly_dark",
         width=1000,
         height=1000,
         showlegend=False,
         scene=dict(
             xaxis=dict(axis),
             yaxis=dict(axis),
             zaxis=dict(axis),
        ),
     margin=dict(
        t=100
    ),
    hovermode='closest',
    annotations=[
           dict(
           showarrow=False,
            text="Data source: <a href='http://bost.ocks.org/mike/miserables/miserables.json'>[1] miserables.json</a>",
            xref='paper',
            yref='paper',
            x=0,
            y=0.1,
            xanchor='left',
            yanchor='bottom',
            font=dict(
            size=14
            )
            )
        ],    )


data=[trace1, trace2]
fig=go.Figure(data=data, layout=layout)



fig.write_html('first_figure.html', auto_open=True)
