import networkx as network

graph = network.read_edgelist("EdgesList.txt", create_using=network.DiGraph())
pageRank = network.pagerank(graph, alpha=0.85, personalization=None, max_iter=30, tol=1e-06, nstart=None, weight='weight', dangling=None)
with open("external_pageRankFile.txt", "w") as output:
    for pid in pageRank:
        output.write([path_to_data]+pid+"="+str(pageRank[pid])+"\n")
