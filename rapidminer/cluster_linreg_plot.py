import analyse

kmeans = analyse.analyze('output/kmeans_cluster_data')
kmedoids = analyse.analyze('output/kmedoids_cluster_data')
dbscans = analyse.analyze('output/dbscan_cluster_data')

def cluster_plot(x, title, col='bo'):
    plt.close()
    plt.title(title)
    plt.xlabel('Content score')
    plt.ylabel('PageRank')
    x1 = x[0].min() - 0.05
    x2 = x[0].max() + 0.05
    y1 = x[1].min() - 0.05
    y2 = x[1].max() + 0.05
    plt.axis([x1, x2, y1, y2])
    plot(x[0], x[1], col)

# Do this for each cluster
x = np.array([-10, 10])
cluster_plot(dbscans, 'DBSCAN')
l = scipy.stats.linregress(dbscans[0], dbscans[1])
y = x * l[0] + l[1]
plot(x, y, 'r')