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

test()

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



################
## Question 3 ##
################

#
# Another way of thinking of a path in the Kevin Bacon game
# is not about finding *short* paths, but by finding paths
# that don’t use obscure movies.  We will give you a
# list of movies along with their obscureness score.
#
# For this assignment, we'll approximate obscurity
# based on the multiplicative inverse of the amount of
# money the movie made.  Though, its not really important where
# the obscurity score came from.
#
# Use the the imdb-1.tsv and imdb-weights.tsv files to find
# the obscurity of the “least obscure”
# path from a given actor to another.
# The obscurity of a path is the maximum obscurity of
# any of the movies used along the path.
#
# You will have to do the processing in your local environment
# and then copy in your answer.
#
# Hint: A variation of Dijkstra can be used to solve this problem.
#

def dijkstra_obs(G,v):

    obs_heap = [v]
    obs_so_far = {v: 0}
    location_dict = {v: 0}

    final_obs = {}
    while len(obs_heap) > 0:
        # get the minimum node/val pair
        w = obs_heap[0]
        val = obs_so_far[w]

        # remove the min pair from the location dict
        del obs_heap[0]
        del obs_so_far[w]
        del location_dict[w]

        # set the last element of obs_heap to the first and down heapify
        if len(obs_heap) > 0:
            obs_heap.insert(0, obs_heap.pop(-1))
            location_dict[obs_heap[0]] = 0
            down_heapify(obs_heap, 0, location_dict, obs_so_far)

        # lock it down!
        final_obs[w] = val

        for x in G[w]:
            if x not in final_obs:
                if x not in obs_heap:
                    obs_heap.append(x)
                    # add the new node to the location dictionary
                    location_dict[x] = len(obs_heap)-1
                    # and add new new distance to the value dictionary
                    obs_so_far[x] = max(G[w][x], final_obs[w])
                    up_heapify(obs_heap, len(obs_heap)-1, location_dict, obs_so_far)
                # if x IS in the dist so far heap, we want to see if it's value is higher than the current
                # distance, and if it is update it
                elif obs_so_far[x] > max(G[w][x], final_obs[w]):
                    obs_so_far[x] = max(G[w][x], final_obs[w])
                    up_heapify(obs_heap, location_dict[x], location_dict, obs_so_far)
    return final_obs

def make_obs_link(G, node1, node2, w):
    if node1 not in G:
        G[node1] = {node2: w}
    elif node1 in G:
        if node2 in G[node1]:
            if (G[node1])[node2] > w:
                (G[node1])[node2] = w
        else:
            (G[node1])[node2] = w
    if node2 not in G:
        G[node2] = {node1: w}
    elif node2 in G:
        if node1 in G[node2]:
            if (G[node2])[node1] > w:
                (G[node2])[node1] = w
        else:
            (G[node2])[node1] = w
    return G

def build_obs_graph(actors_file, weights_file):
    actors_df = pd.read_csv(actors_file, sep='\t', encoding='utf-8')
    weights_df = pd.read_csv(weights_file, sep='\t', encoding='utf-8')
    actors_df.columns = ['actor', 'movie', 'year']
    weights_df.columns = ['movie', 'year', 'weight']
    df = actors_df.merge(weights_df, on=['movie', 'year'])
    # now let's make a graph that connects just actors, based on the least obscure
    # movie they appeared in together
    G = {}
    for actor_1 in set(df['actor'].values):
        actor_1_movies = df.loc[df['actor'] == actor_1, 'movie']
        shared_actors = df.loc[df['movie'].isin(actor_1_movies), 'actor']
        shared_weight = df.loc[df['movie'].isin(actor_1_movies), 'weight']
        for actor_2, w in zip(shared_actors, shared_weight):
            # so we don't double count
            if actor_2 > actor_1:
                G = make_obs_link(G, actor_1, actor_2, w)
    return G

answer_pairs = {(u'Boone Junior, Mark', u'Del Toro, Benicio'): None,
          (u'Braine, Richard', u'Coogan, Will'): None,
          (u'Byrne, Michael (I)', u'Quinn, Al (I)'): None,
          (u'Cartwright, Veronica', u'Edelstein, Lisa'): None,
          (u'Curry, Jon (II)', u'Wise, Ray (I)'): None,
          (u'Di Benedetto, John', u'Hallgrey, Johnathan'): None,
          (u'Hochendoner, Jeff', u'Cross, Kendall'): None,
          (u'Izquierdo, Ty', u'Kimball, Donna'): None,
          (u'Jace, Michael', u'Snell, Don'): None,
          (u'James, Charity', u'Tuerpe, Paul'): None,
          (u'Kay, Dominic Scott', u'Cathey, Reg E.'): None,
          (u'McCabe, Richard', u'Washington, Denzel'): None,
          (u'Reid, Kevin (I)', u'Affleck, Rab'): None,
          (u'Reid, R.D.', u'Boston, David (IV)'): None,
          (u'Restivo, Steve', u'Preston, Carrie (I)'): None,
          (u'Rodriguez, Ramon (II)', u'Mulrooney, Kelsey'): None,
          (u'Rooker, Michael (I)', u'Grady, Kevin (I)'): None,
          (u'Ruscoe, Alan', u'Thornton, Cooper'): None,
          (u'Sloan, Tina', u'Dever, James D.'): None,
          (u'Wasserman, Jerry', u'Sizemore, Tom'): None}

answer = {}

graph = build_obs_graph('./imdb_1.tsv', './imdb_weights.tsv')

for actor_pair in answer_pairs.keys():
    obs_graph = dijkstra_obs(graph, actor_pair[0])
    answer[actor_pair] = round(obs_graph[actor_pair[1]], 4)

print answer
