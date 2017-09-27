###################
###################
## Problem Set 5 ##
###################
###################

################
## Question 1 ##
################


# Write code that can implement the dijkstra algorithm using heaps

# the dijkstra algorithm finds the minimum weighted distance from one node in a graph
# to all other nodes in the graph.  My approach to this problem uses 3 main data
# structures to keep track of nodes in the graph, their current distance from the main node,
# and their location in the heap:

    # 1. a heap that contains just nodes
    # 2. a location dict that has the nodes as keys and the locations in the heap as values
    # 3. the distance so far dictionary that has the nodes as keys and their current distance as value


def parent(i):
    return (i-1)/2
def left_child(i):
    return 2*i+1
def right_child(i):
    return 2*i+2
def is_leaf(L,i):
    return (left_child(i) >= len(L)) and (right_child(i) >= len(L))
def one_child(L,i):
    return (left_child(i) < len(L)) and (right_child(i) >= len(L))

def swap_items(heap, old, new, location_dict):
    location_dict[heap[old]] = new
    location_dict[heap[new]] = old
    (heap[old], heap[new]) = (heap[new], heap[old])

def down_heapify(L, i, location_dict, value_dict):
    # If i is a leaf, heap property holds
    if is_leaf(L, i):
        return
    # If i has one child...
    if one_child(L, i):
        # check heap property
        if value_dict[L[i]] > value_dict[L[left_child(i)]]:
            # If it fails, swap, fixing i and its child (a leaf)
            # (L[i], L[left_child(i)]) = (L[left_child(i)], L[i])
            swap_items(L, i, left_child(i), location_dict)
        return
    # If i has two children...
    # check heap property
    if min(value_dict[L[left_child(i)]], value_dict[L[right_child(i)]]) >= value_dict[L[i]]:
        return
    # If it fails, see which child is the smaller
    # and swap i's value into that child
    # Afterwards, recurse into that child, which might violate
    if value_dict[L[left_child(i)]] < value_dict[L[right_child(i)]]:
        # Swap into left child
        # (L[i], L[left_child(i)]) = (L[left_child(i)], L[i])
        swap_items(L, i, left_child(i), location_dict)
        down_heapify(L, left_child(i), location_dict, value_dict)
        return
    else:
        # (L[i], L[right_child(i)]) = (L[right_child(i)], L[i])
        swap_items(L, i, right_child(i), location_dict)
        down_heapify(L, right_child(i), location_dict, value_dict)
        return

def up_heapify(L, i, location_dict, value_dict):
    # first case is just if we're done, if the node is the root:
    if i == 0:
        return

    if one_child(L, parent(i)):
        assert L[parent(i)]
        try:
            assert L[i]
        except:
            print L, i, location_dict
            assert L[i]
        if value_dict[L[parent(i)]] > value_dict[L[i]]:
            # (L[parent(i)], L[i]) = (L[i], L[parent(i)])
            swap_items(L, parent(i), i, location_dict)
            up_heapify(L, parent(i), location_dict, value_dict)
            return
        else:
            return

    # if the not one leaf and node we're working with is smaller than the parent, then
    # we swap the min child and up heapify
    if value_dict[L[parent(i)]] <= value_dict[L[i]]:
        return

    if value_dict[L[left_child(parent(i))]] < value_dict[L[right_child(parent(i))]]:
        # (L[parent(i)], L[left_child(parent(i))]) = (L[left_child(parent(i))], L[parent(i)])
        swap_items(L, parent(i), left_child(parent(i)), location_dict)
        up_heapify(L, parent(i), location_dict, value_dict)
        return
    # (L[parent(i)], L[right_child(parent(i))]) = (L[right_child(parent(i))], L[parent(i)])
    swap_items(L, parent(i), right_child(parent(i)), location_dict)
    up_heapify(L, parent(i), location_dict, value_dict)
    return

