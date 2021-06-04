import utils

def main():
    g = utils.complete_graph_generator(18)
    best_tour, nearest_cost = utils.nearest_neighbor_tour(g)
    print('Target sequence:', best_tour)
    print('cost of the solution:', nearest_cost)
    utils.genetic(g, 4, nearest_cost)

main()

# todo:
# - ant colony optimization
# - parser for instances of tsplib
# - plot performance