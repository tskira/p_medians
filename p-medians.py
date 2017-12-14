import math
import random

def number_combinations(n, p):
    f = math.factorial
    return (f(n)//f(p)//f(n-p))

def population_size(n, p):
    d = math.ceil(n/p)
    return ((max (2, math.ceil((n/100)*((math.log(number_combinations(n,p)))/d))))*d)

def init_population(n, p):
    k = population_size(n,p)//math.ceil(n/p)
    new_chromosome = set()
    print(population_size(n,p))
    print(k)
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

    print(population)       
    print(len(population))
        

points = {}
population = set()  
info = (tuple(map(int, input().split())))
print(info)
count = 0
for i in range(info[0]):
    points.update({i : (tuple(map(int, input().split())))})

init_population(info[0], info[1])