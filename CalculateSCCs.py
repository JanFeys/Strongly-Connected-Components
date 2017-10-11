#coded in python3
import time

def load_graph(file_name, reverse):
    #Read in the graph data. Reverse may be true or false and reverses the edges.

    g = []
    f = open(file_name,'r')
    g_size = int(f.readline().strip())

    for _ in range(g_size):
        g.append(set())

    if reverse:
        for line in f:
            n1, n2 = line.strip().split(' ')
            n1, n2 = int(n1)-1, int(n2)-1
            g[n2].add(n1)
    else:
        for line in f:
            n1, n2 = line.strip().split(' ')
            n1, n2 = int(n1)-1, int(n2)-1
            g[n1].add(n2)
    f.close()
    return g

def DFS_run(g,vs,start,rev_path):
    #This function executes DFS from the starting node, for as long as possible, avoiding nodes in v.
    
    #g is the graph, given by a list of sets of edges
    #vs are the visited nodes, given as a list of logicals
    #start is the starting node
    #rev_path is the path that was followed, in reverse
    
    dfs_stack = []
    dfs_stack.append(start)

    while (len(dfs_stack)>0):
        current = dfs_stack.pop()

        if current not in vs:
            rev_path.append(current)
            vs.add(current)
            for new in g[current]:
                if (new not in vs):
                    dfs_stack.append(new)
    return vs, rev_path

def DFS_fts(g):
    #This routine calculates finishing times (FT).
    
    fts = dict()
    vs = set()
    
    current_ft = 1
    start_id = len(g)-1

    while (True):
        rev_path = []
        DFS_run(g,vs,start_id,rev_path)
        for i in range(len(rev_path)-1,-1,-1):
            fts[rev_path[i]] = current_ft
            current_ft += 1

        while (start_id>=0) and (start_id in vs):
            start_id = start_id - 1

        if (start_id<0):
            break
    return fts

def DFS_ls(g,fts):
    #This routine calculates leaders.
    
    ls = dict()
    vs = set()
    l_freqs = dict()
    
    inverse_fts = {v: k for k, v in fts.items()}

    start_ft = len(g)
    start_id = inverse_fts[start_ft]

    while (True):
        rev_path = []
        DFS_run(g,vs,start_id,rev_path)
        for i in range(len(rev_path)):
            ls[rev_path[i]] = start_ft
        l_freqs[start_ft-1] = len(rev_path)

        while start_ft >=1 and (inverse_fts[start_ft] in vs):
            start_ft = start_ft - 1

        if (start_ft<1):
            break

        start_id = inverse_fts[start_ft]
    return ls, l_freqs

if __name__ == "__main__":
    file_name =  'SCCtestgraph.txt'

    start = time.time()
    
    g = load_graph(file_name, True)
    fts = DFS_fts(g)

    g = load_graph(file_name, False)
    ls, l_freqs = DFS_ls(g,fts)

    print('Frequency of top five most common leaders:')
    top_l_freqs = sorted(l_freqs,reverse=True)
    print(top_l_freqs[0:15])

    end = time.time()
    print(end - start)
