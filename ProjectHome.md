# OpenPajek #
OpenPajek is a network analysis software that aims to be an open source replacement to proprietary software such as Pajek or UCINET. Its core is igraph, a robust and efficient C library for analyzing networks

It can be used to help understand how micro behavior of the individual nodes yields to important changes in the global structure of the network.

![http://openpajek.googlecode.com/svn/trunk/screenshot.png](http://openpajek.googlecode.com/svn/trunk/screenshot.png)

## Installation notes ##

To run the program you need to download the zip file and uncompress it at any location. When finished uncompressing just double click on the file openpajek.bat and the main window should appear in a few seconds.

## Features ##

### Network Generation ###

- Erdos\_Renyi:
Generates a graph based on the Erdos-Renyi model.
Parameters:
n - the number of vertices.
p - the probability of edges. If given, m must be missing.

- Lattice:
Generates a regular lattice.
Parameters:
dim - list with the dimensions of the lattice

- Barabasi:
Generates a graph based on the Barabasi-Albert model.
Parameters:
n - the number of vertices
m - number of outgoing edges generated for each vertex

- Watts:
Generates a regular lattice of dimension 1 (ring) where each vertex is connected to its 4 nearest neighbors. Generates a high clustering coefficient.
Parameters:
n - the number of vertices

### Simulation ###

All simulation processes behave similarly. A random link is removed and a new one is created following a specific strategy. When the user selects any of the three methods, the program will ask for a specific number of iterations.

- Random:
The link created is chosen randomly from all the possible links.

Keyboard shortcut for one iteration: r

- Neighbor:
A random node is chosen, and linked together with another node reachable in exactly two steps.

Keyboard shortcut for one iteration: n

- Preferential attachment:
A random node n1 is chosen where all nodes have the same probability of being chosen.
A random node n2 is chosen with each node having the probability of being chosen proportional to its degree.
if n1 and n2 are not the same node, and not linked together, a link is formed between n1 and n2.

Keyboard shortcut for one iteration: p

### Layouts ###

A layout is an algorithm that locates the nodes of a network on a two dimensional space. Their objective is to make the graph look good to the human eye, and there are many different methods.
Here is the list of implemented methods: circular, drl, fruchterman\_reingold, graphopt, grid\_fruchterman\_reingold, kamada\_kawai, large\_graph, random, reingold\_tilford, reingold\_tilford\_circular.
See the igraph documentation http://igraph.sourceforge.net/doc/python/index.html for more information about the algorithms.

The graph being used will be shown at all times in the main window using the layout selected. The layout is not recalculated on the simulation process, so it's a good idea to recalculate the layout by selecting it again in the layout menu after a few simulation steps.

### Plots ###

There are three plots shown in the main window. Two of them show the average path length and the clustering coefficient of the whole network over time. The bottom plot shows the degree distribution. The scale of the plots can be changed to logarithmic or linear under 'plot' in the menu bar.

## Proposed experiments ##

  * Create regular lattice. use the circular layout to understand its structure

  * Create a watts lattice and randomize it (simulate/random on the menu bar or 'n' keyboard shortcut) to create a small world. notice how the apl drops more rapidly than cc does. use logarithmic scale (plot/log on the menu bar) Recommended reading: http://www.nature.com/nature/journal/v393/n6684/abs/393440a0.html

  * Create a random network (Erdos\_Renyi) and use the neighbor rule. Observe how both the clustering coefficient and average path length increase

  * Create a random network. Observe how the degree distribution approximates to a poisson distribution. Use a high number of nodes to see it more clearly.Create a barabasi network. Observe how the degree distribution approximates to a power law. Use a logarithmic scale. Now create a random network, which will initially have a poisson distribution and use the preferential attachment rule to evolve the network. See how the distribution will approximate to a power law. You can replot the graph once in a while using the fruchterman\_reingold layout to see its star structure.