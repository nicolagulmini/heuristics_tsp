import networkx as nx
import random
random.seed(3)

def complete_graph_generator(number_of_nodes):
    n = number_of_nodes
    g = nx.Graph()
    g.add_nodes_from(list(range(1, n+1)))
    for u in g.nodes: 
        for v in g.nodes:
            if u != v:
                tmp = random.randint(1, 10)
                g.add_edge(u, v, weight=tmp)
    print('Graph with', g.number_of_nodes(), 'nodes and', g.number_of_edges(), 'edges successfully created.')
    nx.draw_spring(g, with_labels=True)
    return g

def check(number, list_of_numbers):
    for el in list_of_numbers:
        if number == el:
            return True
    return False

def nearest_neighbor_tour(graph):
    n = graph.number_of_nodes()
    if n == 0:
        print('Empty graph.')
        return
    if n == 1:
        print('Graph is a single node.')
        return
    best_tour = []
    best_cost = n*11
    for i in range(1, n+1):
        already_vis = [i]
        total_cost = 0
        while len(already_vis) < n:
            node = already_vis[len(already_vis)-1]
            best_weight = 11
            best_node = node
            for neighbor in graph.neighbors(node):
                tmp_node = neighbor
                if not check(tmp_node, already_vis):
                    tmp_weight = graph[node][tmp_node]['weight']
                    if tmp_weight <= best_weight:
                        best_weight = tmp_weight
                        best_node = tmp_node
            already_vis.append(best_node)
            total_cost += best_weight
        total_cost += graph[already_vis[len(already_vis)-1]][i]['weight'] # cost to return at the first node
        if total_cost <= best_cost:
            best_cost = total_cost
            best_tour = already_vis
    return best_tour, best_cost

def factorial(n):
    ret = 1
    for i in range(n):
        ret *= n-i
    return ret
    
# ----------------------------------------------------------------------------

def fit(cand, graph): # tour cost
    fitness_function = 0
    n = graph.number_of_nodes()
    if n != len(cand):
        print('Errore')
    for i in range(n-1):
        fitness_function += graph[cand[i]][cand[i+1]]['weight']
    fitness_function += graph[cand[n-1]][cand[0]]['weight']
    return fitness_function

def print_pop(pop):
    for ind in pop:
        print(ind)

def probabilities(pop, graph):
    size_of_a_member = len(pop[0])
    n = graph.number_of_nodes()
    if n != size_of_a_member:
        print('Errore')
    members = len(pop)
    tmp = []
    pro = []
    s = 0
    for cand in pop:
        tmp_fit = 11*(n+1) - fit(cand, graph) # since a good fit is small, take how much it is far from the max
        tmp.append(tmp_fit)
        s += tmp_fit
    if s == 0:
        ret = []
        for i in range(n):
            ret.append(1/members)
        return ret
    for el in tmp:
        pro.append(el/s)
    return pro
        
def initialize_population(members, size_of_a_member): # generate a random tour
    pop = []
    for i in range(members):
        tmp_member = []
        tmp_list = list(range(1, size_of_a_member+1))
        for j in range(size_of_a_member):
            tmp = random.choice(list(range(len(tmp_list))))
            el = tmp_list.pop(tmp)
            tmp_member.append(el)
        pop.append(tmp_member)
    return pop

def selection(pop, pro):
    members = len(pop)
    return random.choices(population=pop, weights=pro, k=members)

def control_and_return(pop, graph, ref_cost):
    epsilon = 1
    for el in pop:
        fit_value = fit(el, graph)
        if fit_value <= ref_cost - epsilon:
            return True, fit_value
    return False, fit_value

