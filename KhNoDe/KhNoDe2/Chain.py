

class Chain:

    def __init__(self, diagram, generators, coefficients):
        self.diagram = diagram
        self.generators = generators
        self.coefficients = coefficients

    def addSummand(self, gen, coefficient):
        index = self.contains(gen)
        if index == -1:
            self.generators.append(gen)
            self.coefficients.append(coefficient)
        else:
            self.coefficients[index] = self.coefficients[index] + coefficient
            if self.coefficients[index] == 0:
                self.generators.remove(self.generators[index])
                self.coefficients.remove(self.coefficients[index])

    def getHomologicalGrading(self):
        if len(self.generators) == 0:
            return 0
        else:
            return self.generators[0].h

    def getQuantumGrading(self):
        if len(self.generators) == 0:
            return 0
        else:
            return self.generators[0].q

    def getCoefficients(self):
        return self.coefficients

    def getGenerators(self):
        return self.generators

    # returns -1 if not in generators, else returns index of common generator
    def contains(self, gen):
        for i in range(len(self.generators)):
            if (gen.strandSmoothingSequence == self.generators[i].strandSmoothingSequence) and (gen.label == self.generators[i].label):
                return i
        return -1

    def viewChain(self):
        if len(self.generators) == 0:
            print("Chain is trivial")
        else:
            for i in range(0, len(self.generators)):
                self.generators[i].viewGenerator()

    def isCycle(self):
        return len(self.d().generators) == 0

    def d(self):
        dChain = []
        dChainCoefficients = []
        for i in range(len(self.generators)):
            nextGen = self.generators[i]
            newChain = nextGen.d()
            dGenerators = newChain.generators
            dCoefficients = newChain.coefficients
            for j in range(len(dCoefficients)):
                temp = dCoefficients[j]
                dCoefficients[j] = temp * self.coefficients[i]
            temp = 0
            for j in range(len(dGenerators)):
                for k in range(len(dChain)):
                    if self.compareGenerators(dGenerators[j], dChain[k]):
                        dChainCoefficients[k] = dChainCoefficients[k] + dCoefficients[j]
                        temp = 1
                if temp != 1:
                    dChain.append(dGenerators[j])
                    dChainCoefficients.append(dCoefficients[j])
                    temp = 0
        count = 0
        for i in range(len(dChainCoefficients)):
            if (dChainCoefficients[i - count] == 0):
                dChain.remove(dChain[i - count])
                dChainCoefficients.remove(dChainCoefficients[i - count])
                count = count + 1
        return Chain(self.diagram, dChain, dChainCoefficients)

    def compareGenerators(self, s1, s2):
        if s1.strandSmoothingSequence == s2.strandSmoothingSequence and s1.label == s2.label and s1.componentSmoothingSequence == s2.componentSmoothingSequence:
            return True
        return False