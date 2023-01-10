import Chain
import tkinter as tk


class Generator:
    def __init__(self, diagram, binarySequence, label=""):
        self.diagram = diagram
        self.grid = self.diagram.grid
        self.binarySequence = binarySequence
        self.label = label

        self.components = self.diagram.components
        self.crossings = self.diagram.crossings
        self.componentNumber = len(self.diagram.strands)

        self.n = len(self.crossings)
        self.np = self.diagram.np
        self.nn = self.diagram.nn

        self.strandNumbers = self.diagram.strandNumbers
        self.strandSmoothingSequence = self.initializeStrandSmoothingSequences()[0]
        self.componentSmoothingSequence = self.initializeStrandSmoothingSequences()[1]
        self.entrySmoothingSequence = self.initializeEntrySmoothingSequence()

        self.h = self.setHomologicalGrading()
        self.q = self.setQuantumGrading()

        self.canvas_height = (len(self.diagram.grid) + 1) * 100
        self.canvas_width = (len(self.diagram.grid[0]) + 1) * 100

    # TO DO
    def initializeSmoothingGrid(self):
        sGrid = [''] * len(self.diagram.grid)

        return sGrid

    # TO DO
    def initializeStrandSmoothingSequences(self):
        strandSmoothingSequence = list()
        componentSequence = list()

        # create an array to track used strands
        # call it usedStrands[linkComponent, strand]
        usedStrands = [0] * self.componentNumber
        for i in range(self.componentNumber):
            usedStrands[i] = [0] * self.strandNumbers[i]
        breaker = 0
        while not self.isAllOneArray(usedStrands):
            # find first strand for component
            # call it temp[linkComponent, strand]
            temp = [0, 0]
            breaker = 0
            # check if there are unused strands
            for i in range(len(usedStrands)):
                for j in range(len(usedStrands[i])):
                    if usedStrands[i][j] == 0 and breaker == 0:
                        temp[0] = i + 1
                        temp[1] = j + 1
                        breaker = 1
            # if breaker=0 at this point, all strands have been used, so we are done
            if breaker != 0:
                firstStrand = temp[1]
                firstComponent = temp[0]
                # create string to track the strands in the smoothing
                component = str(firstStrand)
                # create string to track associated component for each strand in smoothing
                linkComponent = str(firstComponent)
                usedStrands[temp[0] - 1][temp[1] - 1] = 1
                nextStrand = 0
                nextComponent = 0
                direction = 0
                while nextStrand != firstStrand or nextComponent != firstComponent:
                    if nextStrand == 0:
                        nextStrand = firstStrand
                        nextComponent = firstComponent
                    nxt = self.findNextStrand(nextComponent, nextStrand, direction)
                    nextComponent = nxt[0]
                    nextStrand = nxt[1]
                    direction = nxt[2]
                    if nextStrand != firstStrand or nextComponent != firstComponent:
                        component = component + "," + str(nextStrand)
                        linkComponent = linkComponent + "," + str(nextComponent)
                        usedStrands[nxt[0] - 1][nxt[1] - 1] = 1
                strandSmoothingSequence.append(component)
                componentSequence.append(linkComponent)

        return [strandSmoothingSequence, componentSequence]

    def findNextStrand(self, linkcomponent, strand, direction):
        nxt = []
        for i in range(self.n):
            # if the direction is with (direction = 0)
            if direction == 0:
                # Case 1: check if strand is first strand of crossing
                if self.crossings[i][0] == strand and self.components[i][0] == linkcomponent:
                    right = 1
                    left = 3
                    # Return array based on smoothing and direction of over-strand (2 cases)
                    if self.binarySequence[i] == '0':
                        # check if crossing is positively oriented
                        if self.diagram.crossingOrientationGrid[self.diagram.centers[i][0]][self.diagram.centers[i][1]] == 'p':
                            nxt.append(self.components[i][right])
                            nxt.append(self.crossings[i][right])
                            nxt.append(0)
                            return nxt
                        # otherwise crossing is negatively oriented
                        else:
                            nxt.append(self.components[i][right])
                            nxt.append(self.crossings[i][right])
                            nxt.append(1)
                            return nxt
                    else:
                        # check if crossing is positively oriented
                        if self.diagram.crossingOrientationGrid[self.diagram.centers[i][0]][self.diagram.centers[i][1]] == 'p':
                            nxt.append(self.components[i][left])
                            nxt.append(self.crossings[i][left])
                            nxt.append(1)
                            return nxt
                        # otherwise crossing is negatively oriented
                        else:
                            nxt.append(self.components[i][left])
                            nxt.append(self.crossings[i][left])
                            nxt.append(0)
                            return nxt
                # Case 2: check if strand is second strand of crossing and verify direction
                # note... direction of under-strand AND over-strand is fixed, so there is only one case
                if (self.crossings[i][1] == strand) and self.components[i][1] == linkcomponent and self.diagram.crossingOrientationGrid[self.diagram.centers[i][0]][self.diagram.centers[i][1]] == 'n':
                    right = 2
                    left = 0
                    # Return array based on smoothing
                    if self.binarySequence[i] == '0':
                        nxt.append(self.components[i][left])
                        nxt.append(self.crossings[i][left])
                        nxt.append(1)
                        return nxt
                    else:
                        nxt.append(self.components[i][right])
                        nxt.append(self.crossings[i][right])
                        nxt.append(0)
                        return nxt
                # Case 3: check if strand is fourth strand of crossing and verify direction
                # note... direction of under-strand AND over-strand is fixed, so there is only one case
                if (self.crossings[i][3] == strand) and self.components[i][3] == linkcomponent and self.diagram.crossingOrientationGrid[self.diagram.centers[i][0]][self.diagram.centers[i][1]] == 'p':
                    right = 0
                    left = 2
                    # Return array based on smoothing
                    if self.binarySequence[i] == '0':
                        nxt.append(self.components[i][left])
                        nxt.append(self.crossings[i][left])
                        nxt.append(0)
                        return nxt
                    else:
                        nxt.append(self.components[i][right])
                        nxt.append(self.crossings[i][right])
                        nxt.append(1)
                        return nxt
            # otherwise the direction is against (direction = 1)
            else:
                # Case 4: check if strand is second strand of crossing and verify direction
                # note... direction of under-strand AND over-strand is fixed, so there is only one case
                if (self.crossings[i][1] == strand) and self.components[i][1] == linkcomponent and self.diagram.crossingOrientationGrid[self.diagram.centers[i][0]][self.diagram.centers[i][1]] == 'p':
                    right = 2
                    left = 0
                    # Return array based on smoothing (direction of under-strand is fixed)
                    if self.binarySequence[i] == '0':
                        nxt.append(self.components[i][left])
                        nxt.append(self.crossings[i][left])
                        nxt.append(1)
                        return nxt
                    else:
                        nxt.append(self.components[i][right])
                        nxt.append(self.crossings[i][right])
                        nxt.append(0)
                        return nxt
                # Case 5: check if strand is third strand of crossing and verify direction (2 cases)
                if (self.crossings[i][2] == strand and self.components[i][2] == linkcomponent):
                    right = 3
                    left = 1
                    # Return array based on smoothing and direction of over-strand (2 cases)
                    if self.binarySequence[i] == '0':
                        # check if crossing is positively oriented
                        if self.diagram.crossingOrientationGrid[self.diagram.centers[i][0]][self.diagram.centers[i][1]] == 'p':
                            nxt.append(self.components[i][right])
                            nxt.append(self.crossings[i][right])
                            nxt.append(1)
                            return nxt
                        # otherwise crossing is negatively oriented
                        else:
                            nxt.append(self.components[i][right])
                            nxt.append(self.crossings[i][right])
                            nxt.append(0)
                            return nxt
                    else:
                        # check if crossing is positively oriented
                        if self.diagram.crossingOrientationGrid[self.diagram.centers[i][0]][self.diagram.centers[i][1]] == 'p':
                            nxt.append(self.components[i][left])
                            nxt.append(self.crossings[i][left])
                            nxt.append(0)
                            return nxt
                        # otherwise crossing is negatively oriented
                        else:
                            nxt.append(self.components[i][left])
                            nxt.append(self.crossings[i][left])
                            nxt.append(1)
                            return nxt
                # Case 6: check if strand is fourth strand of crossing and verify direction
                # note... direction of under-strand AND over-strand is fixed, so there is only one case
                if (self.crossings[i][3] == strand) and self.components[i][3] == linkcomponent and self.diagram.crossingOrientationGrid[self.diagram.centers[i][0]][self.diagram.centers[i][1]] == 'n':
                    right = 0
                    left = 2
                    # Return array based on smoothing
                    if self.binarySequence[i] == '0':
                        nxt.append(self.components[i][left])
                        nxt.append(self.crossings[i][left])
                        nxt.append(0)
                        return nxt
                    else:
                        nxt.append(self.components[i][right])
                        nxt.append(self.crossings[i][right])
                        nxt.append(1)
                        return nxt

    def isAllOneArray(self, arr):
        test = True
        for i in range(len(arr)):
            for j in range(len(arr[i])):
                test = test and (arr[i][j] == 1)
        return test

    def initializeEntrySmoothingSequence(self):
        entrySmoothingSequence = [] * len(self.strandSmoothingSequence)
        for i in range(0, len(self.strandSmoothingSequence)):
            entrySmoothingSequence.append([])

        # cycle through strand numbers in each smoothing
        for i in range(0, len(self.strandSmoothingSequence)):
            smoo = self.strandSmoothingSequence[i].split(',')
            comp = self.componentSmoothingSequence[i].split(',')
            for j in range(0, len(smoo)):
                smooInt = int(smoo[j])-1
                compInt = int(comp[j])-1
                if entrySmoothingSequence[i] == []:
                    entrySmoothingSequence[i] = entrySmoothingSequence[i] + self.diagram.strands[compInt][smooInt]
                else:
                    if entrySmoothingSequence[i][len(entrySmoothingSequence)-1] == self.diagram.strands[compInt][smooInt][0]:
                        entrySmoothingSequence[i] = entrySmoothingSequence[i] + self.diagram.strands[compInt][smooInt][1:]
                    else:
                        self.diagram.strands[compInt][smooInt].reverse()
                        entrySmoothingSequence[i] = entrySmoothingSequence[i] + self.diagram.strands[compInt][smooInt][1:]
        return entrySmoothingSequence


    def viewGenerator(self):
        window = tk.Tk()
        window.geometry('750x750')
        window.configure(background='white')
        window.title("Current generators")

        my_canvas = tk.Canvas(window, width=650, height=650, bg="white")
        my_canvas.pack(pady=20)

        xScale = int(550/len(self.grid))
        yScale = int(550/len(self.grid[0]))
        m = min(xScale, yScale)
        m2 = m/2

        # Draw Grid
        # horizontal lines
        for i in range(0, len(self.grid) + 1):
            my_canvas.create_line(m2, i * m + m2, (len(self.grid[0]) + 1) * m - m2, i * m + m2, fill='gray')
        # vertical lines
        for i in range(0, len(self.grid[0]) + 1):
            my_canvas.create_line(i * m + m2, m2, i * m + m2, (len(self.grid) + 1) * m - m2, fill='gray')

        # Draw smoothings
        # cycle through centers
        for i in range(0, len(self.diagram.centers)):
            y = self.diagram.centers[i][0]
            x = self.diagram.centers[i][1]
            if self.diagram.grid[y][x] == 'v':
                if self.binarySequence[i] == '0':
                    my_canvas.create_arc(x * m + 2*m2, y * m, x * m + 4*m2, y * m + 2*m2, start=180,
                                         extent=90, style=tk.ARC, width=3)
                    my_canvas.create_arc(x * m, y * m + 2*m2, x * m + 2*m2, y * m + 4*m2, start=0,
                                         extent=90, style=tk.ARC, width=3)
                if self.binarySequence[i] == '1':
                    my_canvas.create_arc(x * m, y * m, x * m + 2*m2, y * m + 2*m2, start=270,
                                         extent=90, style=tk.ARC, width=3)
                    my_canvas.create_arc(x * m + 2*m2, y * m + 2*m2, x * m + 4*m2, y * m + 4*m2, start=90,
                                         extent=90, style=tk.ARC, width=3)
            if self.diagram.grid[y][x] == 'h':
                if self.binarySequence[i] == '0':
                    my_canvas.create_arc(x * m, y * m, x * m + 2*m2, y * m + 2*m2, start=270,
                                         extent=90, style=tk.ARC, width=3)
                    my_canvas.create_arc(x * m + 4*m2, y * m + 2*m2, x * m + 2*m2, y * m + 4*m2, start=90,
                                         extent=90, style=tk.ARC, width=3)
                if self.binarySequence[i] == '1':
                    my_canvas.create_arc(x * m + 2*m2, y * m, x * m + 4*m2, y * m + 2*m2, start=180,
                                         extent=90, style=tk.ARC, width=3)
                    my_canvas.create_arc(x * m, y * m + 2*m2, x * m + 2*m2, y * m + 4*m2, start=0,
                                         extent=90, style=tk.ARC, width=3)

        # Draw horizontal lines
        for i in range(0, len(self.grid)):
            for j in range(0, len(self.grid[0])):
                if 'e' in self.grid[i][j]:
                    c = j+1
                    while 'w' not in self.grid[i][c]:
                        if self.grid[i][c] != 'v' and self.grid[i][c] != 'h':
                            my_canvas.create_line(c*m+m2, i*m+2*m2, c*m+3*m2, i*m+2*m2, width=3)
                        c += 1

        # Draw vertical lines
        for j in range(0, len(self.grid[0])):
            for i in range(0, len(self.grid)):
                if 's' in self.grid[i][j]:
                    c = i+1
                    while 'n' not in self.grid[c][j]:
                        if self.grid[c][j] != 'v' and self.grid[c][j] != 'h':
                            my_canvas.create_line(j*m+2*m2, c*m+m2, j*m+2*m2, c*m+3*m2, width=3)
                        c += 1

        # Draw straight corners
        for i in range(0, len(self.grid)):
            for j in range(0, len(self.grid[0])):
                if self.grid[i][j] == 'ne':
                    my_canvas.create_line(j * m + 2*m2, i * m + 2*m2, j * m + 3*m2, i * m + 2*m2, width=3)
                    my_canvas.create_line(j * m + 2*m2, i * m + m2, j * m + 2*m2, i * m + 2*m2, width=3)
                if self.grid[i][j] == 'nw':
                    my_canvas.create_line(j * m + m2, i * m + 2*m2, j * m + 2*m2, i * m + 2*m2, width=3)
                    my_canvas.create_line(j * m + 2*m2, i * m + m2, j * m + 2*m2, i * m + 2*m2, width=3)
                if self.grid[i][j] == 'se':
                    my_canvas.create_line(j * m + 2*m2, i * m + 2*m2, j * m + 3*m2, i * m + 2*m2, width=3)
                    my_canvas.create_line(j * m + 2*m2, (i + 1) * m, j * m + 2*m2, (i + 1) * m + m2, width=3)
                if self.grid[i][j] == 'sw':
                    my_canvas.create_line(j * m + m2, i * m + 2*m2, j * m + 2*m2, i * m + 2*m2, width=3)
                    my_canvas.create_line(j * m + 2*m2, (i + 1) * m, j * m + 2*m2, (i + 1) * m + m2, width=3)

        # # Draw rounded corners
        # for i in range(0, len(self.diagram.grid)):
        #     for j in range(0, len(self.diagram.grid[0])):
        #         if self.diagram.grid[i][j] == 'ne':
        #             my_canvas.create_arc(j * 100 + 100, i * 100, j * 100 + 200, i * 100 + 100, start=180,
        #                                  extent=90, style=tk.ARC, width=3)
        #         if self.diagram.grid[i][j] == 'nw':
        #             my_canvas.create_arc(j * 100, i * 100, j * 100 + 100, i * 100 + 100, start=270, extent=90,
        #                                  style=tk.ARC, width=3)
        #         if self.diagram.grid[i][j] == 'se':
        #             my_canvas.create_arc(j * 100 + 100, i * 100 + 100, j * 100 + 200, i * 100 + 200, start=90,
        #                                  extent=90,
        #                                  style=tk.ARC, width=3)
        #         if self.diagram.grid[i][j] == 'sw':
        #             my_canvas.create_arc(j * 100, i * 100 + 100, j * 100 + 100, i * 100 + 200, start=0,
        #                                  extent=90, style=tk.ARC, width=3)

        # Draw strand numbers
        for k in range(0, len(self.diagram.strands)):
            for i in range(0, len(self.diagram.strands[k])):
                if len(self.diagram.strands[k][i]) % 2 == 0:
                    mid = int(len(self.diagram.strands[k][i]) / 2)
                    xAvg = (self.diagram.strands[k][i][mid][1] + self.diagram.strands[k][i][mid - 1][1]) / 2
                    yAvg = (self.diagram.strands[k][i][mid][0] + self.diagram.strands[k][i][mid - 1][0]) / 2
                    my_canvas.create_text(xAvg * m + 2*m2+10, yAvg * m + 2*m2+10, text=str(i + 1), fill="blue")
                else:
                    mid = int((len(self.diagram.strands[k][i]) - 1) / 2)
                    my_canvas.create_text(self.diagram.strands[k][i][mid][1] * m + 2*m2+10,
                                          self.diagram.strands[k][i][mid][0] * m + 2*m2+10, text=str(i + 1), fill="blue")

        # Draw smoothing numbers
        for i in range(0, len(self.diagram.centers)):
            my_canvas.create_oval(self.diagram.centers[i][1] * m + 2*m2-7, self.diagram.centers[i][0] * m + 2*m2-7, self.diagram.centers[i][1] * m + 2*m2+7, self.diagram.centers[i][0] * m + 2*m2+7, fill="black", width=1)
            my_canvas.create_text(self.diagram.centers[i][1] * m + 2*m2, self.diagram.centers[i][0] * m + 2*m2, text=self.binarySequence[i], fill="white")

        # Draw smoothing numbers
        for i in range(0, len(self.diagram.centers)):
            x1 = self.diagram.centers[i][0]
            y1 = self.diagram.centers[i][1]
            my_canvas.create_polygon(x1 * m + 3/2*m2, y1 * m + 3/2*m2-10, x1 * m + 3/2*m2-10, y1 * m + 3/2*m2, x1 * m + 3/2*m2,
                                     y1 * m + 3/2*m2+10, x1 * m + 3/2*m2+10, y1 * m + 3/2*m2, outline="red", fill="white")
            my_canvas.create_text(x1 * m + 3/2*m2, y1 * m + 3/2*m2, text=str(i + 1), fill="red")

        # Draw smoothing component numbers
        for i in range(0, len(self.entrySmoothingSequence)):
            u = self.findUniqueStrandSmoothingEntry(i)
            x1 = self.entrySmoothingSequence[i][u][0]
            y1 = self.entrySmoothingSequence[i][u][1]
            my_canvas.create_polygon(y1*m+3/2*m2-8, x1*m+3/2*m2-8, y1*m+3/2*m2+8, x1*m+3/2*m2-8, y1*m+3/2*m2+8, x1*m+3/2*m2+8, y1*m+3/2*m2-8, x1*m+3/2*m2+8, outline="purple", fill="white")
            my_canvas.create_text(y1 * m + 3/2*m2, x1 * m + 3/2*m2, text=str(i + 1), fill="purple")

        # draw labels
        for i in range(0, len(self.label)):
            x1 = self.entrySmoothingSequence[i][0][0]
            x2 = self.entrySmoothingSequence[i][1][0]
            y1 = self.entrySmoothingSequence[i][0][1]
            y2 = self.entrySmoothingSequence[i][1][1]
            x = (x1+x2)/2
            y = (y1+y2)/2
            my_canvas.create_oval(y*m+2*m2-7, x*m+2*m2-7, y*m+2*m2+7, x*m+2*m2+7, fill="green")
            if self.label[i] == 'x':
                my_canvas.create_text(y*m+2*m2+1, x*m+2*m2-1, text=self.label[i], fill="yellow")
            else:
                my_canvas.create_text(y*m+2*m2, x*m+2*m2, text=self.label[i], fill="yellow")

        # Key
        my_canvas.create_oval(m2 + 8, 620 + 8, m2 - 8, 620 - 8, outline="black", fill="green")
        my_canvas.create_text(m2 + 25, 620, text='label')
        my_canvas.create_text(m2, 620, text='?', fill="white")

        my_canvas.create_oval(m2 + 75 + 8, 620 + 8, m2 + 75 - 8, 620 - 8, outline="black", fill="black")
        my_canvas.create_text(m2 + 130, 620, text='smoothing type')
        my_canvas.create_text(m2 + 75, 620, text='#', fill="white")

        my_canvas.create_polygon(m2 + 200, 620 - 10, m2 + 200 - 10, 620, m2 + 200, 620 + 10, m2 + 200 + 10, 620,
                                 outline="red", fill="white")
        my_canvas.create_text(m2 + 260, 620, text='crossing number', fill="red")
        my_canvas.create_text(m2 + 200, 620, text='#', fill="red")

        my_canvas.create_polygon(m2 + 335-8, 620 - 8, m2 + 335 + 8, 620-8, m2 + 335+8, 620 + 8, m2 + 335-8, 620+8, outline="purple", fill="white")
        my_canvas.create_text(m2 + 410, 620, text='smoothing component', fill="purple")
        my_canvas.create_text(m2 + 335, 620, text='#', fill="purple")

        window.mainloop()

    def setHomologicalGrading(self):
        h = 0
        for i in range(len(self.binarySequence)):
            h = h + int(self.binarySequence[i])
        return h - self.nn

    def setQuantumGrading(self):
        vp = 0
        vn = 0
        for i in range(len(self.label)):
            if self.label[i] == '1':
                vp += 1
            else:
                vn += 1
        return vp - vn + self.h + self.np - self.nn

    # returns index for a strand entry unique to the i-th smoothing component
    def findUniqueStrandSmoothingEntry(self, i):
        # iterate through entries of smoothing component
        for j in range(0, len(self.entrySmoothingSequence[i])):
            breaker = 0

            # check to see if strand entry is a center
            if self.entrySmoothingSequence[i][j] in self.diagram.centers:
                breaker = -1

            # iterate through other smoothing components
            for k in range(0, len(self.entrySmoothingSequence)):
                if k != i:
                    # check to see if strand entry is in other smoothing components
                    if self.entrySmoothingSequence[i][j] in self.entrySmoothingSequence[k]:
                        breaker = -1

            if breaker != -1:
                return j

    def d(self):
        dsmoothings = []
        dcoefficients = []
        dgen = Chain.Chain(self.diagram, dsmoothings, dcoefficients)
        binarySequence = self.binarySequence
        for i in range(len(binarySequence)):
            if binarySequence[self.diagram.n - i - 1] == '0':
                j = self.diagram.n - i
                newBinarySequence = binarySequence[:self.diagram.n - i - 1] + '1' + binarySequence[j:]

                newGenerator = Generator(self.diagram, newBinarySequence, "")
                xi = 0
                for j in range(self.diagram.n - i - 1):
                    xi = xi + int(binarySequence[j])
                newCoefficient = (-1)**xi
                oldComponents = self.strandSmoothingSequence
                newComponents = newGenerator.strandSmoothingSequence
                reducedOldComponents = []
                reducedNewComponents = []
                oldLabel = self.label
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
                        newGenerator2 = Generator(self.diagram, newBinarySequence)
                        newCoefficient2 = newCoefficient
                        newGenerator.setLabel(newLabel1)
                        dgen.addSummand(newGenerator, newCoefficient)
                        newGenerator2.setLabel(newLabel2)
                        dgen.addSummand(newGenerator2, newCoefficient2)
                    else:
                        newGenerator.setLabel(newLabel)
                        dgen.addSummand(newGenerator, newCoefficient)
        return dgen

    def setLabel(self, lab):
        if len(lab) == len(self.strandSmoothingSequence):
            self.label = lab
            self.q = self.setQuantumGrading()
        else:
            raise Exception("Label size does not match number of components.")

