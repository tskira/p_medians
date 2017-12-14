import math

def number_combinations(n, p):
    f = math.factorial
    return (f(n)//f(p)//f(n-p))

def population_size(n, p):
    d = math.ceil(n/p)
    return ((max (2, math.ceil((n/100)*((math.log(number_combinations(n,p)))/d))))*d)

def init_population(n, p):
    k = population_size(n,p)//math.ceil(n/p)
    new_chromosome = set()
    for i in range(population_size(n, p)// info[1]):
        for j in range(info[1]):
            new_chromosome.add((i * info[1] + j) % info[0])
        population.add(tuple(new_chromosome))
        new_chromosome.clear()
    for i in range(population_size(n,p)//info[1]):
        for j in range(10):
            print("")
    print(population)        
        

points = {}
population = tuple()  
info = (tuple(map(int, input().split())))
print(info)
count = 0
for i in range(info[0]):
    points.update({i : (tuple(map(int, input().split())))})

init_population(info[0], info[1])