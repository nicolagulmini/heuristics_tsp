import networkx as nx

# tutorial networkx

# crate an empty graph
g = nx.Graph()

# add single not connected nodes
g.add_nodes_from([1, 2, 3, 4])

# add weighted edges betwee nodes, given the weights
g.add_weighted_edges_from([(1, 2, 1), (1, 3, 2), (2, 3, .2)])

# tuple as an edge
e = (1, 4)

# add an edge with a weight
g.add_edge(*e, weight=.4)

# display the graph
nx.draw_spring(g, with_labels=True)

# save the figure
#plt.savefig('name.png')
#plt.clf()

# print the number of nodes and the number of edges
print('number of edges:', g.number_of_edges())
print('number of nodes:', g.number_of_nodes())

# take the nodes and edges lists and display them
nodes = list(g.nodes)
edges = list(g.edges)
print('nodes:', nodes)
print('edges:', edges)

print('\nWeights:')
edges = g.edges.data('weight')
print('Weighted edges:', edges)
print('The connection between nodes are:')
for e in nodes:
    neighbors = list(g.neighbors(e))
    print('neighbors of node', e, 'are', neighbors)