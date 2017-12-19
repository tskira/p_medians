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
        count = -1

        while((first_median == -1 or second_median == -1) and count < len(distance_from_medians[i])):            
            count += 1
            if (first_median == -1 and count < len(distance_from_medians[i])):
                if(capacity_medians[distance_from_medians[i][count][1]] - points[i][3] >= 0):
                    first_median = count
                    count += 1
                    
            if(first_median != -1 and second_median == -1 and count < len(distance_from_medians[i])):
                if(capacity_medians[distance_from_medians[i][count][1]] - points[i][3] >= 0):
                    second_median = count
        if(second_median == -1 or first_median == -1):
            return -1
        else:
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
        a = generate_assigment_points(size_apl, medians, distance_from_medians, assignment_priority_list, capacity_medians)
        if (a == -1):
            b = [0 for i in range(info[0])]
            return(b)
    return points_assignment

def chromosome_evaluation(resp):
    evaluation = 0
    for i in range(info[0]):
        if (resp[i] != -1):
            evaluation += nodes_distances[i][resp[i]]
    return evaluation

def selection(population):
    target_population = list(population).copy()
    w = list()
    selected_parents = list()
    tournament = list()
    evaluation_next_population = [0 for x in range(len(population))]
    for i in range(len(population)):
        evaluation_next_population[i] = chromosome_evaluation(assignment(list(population)[i]))
    best_fitness = min(evaluation_next_population)
    better = evaluation_next_population.index(best_fitness)
    selected_parents.append(list(population)[better])
    while(len(selected_parents) < int(0.6 * p_size)):
        w = [0 for x in range(len(target_population))]
        for i in range(len(target_population)):        
            w[i] = (1 / chromosome_evaluation(assignment(target_population[i])))
        ranking = random.choices(target_population, weights = w, k = 2)
        for i in range(len(ranking)):
            bisect.insort(tournament, list((chromosome_evaluation(assignment(ranking[i])), ranking[i])))
        if(tournament[0][1] not in selected_parents):
            selected_parents.append(tournament[0][1])
            target_population.remove(tournament[0][1])
        tournament.clear()
        w.clear()
 
    return(selected_parents)

def crossover(next_population):
    next_generation = list()
    evaluation_next_population = [0 for x in range(len(next_population))]
    for i in range(len(next_population)):
        evaluation_next_population[i] = chromosome_evaluation(assignment(list(next_population)[i]))
    best_fitness = min(evaluation_next_population)
    better = evaluation_next_population.index(best_fitness)
    next_population.append(list(population)[better])
    while(len(next_generation) + len(next_population) < p_size):
        parents = random.choices(next_population, k = 2)
        set_parent1 = set(parents[0])
        set_parent2 = set(parents[1])
        new_e1 = set({})
        new_e2 = set({})
        e1 = set_parent1.difference(set_parent2)
        e2 = set_parent2.difference(set_parent1)
        if(not e1):
            if(e2 in next_population):
                next_population.remove(set_parent2)
        else:
            k1 = random.randint(0, len(e1) - 1)
            for i in range(k1):
                new_e1.add(list(e1)[i])
            count = 0
            while(len(new_e1) < info[1]):
                new_e1.add(list(set_parent2)[count])
                count += 1
            k2 = random.randint(0, len(e2) - 1)
            for i in range(k2):
                new_e2.add(list(e2)[i])
            count = 0
            while(len(new_e2) < info[1]):
                new_e2.add(list(set_parent1)[count])
                count += 1
        if (new_e1):
            if ((new_e1 not in next_generation) and new_e1 not in next_population):
                if(chromosome_evaluation(assignment(list(new_e1)))  <=  max(evaluation_next_population)):
                    next_generation.append(tuple(new_e1))
        if (new_e2):
            if((new_e2 not in next_generation) and (new_e2 not in next_population)):
                if(chromosome_evaluation(assignment(list(new_e2)))  <=  max(evaluation_next_population)):
                    next_generation.append(tuple(new_e2))

    for i in range(len(next_generation)):
        next_population.append(next_generation[i])
    return(next_population)
    
    #return (next_generation)

def hypermutation(population):
    target_population = list(population).copy()
    hypermutation_members = random.choices(target_population, k = int(p_size * 0.10))
    for i in hypermutation_members:
        best_current = i
        best_current_evalueted = 0
        for j in range(len(i)):
            apply_mutation = list(i).copy()
            before_mutation = chromosome_evaluation(assignment(i))
            for k in range(info[0]):
                if(k not in apply_mutation):
                    apply_mutation[j] = k
                if (chromosome_evaluation(assignment(apply_mutation)) > best_current_evalueted):
                    best_current = apply_mutation.copy()
                    best_current_evalueted = chromosome_evaluation(assignment(apply_mutation))
        if(i in target_population):
            target_population.remove(tuple(i))
        target_population.append(tuple(best_current))
    return(target_population)

def cap_p_med_ga(population_target):
    init_population(info[0], info[1])
    count = 0
    population_generation = list(population_target).copy()
    while (count < 10):
        for i in range(p_size):
            population_evaluation[i] = chromosome_evaluation(assignment(list(population_generation)[i]))
        #print(population_generation)
        print(min(population_evaluation))
        population_generation = selection(population_generation)
        population_generation = crossover(population_generation)
        population_generation = hypermutation(population_generation)

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

cap_p_med_ga(population)

'''
init_population(info[0], info[1])

assignment(list(population)[0])

for i in range(len(population)):
    population_evaluation[i] = chromosome_evaluation(assignment(list(population)[i]))
print(selection(population))
a = crossover(selection(population))
print(crossover(selection(population)))
print(chromosome_evaluation(assignment(hypermutation(crossover(selection(population)))[random.randint(0,p_size -1)])))
'''