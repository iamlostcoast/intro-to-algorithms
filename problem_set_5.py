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
