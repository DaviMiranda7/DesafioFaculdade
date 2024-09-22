import random

class GeneticAlgorithm:
    def __init__(self, population_size=10, mutation_rate=0.01, generations=100, elitism=False, elite_fraction=0.2):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.elitism = elitism
        self.elite_fraction = elite_fraction
        self.population = self.initialize_population()

    def initialize_population(self):
        return [[random.randint(0, 1) for _ in range(20)] for _ in range(self.population_size)]

    def decode_chromosome(self, chromosome):
        # Convert binary to decimal in the range [-10, 10]
        decimal_value = int("".join(map(str, chromosome)), 2)
        return -10 + (decimal_value / (2**len(chromosome) - 1)) * 20

    def fitness(self, chromosome):
        x = self.decode_chromosome(chromosome)
        return -1 * (x**3 - 6 * x + 14)  # Minimizar f(x), então usamos o valor negativo

    def selection(self):
        # Seleção por torneio
        selected = []
        for _ in range(self.population_size):
            competitors = random.sample(self.population, 3)
            selected.append(max(competitors, key=self.fitness))
        return selected

    def crossover(self, parent1, parent2):
        point = random.randint(1, len(parent1) - 1)
        return parent1[:point] + parent2[point:]

    def mutation(self, chromosome):
        for i in range(len(chromosome)):
            if random.random() < self.mutation_rate:
                chromosome[i] = 1 - chromosome[i]  # Inverte o gene
        return chromosome

    def run(self):
        best_individuals = []
        for generation in range(self.generations):
            self.population = self.selection()
            new_population = []

            # Adiciona os melhores indivíduos se elitismo estiver ativado
            if self.elitism:
                elite_count = int(self.elite_fraction * self.population_size)
                elite_individuals = sorted(self.population, key=self.fitness, reverse=True)[:elite_count]
                new_population.extend(elite_individuals)

            while len(new_population) < self.population_size:
                parent1 = random.choice(self.population)
                parent2 = random.choice(self.population)
                child = self.crossover(parent1, parent2)
                new_population.append(self.mutation(child))

            self.population = new_population

            best = max(self.population, key=self.fitness)
            best_individuals.append((self.fitness(best), best))

        return best_individuals


# Exemplo de uso
ga = GeneticAlgorithm(population_size=10, mutation_rate=0.01, generations=100, elitism=True, elite_fraction=0.2)
result = ga.run()
print(result)
