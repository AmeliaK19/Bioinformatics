#!/usr/bin/env python3
import sys
import math
import numpy

def parse_dssp(filename, chain):
	dssp_dic = {}
	c = 0
	f = open(filename, 'r')
	for line in f:
		if line.find('  #  RESIDUE ') == 0:
			c = 1
			continue
		if c==0: continue
		if line[11] != chain: continue
		resn = int(line[5:10])
		aa = line[13]
		if aa.islower(): aa='C'
		ss = line[16]
		if ss==' ': ss='C'
		sa = int(line[35:38])
		rsa = min(sa/Norm_Acc.get(aa, 200), 1.0)
		phi = float(line[103:109])
		psi = float(line[109:115])
		dssp_dic[resn] = [aa, ss, sa, rsa, phi, psi]
	return dssp_dic
	

def rsa_change(chain, monomer, tetramer):#compute the loss of rsa of every aminoacid and select upon the given criteria (loss>10%)
	aminoacids = []
	monomer_dic = parse_dssp(monomer, chain)
	tetramer_dic = parse_dssp(tetramer, chain)
	for res in monomer_dic.keys():
		mon_rsa = float(monomer_dic[res][3])
		tet_rsa = float(tetramer_dic[res][3])
		if mon_rsa!=tet_rsa:
			final_rsa = mon_rsa - tet_rsa
			if final_rsa > 0.1*mon_rsa:
				aa = monomer_dic[res][0]
				sa = monomer_dic[res][2]
				identifier = (chain, aa, sa, round(mon_rsa, 4), round(tet_rsa, 4), round(final_rsa, 4))
				aminoacids.append(identifier)
	for item in aminoacids:	
		print ("\t".join([str(i) for i in item]))
	
	
	
def get_total_saa(dssp_dic):#computes solvent accessible area of a monomer
	saa = 0.0
	for aa in dssp_dic.keys():
		saa += dssp_dic[aa][2]
	return saa	
	

def saa_loss_matrix(trimers, tetramer, chains=['A', 'B', 'C', 'D']):#prints the SA loss matrix
	matrix = [['/']+chains]
	for i in range(0,4):
		row=[chains[i]]
		for x in chains:
			if chains[i] == x: row.append('/')
			else:
				pair_distance = acc_loss(tetramer, trimers[i], x)
				row.append(pair_distance)
		matrix.append(row)
					
	return matrix


def acc_loss(tetramer, trimer, chain1): #computes accessibility loss of a monomer when interacts with another
	tri_dic = parse_dssp(trimer, chain1)
	tri_saa = get_total_saa(tri_dic)
	tetra_dic = parse_dssp(tetramer, chain1)
	tetra_saa = get_total_saa(tetra_dic)
	loss = tri_saa - tetra_saa
	return loss
	
	
def residue_acc_change(dic_tetra, dic_mono, chain):#computes SA loss of residues of a chain
	saad = 0.0
	involved_residues = []
	for aa in dic_tetra.keys() and dic_mono.keys():
		saad = dic_mono[aa][2] - dic_tetra[aa][2]
		if saad>0:
			 residue = (aa, chain, saad, dic_mono[aa][2], dic_tetra[aa][2])
			 involved_residues.append(residue)
	return involved_residues, len(involved_residues)	
	

Norm_Acc= {"A" :106.0,  "B" :160.0,
   "C" :135.0,  "D" :163.0,  "E" :194.0,
   "F" :197.0,  "G" : 84.0,  "H" :184.0,
   "I" :169.0,  "K" :205.0,  "L" :164.0,
   "M" :188.0,  "N" :157.0,  "P" :136.0,
   "Q" :198.0,  "R" :248.0,  "S" :130.0,
   "T" :142.0,  "V" :142.0,  "W" :227.0,
   "X" :180.0, "Y" :222.0,  "Z" :196.0}

if __name__ == "__main__":
	dsspfile=sys.argv[1]
	trimer1=sys.argv[2]
	trimer2=sys.argv[3]
	trimer3=sys.argv[4]
	trimer4=sys.argv[5]
	trimers = list((trimer1, trimer2, trimer3, trimer4))

