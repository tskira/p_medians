import math
import random
import bisect

def number_combinations(n, p):
    f = math.factorial
    return (f(n)//f(p)//f(n-p))

def population_size(n, p):
    d = math.ceil(n/p)
    return ((max (2, math.ceil((n/100)*((math.log(number_combinations(n,p)))/d))))*d)

def euclidean_distance(x0,x1,y0,y1):
    return(math.sqrt(((x0 - x1)*(x0 - x1)) + ((y0 - y1)*(y0 - y1))))

def init_population(n, p):
    k = population_size(n,p)//math.ceil(n/p)
    new_chromosome = set()
    for i in range(n//p):
        for j in range(p):
            new_chromosome.add((i * p + j) % n)
        population.add(tuple(new_chromosome))
        new_chromosome.clear()
    count = 0
    for i in range(n//p):
        for j in range(p):
            new_chromosome.add((count % n))
            count += k
            if (count >= n):
                count = (count % n) + 1
        population.add(tuple(new_chromosome))
        new_chromosome.clear()
    while(len(population) < population_size(n,p)):
        fill_chromossome = set()
        while(len(fill_chromossome) < p):
            fill_chromossome.add(random.randint(0, n - 1))
        population.add(tuple(fill_chromossome))
        fill_chromossome.clear()



population = set()  
info = (tuple(map(int, input().split())))
points = [0 for x in range(info[0])]
priority_nodes = [list() for x in range(info[0])]
count = 0
nodes_distances = [[0 for x in range(info[0])] for y in range(info[0])] 
assigment_urgencies = list()

for i in range(info[0]):
    points[i] = (list(map(int, input().split())))

for i in range(info[0]):
    for j in range(info[0]):
        if(i != j):
            nodes_distances[i][j] = euclidean_distance((points[i][0]),(points[j][0]),(points[i][1]),(points[j][1]))
            bisect.insort(priority_nodes[i], list((nodes_distances[i][j], j)))

for i in range(info[0]):
    bisect.insort(assigment_urgencies, list((priority_nodes[i][1][0] - priority_nodes[i][0][0], priority_nodes[i][1][1])))



init_population(info[0], info[1])
