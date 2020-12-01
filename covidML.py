import random
from deap import creator, base, tools, algorithms
import os
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime

def main():
    np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)    
    ## Below added by BPU from TestDFforML.py script
    df = pd.read_csv("mlTestData.csv")
    # Show all ISO_CODEs
    # codes = df
    # ['iso_code'].unique()
    # codes

    # print('Number of ISO Codes:',len(codes))
    
    codes = df['iso_code'].unique()
    # create a list of column names, then strip extra spaces and convert to upper case
    cols = list(df.columns)
    cols = [x.upper().strip() for x in cols]
    df.columns = cols
    #print(df.head(0))
    
    # Convert date column to date/time type
    df['DATE'] = pd.to_datetime(df['DATE'])
    # print(type(df['DATE'][0]))

    df = df.set_index('ISO_CODE')
    #df.head()
   
    # Now that the only NaN values are at the start of each country's rows, remove all rows with NaN in Total_Cases
    df = df.dropna(subset=['TOTAL_CASES'])
    # Now clean up the international and world data
    df = df.dropna(subset=['CONTINENT'])
    #for c in cols:
        #print(c)
    # Fill in missing values using ffill; leading NaN values will NOT be replaced
    codes = (df.index.unique())
    for alpha in range(len(codes)):
        print('Processing ', codes[alpha])
        df.loc[codes[alpha]] = df.loc[codes[alpha]].fillna(method='ffill')
    
    # Create Series of max values for each column in df
    max_vals = df.max(axis=0)
    print('Max GDP: ', max_vals['GDP_PER_CAPITA'])
    print('Max Pop Dens: ', max_vals['POPULATION_DENSITY'])
    
    # Write df to a csv file
    #df.to_csv(data_dir+'testout.csv',index=False)
    
    ## End BPU additions
    
    os.system("pause")
    PopS=10
    NGEN=10 #number of generartions to run
    #start of ml
    factors = ["GDP_PER_CAPITA", "POPULATION_DENSITY"] #not sure how this will work, but I would like these to contain the headers of the data set or some other way of referencing what we are using as factors
    degree = 3
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax) 
    toolbox = base.Toolbox()
    def genRan(): #sets intial weight to random vaule between -1 and 1
        return ((random.random()-.5)*2) #fix

    toolbox.register("Alpha", genRan)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.Alpha, n=(degree)*len(factors))#sets up weights in an indviaul based on the degree of the formuala and the number of factors
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    #above code lays the ground work for individual and the population setup for the ml proccess
    population = toolbox.population(n=PopS)

    

    def predictor(individual, ISO): #this function should take an indviudal and return the predicted value for a given set of days
        #y=P((w0)b + (w1)T+ (w2)T2+ (w3)T3)
        rArray = [df.loc[ISO].head(1)['TOTAL_CASES']] #array of predicted values
        T = len(df.loc[ISO].head()['TOTAL_CASES'])
        for i in range(1, T):
           summ = df.loc[ISO].head(1)['TOTAL_CASES']
           for j in range(len(factors)):
               for k in range(degree):
                  summ += individual[(j*degree)+k]*math.pow(i,k+1)*(df.loc[ISO].head(1)[factors[j]]/max_vals[factors[j]])
                  #      weignt                   time                      indiviual factor
           rArray.append(int(df.loc[ISO].head(1)['POPULATION'][0])*summ[0])
        return (rArray)

    def eval(individual): # this function will be our eval function, aka the fitness function, the closer to zero the better
        tester = 0
        for i in codes:
            actual = df.loc[i].head()['TOTAL_CASES']
            predicted = predictor(individual, i)
            tester -= sum(abs(actual-predicted)/actual)
        return(tester)

    low1 = []
    up1 = []
    for i in range(degree*len(factors)):
        low1.append(-1)
        up1.append(1)
    toolbox.register("evaluate", eval) #lets the code recgognize what our eval/fitness function is 
    toolbox.register("mate", tools.cxBlend, alpha = .05) #sets up mate to produce a new individual with blended weights
    toolbox.register("mutate", tools.mutPolynomialBounded, eta = .2, low=low1, up = up1, indpb=0.5) # sets up mutation chance during mate procces
    toolbox.register("select", tools.selTournament, tournsize=PopS) #Seems best to have this match popsize
    #Above code block sets up info need for ml procces
    print("ML Proccess started")
    
    for gen in range(NGEN):
        offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.25) #cxpd is mating chance and mutpb is the chance of mutation
        fits = toolbox.map(toolbox.evaluate, offspring)
        for fit, ind in zip(fits, offspring):
            ind.fitness.values = fit
        top = tools.selBest(population, k=1) #saves the best of each gen to top, no use now but may be useful for internal stats later
        fts ="\t"
        for j in range(len(factors)):
                fts+=factors[j]+': \t'
                for k in range(degree):
                   fts += str(top[0][(j*degree)+k])+" "
                fts= fts + "\n\t"
        print(str(gen+1)+": "+fts)
        population = toolbox.select(offspring, k=len(population))
    #above code is where the ml proccess occurs the larger the pops and the more gens the better results will be typically

if __name__ == "__main__":
    main()
