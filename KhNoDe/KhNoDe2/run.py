import DrawDiagram
import Diagram
import Generator
import Chain
import ChainComplex
from sympy import *
import tkinter as tk
from tkinter.filedialog import asksaveasfile
from tkinter import filedialog as fd


class run():

    def __init__(self):
        self.my_color_background = "grey90"
        self.my_color_border = "gray12"
        self.my_color_font = "gray10"
        self.my_color_light = "gray80"
        self.my_color_light2 = "gray70"
        self.mode = "light"

        self.root = tk.Tk()
        self.root.geometry("900x730")
        self.root.title("Kh-NoDe")
        self.root.resizable(0,0)
        self.root.configure(bg=self.my_color_background)

        # configure the grid
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=3)

        menubar = tk.Menu(self.root)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.configure(bg=self.my_color_background, fg=self.my_color_font)
        filemenu.add_command(label="New Diagram", command=lambda: [self.updateCanvas(), self.drawDiagram(), self.drawGenerators(0)])
        filemenu.add_command(label="Save", command=lambda: self.save())
        filemenu.add_command(label="Load", command=lambda: self.load())
        filemenu.add_command(label="Exit", command=lambda: self.root.destroy())
        menubar.add_cascade(label="File", menu=filemenu)

        modemenu = tk.Menu(menubar, tearoff=0, background=self.my_color_background, fg=self.my_color_font, )
        modemenu.add_command(label="Dark mode", command=lambda: self.darkMode())
        modemenu.add_command(label="Light mode", command=lambda: self.lightMode())
        menubar.add_cascade(label="Modes", menu=modemenu)

        self.root.config(menu=menubar)

        # initialize variables
        self.D = [] # diagram
        self.G = [] # generators
        self.generatorNumber = -1
        self.C = [] # chain
        self.cycleText = ''
        self.CC = [] # chain complex
        self.boundaryText = ''

        # Create a canvas widget
        self.viewDiagramCanvas = tk.Canvas(self.root, width=300, height=300, highlightthickness=0)
        self.viewDiagramCanvas.place(x=0, y=0)
        self.viewDiagramCanvas.configure(bg=self.my_color_background)
        
        self.diagCanvas = tk.Canvas(self.root, width=300, height=300, highlightthickness=0)
        self.diagCanvas.place(x=300, y=30)
        self.diagCanvas.configure(bg=self.my_color_background)

        self.viewGeneratorsCanvas = tk.Canvas(self.root, width=300, height=400, highlightthickness=0)
        self.viewGeneratorsCanvas.place(x=0, y=300)
        self.viewGeneratorsCanvas.configure(bg=self.my_color_background)
        
        self.genCanvas = tk.Canvas(self.root, width=300, height=350, highlightthickness=0)
        self.genCanvas.place(x=300, y=330)
        self.genCanvas.configure(bg=self.my_color_background)

        self.chainCanvas = tk.Canvas(self.root, width=300, heigh=300, highlightthickness=0)
        self.chainCanvas.place(x=600, y=30)
        self.chainCanvas.configure(bg=self.my_color_background)

        self.boundaryCanvas = tk.Canvas(self.root, width=300, height=300, highlightthickness=0)
        self.boundaryCanvas.place(x=600, y=330)
        self.boundaryCanvas.configure(bg=self.my_color_background)

        self.root.mainloop()

    def darkMode(self):
        print("Feature unavailable with basic package. Update to premium!")
        # self.my_color_background = "grey17"
        # self.my_color_font = "gray75"
        # self.my_color_light = "gray30"
        # self.my_color_light2 = "gray40"
        self.mode = "dark"
        self.updateCanvas()

    def lightMode(self):
        print("Feature unavailable with basic package. Update to premium!")
        self.mode = "light"
        self.updateCanvas()
        
    def drawDiagram(self):
        xScale = int(250 / len(self.D.grid))
        yScale = int(250 / len(self.D.grid[0]))
        m = min(xScale, yScale)
        m2 = m / 2

        # # windows zoom
        # def zoomer(event):
        #     if (event.delta > 0):
        #         self.viewDiagramCanvas.scale("all", event.x, event.y, 1.1, 1.1)
        #     elif (event.delta < 0):
        #         self.viewDiagramCanvas.scale("all", event.x, event.y, 0.9, 0.9)
        #     self.viewDiagramCanvas.configure(scrollregion=self.viewDiagramCanvas.bbox("all"))
        #
        # # linux zoom
        # def zoomerP(event):
        #     self.viewDiagramCanvas.scale("all", event.x, event.y, 1.1, 1.1)
        #     self.viewDiagramCanvas.configure(scrollregion=self.viewDiagramCanvas.bbox("all"))
        #
        # def zoomerM(self, event):
        #     self.viewDiagramCanvas.scale("all", event.x, event.y, 0.9, 0.9)
        #     self.viewDiagramCanvas.configure(scrollregion=self.viewDiagramCanvas.bbox("all"))
        #
        # # linux scroll
        # self.viewDiagramCanvas.bind("<Button-4>", zoomerP)
        # self.viewDiagramCanvas.bind("<Button-5>", zoomerM)
        # # windows scroll
        # self.viewDiagramCanvas.bind("<MouseWheel>", zoomer)
        # # Hack to make zoom work on Windows
        # window.bind_all("<MouseWheel>", zoomer)

        # Draw Grid
        # horizontal lines
        for i in range(0, len(self.D.grid) + 1):
            self.viewDiagramCanvas.create_line(m2, i * m + m2, (len(self.D.grid[0]) + 1) * m - m2, i * m + m2, fill=self.my_color_light2)
        # vertical lines
        for i in range(0, len(self.D.grid[0]) + 1):
            self.viewDiagramCanvas.create_line(i * m + m2, m2, i * m + m2, (len(self.D.grid) + 1) * m - m2, fill=self.my_color_light2)

        # Draw Crossings
        # vertical crossings
        for i in range(0, len(self.D.grid)):
            for j in range(0, len(self.D.grid[0])):
                if self.D.grid[i][j] == 'v':
                    self.viewDiagramCanvas.create_line(j * m + 2 * m2, i * m + m2, j * m + 2 * m2, i * m + 3 * m2, width=3)
                    self.viewDiagramCanvas.create_line(j * m + m2, i * m + 2 * m2, j * m + 3 * m2 / 2, i * m + 2 * m2, width=3)
                    self.viewDiagramCanvas.create_line(j * m + 5 * m2 / 2, i * m + 2 * m2, j * m + 3 * m2, i * m + 2 * m2,
                                          width=3)
        # horizontal crossings
        for i in range(0, len(self.D.grid)):
            for j in range(0, len(self.D.grid[0])):
                if self.D.grid[i][j] == 'h':
                    self.viewDiagramCanvas.create_line(j * m + 2 * m2, i * m + m2, j * m + 2 * m2, i * m + 3 / 2 * m2, width=3)
                    self.viewDiagramCanvas.create_line(j * m + 2 * m2, i * m + 5 / 2 * m2, j * m + 2 * m2, i * m + 3 * m2,
                                          width=3)
                    self.viewDiagramCanvas.create_line(j * m + m2, i * m + 2 * m2, j * m + 3 * m2, i * m + 2 * m2, width=3)

        # Draw horizontal lines
        for i in range(0, len(self.D.grid)):
            for j in range(0, len(self.D.grid[0])):
                if 'e' in self.D.grid[i][j]:
                    c = j + 1
                    while 'w' not in self.D.grid[i][c]:
                        if self.D.grid[i][c] != 'v' and self.D.grid[i][c] != 'h':
                            self.viewDiagramCanvas.create_line(c * m + m2, i * m + 2 * m2, c * m + 3 * m2, i * m + 2 * m2,
                                                  width=3)
                        c += 1

        # Draw vertical lines
        for j in range(0, len(self.D.grid[0])):
            for i in range(0, len(self.D.grid)):
                if 's' in self.D.grid[i][j]:
                    c = i + 1
                    while 'n' not in self.D.grid[c][j]:
                        if self.D.grid[c][j] != 'v' and self.D.grid[c][j] != 'h':
                            self.viewDiagramCanvas.create_line(j * m + 2 * m2, c * m + m2, j * m + 2 * m2, c * m + 3 * m2,
                                                  width=3)
                        c += 1

        # Draw straight corners
        for i in range(0, len(self.D.grid)):
            for j in range(0, len(self.D.grid[0])):
                if self.D.grid[i][j] == 'ne':
                    self.viewDiagramCanvas.create_line(j * m + 2 * m2, i * m + 2 * m2, j * m + 3 * m2, i * m + 2 * m2, width=3)
                    self.viewDiagramCanvas.create_line(j * m + 2 * m2, i * m + m2, j * m + 2 * m2, i * m + 2 * m2, width=3)
                if self.D.grid[i][j] == 'nw':
                    self.viewDiagramCanvas.create_line(j * m + m2, i * m + 2 * m2, j * m + 2 * m2, i * m + 2 * m2, width=3)
                    self.viewDiagramCanvas.create_line(j * m + 2 * m2, i * m + m2, j * m + 2 * m2, i * m + 2 * m2, width=3)
                if self.D.grid[i][j] == 'se':
                    self.viewDiagramCanvas.create_line(j * m + 2 * m2, i * m + 2 * m2, j * m + 3 * m2, i * m + 2 * m2, width=3)
                    self.viewDiagramCanvas.create_line(j * m + 2 * m2, (i + 1) * m, j * m + 2 * m2, (i + 1) * m + m2, width=3)
                if self.D.grid[i][j] == 'sw':
                    self.viewDiagramCanvas.create_line(j * m + m2, i * m + 2 * m2, j * m + 2 * m2, i * m + 2 * m2, width=3)
                    self.viewDiagramCanvas.create_line(j * m + 2 * m2, (i + 1) * m, j * m + 2 * m2, (i + 1) * m + m2, width=3)

        # # Draw rounded corners
        # for i in range(0, len(self.D.grid)):
        #     for j in range(0, len(self.D.grid[0])):
        #         if self.D.grid[i][j] == 'ne':
        #             self.viewDiagramCanvas.create_arc(j * 100 + 100, i * 100, j * 100 + 200, i * 100 + 100, start=180,
        #                                  extent=90, style=tk.ARC, width=3)
        #         if self.D.grid[i][j] == 'nw':
        #             self.viewDiagramCanvas.create_arc(j * 100, i * 100, j * 100 + 100, i * 100 + 100, start=270, extent=90,
        #                                  style=tk.ARC, width=3)
        #         if self.D.grid[i][j] == 'se':
        #             self.viewDiagramCanvas.create_arc(j * 100 + 100, i * 100 + 100, j * 100 + 200, i * 100 + 200, start=90,
        #                                  extent=90,
        #                                  style=tk.ARC, width=3)
        #         if self.D.grid[i][j] == 'sw':
        #             self.viewDiagramCanvas.create_arc(j * 100, i * 100 + 100, j * 100 + 100, i * 100 + 200, start=0,
        #                                  extent=90, style=tk.ARC, width=3)

        # # Draw strand numbers
        # for k in range(0, len(self.strands)):
        #     for i in range(0, len(self.strands[k])):
        #         if len(self.strands[k][i]) % 2 == 0:
        #             mid = int(len(self.strands[k][i])/2)
        #             xAvg = (self.strands[k][i][mid][1] + self.strands[k][i][mid - 1][1]) / 2
        #             yAvg = (self.strands[k][i][mid][0] + self.strands[k][i][mid - 1][0]) / 2
        #             self.viewDiagramCanvas.create_text(xAvg * m + 2*m2+10, yAvg * m + 2*m2+10, text=str(i + 1), fill="blue")
        #         else:
        #             mid = int((len(self.strands[k][i])-1)/2)
        #             self.viewDiagramCanvas.create_text(self.strands[k][i][mid][1]*m+2*m2+10, self.strands[k][i][mid][0]*m+2*m2+10, text=str(i + 1), fill="blue")

        # Draw crossing enumeration
        for i in range(0, len(self.D.centers)):
            self.viewDiagramCanvas.create_text(self.D.centers[i][1] * m + 3 / 2 * m2, self.D.centers[i][0] * m + 3 / 2 * m2,
                                  text=str(i + 1), fill="red")

        # Draw component enumeration
        for i in range(0, len(self.D.strands)):
            midIndex = int(len(self.D.strands[i][0]) / 3)
            self.viewDiagramCanvas.create_text(self.D.strands[i][0][midIndex][1] * m + 5 / 2 * m2,
                                  self.D.strands[i][0][midIndex][0] * m + 3 / 2 * m2, text=str(i + 1), fill="green")

        # Draw orientations
        for i in range(0, len(self.D.strands)):
            # find entry from strand[i][0] not common to other strands

            u = self.D.findUniqueStrandEntry(i)
            u1 = u[0]
            u2 = u[1]

            draw = 0
            if 'u' in self.D.orientationGrid[self.D.strands[i][u1][u2][0]][self.D.strands[i][u1][u2][1]]:
                if draw == 0:
                    self.viewDiagramCanvas.create_line(self.D.strands[i][u1][u2][1] * m + 2 * m2,
                                          self.D.strands[i][u1][u2][0] * m + 3 / 2 * m2,
                                          self.D.strands[i][u1][u2][1] * m + 2 * m2,
                                          self.D.strands[i][u1][u2][0] * m + m2, arrow=tk.LAST, width=3)
                    draw += 1
            if 'd' in self.D.orientationGrid[self.D.strands[i][u1][u2][0]][self.D.strands[i][u1][u2][1]]:
                if draw == 0:
                    self.viewDiagramCanvas.create_line(self.D.strands[i][u1][u2][1] * m + 2 * m2,
                                          self.D.strands[i][u1][u2][0] * m + 5 / 2 * m2,
                                          self.D.strands[i][u1][u2][1] * m + 2 * m2,
                                          self.D.strands[i][u1][u2][0] * m + 3 * m2,
                                          arrow=tk.LAST, width=3)
                    draw += 1
            if 'l' in self.D.orientationGrid[self.D.strands[i][u1][u2][0]][self.D.strands[i][u1][u2][1]]:
                if draw == 0:
                    self.viewDiagramCanvas.create_line(self.D.strands[i][u1][u2][1] * m + 3 / 2 * m2,
                                          self.D.strands[i][u1][u2][0] * m + 2 * m2,
                                          self.D.strands[i][u1][u2][1] * m + m2,
                                          self.D.strands[i][u1][u2][0] * m + 2 * m2,
                                          arrow=tk.LAST, width=3)
                    draw += 1
            if 'r' in self.D.orientationGrid[self.D.strands[i][u1][u2][0]][self.D.strands[i][u1][u2][1]]:
                if draw == 0:
                    self.viewDiagramCanvas.create_line(self.D.strands[i][u1][u2][1] * m + 5 / 2 * m2,
                                          self.D.strands[i][u1][u2][0] * m + 2 * m2,
                                          self.D.strands[i][u1][u2][1] * m + 3 * m2,
                                          self.D.strands[i][u1][u2][0] * m + 2 * m2,
                                          arrow=tk.LAST, width=3)
                    draw += 1
                    
    def drawGenerators(self, genNumber):
        self.viewGeneratorsCanvas.delete("all")

        xScale = int(250 / len(self.D.grid))
        yScale = int(250 / len(self.D.grid[0]))
        m = min(xScale, yScale)
        m2 = m / 2
        
        if self.G == []:
            # Draw Grid
            # horizontal lines
            for i in range(0, len(self.D.grid) + 1):
                self.viewGeneratorsCanvas.create_line(m2, i * m + m2, (len(self.D.grid[0]) + 1) * m - m2, i * m + m2, fill='gray')
            # vertical lines
            for i in range(0, len(self.D.grid[0]) + 1):
                self.viewGeneratorsCanvas.create_line(i * m + m2, m2, i * m + m2, (len(self.D.grid) + 1) * m - m2, fill='gray')
        else:
            # Draw Grid
            # horizontal lines
            for i in range(0, len(self.D.grid) + 1):
                self.viewGeneratorsCanvas.create_line(m2, i * m + m2, (len(self.D.grid[0]) + 1) * m - m2, i * m + m2, fill='gray')
            # vertical lines
            for i in range(0, len(self.D.grid[0]) + 1):
                self.viewGeneratorsCanvas.create_line(i * m + m2, m2, i * m + m2, (len(self.D.grid) + 1) * m - m2, fill='gray')

            # Draw smoothings
            # cycle through centers
            for i in range(0, len(self.D.centers)):
                y = self.D.centers[i][0]
                x = self.D.centers[i][1]
                if self.D.grid[y][x] == 'v':
                    if self.G[genNumber].binarySequence[i] == '0':
                        self.viewGeneratorsCanvas.create_arc(x * m + 2 * m2, y * m, x * m + 4 * m2, y * m + 2 * m2, start=180,
                                             extent=90, style=tk.ARC, width=3)
                        self.viewGeneratorsCanvas.create_arc(x * m, y * m + 2 * m2, x * m + 2 * m2, y * m + 4 * m2, start=0,
                                             extent=90, style=tk.ARC, width=3)
                    if self.G[genNumber].binarySequence[i] == '1':
                        self.viewGeneratorsCanvas.create_arc(x * m, y * m, x * m + 2 * m2, y * m + 2 * m2, start=270,
                                             extent=90, style=tk.ARC, width=3)
                        self.viewGeneratorsCanvas.create_arc(x * m + 2 * m2, y * m + 2 * m2, x * m + 4 * m2, y * m + 4 * m2, start=90,
                                             extent=90, style=tk.ARC, width=3)
                if self.D.grid[y][x] == 'h':
                    if self.G[genNumber].binarySequence[i] == '0':
                        self.viewGeneratorsCanvas.create_arc(x * m, y * m, x * m + 2 * m2, y * m + 2 * m2, start=270,
                                             extent=90, style=tk.ARC, width=3)
                        self.viewGeneratorsCanvas.create_arc(x * m + 4 * m2, y * m + 2 * m2, x * m + 2 * m2, y * m + 4 * m2, start=90,
                                             extent=90, style=tk.ARC, width=3)
                    if self.G[genNumber].binarySequence[i] == '1':
                        self.viewGeneratorsCanvas.create_arc(x * m + 2 * m2, y * m, x * m + 4 * m2, y * m + 2 * m2, start=180,
                                             extent=90, style=tk.ARC, width=3)
                        self.viewGeneratorsCanvas.create_arc(x * m, y * m + 2 * m2, x * m + 2 * m2, y * m + 4 * m2, start=0,
                                             extent=90, style=tk.ARC, width=3)

            # Draw horizontal lines
            for i in range(0, len(self.D.grid)):
                for j in range(0, len(self.D.grid[0])):
                    if 'e' in self.D.grid[i][j]:
                        c = j + 1
                        while 'w' not in self.D.grid[i][c]:
                            if self.D.grid[i][c] != 'v' and self.D.grid[i][c] != 'h':
                                self.viewGeneratorsCanvas.create_line(c * m + m2, i * m + 2 * m2, c * m + 3 * m2, i * m + 2 * m2,
                                                      width=3)
                            c += 1

            # Draw vertical lines
            for j in range(0, len(self.D.grid[0])):
                for i in range(0, len(self.D.grid)):
                    if 's' in self.D.grid[i][j]:
                        c = i + 1
                        while 'n' not in self.D.grid[c][j]:
                            if self.D.grid[c][j] != 'v' and self.D.grid[c][j] != 'h':
                                self.viewGeneratorsCanvas.create_line(j * m + 2 * m2, c * m + m2, j * m + 2 * m2, c * m + 3 * m2,
                                                      width=3)
                            c += 1

            # Draw straight corners
            for i in range(0, len(self.D.grid)):
                for j in range(0, len(self.D.grid[0])):
                    if self.D.grid[i][j] == 'ne':
                        self.viewGeneratorsCanvas.create_line(j * m + 2 * m2, i * m + 2 * m2, j * m + 3 * m2, i * m + 2 * m2, width=3)
                        self.viewGeneratorsCanvas.create_line(j * m + 2 * m2, i * m + m2, j * m + 2 * m2, i * m + 2 * m2, width=3)
                    if self.D.grid[i][j] == 'nw':
                        self.viewGeneratorsCanvas.create_line(j * m + m2, i * m + 2 * m2, j * m + 2 * m2, i * m + 2 * m2, width=3)
                        self.viewGeneratorsCanvas.create_line(j * m + 2 * m2, i * m + m2, j * m + 2 * m2, i * m + 2 * m2, width=3)
                    if self.D.grid[i][j] == 'se':
                        self.viewGeneratorsCanvas.create_line(j * m + 2 * m2, i * m + 2 * m2, j * m + 3 * m2, i * m + 2 * m2, width=3)
                        self.viewGeneratorsCanvas.create_line(j * m + 2 * m2, (i + 1) * m, j * m + 2 * m2, (i + 1) * m + m2, width=3)
                    if self.D.grid[i][j] == 'sw':
                        self.viewGeneratorsCanvas.create_line(j * m + m2, i * m + 2 * m2, j * m + 2 * m2, i * m + 2 * m2, width=3)
                        self.viewGeneratorsCanvas.create_line(j * m + 2 * m2, (i + 1) * m, j * m + 2 * m2, (i + 1) * m + m2, width=3)

            # # Draw rounded corners
            # for i in range(0, len(self.D.grid)):
            #     for j in range(0, len(self.D.grid[0])):
            #         if self.D.grid[i][j] == 'ne':
            #             self.viewGeneratorsCanvas.create_arc(j * 100 + 100, i * 100, j * 100 + 200, i * 100 + 100, start=180,
            #                                  extent=90, style=tk.ARC, width=3)
            #         if self.D.grid[i][j] == 'nw':
            #             self.viewGeneratorsCanvas.create_arc(j * 100, i * 100, j * 100 + 100, i * 100 + 100, start=270, extent=90,
            #                                  style=tk.ARC, width=3)
            #         if self.D.grid[i][j] == 'se':
            #             self.viewGeneratorsCanvas.create_arc(j * 100 + 100, i * 100 + 100, j * 100 + 200, i * 100 + 200, start=90,
            #                                  extent=90,
            #                                  style=tk.ARC, width=3)
            #         if self.D.grid[i][j] == 'sw':
            #             self.viewGeneratorsCanvas.create_arc(j * 100, i * 100 + 100, j * 100 + 100, i * 100 + 200, start=0,
            #                                  extent=90, style=tk.ARC, width=3)

            # # Draw strand numbers
            # for k in range(0, len(self.D.strands)):
            #     for i in range(0, len(self.D.strands[k])):
            #         if len(self.D.strands[k][i]) % 2 == 0:
            #             mid = int(len(self.D.strands[k][i]) / 2)
            #             xAvg = (self.D.strands[k][i][mid][1] + self.D.strands[k][i][mid - 1][1]) / 2
            #             yAvg = (self.D.strands[k][i][mid][0] + self.D.strands[k][i][mid - 1][0]) / 2
            #             self.viewGeneratorsCanvas.create_text(xAvg * 100 + 110, yAvg * 100 + 110, text=str(i + 1), fill="blue")
            #         else:
            #             mid = int((len(self.D.strands[k][i]) - 1) / 2)
            #             self.viewGeneratorsCanvas.create_text(self.D.strands[k][i][mid][1] * 100 + 110,
            #                                   self.D.strands[k][i][mid][0] * 100 + 110, text=str(i + 1), fill="blue")

            # Draw smoothing types (0 or 1)
            for i in range(0, len(self.D.centers)):
                # self.viewGeneratorsCanvas.create_oval(self.D.centers[i][1] * m + 2 * m2 - 7,
                #                       self.D.centers[i][0] * m + 2 * m2 - 7,
                #                       self.D.centers[i][1] * m + 2 * m2 + 7,
                #                       self.D.centers[i][0] * m + 2 * m2 + 7, fill="black", width=1)
                self.viewGeneratorsCanvas.create_text(self.D.centers[i][1] * m + 2 * m2, self.D.centers[i][0] * m + 2 * m2,
                                      text=self.G[genNumber].binarySequence[i])

            # Draw smoothing enumeration
            for i in range(0, len(self.D.centers)):
                x1 = self.D.centers[i][0]
                y1 = self.D.centers[i][1]
                self.viewGeneratorsCanvas.create_text(x1 * m + 3 / 2 * m2, y1 * m + 3 / 2 * m2, text=str(i + 1), fill="red")

            # Draw smoothing component enumeration
            for i in range(0, len(self.G[genNumber].entrySmoothingSequence)):
                u = self.G[genNumber].findUniqueStrandSmoothingEntry(i)
                x1 = self.G[genNumber].entrySmoothingSequence[i][u][0]
                y1 = self.G[genNumber].entrySmoothingSequence[i][u][1]
                self.viewGeneratorsCanvas.create_text(x1 * m + 3 / 2 * m2, y1 * m + 3 / 2 * m2, text=str(i + 1), fill="purple")

            # draw labels
            for i in range(0, len(self.G[genNumber].label)):
                x1 = self.G[genNumber].entrySmoothingSequence[i][0][0]
                x2 = self.G[genNumber].entrySmoothingSequence[i][1][0]
                y1 = self.G[genNumber].entrySmoothingSequence[i][0][1]
                y2 = self.G[genNumber].entrySmoothingSequence[i][1][1]
                x = (x1 + x2) / 2
                y = (y1 + y2) / 2
                # self.viewGeneratorsCanvas.create_oval(y * m + 2 * m2 - 7, x * m + 2 * m2 - 7, y * m + 2 * m2 + 7, x * m + 2 * m2 + 7,
                #                       fill="green")
                if self.G[genNumber].label[i] == 'x':
                    self.viewGeneratorsCanvas.create_text(y * m + 2 * m2 + 1, x * m + 2 * m2 - 1, text=self.G[genNumber].label[i], fill="green")
                else:
                    self.viewGeneratorsCanvas.create_text(y * m + 2 * m2, x * m + 2 * m2, text=self.G[genNumber].label[i], fill="green")

            # Key
            self.viewGeneratorsCanvas.create_oval(m2 + 8, 620 + 8, m2 - 8, 620 - 8, outline="black", fill="green")
            self.viewGeneratorsCanvas.create_text(m2 + 25, 620, text='label')
            self.viewGeneratorsCanvas.create_text(m2, 620, text='?', fill="white")

            self.viewGeneratorsCanvas.create_oval(m2 + 75 + 8, 620 + 8, m2 + 75 - 8, 620 - 8, outline="black", fill="black")
            self.viewGeneratorsCanvas.create_text(m2 + 130, 620, text='smoothing type')
            self.viewGeneratorsCanvas.create_text(m2 + 75, 620, text='#', fill="white")

            self.viewGeneratorsCanvas.create_polygon(m2 + 200, 620 - 10, m2 + 200 - 10, 620, m2 + 200, 620 + 10, m2 + 200 + 10, 620,
                                     outline="red", fill="white")
            self.viewGeneratorsCanvas.create_text(m2 + 260, 620, text='crossing number', fill="red")
            self.viewGeneratorsCanvas.create_text(m2 + 200, 620, text='#', fill="red")

            self.viewGeneratorsCanvas.create_polygon(m2 + 335 - 8, 620 - 8, m2 + 335 + 8, 620 - 8, m2 + 335 + 8, 620 + 8, m2 + 335 - 8,
                                     620 + 8, outline="purple", fill="white")
            self.viewGeneratorsCanvas.create_text(m2 + 410, 620, text='smoothing component', fill="purple")
            self.viewGeneratorsCanvas.create_text(m2 + 335, 620, text='#', fill="purple")

    def updateCanvas(self):
        if self.D == []:
            grid = DrawDiagram.DrawDiagram(300, 300, self.mode).grid
            self.D = Diagram.Diagram(grid)

        # DIAGRAM
        #
        # title
        diagram_title_label = tk.Label(self.diagCanvas, text="Diagram", fg="pink", font=("Helvetica", 18), bg=self.my_color_background)
        diagram_title_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        # view diagram
        view_diagram_button = tk.Button(self.diagCanvas, bg=self.my_color_background, text="View Diagram", command=lambda: self.D.viewDiagram())
        view_diagram_button_window = self.diagCanvas.create_window(50, 25, window=view_diagram_button)
        view_diagram_button.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

        # change crossings
        change_crossing_button = tk.Button(self.diagCanvas, bg=self.my_color_background, text="Re-enumerate", command=lambda: self.changeCrossings(crossing_permutation_entry.get()))
        change_crossing_button_window = self.diagCanvas.create_window(50, 25, window=change_crossing_button)
        change_crossing_button.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)

        crossing_permutation_label = tk.Label(self.diagCanvas, text="New order:", bg=self.my_color_background, fg=self.my_color_font)
        crossing_permutation_label.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)

        crossing_permutation_entry = tk.Entry(self.diagCanvas)
        crossing_permutation_entry.grid(column=1, row=3, sticky=tk.W, padx=5, pady=5)

        # change orientation
        change_orientation_button = tk.Button(self.diagCanvas, text="Change orientation", command=lambda: self.changeOrientation(component_orientation_entry.get()))
        change_orientation_button_window = self.diagCanvas.create_window(50, 25, window=change_orientation_button)
        change_orientation_button.grid(column=0, row=4, sticky=tk.W, padx=5, pady=5)

        component_orientation_label = tk.Label(self.diagCanvas, text="Component:", bg=self.my_color_background, fg=self.my_color_font)
        component_orientation_label.grid(column=0, row=5, sticky=tk.W, padx=5, pady=5)

        component_orientation_entry = tk.Entry(self.diagCanvas)
        component_orientation_entry.grid(column=1, row=5, sticky=tk.W, padx=5, pady=5)

        # GENERATORS
        #
        # title
        generators_title_label = tk.Label(self.genCanvas, text="Generators", fg="pink", bg=self.my_color_background, font=("Helvetica", 18))
        generators_title_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        # new generator
        create_generator_button = tk.Button(self.genCanvas, text="Add generator", bg=self.my_color_background, fg=self.my_color_font, command=lambda: self.newGenerator(generator_smoothing_entry.get(), generator_label_entry.get()))
        create_generator_button_window = self.genCanvas.create_window(50, 25, window=create_generator_button)
        create_generator_button.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

        # preview smoothing
        preview_smoothing_button = tk.Button(self.genCanvas, text="Preview smoothing", command=lambda: self.D.previewSmoothing(generator_smoothing_entry.get()))
        preview_smoothing_button_window = self.genCanvas.create_window(50, 25, window=preview_smoothing_button)
        preview_smoothing_button.grid(column=1, row=4, sticky=tk.W, padx=5, pady=5)

        generator_smoothing_label = tk.Label(self.genCanvas, text="Binary sequence:", bg=self.my_color_background, fg=self.my_color_font)
        generator_smoothing_label.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)

        generator_smoothing_entry = tk.Entry(self.genCanvas)
        generator_smoothing_entry.grid(column=1, row=2, sticky=tk.W, padx=5, pady=5)

        generator_label_label = tk.Label(self.genCanvas, text="Label:", bg=self.my_color_background, fg=self.my_color_font)
        generator_label_label.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)

        generator_label_entry = tk.Entry(self.genCanvas)
        generator_label_entry.grid(column=1, row=3, sticky=tk.W, padx=5, pady=5)

        # view generators
        previous_generator_button = tk.Button(self.viewGeneratorsCanvas, text="<", command=lambda: self.previousGenerator())
        previousGenerator_button_window = self.viewGeneratorsCanvas.create_window(25, 25, window=previous_generator_button)
        previous_generator_button.place(x=145, y=305)

        next_generator_button = tk.Button(self.viewGeneratorsCanvas, text=">", command=lambda: self.nextGenerator())
        nextGenerator_button_window = self.viewGeneratorsCanvas.create_window(50, 25, window=next_generator_button)
        next_generator_button.place(x=165, y=305)

        view_generator_button = tk.Button(self.viewGeneratorsCanvas, text="View generator", command=lambda: self.viewGenerator())
        view_generator_button_window = self.viewGeneratorsCanvas.create_window(50, 25, window=view_generator_button)
        view_generator_button.place(x=120, y=340)

        remove_generator_button = tk.Button(self.viewGeneratorsCanvas, text="Remove generator", command=lambda: self.removeGenerator())
        remove_generator_button_window = self.viewGeneratorsCanvas.create_window(50, 25, window=remove_generator_button)
        remove_generator_button.place(x=110, y=370)

        generator_count_label = tk.Label(self.viewGeneratorsCanvas, text=str(self.generatorNumber+1) + "/" + str(len(self.G)), bg=self.my_color_background, fg=self.my_color_font)
        generator_count_label.place(x=250, y=295)

        # CHAINS
        #
        # title
        diagram_title_label = tk.Label(self.chainCanvas, text="Chain", fg="pink", font=("Helvetica", 18), bg=self.my_color_background)
        diagram_title_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        # set coefficients
        set_coefficients_button = tk.Button(self.chainCanvas, text="Create Chain", command=lambda: self.newChain(coefficient_entry.get()))
        set_coefficients_button_window = self.chainCanvas.create_window(50, 25, window=set_coefficients_button)
        set_coefficients_button.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

        coefficient_label = tk.Label(self.chainCanvas, text="Coefficients:", bg=self.my_color_background, fg=self.my_color_font)
        coefficient_label.grid(column=0, row=2, sticky=tk.E, padx=5, pady=5)

        coefficient_entry = tk.Entry(self.chainCanvas)
        coefficient_entry.grid(column=1, row=2, sticky=tk.E, padx=5, pady=5)

        # gradings
        if self.C != []:
            if self.consistentBigrading():
                h_grading_label = tk.Label(self.chainCanvas,
                                           text="Bi-grading: (" + str(self.G[0].h) + ", " + str(self.G[0].q) + ")", bg=self.my_color_background, fg=self.my_color_font)
                h_grading_label.grid(column=0, row=3)
            else:
                h_grading_label = tk.Label(self.chainCanvas, text="Bigrading: multiple detected", bg=self.my_color_background, fg=self.my_color_font)
                h_grading_label.grid(column=0, row=3)
        else:
            h_grading_label = tk.Label(self.chainCanvas, text="Bi-grading:", bg=self.my_color_background, fg=self.my_color_font)
            h_grading_label.grid(column=0, row=3)

        # NONTRIVIALITY
        #
        # title
        diagram_title_label = tk.Label(self.boundaryCanvas, text="Nontriviality", fg="pink", font=("Helvetica", 18), bg=self.my_color_background)
        diagram_title_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        # isCycle
        cycle_button = tk.Button(self.boundaryCanvas, text="Is cycle?", command=lambda: self.isCycle())
        cycle_button_window = self.boundaryCanvas.create_window(50, 25, window=cycle_button)
        cycle_button.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

        cycle_label = tk.Label(self.boundaryCanvas, text=self.cycleText, bg=self.my_color_background, fg=self.my_color_font)
        cycle_label.grid(column=1, row=1, sticky=tk.W, padx=5, pady=5)

        # isBoundary
        boundary_button = tk.Button(self.boundaryCanvas, text="Is boundary?", command=lambda: self.isBoundary())
        boundary_button_window = self.boundaryCanvas.create_window(50, 25, window=boundary_button)
        boundary_button.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)

        boundary_label = tk.Label(self.boundaryCanvas, text=self.boundaryText, bg=self.my_color_background, fg=self.my_color_font)
        boundary_label.grid(column=1, row=2, sticky=tk.W, padx=5, pady=5)

        # view boundary generators
        gen_label = tk.Label(self.boundaryCanvas, text="View boundary generator:", bg=self.my_color_background, fg=self.my_color_font)
        gen_label.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)

        gen_entry = tk.Entry(self.boundaryCanvas)
        gen_entry.grid(column=1, row=3, sticky=tk.W, padx=5, pady=5)

        if self.CC != []:
            boundary_gens = self.CC.getChainGroup(self.C.generators[0].h-1, self.C.generators[0].q)

        view_gen_button = tk.Button(self.boundaryCanvas, text="View boundary generator", command=lambda: boundary_gens[int(gen_entry.get())-1].viewGenerator())
        view_gen_button_window = self.boundaryCanvas.create_window(50, 25, window=view_gen_button)
        view_gen_button.grid(column=0, row=4, sticky=tk.W, padx=5, pady=5)

    def load(self):
        savedFile = fd.askopenfilename()
        with open(savedFile, 'r') as f:
            data = f.read()
        data = data.split('\n')

        # get index of diagram, generators, and chain coefficients
        genIndex = -1
        chainIndex = -1
        for i in range(0, len(data)):
            if data[i] == "Generators:":
                genIndex = i+1
            elif data[i] == "Chain:":
                data.pop(i)
                chainIndex = i

        if chainIndex == -1:
            data.pop(len(data)-1)

        # get diagram
        diagramData = data[1]
        diagramData = diagramData.split(';')
        for i in range(0, len(diagramData)):
            diagramData[i] = diagramData[i].split(',')
        self.D = Diagram.Diagram(diagramData)

        # get generators
        if genIndex != -1:
            if chainIndex != -1:
                for i in range(genIndex, chainIndex+1):
                    genData = data[i].split(';')
                    self.G.append(Generator.Generator(self.D, genData[0], genData[1]))
            else:
                for i in range(genIndex, len(data)):
                    genData = data[i].split(';')
                    self.G.append(Generator.Generator(self.D, genData[0], genData[1]))
            self.generatorNumber = 0

        # get chain coefficients
        if chainIndex != -1:
            for i in range(chainIndex, len(data)):
                print(data[i])

        self.viewGeneratorsCanvas.delete("all")
        self.viewDiagramCanvas.delete("all")
        self.updateCanvas()
        self.drawDiagram()
        self.drawGenerators(0)

    def save(self):
        fileName = asksaveasfile(initialfile='Untitled.txt', defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
        with open(fileName.buffer.name, 'w') as f:
            f.write("Diagram:" + '\n')
            for i in range(0, len(self.D.grid)):
                for j in range(0, len(self.D.grid[i])):
                    if j != len(self.D.grid[i])-1:
                        f.write(str(self.D.grid[i][j])+",")
                    else:
                        f.write(str(self.D.grid[i][j]))
                if i != len(self.D.grid)-1:
                    f.write(";")
            f.write('\n')
            if self.G != []:
                f.write("Generators:" + '\n')
                for i in range(0, len(self.G)):
                    f.write(str(self.G[i].binarySequence) + ";" + str(self.G[i].label))
                    f.write('\n')
            if self.C != []:
                f.write("Chain:" + '\n')
                f.write(str(self.C.coefficients))

    def consistentBigrading(self):
        h = self.C.generators[0].h
        q = self.C.generators[0].q
        for i in range(0, len(self.C.generators)):
            if self.C.generators[i].h == h and self.C.generators[i].q == q:
                return True
            else:
                return False

    def changeCrossings(self, order):
        if order == '':
            print("No order entered")
        else:
            self.D.reEnumerate(order)
            print("New crossing enumeration")
            self.viewDiagramCanvas.delete("all")
            self.updateCanvas()
            self.drawDiagram()

    def changeOrientation(self, component):
        if component == '':
            print("No component entered")
        else:
            self.D.changeOrientation(int(component)-1)
            print("Orientation of component #" + str(component) + " changed")
            self.viewDiagramCanvas.delete("all")
            self.updateCanvas()
            self.drawDiagram()

    def newGenerator(self, bs, l):
        if bs == "":
            print("No binary sequence provided")
        elif l == "":
            print("No label provided")
        else:
            # add generator
            gen = Generator.Generator(self.D, str(bs), str(l))
            self.G.append(gen)
            if self.generatorNumber == -1:
                self.generatorNumber = 0
            # re-populate canvas
            print("Generator submitted")
            self.updateCanvas()
            self.drawGenerators(self.generatorNumber)

    def nextGenerator(self):
        if self.generatorNumber < len(self.G)-1:
            self.increaseGeneratorNumber()
            self.updateCanvas()
            self.drawGenerators(self.generatorNumber)

    def previousGenerator(self):
        if self.generatorNumber > 0:
            self.decreaseGeneratorNumber()
            self.updateCanvas()
            self.drawGenerators(self.generatorNumber)

    def increaseGeneratorNumber(self):
        self.generatorNumber = self.generatorNumber + 1

    def decreaseGeneratorNumber(self):
        self.generatorNumber = self.generatorNumber - 1

    def viewGenerator(self):
        if self.G != []:
            self.G[self.generatorNumber].viewGenerator()

    def removeGenerator(self):
        if self.generatorNumber == 0 and len(self.G) > 1:
            self.G.pop(self.generatorNumber)
        elif self.G != []:
            self.G.pop(self.generatorNumber)
            self.decreaseGeneratorNumber()
        self.updateCanvas()
        self.drawGenerators(self.generatorNumber)
        print("Generator removed")

    def newChain(self, coeff):
        if coeff == "":
            print("No coefficient(s) provided")
        else:
            coeff = list(map(int, coeff.split(',')))
            # set chain
            self.C = Chain.Chain(self.D, self.G, coeff)
            self.CC = ChainComplex.ChainComplex(self.D)
            #re-populate canvas
            self.updateCanvas()
            print("Chain submitted")

    def isCycle(self):
        if self.C == []:
            print("No chain provided")
        dC = self.C.d()
        if dC.generators == []:
            print("Chain is a cycle")
            self.cycleText = "Yes"
        else:
            print("Chain is not a cycle; showing image under differential.")
            self.cycleText = "No"
            dC.viewChain()
        self.boundaryCanvas.delete("all")
        self.updateCanvas()

    def isBoundary(self):
        solution = self.CC.isBoundary(self.C)
        if solution == EmptySet:
            self.boundaryText = 'No'
            self.boundaryCanvas.delete("all")
            self.updateCanvas()
        else:
            self.boundaryText = 'Probably'
            self.boundaryCanvas.delete("all")
            self.updateCanvas()
