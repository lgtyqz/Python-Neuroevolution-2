import random
from matrix import *
class Neural_Network:
    def __init__(self, numInputUnits, numOutputUnits, numHidLayers, numHidUnits,
                 weights=None, name=""):
        assert numInputUnits > 0, "You must certainly have some input units!"
        assert numOutputUnits > 0, "You want something to come out, right?"
        assert numHidLayers > -1, "One does not simply have -1 hidden layers."
        assert numHidUnits > 0, "user plz"
        self.name = name
        self.numInputUnits = numInputUnits
        self.numOutputUnits = numOutputUnits
        self.numHidLayers = numHidLayers
        self.numHidUnits = numHidUnits
        self.a = []
        if weights == None:
            # Randomly initialize weights.
            self.weights = []
            layer0Weights = []
            # Step 1: Create input unit weights.
            # +1 is for the bias unit
            for i in range(numInputUnits + 1):
                nodeWeights = []
                if numHidLayers > 0:
                    # Bias unit not included, of course
                    for j in range(numHidUnits):
                        nodeWeights.append(random.random() * 2 - 1)
                else:
                    # If there aren't any hidden units, just link to the
                    # output units.
                    for j in range(numOutputUnits):
                        nodeWeights.append(random.random() * 2 - 1)
                layer0Weights.append(nodeWeights)
            layer0Weights = Matrix(layer0Weights)
            self.weights.append(layer0Weights)
            # Step 2: Create weights for the hidden layers.
            # This assumes that all hidden layers have the
            # same number of weights.
            if numHidLayers > 0:
                for layer in range(numHidLayers):
                    hidLayerWeights = []
                    # Gotta include the bias unit
                    for i in range(numHidUnits + 1):
                        nodeWeights = []
                        # If it's the last hidden layer, link to the
                        # output layer.
                        if layer == numHidLayers - 1:
                            for j in range(numOutputUnits):
                                nodeWeights.append(random.random() * 2 - 1)
                        else:
                            for j in range(numHidUnits):
                                nodeWeights.append(random.random() * 2 - 1)
                        hidLayerWeights.append(nodeWeights)
                    hidLayerWeights = Matrix(hidLayerWeights)
                    self.weights.append(hidLayerWeights)

        else:
            assert type(weights) == list and type(weights[0]) == Matrix, \
                   "Weights must be in a list of matrices."
            self.weights = weights
        # print(self.weights)
    def forwardPropagate(self, inputValues, delta=False):
        if delta:
            self.a = []
        assert type(inputValues) == list, \
               "Input values must be contained in a list."
        assert len(inputValues) == self.weights[0].size[0] - 1, \
               "Incorrect number of matrix input values."
        inputMatrix = []
        inputValues.insert(0, 1)
        inputMatrix.append(inputValues)
        inputMatrix = Matrix(inputMatrix)
        resultMatrix = copy.deepcopy(inputMatrix)
##        if delta:
##            self.a.append(Matrix(resultMatrix.matrixData[0][1:]))
##            self.a[0].size = [len(self.a[0].matrixData),
##                              len(self.a[0].matrixData[0])]
        for layer in range(len(self.weights)):
            # print("Layer:", layer)
            # print("Result Matrix", resultMatrix.transpose())
            resultingMatrix = []
            resultingMatrixRow = []
            # Is it the final layer?
            for outputNode in range(self.weights[layer].size[1]):
                nodeWeightMatrix = []
                nodeWeightRow = []
                for nodeWeightSet in self.weights[layer].matrixData:
                    nodeWeightRow.append(nodeWeightSet[outputNode])
                nodeWeightMatrix.append(nodeWeightRow)
                nodeWeightMatrix = Matrix(nodeWeightMatrix)
                # print("Node Weight Matrix", outputNode,
                #      nodeWeightMatrix.matrixData)
                nodeResult = nodeWeightMatrix * Matrix(resultMatrix.transpose())
                resultingMatrixRow.append(nodeResult[0][0])
            resultingMatrix.append(resultingMatrixRow)
            resultMatrix = Matrix(resultingMatrix)
            resultMatrix = Matrix(resultMatrix.sigmoid())
            self.a.append(resultMatrix)
            # print(resultMatrix.matrixData)
            if layer != len(self.weights) - 1:
                resultMatrix.matrixData[0].insert(0, 1)
                resultMatrix.size[1] += 1
            # print("\nResulting Matrix:", resultMatrix.matrixData, "\n")

        # print(resultMatrix.matrixData)

        # Returns the resulting values as a row vector/matrix.
        return resultMatrix

    # The following methods are unused. They were planned for another project,
    # but then I realized that they weren't the best methods.
    def backpropagate(self, inputValues, realOutput, alpha, LAMBDA=0):
