import random
from deap import creator, base, tools, algorithms
import os
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def main():
    factors = ["GDP", "Strignecy","PopDen"] #not sure how this will work, but I would like these to contain the headers of the data set or some other way of referencing what we are using as factors
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax) 
    toolbox = base.Toolbox()
    def genRan():
        return (random.random())
    toolbox.register("Alpha", genRan)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.Alpha, n=4*len(factors))
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    #above code lays the ground work for individual and the population setup for the ml proccess

    def predictor(individual, T): #this function should take an indviudal and return the predicted value for a given set of days
        return (0)

    def eval(individual): # this function will be our eval function, aka the fitness function, the closer to zero the better
        return(0)

    toolbox.register("evaluate", eval)
    toolbox.register("mate", tools.cxBlend, alpha = .05)
    toolbox.register("mutate", tools.mutPolynomialBounded, eta = .2, low=[0,0], up = [1,1], indpb=0.5)
    toolbox.register("select", tools.selTournament, tournsize=100)
    #Above code block sets up info need for ml procces

    NGEN=100
    for gen in range(NGEN):
        offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.25)
        fits = toolbox.map(toolbox.evaluate, offspring)
        for fit, ind in zip(fits, offspring):
            ind.fitness.values = fit
        population = toolbox.select(offspring, k=len(population))
        
if __name__ == "__main__":
    main()