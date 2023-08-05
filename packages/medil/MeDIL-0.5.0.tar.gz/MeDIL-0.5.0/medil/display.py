import numpy as np
# from networkx import from_numpy_matrix, Graph, draw
# from matplotlib.pyplot import show
# from networkx.drawing.nx_pydot import write_dot
# from graphviz import Digraph, render


# probably gets its own method? no, maybe its rather a property of the
# graph object returned by ECC finding? or is ECC finding just a sub
# func in the class/method (ahh, don't know termin) of the UDG, which
# could be a property of the data?
def display_graph(adjacency_matrix):
    graph = from_numpy_matrix(adjacency_matrix, create_using=Graph())
    draw(graph)
    show()

# def display_graph(adjacency_matrix, name):
#     path = '/home/alex_work/Documents/causal_concept_discovery/software/misc/'
#     graph = from_numpy_matrix(adjacency_matrix, create_using=DiGraph())
#     write_dot(graph, path + name + '.gv')
#     graph = Digraph('g', filename=path+name+'.gv')
#     graph.render
