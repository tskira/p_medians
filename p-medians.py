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

def generate_assigment_points(size_apl, medians, distance_from_medians, assigment_priority_list):
     for i in size_apl:
        for j in medians:
            bisect.insort(distance_from_medians[i], list((nodes_distances[i][j], j)))
        bisect.insort(assigment_priority_list, list((distance_from_medians[i][1][0] - distance_from_medians[i][0][0], i, distance_from_medians[i][1][1])))
 
def assignment(target_medians):
    medians = list(target_medians).copy()
    size_apl = [i for i in range(info[0])]
    distance_from_medians = [list() for x in range(info[0])]
    assigment_priority_list = list()
    points_assignment = [-1 for i in range(info[0])]
    medians_capacity = [(points[i][2] - points[i][3]) for i in range(info[0])]
    print(target_medians)

    for i in medians:
        size_apl.remove(i)

    generate_assigment_points(size_apl, medians, distance_from_medians, assigment_priority_list)    

    while(size_apl):
        for i in assigment_priority_list:
            if (medians_capacity[i[2]] - points[i[1]][3] >= 0):
                medians_capacity[i[2]] -= points[i[1]][3]
                points_assignment[i[1]] = i[2]
                print(size_apl)
                print(i[1])
                print(medians)
                size_apl.remove(i[1])

        if(medians_capacity[i[2]] == 0):
            medians.remove(i[2])

        assigment_priority_list.clear()
        generate_assigment_points(size_apl, medians, distance_from_medians, assigment_priority_list)    
    print(points_assignment)

population = set()  
info = (tuple(map(int, input().split())))
nodes_distances = [[0 for x in range(info[0])] for y in range(info[0])] 
points = [0 for x in range(info[0])]

for i in range(info[0]):
    points[i] = (list(map(int, input().split())))

for i in range(info[0]):
    for j in range(info[0]):
        if(i != j):
            nodes_distances[i][j] = euclidean_distance((points[i][0]),(points[j][0]),(points[i][1]),(points[j][1]))

init_population(info[0], info[1])
assignment(list(population)[0])