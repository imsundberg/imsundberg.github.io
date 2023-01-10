import Generator
import Chain
from sympy import *
from sympy.solvers.solveset import linsolve

class ChainComplex:
    def __init__(self, diagram):
        self.diagram = diagram
        self.binarySequence = self.initializeBinarySequences()
        self.chainElements = self.initializeGenerators()

    def initializeBinarySequences(self):
        binarySequences = []
        for i in range(2**self.diagram.n):
            temp = bin(i).replace("0b", "")
            while len(temp) < self.diagram.n:
                temp = '0' + temp
            binarySequences.append(temp)
        return binarySequences

    def initializeGenerators(self):
        generators = []
        for i in range(len(self.binarySequence)):
            binarySequence = self.binarySequence[i]
            gen = Generator.Generator(self.diagram, binarySequence)
            for j in range(2**len(gen.strandSmoothingSequence)):
                generators.append(Generator.Generator(self.diagram, binarySequence, self.addPadding(bin(j).replace("0b", ""), len(gen.strandSmoothingSequence)).replace("0", "x")))
        return generators

    @staticmethod
    def addPadding(temp, num):
        difference = num - len(temp)
        for i in range(difference):
            temp = "0" + temp
        return temp

    def d(self, generator):
        dsmoothings = []
        dcoefficients = []
        dgen = Chain.Chain(self.diagram, dsmoothings, dcoefficients)
        binarySequence = generator.binarySequence
        for i in range(len(binarySequence)):
            if binarySequence[self.diagram.n - i - 1] == '0':
                j = self.diagram.n - i
                newBinarySequence = binarySequence[:self.diagram.n - i - 1] + '1' + binarySequence[j:]
                newGenerator = Generator.Generator(self.diagram, newBinarySequence)
                xi = 0
                for j in range(self.diagram.n - i - 1):
                    xi = xi + int(binarySequence[j])
                newCoefficient = (-1)**xi
                oldComponents = generator.strandSmoothingSequence
                newComponents = newGenerator.strandSmoothingSequence
                reducedOldComponents = []
                reducedNewComponents = []
                oldLabel = generator.label
                reducedOldLabel = ""
                reducedNewLabel = ""
                for j in range(len(newComponents)):
                    if newComponents[j] not in oldComponents:
                        reducedNewComponents.append(newComponents[j])
                for j in range(len(oldComponents)):
                    if oldComponents[j] not in newComponents:
                        reducedOldComponents.append(oldComponents[j])
                        reducedOldLabel = reducedOldLabel + oldLabel[j]
                if len(reducedOldComponents) > len(reducedNewComponents):
                    if reducedOldLabel[0] == '1' and reducedOldLabel[1] == '1':
                        reducedNewLabel = '1'
                    elif (reducedOldLabel[0] == '1' and reducedOldLabel[1] == 'x') or (reducedOldLabel[1] == '1' and reducedOldLabel[0] == 'x'):
                        reducedNewLabel = 'x'
                    else:
                        newCoefficient = 0
                elif len(reducedOldComponents) < len(reducedNewComponents):
                    if reducedOldLabel == '1':
                        reducedNewLabel = '1x+x1'
                    elif reducedOldLabel == 'x':
                        reducedNewLabel = 'xx'
                    else:
                        raise Exception("Impossible label on component when performing differential.")
                else:
                    raise Exception("Error in number of components before/after differential.")
                newLabel = ""
                count = 0
                newLabel1 = ""
                newLabel2 = ""
                for j in range(len(newComponents)):
                    if newComponents[j] in oldComponents:
                        if count == 0:
                            newLabel = newLabel + oldLabel[oldComponents.index(newComponents[j])]
                        else:
                            newLabel1 = newLabel1 + oldLabel[oldComponents.index(newComponents[j])]
                            newLabel2 = newLabel2 + oldLabel[oldComponents.index(newComponents[j])]
                    else:
                        if len(reducedNewLabel) == 1:
                            newLabel = newLabel + reducedNewLabel
                        elif reducedNewLabel == 'xx':
                            newLabel = newLabel + 'x'
                        else:
                            if count == 0:
                                newLabel1 = newLabel + '1'
                                newLabel2 = newLabel + 'x'
                                count += 1
                            else:
                                newLabel1 = newLabel1 + 'x'
                                newLabel2 = newLabel2 + '1'
                if newCoefficient != 0:
                    if newLabel1 != "":
                        newGenerator2 = Generator.Generator(self.diagram, newBinarySequence)
                        newCoefficient2 = newCoefficient
                        newGenerator.setLabel(newLabel1)
                        dgen.addSummand(newGenerator, newCoefficient)
                        newGenerator2.setLabel(newLabel2)
                        dgen.addSummand(newGenerator2, newCoefficient2)
                    else:
                        newGenerator.setLabel(newLabel)
                        dgen.addSummand(newGenerator, newCoefficient)
        return dgen

    def dChain(self, chain):
        '''
        dChain = []
        dChainCoefficients = []
        for i in range(len(chain.generators)):
            nextGen = chain.generators[i]
            newChain = self.d(nextGen)
            dGenerators = newChain.generators
            dCoefficients = newChain.coefficients
            for j in range(len(dCoefficients)):
                temp = dCoefficients[j]
                dCoefficients[j] = temp*chain.coefficients[i]
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
            if (dChainCoefficients[i-count] == 0):
                dChain.remove(dChain[i-count])
                dChainCoefficients.remove(dChainCoefficients[i-count])
                count = count+1
        return Chain.Chain(self.diagram, dChain, dChainCoefficients)
        '''
        vec = self.dChainVector(chain)
        h = chain.getHomologicalGrading()
        q = chain.getQuantumGrading()
        imageGroup = self.getChainGroup(h+1,q)
        ch = Chain.Chain(self.diagram, [], [])
        for i in range(len(vec)):
            if vec[i] != 0:
                ch.addSummand(imageGroup[i], vec[i])
        return ch

    def dChainVector(self, chain):
        h = chain.getHomologicalGrading()
        q = chain.getQuantumGrading()
        imageGroup = self.getChainGroup(h+1, q)
        x = [0] * len(imageGroup)
        for i in range(len(chain.generators)):
            newChain = self.getVector(self.d(chain.generators[i]))
            for j in range(len(x)):
                x[j] = x[j] + newChain[j]*chain.coefficients[i]
        return x

    def isCycle(self, chain):
        return len(self.dChain(chain).generators) == 0

    def isCycleAsVector(self, chainVector):
        b = True
        for i in range(len(chainVector)):
            if chainVector[i] != 0:
                b = False
        return b

    def getChainGroup(self, hom, qua):
        domain = []
        for i in range(len(self.chainElements)):
            if self.chainElements[i].h == hom and self.chainElements[i].q == qua:
                domain.append(self.chainElements[i])
        return domain

    def getChainMap(self, hom, qua):
        domain = self.getChainGroup(hom, qua)
        image = self.getChainGroup(hom+1, qua)
        return self.initializeMatrix(domain, image)

    def printChainMap(self, hom, qua):
        print("-------------------")
        print("Chain Map (" + str(hom) + "," + str(qua) + ") --> ("+ str(hom+1) + "," + str(qua) + ")")
        print("-------------------")
        arr = self.getChainMap(hom,qua)
        for i in range(len(arr)):
            print("|", end="")
            for j in range(len(arr[i])):
                if arr[i][j] < 0:
                    print(" " + str(arr[i][j]) + " ", end="")
                else:
                    print("  " + str(arr[i][j]) + " ", end="")
            print(" |")

    def printChainGroup(self, hom, qua):
        print("-------------------")
        print("Chain Group (" + str(hom) + "," + str(qua) + ")")
        print("-------------------")
        arr = self.getChainGroup(hom, qua)
        for i in range(len(arr)):
            arr[i].printGenerator(i+1)

    def initializeMatrix(self, dom, image):
        matrix = [0] * len(image)
        for i in range(len(image)):
            if len(dom) == 0:
                matrix[i] = [0]
            else:
                matrix[i] = [0] * len(dom)
        for i in range(len(dom)):
            cycle = self.d(dom[i])
            gens = cycle.generators
            for j in range(len(image)):
                for k in range(len(gens)):
                    if self.compareGenerators(gens[k], image[j]):
                        matrix[j][i] = cycle.coefficients[k]
        return matrix

    def isInChain(self, arr, smoo):
        if len(arr) == 0:
            return False
        for i in range(len(arr)):
            if self.compareGenerators(arr.getGenerators()[i], smoo):
                return True
        return False

    @staticmethod
    def compareGenerators(s1, s2):
        if s1.strandSmoothingSequence == s2.strandSmoothingSequence and s1.label == s2.label and s1.componentSmoothingSequence == s2.componentSmoothingSequence:
            return True
        return False

    def getVector(self, chain):
        image = self.getChainGroup(chain.getHomologicalGrading(),chain.getQuantumGrading())
        x = [[0]] * len(image)
        for i in range(0, len(image)):
            for j in range(0, len(chain.generators)):
                if self.compareGenerators(image[i], chain.generators[j]):
                    x[i] = [chain.coefficients[j]]
        return x

    def printVector(self, chain):
        x = self.getVector(chain)
        print("-------------------")
        print("Vector in bigrading (" + str(chain.getHomologicalGrading()) + "," + str(chain.getQuantumGrading()) + ")")
        print("-------------------")
        for i in range(len(x)):
            if x[i][0] < 0:
                print("| " + str(x[i]) + " |")
            else:
                print("|  " + str(x[i]) + " |")

    def isBoundary(self, cycle):
        hom = cycle.getHomologicalGrading()
        qua = cycle.getQuantumGrading()
        A = Matrix(self.getChainMap(hom-1, qua))
        b = Matrix(self.getVector(cycle))
        aug = A.row_join(b)

        s = list(symbols('gen1:' + str(len(b)+1)))

        # print(linsolve(aug, s))
        # print(linsolve((A, b), s))

        # solution = linsolve(aug, s)
        solution = linsolve((A, b), s)

        return solution

        if solution != EmptySet:
            print("Chain is probably a boundary. Please interpret the solution set to verify:")
            for i in range(0, len(solution)):
                for j in range(0, len(solution.args[i])):
                    # s = solution.args[i]
                    # for i in range(len(s)):
                    #     str(solution.args[i][j]).replace('a','gen')
                    # print(" g" + str(solution.args[i][j]).replace('a',''))
                    print(" gen" + str(j+1) + " = " + str(solution.args[i][j]).replace('gen', 'c'))
            print("Isaac should give you access to gen1, gen2, etc... ")
            print("Also, this probably will be messy if integral solutions are provided...")
        else:
            print("Chain is not a boundary.")
