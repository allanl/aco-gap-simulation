
def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

def calc_max_pheromones(evaporation_rate, best_path_length):
    return int((1000.0 / (1 - evaporation_rate)) * (1.0 / best_path_length))

def calc_min_pheromones(max_pheromones, number_connections,
        num_steps, best_path_prob):
    # formula: (tau_{max} * (1 - \sqrt[n]p_{best})) / ((num_conn - 1) *
    # \sqrt[n]p_{best})
    # chose not to reduce number of connections by 1 to avoid divide by 0
    nth_root = calc_nth_root(best_path_prob, num_steps)
    dividend = max_pheromones * (1.0 - nth_root)
    # increment divisor by 1 to prevent divisor being less than 1
    # and so min_ph potentially being higher than max_ph
    divisor = number_connections * nth_root + 1
    return int(dividend / divisor)

def calc_nth_root(number, root):
    if root == 0: root = 1
    return number ** (1.0 / root)

def get_base_min_pheromones(max_pheromones):
    # return constant relative to base_pheromone to save processing
    # add 1 to ensure at least possible to follow path
    return int(max_pheromones / 20) + 1

def evaporate_pheromones(evaporation_rate, pheromones):
    return int((1 - evaporation_rate) * pheromones)