def find_two_maximal_pos(lista, graph):
    pos_1, pos_2, w1, w2, arr_1, arr_2 = 0, 0, 0, 0, 0, 0
    last_pos = len(lista)-1
    for i in range(len(lista)-1):
        tmp_node = lista[i]
        tmp_side = lista[i+1]
        tmp_w = graph[tmp_node][tmp_side]['weight']
        if tmp_w > w1:
            w1 = tmp_w
            pos_1 = i
            arr_1 = i+1
    out_tmp_w = graph[lista[last_pos]][lista[0]]['weight']
    if out_tmp_w > w1: # check the last
        w1 = out_tmp_w
        pos_1 = last_pos
        arr_1 = 0
    for i in range(len(lista)-1):
        if i != pos_1-1 and i != pos_1 and i != pos_1+1 and i != arr_1:
            tmp_node = lista[i]
            tmp_side = lista[i+1]
            tmp_w = graph[tmp_node][tmp_side]['weight']
            if tmp_w > w2:
                w2 = tmp_w
                pos_2 = i
                arr_2 = i+1
    if out_tmp_w > w2: # check the last
        if last_pos != pos_1-1 and last_pos != pos_1 and last_pos != pos_1+1 and pos_1 != 0:
            w2 = tmp_w
            pos_2 = last_pos
            arr_2 = 0
    return pos_1, pos_2, arr_1, arr_2

def single_swap_improve(pop, graph):
    new_pop = []
    for mem in pop:
        new_mem = []
        pos_1, pos_2, arr_1, arr_2 = find_two_maximal_pos(mem, graph)
        node_1 = mem[pos_1]
        side_1 = mem[arr_1]
        node_2 = mem[pos_2]
        side_2 = mem[arr_2]
        normal = graph[node_1][side_1]['weight']+graph[node_2][side_2]['weight']
        quad = graph[node_1][node_2]['weight']+graph[side_1][side_2]['weight']
        cross = graph[node_1][side_2]['weight']+graph[node_2][side_1]['weight']
        if quad < normal:
            if quad < cross: # do a quad configuration member
                for i in range(len(mem)):
                    if i == arr_1:
                        new_mem.append(mem[pos_2])
                    elif i == pos_2:
                        new_mem.append(mem[arr_1])
                    else:
                        new_mem.append(mem[i])
            else: # do a cross configuration member
                for i in range(len(mem)):
                    if i == arr_1:
                        new_mem.append(mem[arr_2])
                    elif i == arr_2:
                        new_mem.append(mem[arr_1])
                    else:
                        new_mem.append(mem[i])
        elif cross < normal: # cross
            for i in range(len(mem)):
                    if i == arr_1:
                        new_mem.append(mem[arr_2])
                    elif i == arr_2:
                        new_mem.append(mem[arr_1])
                    else:
                        new_mem.append(mem[i])
        else: # otherwise do not touch
            new_mem = mem
        new_pop.append(new_mem)
    return new_pop

def random_mutation(pop):
    new_pop = []
    number_of_nodes = len(pop[0])
    for el in pop:
        new_el = []
        first_pos = random.choice(list(range(number_of_nodes)))
        second_pos = random.choice(list(range(number_of_nodes)))
        for i in range(len(el)):
            if i == first_pos:
                new_el.append(el[second_pos])
            elif i == second_pos:
                new_el.append(el[first_pos])
            else:
                new_el.append(el[i])
        new_pop.append(new_el)
    return new_pop
        
def genetic(graph, members, ref_cost):
    n = graph.number_of_nodes()
    # cross takes an even number of members
    if members % 2 != 0:
        members += 1
    population = initialize_population(members, n) # members, size_of_a_member
    cont = 0
    cond = True
    while cond:
        cont += 1
        prob = probabilities(population, graph)
        population = selection(population, prob)
        population = single_swap_improve(population, graph) # recombine edges to obtain a lower cost
        population = random_mutation(population)

        if cont % 50000 == 0:
            print()
            print_pop(population)
        condition_to_stop, a_fit_value = control_and_return(population, graph, ref_cost)
        if condition_to_stop:
            print('\nReached a good solution in', cont, 'iterations')
            print_pop(population)
            print('cost of the solution:', a_fit_value)
            cond = False
        elif cont >= 1000000:
            print('\nToo much iterations. Return the current solution.')
            print_pop(population)
            print('cost of the solution:', a_fit_value)
            cond = False