def dijkstra(G,v):

    dist_so_far_heap = [v]
    dist_so_far_values = {v: 0}
    location_dict = {v: 0}

    final_dist = {}
    while len(final_dist) < len(G):
        # get the minimum node/val pair
        w = dist_so_far_heap[0]
        val = dist_so_far_values[w]

        # remove the min pair from the location dict
        del dist_so_far_heap[0]
        del dist_so_far_values[w]
        del location_dict[w]

        # set the last element of dist_so_far_heap to the first and down heapify
        if len(dist_so_far_heap) > 0:
            dist_so_far_heap.insert(0, dist_so_far_heap.pop(-1))
            location_dict[dist_so_far_heap[0]] = 0
            down_heapify(dist_so_far_heap, 0, location_dict, dist_so_far_values)

        # lock it down!
        final_dist[w] = val

        for x in G[w]:
            if x not in final_dist:
                if x not in dist_so_far_heap:
                    dist_so_far_heap.append(x)
                    # add the new node to the location dictionary
                    location_dict[x] = len(dist_so_far_heap)-1
                    # and add new new distance to the value dictionary
                    dist_so_far_values[x] = final_dist[w] + G[w][x]
                    up_heapify(dist_so_far_heap, len(dist_so_far_heap)-1, location_dict, dist_so_far_values)
                # if x IS in the dist so far heap, we want to see if it's value is higher than the current
                # distance, and if it is update it
                elif dist_so_far_values[x] > final_dist[w] + G[w][x]:
                    dist_so_far_values[x] = final_dist[w] + G[w][x]
                    up_heapify(dist_so_far_heap, location_dict[x], location_dict, dist_so_far_values)
    return final_dist


def make_link(G, node1, node2, w):
    if node1 not in G:
        G[node1] = {}
    if node2 not in G[node1]:
        (G[node1])[node2] = 0
    (G[node1])[node2] += w
    if node2 not in G:
        G[node2] = {}
    if node1 not in G[node2]:
        (G[node2])[node1] = 0
    (G[node2])[node1] += w
    return G

def test():
    # shortcuts
    (a,b,c,d,e,f,g) = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
    triples = ((a,c,3),(c,b,10),(a,b,15),(d,b,9),(a,d,4),(d,f,7),(d,e,3),
               (e,g,1),(e,f,5),(f,g,2),(b,f,1))
    G = {}
    for (i,j,k) in triples:
        make_link(G, i, j, k)

    dist = dijkstra(G, a)
    assert dist[g] == 8 #(a -> d -> e -> g)
    assert dist[b] == 11 #(a -> d -> e -> g -> f -> b)

# test()

################
## Question 1 ##
################

# part 1

# Use your code from earlier to change the Marvel graph to only have characters as nodes.
# Use 1.0/count as the weight, where count is the number of comic books each character
# appeared in together

import pandas as pd
import csv