##        This is a bit of a WIP project here.
##
##        
##        deltaErrors = []
##        capitalDeltas = []
##        derivatives = []
##        assert type(inputValues) == list, \
##               "Input values must be contained in a list."
##        assert type(realOutput) == list, \
##               "The true output values must also be contained in a list. =)"
##        estOutput = self.forwardPropagate(inputValues)
##        y = Matrix([realOutput])
##        deltaErrors.append(estOutput - y)
##        ## WIP
##        ## WIP
##        ## WWWWIIIIIPPPP
##        for i in range(len(self.a) - 1):
##            deltaErrors.insert(0, self.a[len(self.a) - i])
        pass
    
    def rawWeightCount(self):
        count = 0
        for layer in self.weights:
            for node in layer.matrixData:
                for weight in node:
                    count += 1
                    
        return count
        
    def applyMutations(self, chance=0.0002):
        counter = 0
        for layer in range(len(self.weights)):
            for node in range(len(self.weights[layer].matrixData)):
                for weight in range(len(self.weights[layer].matrixData[node])):
                    if(random.random() < chance):
                        self.weights[layer].matrixData[node][weight] = \
                        random.random() * 2 - 1
                        counter += 1
        print("# of mutations:", counter)
    
    def saveData(self, filename, serial=False, endTag=False):
        if serial:
            file = open(filename, "a")
        else:
            file = open(filename, "w")
        print("\nNN file writing in progress...")
        # wip!!!!!!!!! Need metadata to properly process data
        file.write("{0} {1} {2} {3}\n".format(self.numInputUnits,
                                            self.numOutputUnits,
                                            self.numHidLayers,
                                            self.numHidUnits))
        weightString = ""
        # Write the weights in a loooong list.
        for layer in self.weights:
            for node in layer.matrixData:
                for weight in node:
                    weightString += "{0} ".format(str(weight))

        file.write(weightString)
        file.write("\n")
        if endTag:
            file.write("aesthetic4life\n")
        file.close()
        print("NN file writing complete.\n")
    # Update to match Neural_Network.saveData()
    def loadData(self, filename, serial=False, raw=False):
        if not raw:
            print("\nLoading file...")
            try:
                file = open(filename, "r")
            except (FileNotFoundError, IOError):
                print("File not found.")
                return None
            contents = file.read()
        else:
            print("Loading raw NN data...")
            # Assumes "filename" is just raw weight data,
            # minus leading/trailing whitespace
            contents = filename.strip()
        contents = contents.split("\n")
        print(contents[0])
        contents[0] = contents[0].split(" ") # Metadata
        print(contents[0])
        contents[1] = contents[1].split(" ") # Weight Values
        self.numInputUnits = int(contents[0][0])
        self.numOutputUnits = int(contents[0][1])
        self.numHidLayers = int(contents[0][2])
        self.numHidUnits = int(contents[0][3])
        for i in contents:
            counter = 0
        self.weights = []
        layer0Weights = []
        counter = 0
        # Adapting the neural network random weight generation alg here
        for i in range(self.numInputUnits + 1):
            nodeWeights = []
            if self.numHidLayers > 0:
                for j in range(self.numHidUnits):
                    nodeWeights.append(float(contents[1][counter]))
                    counter += 1
            else:
                for j in range(self.numOutputUnits):
                    nodeWeights.append(float(contents[1][counter]))
                    counter += 1
            layer0Weights.append(nodeWeights)
        layer0Weights = Matrix(layer0Weights)
        self.weights.append(layer0Weights)
        if self.numHidLayers > 0:
            for layer in range(self.numHidLayers):
                hidLayerWeights = []
                for i in range(self.numHidUnits + 1):
                    nodeWeights = []
                    if layer == self.numHidLayers - 1:
                        for j in range(self.numOutputUnits):
                            nodeWeights.append(float(contents[1][counter]))
                            counter += 1
                    else:
                        for i in range(self.numHidUnits):
                            nodeWeights.append(float(contents[1][counter]))
                            counter += 1

                    hidLayerWeights.append(nodeWeights)
                hidLayerWeights = Matrix(hidLayerWeights)
                self.weights.append(hidLayerWeights)
        print("File reading complete.\n")
        if not raw:
            file.close()
        if serial:
            return self.weights
