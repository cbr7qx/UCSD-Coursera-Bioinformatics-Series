kmerList = "AAAT AATG ACCC ACGC ATAC ATCA ATGC CAAA CACC CATA CATC CCAG CCCA CGCT CTCA GCAT GCTC TACG TCAC TCAT TGCA"

def DeBruijn_Graph2(kmers):
    adjacency_list = {}
    k = len(kmers[0])
    for kmer in kmers:
        prefix = kmer[0:k-1]
        suffix = kmer[1:k]
        if prefix not in adjacency_list: adjacency_list[prefix] = []
        adjacency_list[prefix].append(suffix)
    return adjacency_list


def EulerianPath(graph):
    
    from collections import deque

    # Re-format the input and generate a graph dictionary where the key is node and value is a set consisting of its adjacent nodes, e.g., graph = {"a": ["b", "c"]}
    if isinstance(graph, str):
        graph = dict(item.split(": ") for item in graph.strip().split("\n"))
        graph = {key.strip(): value.split() for key, value in graph.items()}
    nodes = set(graph.keys()) | {v for values in graph.values() for v in values}

    # Initialize in- and out-degree dictionaries, calculate in- and out-degrees for each node
    in_degree = {node: 0 for node in nodes}
    out_degree = {node: 0 for node in nodes}
    for node, adjacents in graph.items():
        out_degree[node] += len(adjacents)
        for adjacent in adjacents: 
            in_degree[adjacent] += 1

    # Find the imbalanced nodes to determine start and end of the Eulerian path
    start, end = None, None
    for node in nodes:
        if in_degree[node] < out_degree[node]:
            start = node
        elif in_degree[node] > out_degree[node]:
            end = node
    
    # Append one directed edge from the end to the start, and generate an Eulerian cycle
    if end in graph:
        graph[end].append((start, "artificial"))
    else:
        graph[end] = [(start, "artificial")]
    print('final graph: ',graph)

    cycle = deque([start])
    while graph:
        current_node = cycle[-1]
        if current_node in graph:
            # Pick the next node and remove it from the current node's adjacency list
            next_node = graph[current_node].pop()
            cycle.append(next_node)
            # If the current node's adjacency list is empty, remove the node from the graph
            if not graph[current_node]:
                del graph[current_node]
        else:
            # Rotate the cycle to find a new starting point with available edges
            cycle.rotate(-1)
    
    cycle = list(cycle)
    print('final cycle: ',cycle)
    # Find the artificial edge
    for index, node in enumerate(cycle):
        if isinstance(node, tuple) and node[-1] == "artificial": #I CHANGED THIS FROM node[1] to node[-1] to acccount for an end node that appears multiple times during the cycle.
            # Remove the marker and break the cycle
            cycle[index] = node[0]
            path = cycle[index + 1:] + cycle[:index]
            break
    
    #print(" ".join(str(x) for x in path))
    return path


def DnaString(genome_path):
    import pyperclip3
    number_of_kmers = len(genome_path) #note that this is the list genome_path, not the raw_genome_path.
    k = len(genome_path[0]) #length of each kmer
    string = str(genome_path[0])
    for i in range(1,number_of_kmers): 
        string += genome_path[i][k-1]
    pyperclip3.copy(string)
    print('the string has been copied to the clipboard')
    return string


def Genome_Assembly(kmerList): #input is a string of spaced separated kmers
    kmers = kmerList.split()
    graph = DeBruijn_Graph2(kmers)
    path = EulerianPath(graph)
    genome = DnaString(path)
    return genome


print(Genome_Assembly(kmerList))


