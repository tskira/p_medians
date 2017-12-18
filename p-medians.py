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

def generate_assigment_points(size_apl, medians, distance_from_medians, assigment_priority_list, capacity_medians):
    distance_from_medians = [list() for i in range(info[0])]

    for i in size_apl:
        for j in medians: 
            if(capacity_medians[j] - points[i][3] >= 0):
                bisect.insort(distance_from_medians[i], list((nodes_distances[i][j], j)))
    
        first_median = -1
        second_median = -1
        count = 0
        while ((first_median == -1 or second_median == -1) and count <= len(medians)):
            if (first_median == -1):
                if(capacity_medians[distance_from_medians[i][count][1]] - points[i][3] >= 0):
                    first_median = count
                    count += 1
            if(first_median != -1 and second_median == -1):
                if(capacity_medians[distance_from_medians[i][count][1]] - points[i][3] >= 0):
                    second_median = count
            count += 1
        bisect.insort(assigment_priority_list, list((distance_from_medians[i][second_median][0] - distance_from_medians[i][first_median][0], i, distance_from_medians[i][second_median][1], distance_from_medians[i][first_median][1])))
    

def assignment(target_medians):
    medians = list(target_medians).copy()
    size_apl = [i for i in range(info[0])]
    points_assignment = [-1 for i in range(info[0])]
    capacity_medians = [(points[i][2] - points[i][3]) for i in range(info[0])]
    distance_from_medians = [list() for i in range(info[0])]
    assignment_priority_list = list()

    for i in medians:
        size_apl.remove(i)
        
    generate_assigment_points(size_apl, medians, distance_from_medians, assignment_priority_list, capacity_medians)
    
    while(size_apl):
        for i in reversed(assignment_priority_list):
            if (capacity_medians[i[3]] - points[i[1]][3] >= 0):
                capacity_medians[i[3]] -= points[i[1]][3]
                if(capacity_medians[i[3]] == 0):
                    medians.remove(i[3])
                points_assignment[i[1]] = i[3]
                size_apl.remove(i[1])

        assignment_priority_list.clear()
        generate_assigment_points(size_apl, medians, distance_from_medians, assignment_priority_list, capacity_medians)
    
    return points_assignment

def chromosome_evaluation(resp):
    evaluation = 0
    for i in range(info[0]):
        if (resp[i] != -1):
            evaluation += nodes_distances[i][resp[i]]
    return evaluation

def selection(target_population):
    w = [(1/population_evaluation[i]) for i in range(p_size)]
    


population = set()  
info = (tuple(map(int, input().split())))
nodes_distances = [[0 for x in range(info[0])] for y in range(info[0])] 
points = [0 for x in range(info[0])]
p_size = population_size(info[0], info[1])
population_evaluation = [0 for i in range(p_size)]
tournament_size = int(p_size * 0.1)

for i in range(info[0]):
    points[i] = (list(map(int, input().split())))

for i in range(info[0]):
    for j in range(info[0]):
        if(i != j):
            nodes_distances[i][j] = euclidean_distance((points[i][0]),(points[j][0]),(points[i][1]),(points[j][1]))

init_population(info[0], info[1])

for i in range(len(population)):
    population_evaluation[i] = chromosome_evaluation(assignment(list(population)[i]))

a = [1 ,2, 3, 4]
print(a)
print(random.choices(a, weights=[10,20,30,40], k=4))
selection(population)
