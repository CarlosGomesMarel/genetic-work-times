from collections import namedtuple
from functools import partial
from random import choices, randint, randrange, random
from typing import List, Optional, Callable, Tuple

from csv_utility import convert_input_data

csv_file_path = r'input_data.csv'
_, input_hours = convert_input_data(csv_file_path)

Genome = List[int]
Population = List[Genome]
PopulateFunc = Callable[[], Population]
FitnessFunc = Callable[[Genome], int]
SelectionFunc = Callable[[Population, FitnessFunc], Tuple[Genome, Genome]]
CrossoverFunc = Callable[[Genome, Genome], Tuple[Genome, Genome]]
MutationFunc= Callable[[Genome], Genome]

PrinterFunc = Callable[[Population, int, FitnessFunc], None]

Thing = namedtuple('Thing', ['name', 'value'])

def generate_genome(length: int):
    return choices([0,1], k=length)

def maxHours(genome, count: int = 5):
    while sum(genome) > count:
        idx = randint(0, len(genome) - 1)
        genome[idx] = 0
    return genome

def generate_population(size: int, genome_length: int) -> Population:
    return [generate_genome(genome_length) for _ in range(size)]

def fitness(genome: Genome, hours) -> int:
    if len(genome) != len(hours):
        raise ValueError("genome and things must be of the same length")

    if (sum(genome) > 5):
        print('Too long', sum(genome), genome)

    value = 0

    for i, thing in enumerate(hours):
        if genome[i] == 1:
            #print(int(sum(thing)/len(thing)), sum(thing)/len(thing))
            value += int(sum(thing)/len(thing))

    return value

def selection_pair(population: Population, fitness_func: FitnessFunc) -> Population:
    return choices(
        population=population,
        weights=[fitness_func(genome) for genome in population],
        k=2
    )

def single_point_crossover(a: Genome, b: Genome) -> Tuple[Genome, Genome]:
    if len(a) != len(b):
        raise ValueError("Genome length must be the same length")

    length = len(a)
    if length < 2:
        return a, b

    p = randint(1, length - 1)
    return a[0:p] + b[p:], b[0:p] + a[p:]

def mutation(genome: Genome, num: int = 1, probability: float = 0.5) -> Genome:
    for _ in range(num):
        index = randrange(len(genome))
        genome[index] = genome[index] if random() > probability else abs(genome[index] - 1)
    return genome

def genome_to_string(genome: Genome) -> str:
    return "".join(map(str, genome))

def population_fitness(population: Population, fitness_func: FitnessFunc) -> int:
    return sum([fitness_func(genome) for genome in population])

def sort_population(population: Population, fitness_func: FitnessFunc) -> Population:
    return sorted(population, key=fitness_func, reverse=True)

def print_stats(population: Population, generation_id: int, fitness_func: FitnessFunc):
    print("GENERATION %02d" % generation_id)
    print("=============")
    print("Population: [%s]" % ", ".join([genome_to_string(gene) for gene in population]))
    print("Avg. Fitness: %f" % (population_fitness(population, fitness_func) / len(population)))
    sorted_population = sort_population(population, fitness_func)
    print(
        "Best: %s (%f)" % (genome_to_string(sorted_population[0]), fitness_func(sorted_population[0])))
    print("Worst: %s (%f)" % (genome_to_string(sorted_population[-1]),
                              fitness_func(sorted_population[-1])))
    print("")

    return sorted_population[0]

def to_string(things: List[Thing]):
    return f"[{', '.join([t.name for t in things])}]"

def value(things: List[Thing]):
    return sum([t.value for t in things])

def print_knap_stats(things: List[Thing]):
    print(f"Things: {to_string(things)}")
    print(f"Value {value(things)}")

def run_evolution(
    populate_func: PopulateFunc,
    fitness_func: FitnessFunc,
    fitness_limit: int,
    selection_func: SelectionFunc = selection_pair,
    crossover_func: CrossoverFunc = single_point_crossover,
    mutation_func: MutationFunc = mutation,
    generation_limit: int = 100
) -> Tuple[Population, int]:

    population = populate_func()
    population = [maxHours(genome) for genome in population]

    for i in range(generation_limit):
        population = sorted(
            population,
            key = lambda genome: fitness_func(genome),
            reverse=True
        )

        if fitness_func(population[0]) >= fitness_limit:
            break

        next_generation = population[0:2]

        for j in range(int(len(population) / 2) -1 ):
            parents = selection_func(population, fitness_func)
            offspring_a, offspring_b = crossover_func(parents[0], parents[1])
            offspring_a = maxHours(mutation_func(offspring_a))
            offspring_b = maxHours(mutation_func(offspring_b))
            next_generation += [offspring_a, offspring_b]

        population = next_generation

    population = sorted(
        population,
        key = lambda genome: fitness_func(genome),
        reverse=True
    )

    return population, i

def from_genome(genome: Genome, things: List[Thing]) -> List[Thing]:
    result = []
    for i, thing in enumerate(things):
        if genome[i] == 1:
            result += [thing]

    return result

population, generations = run_evolution(
    populate_func=partial(
        generate_population, size=10, genome_length=len(input_hours)
    ),
    fitness_func=partial(
        fitness, hours=input_hours
    ),
    fitness_limit=1310,
    generation_limit=100
)

print(generations, population[0])
