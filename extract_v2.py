import networkx as nx
import sys
import random
import matplotlib.pyplot as plt


def has3ClawMax(G):
		#is there a 5-clique in the complement of the neighborood
		for n in G.nodes():
			neib = list(G[n])
			compl = nx.complement(G.subgraph(neib))
			has_4_claw = False
			has_3_claw = False
			maxClique = list(nx.find_cliques(compl))
			print(maxClique)
			tailleClique = []
			for elem in maxClique:
				tailleClique.append(len(elem))
			#nx.draw(maxClique)
			#plt.show()
			if(max(tailleClique)==3):
				return True
		return False
	 


#n = 15
#http://www.jaist.ac.jp/~uehara/graphs/

#saw = set()

if len(sys.argv) < 2:
		print("Usage python2 script fileWithIntervalGraphs")
		sys.exit()



#f = open("interval_disconnected_9.txt", "r")
f = open(sys.argv[1], "r")
newFile = open("filesWithAllIntervalGraphs/Test.txt", "w")
nbTested=1
for l in f:
	arr = l.split()
	#print (arr)

	pos = {}
	i = 0
	for a in arr:
		if a in pos:
			pos[a] = (pos[a],i)
		else:
			pos[a] = i
		i += 1


	G = nx.Graph()

     #vertex <-> pair of i in the array
     #edge uv <-> u and v are interleaved

	for i in pos:
		first,second = pos[i][0], pos[i][1]
		for j in range(first+1,second):
			G.add_edge(i,arr[j])
	
	if(nbTested%10000 == 0):
		print("NB ", nbTested, "initial array ", arr)
	nbTested+=1

     

	if not has3ClawMax(G) and len(G.edges())>0:
		print("WILL SOLVE !", G.edges())
		newFile.write(l)
		#CODE
	#else:
		
		#print("has a 5 claw, continue")