import random
import math
import numpy
from itertools import combinations
# Set parameters
t = 2
v = 2

combinations = [(0,0), (0,1), (1,0), (1,1)]
domain = set(range(v))



# Initialize matrix
def initialize_matrix(k,N):
    return [[random.choice(list(domain)) for j in range(k)] for i in range(N)]



# Objective function
def objective_function(matrix):
    total_missing = 0
    for subset in range(N):
        covered = set()
        for comb in combinations:
            if comb in covered:
                continue
            comb_missing = True
            for j in range(k):
                if matrix[subset][j] == comb[0] or matrix[subset][j] == comb[1]:
                    comb_missing = False
                    break
            if not comb_missing:
                covered.add(comb)
        total_missing += len(combinations) - len(covered)
    return total_missing



# Neighborhood function
def neighborhood_function(matrix):
    i = random.randint(0, N-1)
    j = random.randint(0, k-1)
    neighbor_matrix = [row[:] for row in matrix]
    for symbol in domain:
        if symbol != matrix[i][j]:
            neighbor_matrix[i][j] = symbol
            yield neighbor_matrix



# Simulated annealing function
def simulated_annealing(k,N):
    # Initialize solution
    temp = math.comb(k,t)
    phi = int(pow(v,t)*temp)
    solution = initialize_matrix(k,N)
    best_solution = solution
    # Initialize temperature and cooling rate
    temperature = k
    cooling_rate = 0.99
    # Initialize iteration counter and frozen factor counter
    iteration = 0
    frozen_factor = 0
    # Run simulated annealing
    while temperature >random.random() and frozen_factor < phi:
        # Choose a neighbor solution randomly
        iteration+=1
        for neighbor_solution in neighborhood_function(solution):
            
            # Calculate the energy difference between the current solution and the neighbor solution
            current_energy = objective_function(solution)
            neighbor_energy = objective_function(neighbor_solution)
            energy_difference = current_energy - neighbor_energy
            # Accept the neighbor solution if it has lower energy or with a certain probability
            if energy_difference < 0 or math.exp(-energy_difference/temperature) > random.uniform(0,1):
                solution = neighbor_solution
                if neighbor_energy < objective_function(best_solution):
                    best_solution = neighbor_solution
                break
        # Decrease temperature
        temperature *= cooling_rate
        # Check if the best solution has not improved for phi consecutive temperature decrements
        if solution == best_solution:
            frozen_factor += 1
        else:
            frozen_factor = 0
        # Increment iteration counter
    # Return the best solution and the number of iterations performed
    if objective_function(best_solution) == 0:
        return best_solution, iteration, "solution"
    elif frozen_factor == phi:
        return None, iteration, "frozen"
    else:
        return best_solution, iteration, "final temperature achieved"
    
# Run simulated annealing for each value of k in the domain

f=open("output.txt","w")
for k in range(5, 8):
    N=k
    flag = []
    f.write("For k:")
    f.write(str(k))
    for a in range(0,30):  
        print(f"k = {k}")
        ca, iterations, stop_criterion = simulated_annealing(k,N)
        flag.append(iterations)
        if ca is None:
            print("The algorithm could not find a CA.")
        else:
            print("The algorithm found a CA:")
            for row in ca:
                f.write(str(row))
                f.write("\n")
            f.write("\n")
        print(f"Number of iterations: {iterations}")
        print(f"Stop criterion: {stop_criterion}")
    print("Average number of iterations:",numpy.average(flag))
f.close()
