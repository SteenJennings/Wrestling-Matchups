# implementation of an undirected graph using Adjacency Lists
class Wrestler:
    """This modified class includes references from an adjanceny list class found on github
    this was the first result in searching for adjaceny list implementations in python and it was
    it fits the requirements well at this link https://github.com/joeyajames/Python/blob/master/graph_adjacency-list.py"""

    def __init__(self, name):
        self.name = name
        self.visited = "WHITE"         # used to track what we have visited
        self.parent_node = None      # will be update in BFS to navigate
        self.rivals = []
        self.distance = 0            # used to track our dist from source in BFS

    def add_rivals(self, w):
        if w not in self.rivals:
            self.rivals.append(w)

class Graph:
    #tracks the wrestlers in a "name":object dictionary
    wrestlers = {}
    def __init__(self):
        self.babyfaces = []
        self.heels = []         

    #this portion of the code was modified but borrowed from the github repo on adjacency lists
    def add_wrestler(self, wrestler):
        if isinstance(wrestler, Wrestler) and wrestler.name not in self.wrestlers:
            self.wrestlers[wrestler.name] = wrestler
            return True
        else:
            return False
        
    #adds a rivalry (edge) to the graph
    def add_rivalry(self, u, v):
        if u in self.wrestlers and v in self.wrestlers:
            #has to add the rivalry in both directions (to rival lists for each node)
            self.wrestlers[u].add_rivals(v)
            self.wrestlers[v].add_rivals(u)
            return True
        else:
            return False

    #tool used for testing
    def print_graph(self):
        for key in sorted(list(self.wrestlers.keys())):
            print(key + str(self.wrestlers[key].rivals))

    #utilizing bfs to search through the graph and update the nodes, while tracking depth
    def BFS(self, start_node):
        queue = []
        queue.append(start_node)
        while queue:
            wrestler_name = queue.pop(0)
            #for rival wrestler of the current wrestler (visit each edge of the current vertex)
            for wrestler in self.wrestlers[wrestler_name].rivals:
                if self.wrestlers[wrestler].visited == "WHITE":
                    queue.append(wrestler)
                    self.wrestlers[wrestler].visited = "GRAY"
                    self.wrestlers[wrestler].parent_node = wrestler_name
                    self.wrestlers[wrestler].distance = self.wrestlers[wrestler_name].distance + 1
            self.wrestlers[wrestler_name].visited = "BLACK"
        for wrestler in self.wrestlers:
            if self.wrestlers[wrestler].visited != "BLACK":    
                self.BFS(self.wrestlers[wrestler].name)
    

    #we are splittling the teams based on depth/distance because noone on the same depth can be on a team (rivalries would not align)
    def divide_teams(self):
        #we have to sort our data here to match the outputs exactly
        #since it's stored in the dict, we make it a list of keys, then sort the list
        for key in sorted(list(self.wrestlers.keys())):
            if self.wrestlers[key].distance % 2 == 0:
                self.babyfaces.append(key)
            else:
                self.heels.append(key)
    
    def print_teams(self):
        print("Yes Possible")
        print("Babyfaces: {}".format(" ".join(self.babyfaces)))
        print("Heels: {}".format(" ".join(self.heels)))
    
    #checks to make sure that no babyfaces and no heels have any "teammate rivals" which would break out rules
    def is_impossible(self):
        for babyface in self.babyfaces:
            for rival in self.wrestlers[babyface].rivals:
                if rival in self.babyfaces:
                    return True
        for heels in self.heels:
            for rival in self.wrestlers[heels].rivals:
                if rival in self.heels:
                    return True
        return False


g = Graph()
#reads our file input
with open("wrestler.txt") as inFile:
    num_wrestlers = inFile.readline()
    for wrestler in range(int(num_wrestlers)):
        wrestler = inFile.readline().rstrip()
        g.add_wrestler(Wrestler(wrestler))
            
    num_rivalries = inFile.readline()
    for matchup in range(int(num_rivalries)):
        matchup_list = inFile.readline().rstrip().split(" ")
        w1 = matchup_list[0]
        w2 = matchup_list[1]
        g.add_rivalry(w1, w2)
    inFile.close

#calling BFS on the first wrestler which, in our case is the first key in the dict of stored wrestlers
g.BFS(g.wrestlers[list(g.wrestlers.keys())[0]].name)
g.divide_teams()
if not g.is_impossible():
    g.print_teams()
else:
    print("Impossible")



