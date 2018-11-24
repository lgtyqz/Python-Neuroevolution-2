import random
import math
from neuralNetwork import *
class Neural_Organism:
    def __init__(self, numInputUnits, numOutputUnits, numHidLayers, numHidUnits,
    name="", empty=False):
        self.chromosomes = []
        if not empty:
            self.chromosomes = [
                Neural_Network(numInputUnits, numOutputUnits, numHidLayers,
                numHidUnits, None, name), # C
                Neural_Network(numInputUnits, numOutputUnits, numHidLayers,
                numHidUnits, None, name) # D
            ]
        else:
            self.chromosomes = []
        self.name = name
        self.fitness = 0
        self.onChrom = 0
    
    def forwardPropagate(self, inputValues):
        # Random is too inconsistent.
##        r = random.random()
##        i = math.floor(r * len(self.chromosomes))
##        return self.chromosomes[i].forwardPropagate(inputValues)
        self.onChrom += 1
        self.onChrom %= 2
        return self.chromosomes[self.onChrom].forwardPropagate(inputValues)
    
    def generateGamete(self):
        # Meiosis lol
        gametes = []
        # First, provide template for crossed-over chromosomes
        for i in range(4):
            gametes.append(
            Neural_Network(
                self.chromosomes[0].numInputUnits,
                self.chromosomes[0].numOutputUnits,
                self.chromosomes[0].numHidLayers,
                self.chromosomes[0].numHidUnits,
                None,
                self.chromosomes[0].name)
            )
        # Crossing over: with chromosomes C and D, homo-chromes produced will be
        # C1, C2, D1, and D2. C1 and C2 will bind, and D1 and D2 will bind.
        # C1 and C2 are identical, as are D1 and D2.
        # C1 will cross over with D1, and C2 will cross over with D2.
        
        # Pick only the templates for crossing over to cross over with
        for N in range(0, len(gametes), 2): # N for Neural Net big boi
            # Choose crossover points
            crossoverPoints = []
            for rand in range(random.randint(0, 2)):
                crossoverPoints.append(
                    random.randint(1, self.chromosomes[0].rawWeightCount() - 1))
            
            counter = 0
            selectedChrom = (N / 2) % len(self.chromosomes)
            # 4 by for ayy lmao
            # Cross 'em over
            for layer in range(len(self.chromosomes[0].weights)):
                for node in range(len(self.chromosomes[0].weights[layer].matrixData)):
                    for weight in range(len(self.chromosomes[0].weights[layer].matrixData[node])):
                        for crip in crossoverPoints:
                            # Crossover point detected!
                            if crip == counter:
                                # Switch chromosome readings!
                                selectedChrom += 1
                                selectedChrom %= 2
                        # set em
                        gametes[N].weights[layer].matrixData[node][weight] = \
                        gametes[int(selectedChrom)].weights[layer].matrixData[node][weight]
                        # set the evil twin as well
                        gametes[N + 1].weights[layer].matrixData[node][weight] = \
                        gametes[int(selectedChrom + 1) % 2].weights[layer].matrixData[node][weight]
                        
        for g in gametes:
            # Boom boom radiation motherf$!@ers
            g.applyMutations()
        
        # Meiosis II all at once
        return gametes[random.randint(0, len(gametes) - 1)]
        
    
    def mate(self, other, numOffspring):
        assert type(other) == Neural_Organism, \
        "Neural_Organisms can only mate with other Neural_Organisms, dimwit!"
        # Form the templates
        offspring = []
        for o in range(numOffspring):
            offspring.append(
                Neural_Organism(
                self.chromosomes[0].numInputUnits,
                self.chromosomes[0].numOutputUnits,
                self.chromosomes[0].numHidLayers,
                self.chromosomes[0].numHidUnits,
                self.chromosomes[0].name, True)
            )
            # Pick a random gamete from each, then combine to form a
            # Neural_Organism
            offspring[o].chromosomes.append(self.generateGamete())
            offspring[o].chromosomes.append(other.generateGamete())
                
        return offspring
        
    def saveData(self, filename, serial=False):
        if serial:
            file = open(filename, "a")
        else:
            file = open(filename, "w")
        self.chromosomes[0].saveData(filename, True, True)
        self.chromosomes[1].saveData(filename, True)
        file.close()
