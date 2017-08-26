# This file includes functions that can be used to find 'bridge edges' in a graph

def create_rooted_spanning_tree(G, root):
    S = {}
    open_list = [root]
    while len(open_list) > 0:
        current = open_list[0]
        del open_list[0]
        # create a dict for current if there isn't one already
        if current not in S.keys():
            S[current] = {}
        for node in G[current].keys():
            # check to see if the node has been added to the graph yet
            if node not in S.keys():
                S[node] = {}
                S[node][current] = 'green'
                S[current][node] = 'green'
                open_list.append(node)
            elif node in S.keys():
                try:
                    S[current][node]
                except:
                    S[current][node] = 'red'
                    S[node][current] = 'red'
                    open_list.append(node)                
    return S

def post_order(S, root):
    open_list = [root]
    #parent = None
    po = {key: None for key in S.keys()}
    current_value = 1
    numbered_nodes = []
    while len(open_list) > 0:
        # We'll remove nodes from 'nodes' if:
        # they are the current node, they have a red
        # connetion, and if they're numbered
        current = open_list.pop()
        nodes = S[current].keys()
        check_nodes = S[current].keys()
        #if parent in nodes:
        #    nodes.remove(current)
        # check to see if node is numbered
        for node in nodes:
            if node in numbered_nodes:
                check_nodes.remove(node)
            elif S[current][node] == 'red':
                check_nodes.remove(node)
            elif node in open_list:
                check_nodes.remove(node)
            else:
                continue
        if len(check_nodes) == 0:
            numbered_nodes.append(current)
            po[current] = current_value
            current_value += 1
        else:
            open_list.append(current)
            open_list += check_nodes
    return po

def number_of_descendents(S, root):
    open_list = [root]
    #parent = None
    descendents = {key: 0 for key in S.keys()}
    numbered_nodes = []
    while len(open_list) > 0:
        # We'll remove nodes from 'nodes' if:
        # they are the current node, they have a red
        # connetion, and if they're numbered
        current = open_list.pop()
        nodes = S[current].keys()
        check_nodes = S[current].keys()
        #if parent in nodes:
        #    nodes.remove(current)
        # check to see if node is numbered
        node_value = 0
        for node in nodes:
            if S[current][node] == 'red':  
                check_nodes.remove(node)
            elif node in numbered_nodes:
                check_nodes.remove(node)
                node_value += descendents[node]
            elif node in open_list:
                check_nodes.remove(node)
            else:
                continue
        if len(check_nodes) == 0:
            numbered_nodes.append(current)
            descendents[current] = node_value + 1
        else:
            open_list.append(current)
            open_list += check_nodes
    return descendents

def lowest_post_order(S, root, po):
    lowest_po = {node: None for node in S.keys()}
    numbered_nodes = []
    open_list = [root]
    while len(open_list) > 0:
        current = open_list.pop()
        check_nodes = S[current].keys()
        non_parent_nodes = S[current].keys()
        for node in S[current].keys():
            if S[current][node] == 'red':
                check_nodes.remove(node)
            elif node in numbered_nodes:
                check_nodes.remove(node)
            elif node in open_list:
                non_parent_nodes.remove(node)
                check_nodes.remove(node)
            else:
                continue    
        if len(check_nodes) == 0:
            # now we need to find all the children and red nodes
            # connection to this node
            children = []
            c_open_list = [current]
            while len(c_open_list) > 0:
                c_current = c_open_list.pop()
                c_check_nodes = S[c_current].keys()
                for node in S[c_current].keys():
                    if S[c_current][node] == 'red':
                        c_check_nodes.remove(node)
                    elif node in open_list:
                        c_check_nodes.remove(node)
                    elif node in c_open_list:
                        c_check_nodes.remove(node)
                    elif node in children:
                        c_check_nodes.remove(node)
                if len(c_check_nodes) == 0:
                    children.append(c_current)
                else:
                    c_open_list.append(c_current)
                    c_open_list += c_check_nodes
            # now we need to add red connections
            for node, connection in S[c_current].items():
                if connection == 'red':
                    children.append(node)
            # with the children, now we need to find the min value of po for them
            po_values = [po[node] for node in children]
            for child in children:
                if lowest_po[child]:
                    po_values.append(lowest_po[child])
            lowest_po[current] = min(po_values)
            numbered_nodes.append(current)
        else:
            open_list.append(current)
            open_list += check_nodes
    return lowest_po

def highest_post_order(S, root, po):
    highest_po = {node: None for node in S.keys()}
    numbered_nodes = []
    open_list = [root]
    while len(open_list) > 0:
        current = open_list.pop()
        check_nodes = S[current].keys()
        non_parent_nodes = S[current].keys()
        for node in S[current].keys():
            if S[current][node] == 'red':
                check_nodes.remove(node)
            elif node in numbered_nodes:
                check_nodes.remove(node)
            elif node in open_list:
                non_parent_nodes.remove(node)
                check_nodes.remove(node)
            else:
                continue    
        if len(check_nodes) == 0:
            # now we need to find all the children and red nodes
            # connection to this node
            children = []
            c_open_list = [current]
            while len(c_open_list) > 0:
                c_current = c_open_list.pop()
                c_check_nodes = S[c_current].keys()
                for node in S[c_current].keys():
                    if S[c_current][node] == 'red':
                        c_check_nodes.remove(node)
                    elif node in open_list:
                        c_check_nodes.remove(node)
                    elif node in c_open_list:
                        c_check_nodes.remove(node)
                    elif node in children:
                        c_check_nodes.remove(node)
                if len(c_check_nodes) == 0:
                    children.append(c_current)
                else:
                    c_open_list.append(c_current)
                    c_open_list += c_check_nodes
            # now we need to add red connections
            for node, connection in S[c_current].items():
                if connection == 'red':
                    children.append(node)
            # with the children, now we need to find the min value of po for them
            po_values = [po[node] for node in children]
            for child in children:
                if highest_po[child]:
                    po_values.append(highest_po[child])
            highest_po[current] = max(po_values)
            numbered_nodes.append(current)
        else:
            open_list.append(current)
            open_list += check_nodes
    return highest_po
