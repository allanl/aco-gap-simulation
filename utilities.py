
def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

def calc_max_pheromones(evaporation_rate, best_path_length):
    return (1000.0 / (1 - evaporation_rate)) * (1.0 / best_path_length)

def evaporate_pheromones(evaporation_rate, pheromones):
    return int((1 - evaporation_rate) * pheromones)
