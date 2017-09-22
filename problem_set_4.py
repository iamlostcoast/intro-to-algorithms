
####################
#### PROBLEM 2 #####
####################

# write up_heapify, an algorithm that checks if
# node i and its parent satisfy the heap
# property, swapping and recursing if they don't
#
# L should be a heap when up_heapify is done


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

def up_heapify(L, i):
    # your code here
    # first case is just if we're done, if the node is the root:
    if i == 0:
        return

    if one_child(L, parent(i)):
        if L[parent(i)] > L[i]:
            (L[parent(i)], L[i]) = (L[i], L[parent(i)])
            up_heapify(L, parent(i))
            return
        else:
            return

    # if the not one leaf and node we're working with is smaller than the parent, then
    # we swap the min child and up heapify
    if L[parent(i)] <= L[i]:
        return

    if L[left_child(parent(i))] < L[right_child(parent(i))]:
        (L[parent(i)], L[left_child(parent(i))]) = (L[left_child(parent(i))], L[parent(i)])
        up_heapify(L, parent(i))
        return
    (L[parent(i)], L[right_child(parent(i))]) = (L[right_child(parent(i))], L[parent(i)])
    up_heapify(L, parent(i))
    return


####################
#### PROBLEM 6 #####
####################

# Given data of movies and actors who appeared in them, build a bipartite graph
# and find the actor with the 20th lower average centrality

# first function will read in a file, and build the graph and lists of elements
# for the members of the graph
def create_imdb_graph(fname):
    G, actors, movies, index = {}, [], [], 0
    file = csv.reader(open(fname, 'rb'), delimiter='\t')
    for row in file:
        actor = row[0]
        movie = '%s (%s)' % (row[1], row[2]) # row[1]
        if actor not in actors:
            actors.append(actor)
        if movie not in movies:
            movies.append(movie)
        make_link(G, actor, movie)
    return G, actors, movies

# create our objects
G, actors, movies = create_imdb_graph("./file.tsv")

# for a given node, determine its centrality within a graph
def centrality(G, v):
    distance_from_start = {}
    open_list = [v]
    distance_from_start[v] = 0
    while len(open_list) > 0:
        current = open_list[0]
        del open_list[0]
        for neighbor in G[current].keys():
            if neighbor not in distance_from_start:
                distance_from_start[neighbor] = distance_from_start[current] + 1
                open_list.append(neighbor)
    return float(sum(distance_from_start.values()))/len(distance_from_start)

# given a dictionary of centralities, find the element at rank i (the ith lowest centrality)
def find_rank(L, i):
    lt = {}
    eq = {}
    gt = {}
    v = random.choice(L.keys())
    for l in L.keys():
        if L[l] < L[v]: lt[l] = L[l]
        elif L[l] == L[v]: eq[l] = L[l]
        elif L[l] > L[v]: gt[l] = L[l]
    if len(lt) >= i: find_rank(lt, i)
    elif len(lt) + len(eq) >= i: print v, len(lt) + len(eq), len(L)
    else: return find_rank(gt, i - len(lt) - len(eq))

# build our centralities dictionary
centralities = {}
for actor in actors:
    centralities[actor] = centrality(G, actor)

print find_rank(centralities, 20)
    
