#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations

def get_id(tid):
	pid = None
	lid = tid.split(":")
	if lid[0]=='uniprotkb':
		no_iso = lid[1].split("-")
		pid = no_iso[0]
	
	return pid

def parse_network(filename):
	#define a dictionary, include the elements from different lines
	f = open(filename)
	edges = {}
	nodes={}
	for line in f:
		v = line.split("\t")
		pid1 = get_id(v[0])
		pid2 = get_id(v[1])
		if not pid1 or not pid2: continue
		edge = [pid1, pid2]
		edge.sort()
		edges[tuple(edge)] = 1
		nodes[pid1] = 1
		nodes[pid2] = 1
	return list(nodes.keys()), list(edges.keys())
	
def net_analysis(edges): #gain info regarding features of the network and our nodes of interest
	g = nx.Graph()
	g.add_edges_from(edges)
	
	dgs=dict(g.degree())
	ldgs = [(v,k) for k, v in dgs.items()]
	ldgs.sort()
	alpha_degree = dgs['P69905']
	beta_degree = dgs['P68871']
	cluster = nx.clustering(g)
	lcl = [(v,k) for k, v in cluster.items()]
	lcl.sort()
	alpha_cluster = cluster['P69905']
	beta_cluster = cluster['P68871']

	btw = dict(nx.betweenness_centrality(g, normalized=False))
	alpha_btw = btw['P69905']
	beta_btw = btw['P68871']
	return ldgs[-1], alpha_degree, beta_degree, alpha_cluster, beta_cluster, alpha_btw, beta_btw


def neigh(edges):#find the neightbours of Alpha and Beta and create a network using them
	g = nx.Graph()
	g.add_edges_from(edges)
	neighbors = []
	neighbors += list(g.neighbors('P69905'))
	neighbors += list(g.neighbors('P68871'))
	neighbors = set(neighbors)
	s = g.subgraph(neighbors)
	return s.edges()
	
def remove_subunits(edges, sub_id, left_node_id): #remove once alpha then beta and analyse how their parameter change
	g = nx.Graph()
	g.add_edges_from(edges)
	g.remove_node(sub_id)
	dgs=dict(g.degree())

	left_node_degree = dgs[left_node_id]
	cluster = nx.clustering(g)
	left_node_cluster = cluster[left_node_id]
	btw = dict(nx.betweenness_centrality(g, normalized=False))
	left_node_btw = btw[left_node_id]

	return left_node_degree, left_node_cluster, left_node_btw
	

def remove_edge(edges):#removing edge of alpha-beta and compute the shortest path 
	g = nx.Graph()
	g.add_edges_from(edges)
	g.remove_edge('P68871','P69905')
	shortest_path = nx.shortest_path_length(g, source='P68871', target='P69905')
	paths = [p for p in nx.all_shortest_paths(g, source='P68871', target='P69905')]
	degrees = g.degree()
	clustering = nx.clustering(g)
	betweenness = dict(nx.betweenness_centrality(g, normalized=False))
	return np.mean(list(degrees.values())), np.mean(list(clustering.values())), np.mean(list(betweenness.values()))
	
	
def major_comp(edges):#find the major component
	g = nx.Graph()
	g.add_edges_from(edges)
	cc = nx.connected_components(g)
	major_cc = max(cc, key=len)
	return len(major_cc) #both subunits included, len=3254
	
def plot_net(edges):
	g = nx.Graph()
	g.add_edges_from(edges)
	nx.draw(g, with_labels=True, width=1)
	plt.show()

def histo(edges, average, title, lab, alpha=0, beta=0):
	histogram = plt.hist(edges, bins=30, range=[0, 30000], color='lightcyan')
	plt.vlines(x=average, ymin=0, ymax=3000, color='r', label=lab)
	plt.vlines(x=alpha, ymin=0, ymax=3000, color='y', label='Alpha')
	plt.vlines(x=beta, ymin=0, ymax=3000, color='m', label='Beta')
	plt.legend()
	plt.title(title)
	plt.ylabel('Number of Nodes')
	plt.xlabel('Values of Nodes')
	plt.show()
	
if __name__ == "__main__":
	import sys

	filename = sys.argv[1]

	node, edges = parse_network(filename)
	print(remove_edge(edges))
	
	
	
