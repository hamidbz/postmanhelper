from random import random, randint, sample



""" this class is the implementation of genetic algorithm
    for finding the optimal path in a graph.
"""
class GA:
    def __init__(self, population_size:int, number_of_nodes:int,
                  mutation_rate:float, crossover_rate:float,
                 iterations:int ,graph_nodes:list, start, end,
                   fitness_function):
        self.population_size = population_size
        self.number_of_nodes = number_of_nodes 
        self.pc = crossover_rate
        self.pm = mutation_rate
        self.iterations = iterations
        self.nodes_list = graph_nodes 
        self.population = None # this is our population matrix. size number of nodes x 1
        self.goal = []
        self.goal_cost = 0
        self.start = start
        self.end = end
        self.fit_func = fitness_function
        self.fits = [0 for _ in range(self.population_size)]


    """this function initilize a matrix with random paths in a graph.
        each path is a list. each list is a sequence of nodes. in the end
         it returns a matrix(list of lists).

    """
    def initial_population(self)->list:
        p = []
        for _ in range(self.population_size):
            choromosome = self.random_path()
            p.append(choromosome)
        return p


    # generates a random path, this path is a sequence of nodes then returns it as a list
    # output: a list of nodes
    def random_path(self)->list:
        l = self.nodes_list.copy()
        l.remove(self.start)
        l.remove(self.end)
        r = [self.start]
        path_size = randint(0, self.number_of_nodes-2)
        r = r + sample(l, path_size)
        r.append(self.end)
        return r


    # this function calls  fitness function for each chromosome and saves it in fits list
    def calculate_fitness(self):
        for i in range(self.population_size):
            fit = self.fit_func(self.population[i])
            self.fits[i] = fit
            self.update_goal(fit, i)


    # this function does the roulet wheel phase and return the mating pool(parents matrix)
    def roulete_wheel(self):
        total = sum(self.fits)
        chances = [0 for _ in range(self.population_size)]
        s = 0
        for i in range(self.population_size):
            chances[i] = s + self.fits[i] / total
        
        parents = []
        for i in range(self.population_size):
            r = random()
            idx = 0
            for j in range(self.population_size):
                if chances[j] > r:
                    idx = j
                    break
            parents.append(self.population[idx])
        return parents

            
    def crossover(self, parents):
        """ input: parents matrix from roulete wheel phase(a list of lists)
            output: childs matrix(a list of lists)
            this method applies the crossover phase to the selected parents.
            it swap the second half of selected parents.
        """
        child_matrix = []
        i = 0

        while i < self.population_size:
            if self.pc > random():
                child_matrix.append(parents[i])
                i += 1
                child_matrix.append(parents[i])
                i += 1
            else:
                h1 = len(parents[i])
                h2 = len(parents[i+1])
                child1 = parents[i][:h1] + parents[i+1][h2:]
                child2 = parents[i+1][:h2] + parents[i][h1:]
                i+= 2
                child_matrix.append(child1)
                child_matrix.append(child2)
        return child_matrix
    
    
    def mutation(self, childs):
        """ input: childs matrix from crossover phase(a list of lists).
            output: none
        this method aplies the mutation phase on the
            childs matrix(output of the crossover phase).
            after that, it replace the result matrix to the
            population matrix
        """
        for i in childs:
            if self.pm > random():
                i = self.random_path()
        
        self.population = childs
    

    def update_goal(self, fit, i):
        """ input: fit as selsected fitness value, i as the number of selected node.
            output: none.
            this function just check that the given fitness value
            is better than goal or not, if it's better, it replace the goal
            with the given nodes(i).
        """
        if self.goal_cost < fit:
            self.goal = self.population[i]

    
    # this function runs steps of algorithm one time
    def run(self):
        
        for _ in range(self.iterations):
            self.calculate_fitness()
            parents = self.roulete_wheel()
            childs = self.crossover(parents)
            self.mutation(childs)
    

    """ we use this function to run the algorithm. this function
        runs the steps of genetic algorithm several times. this will increase the
        chance of finding the optimal path. in the end it 
        returns a list(sequnce of the nodes of optimal path)
        output: list
    """
    def main(self):
        self.population = self.initial_population()
        for _ in range(10):
            self.run()
        if self.goal == None:
            return []
        else:
            return self.goal , self.goal_cost
