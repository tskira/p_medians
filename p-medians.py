import math

def number_combinations(n, p):
    f = math.factorial
    return (f(n)//f(p)//f(n-p))

def population_size(n, p):
    d = math.ceil(n/p)
    return ((max (2, math.ceil((n/100)*((math.log(number_combinations(n,p)))/d))))*d)

def init_population(n, p):
    k = population_size(n,p)//math.ceil(n/p)
    for i in range(population_size(n, p)// info[1]):
        print(i)

points = {}
population = set()
info = (tuple(map(int, input().split())))
print(info)
count = 0
for i in range(info[0]):
    points.update({i : (tuple(map(int, input().split())))})

init_population(info[0], info[1])