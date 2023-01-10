from tkinter import *
import tkinter as tk
import Generator


class Diagram:

    def __init__(self, grid):
        self.grid = grid
        self.grid = self.initializeFineGrid()
        self.centers = self.initializeCenters()

        self.strandSequence = self.initializeStrandSequence()
        self.strands = self.initializeStrands()
        self.strandNumbers = self.initializeStrandNumbers()

        self.componentGrid = self.initializeComponentGrid()
        self.strandGrid = self.initializeStrandGrid()
        self.orientationGrid = self.initializeOrientationGrid()

        self.components = self.initializeComponents()
        self.crossings = self.initializeCrossings()

        self.n = len(self.crossings)
        self.np = 0
        self.nn = 0
        self.crossingOrientationGrid = []
        # initialize np, nn, and crossingOrientationGrid
        self.initializeCrossingOrientations()

    # creates a sequence of integers representing the number of strands in each component
    def initializeStrandNumbers(self):
        strandNumbers = list()
        for i in range(0, len(self.strands)):
            strandNumbers.append(len(self.strands[i]))
        return strandNumbers

    # creates a sequence of coordinates representing the location of each crossing
    def initializeCenters(self):
        centers = list()

        for i in range(0, len(self.grid)):
            for j in range(0, len(self.grid[i])):
                if self.grid[i][j] == 'h' or self.grid[i][j] == 'v':
                    centers.append([i,j])

        return centers

    # creates a grid which records the component occupying each grid entry
    def initializeComponentGrid(self):
        cGrid = [[]] * len(self.grid)

        for a in range(0, len(cGrid)):
            cGrid[a] = [' '] * len(self.grid[a])
            if a == -1:
                print("")
        for i in range(0, len(self.strandSequence)):
            for j in range(0, len(self.strandSequence[i])):
                if self.grid[self.strandSequence[i][j][0]][self.strandSequence[i][j][1]] != 'v' and self.grid[self.strandSequence[i][j][0]][self.strandSequence[i][j][1]] != 'h':
                    cGrid[self.strandSequence[i][j][0]][self.strandSequence[i][j][1]] = str(i+1)
                else:
                    cGrid[self.strandSequence[i][j][0]][self.strandSequence[i][j][1]] = 'X'

        return cGrid

    # creates a grid which records the orientation in each grid entry
    def initializeOrientationGrid(self):
        # initialize empty grid
        oGrid = [[]] * len(self.grid)
        for i in range(0, len(oGrid)):
            oGrid[i] = [' '] * len(self.grid[i])

        # for each strand sequence, record the orientation
        for i in range(0, len(self.strandSequence)):
            token = ''
            breaker = 0
            for j in range(0, len(self.strandSequence[i])-1):
                if token == 'X':
                    oGrid[self.strandSequence[i][j][0]][self.strandSequence[i][j][1]] = oGrid[self.strandSequence[i][j-3][0]][self.strandSequence[i][j-3][1]]
                    token = ''
                else:
                    token = self.grid[self.strandSequence[i][j][0]][self.strandSequence[i][j][1]]
                if token == 'ne':
                    if self.strandSequence[i][j][0] - self.strandSequence[i][j+1][0] == 1:
                        token = 'u'
                    else:
                        token = 'r'
                if token == 'nw':
                    if self.strandSequence[i][j][0] - self.strandSequence[i][j+1][0] == 1:
                        token = 'u'
                    else:
                        token = 'l'
                if token == 'se':
                    if self.strandSequence[i][j][0] - self.strandSequence[i][j+1][0] == -1:
                        token = 'd'
                    else:
                        token = 'r'
                if token == 'sw':
                    if self.strandSequence[i][j][0] - self.strandSequence[i][j+1][0] == -1:
                        token = 'd'
                    else:
                        token = 'l'
                if token == '':
                    if oGrid[self.strandSequence[i][j-1][0]][self.strandSequence[i][j-1][1]] == 'r':
                        token = 'r'
                    if oGrid[self.strandSequence[i][j-1][0]][self.strandSequence[i][j-1][1]] == 'l':
                        token = 'l'
                    if oGrid[self.strandSequence[i][j-1][0]][self.strandSequence[i][j-1][1]] == 'u':
                        token = 'u'
                    if oGrid[self.strandSequence[i][j-1][0]][self.strandSequence[i][j-1][1]] == 'd':
                        token = 'd'
                    if oGrid[self.strandSequence[i][j-1][0]][self.strandSequence[i][j-1][1]] == 'X':
                        token = oGrid[self.strandSequence[i][j-2][0]][self.strandSequence[i][j-2][1]]

                if token == 'v' or token == 'h':
                    token = 'X'

                oGrid[self.strandSequence[i][j][0]][self.strandSequence[i][j][1]] = token

        for i in range(0, len(oGrid)):
            for j in range(0, len(oGrid[i])):
                if oGrid[i][j] == 'X':
                    oGrid[i][j] = ''
                    # tunnel up
                    count = 1
                    while oGrid[i-count][j] not in ['l','r','u','d']:
                        count += 1
                    if oGrid[i-count][j] == 'd':
                        oGrid[i][j] = oGrid[i][j] + 'd'
                    # tunnel right
                    count = 1
                    while oGrid[i][j+count] not in ['l','r','u','d']:
                        count += 1
                    if oGrid[i][j+count] == 'l':
                        oGrid[i][j] = oGrid[i][j] + 'l'
                    # tunnel down
                    count = 1
                    while oGrid[i+count][j] not in ['l','r','u','d']:
                        count += 1
                    if oGrid[i+count][j] == 'u':
                        oGrid[i][j] = oGrid[i][j] + 'u'
                    # tunnel left
                    count = 1
                    while oGrid[i][j-count] not in ['l','r','u','d']:
                        count += 1
                    if oGrid[i][j-count] == 'r':
                        oGrid[i][j] = oGrid[i][j] + 'r'

        return oGrid

    # creates a grid which records the strand number in each entry
    def initializeStrandGrid(self):
        # initialize empty grid
        sGrid = [[]] * len(self.grid)
        for a in range(0, len(sGrid)):
            sGrid[a] = [''] * len(self.grid[a])

        for i in range(0, len(self.strands)):
            for j in range(0, len(self.strands[i])):
                for k in range(0, len(self.strands[i][j])):
                    if self.grid[self.strands[i][j][k][0]][self.strands[i][j][k][1]] != 'v' and self.grid[self.strands[i][j][k][0]][self.strands[i][j][k][1]] != 'h':
                        sGrid[self.strands[i][j][k][0]][self.strands[i][j][k][1]] = str(j+1)
                    else:
                        sGrid[self.strands[i][j][k][0]][self.strands[i][j][k][1]] = 'X'

        return sGrid

    def initializeCrossings(self):
        crossings = list()

        for i in range(0, len(self.grid)):
            for j in range(0, len(self.grid[i])):
                if self.grid[i][j] == 'h':
                    # tunnel up
                    upCount = 1
                    while self.strandGrid[i-upCount][j] == 'X':
                        upCount += 1
                    # tunnel right
                    rightCount = 1
                    while self.strandGrid[i][j+rightCount] == 'X':
                        rightCount += 1
                    # tunnel down
                    downCount = 1
                    while self.strandGrid[i+downCount][j] == 'X':
                        downCount += 1
                    # tunnel left
                    leftCount = 1
                    while self.strandGrid[i][j-leftCount] == 'X':
                        leftCount += 1
                    if 'd' in self.orientationGrid[i-upCount][j]:
                        if 'r' in self.orientationGrid[i][j - leftCount]:
                            crossings.append([int(self.strandGrid[i - upCount][j]) + upCount - 1,
                                              int(self.strandGrid[i][j - leftCount]) + leftCount - 1,
                                              int(self.strandGrid[i + downCount][j]) - downCount + 1,
                                              int(self.strandGrid[i][j + rightCount]) - rightCount + 1])
                        else:
                            crossings.append([int(self.strandGrid[i - upCount][j]) - upCount + 1,
                                              int(self.strandGrid[i][j - leftCount]) + leftCount - 1,
                                              int(self.strandGrid[i + downCount][j]) + downCount - 1,
                                              int(self.strandGrid[i][j + rightCount]) - rightCount + 1])
                    if 'u' in self.orientationGrid[i+downCount][j]:
                        if 'r' in self.orientationGrid[i][j - leftCount]:
                            crossings.append([int(self.strandGrid[i + downCount][j]) + downCount - 1,
                                              int(self.strandGrid[i][j + rightCount]) - rightCount + 1,
                                              int(self.strandGrid[i - upCount][j]) - upCount + 1,
                                              int(self.strandGrid[i][j - leftCount]) + leftCount - 1])
                        else:
                            crossings.append([int(self.strandGrid[i + downCount][j]) + downCount - 1,
                                              int(self.strandGrid[i][j + rightCount]) - rightCount + 1,
                                              int(self.strandGrid[i - upCount][j]) - upCount + 1,
                                              int(self.strandGrid[i][j - leftCount]) + leftCount - 1,])
                if self.grid[i][j] == 'v':
                    # tunnel up
                    upCount = 1
                    while self.strandGrid[i-upCount][j] == 'X':
                        upCount += 1
                    # tunnel right
                    rightCount = 1
                    while self.strandGrid[i][j+rightCount] == 'X':
                        rightCount += 1
                    # tunnel down
                    downCount = 1
                    while self.strandGrid[i+downCount][j] == 'X':
                        downCount += 1
                    # tunnel left
                    leftCount = 1
                    while self.strandGrid[i][j-leftCount] == 'X':
                        leftCount += 1
                    if 'r' in self.orientationGrid[i][j-leftCount]:
                        if 'd' in self.orientationGrid[i-upCount][j]:
                            crossings.append([int(self.strandGrid[i][j - leftCount]) + leftCount - 1,
                                              int(self.strandGrid[i + downCount][j]) - downCount + 1,
                                              int(self.strandGrid[i][j + rightCount]) - rightCount + 1,
                                              int(self.strandGrid[i - upCount][j]) + upCount - 1])
                        else:
                            crossings.append([int(self.strandGrid[i][j - leftCount]) + leftCount - 1,
                                              int(self.strandGrid[i + downCount][j]) + downCount - 1,
                                              int(self.strandGrid[i][j + rightCount]) - rightCount + 1,
                                              int(self.strandGrid[i - upCount][j]) - upCount + 1])
                    if 'l' in self.orientationGrid[i][j+rightCount]:
                        if 'd' in self.orientationGrid[i-upCount][j]:
                            crossings.append([int(self.strandGrid[i][j + rightCount]) + rightCount - 1,
                                              int(self.strandGrid[i - upCount][j]) + upCount - 1,
                                              int(self.strandGrid[i][j - leftCount]) - leftCount + 1,
                                              int(self.strandGrid[i + downCount][j]) - downCount + 1])
                        else:
                            crossings.append([int(self.strandGrid[i][j + rightCount]) + rightCount - 1,
                                              int(self.strandGrid[i - upCount][j]) - upCount + 1,
                                              int(self.strandGrid[i][j - leftCount]) - leftCount + 1,
                                              int(self.strandGrid[i + downCount][j]) + downCount - 1])

        for i in range(0, len(crossings)):
            for j in range(0, 4):
                crossings[i][j] = crossings[i][j] % self.strandNumbers[int(self.components[i][j])-1]
                if crossings[i][j] == 0:
                    crossings[i][j] = crossings[i][j] + len(self.strands[int(self.components[i][j])-1])

        return crossings

    # returns sequence of quadruplets, one for each crossing, indicating the components at the crossing
    def initializeComponents(self):
        components = list()

        for i in range(0, len(self.grid)):
            for j in range(0, len(self.grid[i])):
                if self.grid[i][j] == 'h':
                    # tunnel up
                    upCount = 1
                    while self.componentGrid[i - upCount][j] == 'X':
                        upCount += 1
                    # tunnel right
                    rightCount = 1
                    while self.componentGrid[i][j + rightCount] == 'X':
                        rightCount += 1
                    # tunnel down
                    downCount = 1
                    while self.componentGrid[i + downCount][j] == 'X':
                        downCount += 1
                    # tunnel left
                    leftCount = 1
                    while self.componentGrid[i][j - leftCount] == 'X':
                        leftCount += 1
                    if 'd' in self.orientationGrid[i-1][j]:
                        components.append([int(self.componentGrid[i-upCount][j]),
                                           int(self.componentGrid[i][j-leftCount]),
                                           int(self.componentGrid[i+downCount][j]),
                                           int(self.componentGrid[i][j+rightCount])])
                    if 'u' in self.orientationGrid[i+1][j]:
                        components.append([int(self.componentGrid[i+downCount][j]),
                                           int(self.componentGrid[i][j+rightCount]),
                                           int(self.componentGrid[i-upCount][j]),
                                           int(self.componentGrid[i][j-leftCount])])
                if self.grid[i][j] == 'v':
                    # tunnel up
                    upCount = 1
                    while self.componentGrid[i - upCount][j] == 'X':
                        upCount += 1
                    # tunnel right
                    rightCount = 1
                    while self.componentGrid[i][j + rightCount] == 'X':
                        rightCount += 1
                    # tunnel down
                    downCount = 1
                    while self.componentGrid[i + downCount][j] == 'X':
                        downCount += 1
                    # tunnel left
                    leftCount = 1
                    while self.componentGrid[i][j - leftCount] == 'X':
                        leftCount += 1
                    if 'r' in self.orientationGrid[i][j-1]:
                        components.append([int(self.componentGrid[i][j-leftCount]),
                                           int(self.componentGrid[i+downCount][j]),
                                           int(self.componentGrid[i][j+rightCount]),
                                           int(self.componentGrid[i-upCount][j])])
                    if 'l' in self.orientationGrid[i][j+1]:
                        components.append([int(self.componentGrid[i][j+rightCount]),
                                           int(self.componentGrid[i-upCount][j]),
                                           int(self.componentGrid[i][j-leftCount]),
                                           int(self.componentGrid[i+downCount][j])])

        return components

    def addRow(self, row=-1):
        if row == -1:
            row = len(self.grid)
        newRow = [''] * len(self.grid[0])
        self.grid.insert(row, newRow)
        self.canvas_height = ((len(self.grid) + 1) * 100)
        print("Row added after row " + str(row - 1))

    def removeRow(self, row=-1):
        if row == -1:
            row = len(self.grid)-1

        # Check for exceptions
        breaker = 0
        for i in range(0, len(self.grid[row])):
            if self.grid[row][i] != '':
                print("Row " + str(row) + " cannot be removed")
                breaker = -1
                break

        # Remove row (if no exceptions found)
        if breaker == 0:
            self.grid.pop(row)
            self.canvas_height = ((len(self.grid) + 1) * 100)
            print("Row " + str(row) + " removed")

    def addCol(self, col=-1):
        if col == -1:
            col = len(self.grid)

        for i in range(0, len(self.grid)):
            self.grid[i].insert(col, '')
        self.canvas_width = (len(self.grid[0]) + 1) * 100
        print("Column added after column " + str(col-1))

    def removeCol(self, col=-1):
        if col == -1:
            col = len(self.grid)

        # Check for exceptions
        breaker = 0
        for i in range(0, len(self.grid[0])-1):
            if self.grid[i][col] != '':
                breaker = -1

        # Remove column (if no exceptions found)
        if breaker == 0:
            for i in range(0, len(self.grid)):
                self.grid[i].pop(col)
            self.canvas_width = (len(self.grid[0]) + 1) * 100
            print("Column " + str(col) + " removed")
        else:
            print("Column " + str(col) + " cannot be removed")

    def viewDiagram(self):
        window = tk.Tk()
        window.geometry('750x750')
        window.configure(background='white')
        window.title("Diagram")

        my_canvas = tk.Canvas(window, width=650, height=650, bg="white")
        my_canvas.pack(pady=20)

        xScale = int(550/len(self.grid))
        yScale = int(550/len(self.grid[0]))
        m = min(xScale, yScale)
        m2 = m/2

        # # windows zoom
        # def zoomer(event):
        #     if (event.delta > 0):
        #         my_canvas.scale("all", event.x, event.y, 1.1, 1.1)
        #     elif (event.delta < 0):
        #         my_canvas.scale("all", event.x, event.y, 0.9, 0.9)
        #     my_canvas.configure(scrollregion=my_canvas.bbox("all"))
        #
        # # linux zoom
        # def zoomerP(event):
        #     my_canvas.scale("all", event.x, event.y, 1.1, 1.1)
        #     my_canvas.configure(scrollregion=my_canvas.bbox("all"))
        #
        # def zoomerM(self, event):
        #     my_canvas.scale("all", event.x, event.y, 0.9, 0.9)
        #     my_canvas.configure(scrollregion=my_canvas.bbox("all"))
        #
        # # linux scroll
        # my_canvas.bind("<Button-4>", zoomerP)
        # my_canvas.bind("<Button-5>", zoomerM)
        # # windows scroll
        # my_canvas.bind("<MouseWheel>", zoomer)
        # # Hack to make zoom work on Windows
        # window.bind_all("<MouseWheel>", zoomer)

        # Draw Grid
        # horizontal lines
        for i in range(0, len(self.grid)+1):
            my_canvas.create_line(m2, i*m+m2, (len(self.grid[0])+1)*m-m2, i*m+m2, fill='gray')
        # vertical lines
        for i in range(0, len(self.grid[0])+1):
            my_canvas.create_line(i*m+m2, m2, i*m+m2, (len(self.grid)+1)*m-m2, fill='gray')

        # Draw Crossings
        # vertical crossings
        for i in range(0, len(self.grid)):
            for j in range(0, len(self.grid[0])):
                if self.grid[i][j] == 'v':
                    my_canvas.create_line(j*m+2*m2, i*m+m2, j*m+2*m2, i*m+3*m2, width=3)
                    my_canvas.create_line(j*m+m2, i*m+2*m2, j*m+3*m2/2, i*m+2*m2, width=3)
                    my_canvas.create_line(j*m+5*m2/2, i*m+2*m2, j*m+3*m2, i*m+2*m2, width=3)
        # horizontal crossings
        for i in range(0, len(self.grid)):
            for j in range(0, len(self.grid[0])):
                if self.grid[i][j] == 'h':
                    my_canvas.create_line(j*m+2*m2, i*m+m2, j*m+2*m2, i*m+3/2*m2, width=3)
                    my_canvas.create_line(j*m+2*m2, i*m+5/2*m2, j*m+2*m2, i*m+3*m2, width=3)
                    my_canvas.create_line(j*m+m2, i*m+2*m2, j*m+3*m2, i*m+2*m2, width=3)

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
        # for i in range(0, len(self.grid)):
        #     for j in range(0, len(self.grid[0])):
        #         if self.grid[i][j] == 'ne':
        #             my_canvas.create_arc(j * 100 + 100, i * 100, j * 100 + 200, i * 100 + 100, start=180,
        #                                  extent=90, style=tk.ARC, width=3)
        #         if self.grid[i][j] == 'nw':
        #             my_canvas.create_arc(j * 100, i * 100, j * 100 + 100, i * 100 + 100, start=270, extent=90,
        #                                  style=tk.ARC, width=3)
        #         if self.grid[i][j] == 'se':
        #             my_canvas.create_arc(j * 100 + 100, i * 100 + 100, j * 100 + 200, i * 100 + 200, start=90,
        #                                  extent=90,
        #                                  style=tk.ARC, width=3)
        #         if self.grid[i][j] == 'sw':
        #             my_canvas.create_arc(j * 100, i * 100 + 100, j * 100 + 100, i * 100 + 200, start=0,
        #                                  extent=90, style=tk.ARC, width=3)

        # # Draw strand numbers
        # for k in range(0, len(self.strands)):
        #     for i in range(0, len(self.strands[k])):
        #         if len(self.strands[k][i]) % 2 == 0:
        #             mid = int(len(self.strands[k][i])/2)
        #             xAvg = (self.strands[k][i][mid][1] + self.strands[k][i][mid - 1][1]) / 2
        #             yAvg = (self.strands[k][i][mid][0] + self.strands[k][i][mid - 1][0]) / 2
        #             my_canvas.create_text(xAvg * m + 2*m2+10, yAvg * m + 2*m2+10, text=str(i + 1), fill="blue")
        #         else:
        #             mid = int((len(self.strands[k][i])-1)/2)
        #             my_canvas.create_text(self.strands[k][i][mid][1]*m+2*m2+10, self.strands[k][i][mid][0]*m+2*m2+10, text=str(i + 1), fill="blue")

        # Draw crossing numbers
        for i in range(0, len(self.centers)):
            my_canvas.create_polygon(self.centers[i][1]*m+3/2*m2, self.centers[i][0]*m+3/2*m2-10, self.centers[i][1]*m+3/2*m2-10, self.centers[i][0]*m+3/2*m2, self.centers[i][1]*m+3/2*m2, self.centers[i][0]*m+3/2*m2+10, self.centers[i][1]*m+3/2*m2+10, self.centers[i][0]*m+3/2*m2, outline="red", fill="white")
            my_canvas.create_text(self.centers[i][1]*m+3/2*m2, self.centers[i][0]*m+3/2*m2, text=str(i+1), fill="red")

        # Draw component numbers
        for i in range(0, len(self.strands)):
            midIndex = int(len(self.strands[i][0])/3)
            my_canvas.create_text(self.strands[i][0][midIndex][1]*m+5/2*m2, self.strands[i][0][midIndex][0]*m+3/2*m2, text=str(i+1), fill="green")
            my_canvas.create_oval(self.strands[i][0][midIndex][1]*m+5/2*m2+8, self.strands[i][0][midIndex][0]*m+3/2*m2+8,
                                  self.strands[i][0][midIndex][1]*m+5/2*m2-8, self.strands[i][0][midIndex][0]*m+3/2*m2-8, outline="green")

        # Draw orientations
        for i in range(0, len(self.strands)):
            # find entry from strand[i][0] not common to other strands

            u = self.findUniqueStrandEntry(i)
            u1 = u[0]
            u2 = u[1]

            draw = 0
            if 'u' in self.orientationGrid[self.strands[i][u1][u2][0]][self.strands[i][u1][u2][1]]:
                if draw == 0:
                    my_canvas.create_line(self.strands[i][u1][u2][1]*m+2*m2, self.strands[i][u1][u2][0]*m+3/2*m2,
                                          self.strands[i][u1][u2][1]*m+2*m2, self.strands[i][u1][u2][0]*m+m2, arrow=tk.LAST, width=3)
                    draw += 1
            if 'd' in self.orientationGrid[self.strands[i][u1][u2][0]][self.strands[i][u1][u2][1]]:
                if draw == 0:
                    my_canvas.create_line(self.strands[i][u1][u2][1]*m+2*m2, self.strands[i][u1][u2][0]*m+5/2*m2,
                                          self.strands[i][u1][u2][1]*m+2*m2, self.strands[i][u1][u2][0]*m+3*m2,
                                          arrow=tk.LAST, width=3)
                    draw += 1
            if 'l' in self.orientationGrid[self.strands[i][u1][u2][0]][self.strands[i][u1][u2][1]]:
                if draw == 0:
                    my_canvas.create_line(self.strands[i][u1][u2][1]*m+3/2*m2, self.strands[i][u1][u2][0]*m+2*m2,
                                          self.strands[i][u1][u2][1]*m+m2, self.strands[i][u1][u2][0]*m+2*m2,
                                          arrow=tk.LAST, width=3)
                    draw += 1
            if 'r' in self.orientationGrid[self.strands[i][u1][u2][0]][self.strands[i][u1][u2][1]]:
                if draw == 0:
                    my_canvas.create_line(self.strands[i][u1][u2][1]*m+5/2*m2, self.strands[i][u1][u2][0]*m+2*m2,
                                          self.strands[i][u1][u2][1]*m+3*m2, self.strands[i][u1][u2][0]*m+2*m2,
                                          arrow=tk.LAST, width=3)
                    draw += 1

        # Key
        my_canvas.create_oval(m2 + 8, 620 + 8, m2 - 8, 620 - 8, outline="green")
        my_canvas.create_text(m2+55, 620, text='link component', fill="green")
        my_canvas.create_text(m2, 620, text='#', fill="green")

        my_canvas.create_polygon(m2+125, 620-10, m2+125-10, 620, m2+125, 620+10, m2+125+10, 620, outline="red", fill="white")
        my_canvas.create_text(m2 + 185, 620, text='crossing number', fill="red")
        my_canvas.create_text(m2 + 125, 620, text='#', fill="red")

        window.mainloop()

    def previewSmoothing(self, binarySequence):
        if binarySequence == "":
            print("No binary sequence provided")
            return 0

        Generator.Generator(self, binarySequence, "").viewGenerator()

    def findUniqueStrandEntry(self, i):
        # iterate through strands from component
        for j in range(0, len(self.strands[i])):

            # iterate through entries of strand
            for k in range(0, len(self.strands[i][j])):
                breaker = 0
                # iterate through other components
                for l in range(0, len(self.strands)):
                    if l != i:
                        # iterate through other component strands
                        for m in range(0, len(self.strands[l])):
                            # check to see if strand entry is in other component strand
                            if self.strands[i][j][k] in self.strands[l][m]:
                                breaker = -1
                if breaker != -1:
                    return [j, k]

    # returns a sequence, whose elements are sequences of coordinates (one for each link component)
    def initializeStrandSequence(self):
        strands = list()

        for i in range(0, len(self.grid)):
            for j in range(0, len(self.grid[i])):
                if self.grid[i][j] != '' and self.grid[i][j] != 'v' and self.grid[i][j] != 'h':
                    count = 0
                    for k in range(0, len(strands)):
                        if [i,j] in strands[k]:
                            count += 1
                    if count == 0:
                        strands.append(self.nextStrand([[i,j]], i, j, i, j+1))
                # if self.grid[i][j] == 'v' or self.grid[i][j] == 'h':
                #     count = 0
                #     for k in range(0, len(strands)):
                #         for l in range(0, len(strands[k])):
                #             if [i,j] == strands[k][l]:
                #                 count += 1
                #     if count != 2:
                #         strands.append(self.nextStrand([[i,j]], i, j, i, j+1))
        if strands == []:
            strands.append(self.nextStrand([[0, 0]], 0, 0, 0, 1))
            return strands
        else:
            return strands

    def nextStrand(self, strands, x1, y1, x2, y2):
        # Base step
        if len(strands) > 1:
            if [x1,y1] == strands[0] and [x2,y2] == strands[1]:
                return strands

        # Recursive step
        # append new square
        strands.append([x2, y2])
        # find next square to append
        if self.grid[x2][y2] == '' or self.grid[x2][y2] == 'h' or self.grid[x2][y2] == 'v':
            if x2 == x1+1:
                self.nextStrand(strands, x2, y2, x2+1, y2)
            if x2 == x1-1:
                self.nextStrand(strands, x2, y2, x2-1, y2)
            if y2 == y1+1:
                self.nextStrand(strands, x2, y2, x2, y2+1)
            if y2 == y1-1:
                self.nextStrand(strands, x2, y2, x2, y2-1)
        if self.grid[x2][y2] == 'ne':
            # if you came from the north
            if x2 == x1+1:
                # then go east
                self.nextStrand(strands, x2, y2, x2, y2+1)
            # if you came from the east
            if y2 == y1-1:
                # then go north
                self.nextStrand(strands, x2, y2, x2-1, y2)
        if self.grid[x2][y2] == 'nw':
            # if you came from the north
            if x2 == x1+1:
                # then go west
                self.nextStrand(strands, x2, y2, x2, y2-1)
            # if you came from the west
            if y2 == y1+1:
                # then go north
                self.nextStrand(strands, x2, y2, x2-1, y2)
        if self.grid[x2][y2] == 'se':
            # if you came from the south
            if x2 == x1-1:
                # then go east
                self.nextStrand(strands, x2, y2, x2, y2+1)
            # if you came from the east
            if y2 == y1-1:
                # then go south
                self.nextStrand(strands, x2, y2, x2+1, y2)
        if self.grid[x2][y2] == 'sw':
            # if you came from the south
            if x2 == x1-1:
                # then go west
                self.nextStrand(strands, x2, y2, x2, y2-1)
            # if you came from the west
            if y2 == y1+1:
                # then go south
                self.nextStrand(strands, x2, y2, x2+1, y2)
        return strands

    # returns a sequence, whose elements are sequences of strands (which are sequences of coordinates, taken from strandSequence)
    def initializeStrands(self):
        strands = list()
        for i in range(0, len(self.strandSequence)):
            index = 0
            strands.append([])
            for j in range(1, len(self.strandSequence[i])):
                if self.grid[self.strandSequence[i][j][0]][self.strandSequence[i][j][1]] == 'v' or self.grid[self.strandSequence[i][j][0]][self.strandSequence[i][j][1]] == 'h':
                    strands[i].append(self.strandSequence[i][index:j+1])
                    index = j
            if strands == [[]]:
                strands[i].append(self.strandSequence[i])
            if strands[i][0][0] != self.strandSequence[i][index]:
                strands[i][0] = self.strandSequence[i][index:j] + strands[i][0]

        if self.strandSequence[0][0] == 'v':
            strands.append(self.strandSequence[index:len(self.strandSequence)])
        elif index != 0:
            strands[0] = self.strandSequence[index:len(self.strandSequence)] + strands[0]

        return strands

    def initializeCrossingOrientations(self):
        # reset initialized variables (in case initialization is redone)
        self.np = 0
        self.nn = 0
        crossingOrientationGrid = [[]] * len(self.grid)
        for a in range(0, len(crossingOrientationGrid)):
            crossingOrientationGrid[a] = [''] * len(self.grid[a])

        for i in range(len(self.centers)):
            center = self.grid[self.centers[i][0]][self.centers[i][1]]
            left = self.orientationGrid[self.centers[i][0]][self.centers[i][1]-1]
            right = self.orientationGrid[self.centers[i][0]][self.centers[i][1]+1]
            up = self.orientationGrid[self.centers[i][0]+1][self.centers[i][1]]
            down = self.orientationGrid[self.centers[i][0]-1][self.centers[i][1]]
            if center == 'v':
                if left == 'r':
                    if up == 'd':
                        self.np += 1
                        crossingOrientationGrid[self.centers[i][0]][self.centers[i][1]] = 'p'
                    else:
                        self.nn += 1
                        crossingOrientationGrid[self.centers[i][0]][self.centers[i][1]] = 'n'
                else:
                    if up == 'd':
                        self.nn += 1
                        crossingOrientationGrid[self.centers[i][0]][self.centers[i][1]] = 'n'
                    else:
                        self.np += 1
                        crossingOrientationGrid[self.centers[i][0]][self.centers[i][1]] = 'p'
            if center == 'h':
                if down == 'u':
                    if left == 'r':
                        self.np += 1
                        crossingOrientationGrid[self.centers[i][0]][self.centers[i][1]] = 'p'
                    else:
                        self.nn += 1
                        crossingOrientationGrid[self.centers[i][0]][self.centers[i][1]] = 'n'
                else:
                    if left == 'r':
                        self.nn += 1
                        crossingOrientationGrid[self.centers[i][0]][self.centers[i][1]] = 'n'
                    else:
                        self.np += 1
                        crossingOrientationGrid[self.centers[i][0]][self.centers[i][1]] = 'p'
        self.crossingOrientationGrid = crossingOrientationGrid

    def initializeFineGrid(self):
        newGrid = [[]] * len(self.grid)
        for a in range(0, len(newGrid)):
            newGrid[a] = [''] * len(self.grid[a])

        for i in range(0, len(self.grid)):
            for j in range(0, len(self.grid[i])):
                newGrid[i][j] = self.grid[i][j]

        for i in range(0, len(self.grid)):
            for j in range(0, len(self.grid[i])):
                newGrid[2*i].insert(2 * j, '')
            newRow = [''] * len(newGrid[0])
            newGrid.insert(2 * i, newRow)
        newGrid.pop(0)
        for i in range(0, len(newGrid)):
            newGrid[i].pop(0)
        return newGrid

    def reEnumerate(self, order):
        order = order.split(',')
        order = list(map(int, order))
        self.crossings = [self.crossings[i-1] for i in order]
        self.centers = [self.centers[i-1] for i in order]

    def changeOrientation(self, component):
        self.strandSequence[component].reverse()

        # re-initialize diagram
        self.strands = self.initializeStrands()
        self.strandNumbers = self.initializeStrandNumbers()
        self.componentGrid = self.initializeComponentGrid()
        self.strandGrid = self.initializeStrandGrid()
        self.orientationGrid = self.initializeOrientationGrid()
        self.components = self.initializeComponents()
        self.crossings = self.initializeCrossings()
        self.n = len(self.crossings)
        self.initializeCrossingOrientations()