def make_link_inverse(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
        (G[node1])[node2] = 1
    elif node1 in G:
        if node2 in G[node1]:
            (G[node1])[node2] = 1/((G[node1])[node2]**-1 + 1)
        else:
            (G[node1])[node2] = 1
    if node2 not in G:
        G[node2] = {}
        (G[node2])[node1] = 1
    elif node2 in G:
        if node1 in G[node2]:
            (G[node2])[node1] = 1/((G[node2])[node1]**-1 + 1)
        else:
            (G[node2])[node1] = 1
    return G


def read_comic_graph(filename):
    # Read an undirected graph in CSV format. Each line is an edge
    tsv = csv.reader(open(filename), delimiter='\t')
    G = {}
    char_df = pd.read_csv(filename, sep='\t', names=['char', 'comic'])

    for char_1 in set(char_df['char'].values):
        char_1_comics = char_df.loc[char_df['char'] == char_1, 'comic']
        char_1_shared_chars = char_df.loc[char_df['comic'].isin(char_1_comics), 'char']
        for char_2 in char_1_shared_chars:
            # so we don't double count
            if char_2 > char_1:
                make_link_inverse(G, char_1, char_2)
    return G

graph = read_comic_graph('super_hero.tsv')

# now we need to find the shortest_weighted and shortest_hops for these 5 characters:

# 'SPIDER-MAN/PETER PAR'
# 'GREEN GOBLIN/NORMAN'
# 'WOLVERINE/LOGAN '
# 'PROFESSOR X/CHARLES '
# 'CAPTAIN AMERICA'

# and for each of those characters count up how many times the shortest weighted path
# is different than the shortest hop path

# we'll modify  the djikstra algorithm from earlier to get the shortest weighted paths,
# and the number of hops it took to get that path.
# we'll also use a new path function to get the shortest hop path dictionary:

def paths(G, v):
    distance_dict = {}
    open_list = [v]
    distance_dict[v] = 0
    while len(open_list) > 0:
        current = open_list[0]
        del open_list[0]
        for neighbor in G[current].keys():
            if neighbor not in distance_dict:
                distance_dict[neighbor] = distance_dict[current] + 1
                open_list.append(neighbor)
    return distance_dict

def dijkstra_plus_hops(G,v):

    dist_so_far_heap = [v]
    dist_so_far_values = {v: 0}
    hops_so_far = {v: 0}

    location_dict = {v: 0}

    final_hops = {}
    final_dist = {}
    # we'll just treat the dist_so_far_heap as an open list
    while len(dist_so_far_heap) > 0:
        # get the minimum node/val pair
        w = dist_so_far_heap[0]
        val = dist_so_far_values[w]
        hops_val = hops_so_far[w]
        # remove the min pair from the location dict
        del dist_so_far_heap[0]
        del dist_so_far_values[w]
        del hops_so_far[w]
        del location_dict[w]

        # set the last element of dist_so_far_heap to the first and down heapify
        if len(dist_so_far_heap) > 0:
            dist_so_far_heap.insert(0, dist_so_far_heap.pop(-1))
            location_dict[dist_so_far_heap[0]] = 0
            down_heapify(dist_so_far_heap, 0, location_dict, dist_so_far_values)

        # lock it down!
        final_hops[w] = hops_val
        final_dist[w] = val

        for x in G[w]:
            if x not in final_dist:
                if x not in dist_so_far_heap:
                    dist_so_far_heap.append(x)
                    # add the new node to the location dictionary
                    location_dict[x] = len(dist_so_far_heap)-1
                    # and add new new distance to the value dictionary
                    dist_so_far_values[x] = final_dist[w] + G[w][x]
                    hops_so_far[x] = final_hops[w] + 1
                    up_heapify(dist_so_far_heap, len(dist_so_far_heap)-1, location_dict, dist_so_far_values)
                # if x IS in the dist so far heap, we want to see if it's value is higher than the current
                # distance, and if it is update it
                elif dist_so_far_values[x] > final_dist[w] + G[w][x]:
                    dist_so_far_values[x] = final_dist[w] + G[w][x]
                    hops_so_far[x] = final_hops[w] + 1
                    up_heapify(dist_so_far_heap, location_dict[x], location_dict, dist_so_far_values)
    return final_dist, final_hops

spiderman_hops = paths(graph, 'SPIDER-MAN/PETER PAR')
spiderman_weighted, spiderman_w_hops = dijkstra_plus_hops(graph, 'SPIDER-MAN/PETER PAR')

goblin_hops = paths(graph, 'GREEN GOBLIN/NORMAN ')
goblin_weighted, goblin_w_hops = dijkstra_plus_hops(graph, 'GREEN GOBLIN/NORMAN ')

wolverine_hops = paths(graph, 'WOLVERINE/LOGAN ')
wolverine_weighted, wolverine_w_hops = dijkstra_plus_hops(graph, 'WOLVERINE/LOGAN ')

prof_hops = paths(graph, 'PROFESSOR X/CHARLES ')
prof_weighted, prof_w_hops = dijkstra_plus_hops(graph, 'PROFESSOR X/CHARLES ')

captain_hops = paths(graph, 'CAPTAIN AMERICA')
captain_weighted, captain_w_hops = dijkstra_plus_hops(graph, 'CAPTAIN AMERICA')

def count_diff(hops_dicts, weights_dicts):
    diff_count = 0
    for (hops, weights) in zip(hops_dicts, weights_dicts):
        for char in hops.keys():
            if hops[char] != weights[char]:
                diff_count += 1
    return diff_count

hops = [spiderman_hops, goblin_hops, wolverine_hops, prof_hops, captain_hops]
weights = [spiderman_w_hops, goblin_w_hops, wolverine_w_hops, prof_w_hops, captain_w_hops]

count = count_diff(hops, weights)
print count
