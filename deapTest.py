
import random
from deap import creator, base, tools, algorithms
import os


def main():
    m = random.random()
    b = random.random()
    print("y="+str(m)+"x+"+str(b))
    testCase = []
    SampleSize = 100
    for x in range(SampleSize):
        testCase.append(x*m+b)
    os.system("pause")
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    def genRan():
        return (random.random())
 
    toolbox.register("Alpha", genRan)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.Alpha, n=2)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    
    def eval2(individual):
        predCase = []
        for x in range(SampleSize):
            predCase.append(x*individual[0]+individual[1])
        evalCase = []
        for x in range(SampleSize):
            evalCase.append(abs(testCase[x]-predCase[x]))
        return 0 - sum(evalCase),
        
    def evalOneMax(individual):
       return sum(individual),


    toolbox.register("evaluate", eval2)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutPolynomialBounded, eta = .5, low=[0,0], up = [1,1], indpb=0.5)
    toolbox.register("select", tools.selTournament, tournsize=100)

    population = toolbox.population(n=1000)
    


    NGEN=1000
    for gen in range(NGEN):
        offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.5)
        fits = toolbox.map(toolbox.evaluate, offspring)
        for fit, ind in zip(fits, offspring):
            ind.fitness.values = fit
        population = toolbox.select(offspring, k=len(population))
        top = tools.selBest(population, k=1)
        bot = tools.selWorst(population, k=1)
        print(str(gen+1)+": " + str(top) +", " +str(bot))

    print("M off by " + str(m-top[0][0])+" and B off by " + str(b-top[0][1]))
   
   

if __name__ == "__main__":
    main()