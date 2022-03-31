#!/usr/bin/env python3
import sys
import math

def parse_pdb(filename, chain):
	atom_dic = {}
	hem_dic ={}
	f = open(filename, 'r')
	for line in f:
		chain_id = line[20:22].strip()
		if line[:4] == 'ATOM' and  chain_id == chain: 
			atom = line[12:16].strip()
			resname = line[17:20].strip()
			resnum = int(line[22:26].strip())
			x = float(line[30:38].strip())
			y = float(line[38:46].strip())
			z = float(line[46:54].strip())
			atom_dic[resnum] = atom_dic.get(resnum, {"Name":resname})
			atom_dic[resnum][atom]=[x, y, z]
		if line[:6] == 'HETATM' and chain_id == chain:
			atom = line[12:16].strip()
			resname = line[17:20].strip()
			if resname != 'HOH':  
				resnum = int(line[22:26].strip())
				x = float(line[30:38].strip())
				y = float(line[38:46].strip())
				z = float(line[46:54].strip())
				hem_dic[resnum] = hem_dic.get(resnum, {"Name":resname})
				hem_dic[resnum][atom]=[x, y, z]
			
	return atom_dic, hem_dic
	
	
def return_atom(dic):
	atoms = []
	for resnum in dic.keys():
		for atom in dic[resnum].keys():
			if atom != 'Name':
				atoms.append((resnum, atom, dic[resnum][atom]))
	return atoms
		
	
def get_distance(at1, at2): #uses coordinates given as inputs to apply mathetamical of distance between two points
	distance = math.sqrt((at1[0] - at2[0])**2 + (at1[1] - at2[1])**2 + (at1[2] - at2[2])**2)
	return round(distance, 3)

def pairs_distance(atom_dic, hem_dic, dist): #computes distance between two atoms given as input
	distances = []
	for atom in return_atom(atom_dic):
		for hem in return_atom(hem_dic):
			distance = get_distance(atom[2], hem[2])
			if distance <= float(dist):
				distances.append((atom[0], atom[1], hem[0], hem[1], distance))
			
	return distances
	
def atoms_distance(chain):#computes distances between atoms of chain and hem/oxy group
	distances_in_format = []
	atom_dic, hem_dic = parse_pdb(filename, chain)
	dist = float(3.5)
	distances = pairs_distance(atom_dic, hem_dic, dist)
	for distance in distances:
		atom_resno = distance[0]
		hem_resno = distance[2]
		atom = distance[1]
		hem = distance[3]
		atom_resname = atom_dic[atom_resno]['Name']
		hem_resname = hem_dic[hem_resno]['Name']
		distance_format = (atom_resno, atom_resname, atom, 
		hem_resno, hem_resname, hem, chain, distance[-1])
		distances_in_format.append(distance_format)
	for item in distances_in_format:	
		print ("\t".join([str(i) for i in item]))

	
def chain_distance(chain1, chain2): #computes all bonds of a given distance between two chains
	distances_in_format = []
	atom_dic_A = parse_pdb(filename, chain1)[0]
	atom_dic_B = parse_pdb(filename, chain2)[0]
	dist = float(3.5)
	distances = pairs_distance(atom_dic_A, atom_dic_B, dist)
	for distance in distances:
		chain1_resno = distance[0]
		chain2_resno = distance[2]
		chain1_atom = distance[1]
		chain2_atom = distance[3]
		chain1_resname = atom_dic_A[chain1_resno]['Name']
		chain2_resname = atom_dic_B[chain2_resno]['Name']
		distance_format = (chain1, chain1_resno, chain1_resname, chain1_atom, 
		chain2, chain2_resno, chain2_resname, chain2_atom, distance[-1])
		distances_in_format.append(distance_format)
	return distances_in_format
	


		
		
			 
if __name__=="__main__":
	filename=sys.argv[1]
	chain = sys.argv[2]
	#chain2 = sys.argv[3]
	atom_dic, hem_dic = parse_pdb(filename, chain)

