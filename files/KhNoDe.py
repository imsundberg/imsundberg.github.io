import tkinter as tk
from tkinter import *
from tkinter.filedialog import asksaveasfile
from tkinter import filedialog as fd
from sympy import *
from sympy.solvers.solveset import linsolve


class KhNoDe:

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
        self.root.resizable(0, 0)
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
        self.D = []  # diagram
        self.G = []  # generators
        self.generatorNumber = -1
        self.C = []  # chain
        self.cycleText = ''
        self.CC = []  # chain complex
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
            grid = DrawDiagram(300, 300, self.mode).grid
            self.D = Diagram(grid)

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

        generator_count_label = tk.Label(self.viewGeneratorsCanvas, text=str(self.generatorNumber + 1) + "/" + str(len(self.G)), bg=self.my_color_background, fg=self.my_color_font)
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
            boundary_gens = self.CC.getChainGroup(self.C.generators[0].h - 1, self.C.generators[0].q)

        view_gen_button = tk.Button(self.boundaryCanvas, text="View boundary generator", command=lambda: boundary_gens[int(gen_entry.get()) - 1].viewGenerator())
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
                genIndex = i + 1
            elif data[i] == "Chain:":
                data.pop(i)
                chainIndex = i

        if chainIndex == -1:
            data.pop(len(data) - 1)

        # get diagram
        diagramData = data[1]
        diagramData = diagramData.split(';')
        for i in range(0, len(diagramData)):
            diagramData[i] = diagramData[i].split(',')
        self.D = Diagram(diagramData)

        # get generators
        if genIndex != -1:
            if chainIndex != -1:
                for i in range(genIndex, chainIndex + 1):
                    genData = data[i].split(';')
                    self.G.append(Generator(self.D, genData[0], genData[1]))
            else:
                for i in range(genIndex, len(data)):
                    genData = data[i].split(';')
                    self.G.append(Generator(self.D, genData[0], genData[1]))
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
                    if j != len(self.D.grid[i]) - 1:
                        f.write(str(self.D.grid[i][j]) + ",")
                    else:
                        f.write(str(self.D.grid[i][j]))
                if i != len(self.D.grid) - 1:
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
            self.D.changeOrientation(int(component) - 1)
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
            gen = Generator(self.D, str(bs), str(l))
            self.G.append(gen)
            if self.generatorNumber == -1:
                self.generatorNumber = 0
            # re-populate canvas
            print("Generator submitted")
            self.updateCanvas()
            self.drawGenerators(self.generatorNumber)

    def nextGenerator(self):
        if self.generatorNumber < len(self.G) - 1:
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
            self.C = Chain(self.D, self.G, coeff)
            self.CC = ChainComplex(self.D)
            # re-populate canvas
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

        Generator(self, binarySequence, "").viewGenerator()

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

class DrawDiagram():

    def __init__(self, w, h, mode):
        # initialize colors
        self.mode = mode
        if self.mode == "light":
            self.my_color_background = "grey90"
            self.my_color_font = "gray17"
            self.my_color_light = "gray80"
            self.my_color_light2 = "gray65"
        else:
            self.my_color_background = "grey17"
            self.my_color_font = "gray75"
            self.my_color_light = "gray30"
            self.my_color_light2 = "gray40"
        self.player_color = "magenta3"

        # initialize dimensions
        self.width = w
        self.height = h
        self.xRoot = int(self.height / 10 / 2)
        self.yRoot = int(self.width / 10 / 2)
        self.x = self.xRoot
        self.y = self.yRoot

        # initialize GUI
        root = tk.Tk()
        root.title("Draw Diagram")
        root.configure(bg=self.my_color_background)
        self.canvas = tk.Canvas(root, width=self.width, height=self.height + 215, highlightthickness=0)
        self.canvas.pack()
        self.canvas.configure(bg=self.my_color_background)

        # initialize grid
        self.grid = [[]] * int(self.height / 10)
        for i in range(0, int(self.height / 10)):
            self.grid[i] = [''] * int(self.width / 10)
        # draw grid
        # background
        self.canvas.create_rectangle(10, 10, self.height-10, self.width-10, fill=self.my_color_light)
        # horizontal lines
        for i in range(0, int(self.height / 10) - 1):
            self.canvas.create_line(10, i * 10 + 10, self.width - 10, i * 10 + 10, fill=self.my_color_light2)
        # vertical lines
        for i in range(0, int(self.width / 10) - 1):
            self.canvas.create_line(i * 10 + 10, 10, i * 10 + 10, self.height - 10, fill=self.my_color_light2)

        # new component
        xEntry = tk.Entry(root, bg=self.my_color_light)
        xEntry.place(x=90, y=300)

        yEntry = tk.Entry(root, bg=self.my_color_light)
        yEntry.place(x=90, y=320)

        new_component_button = tk.Button(root, bg=self.my_color_light, fg=self.my_color_font, text="New component", command=lambda: self.newComponent(xEntry.get(), yEntry.get()))
        new_component_button.place(x=99, y=345)

        # submit diagram button
        submit_diagram_button = tk.Button(root, bg=self.my_color_light, fg=self.my_color_font, text="Submit diagram", command=lambda: closeWindow())
        submit_diagram_button.place(x=101, y=380)

        # label instructions
        instruction_label1 = tk.Label(self.canvas, text="Arrow keys to draw (default over-crossing)", fg=self.my_color_font, bg=self.my_color_background)
        instruction_label1.place(x=5, y=430)
        instruction_label2 = tk.Label(self.canvas, text="Shift+arrow to draw under-crossings", fg=self.my_color_font, bg=self.my_color_background)
        instruction_label2.place(x=5, y=450)
        instruction_label3 = tk.Label(self.canvas, text="Return to create a new component,", fg=self.my_color_font, bg=self.my_color_background)
        instruction_label3.place(x=5, y=470)
        instruction_label4 = tk.Label(self.canvas, text="   then ctrl+arrow to relocate", fg=self.my_color_font, bg=self.my_color_background)
        instruction_label4.place(x=5, y=490)

        self.player = self.canvas.create_rectangle
        self.player((self.x * 10, self.y * 10, self.x * 10 + 10, self.y * 10 + 10), outline=self.player_color)

        root.bind("<Up>", self.moveUp)
        root.bind("<Down>", self.moveDown)
        root.bind("<Left>", self.moveLeft)
        root.bind("<Right>", self.moveRight)
        root.bind("<Shift-Up>", self.moveUpShift)
        root.bind("<Shift-Down>", self.moveDownShift)
        root.bind("<Shift-Left>", self.moveLeftShift)
        root.bind("<Shift-Right>", self.moveRightShift)

        root.bind("<Control-Up>", self.relocateUp)
        root.bind("<Control-Down>", self.relocateDown)
        root.bind("<Control-Left>", self.relocateLeft)
        root.bind("<Control-Right>", self.relocateRight)

        root.bind("<Return>", self.enter)
        self.color = 0

        # create method to close window
        def closeWindow():
            print("Diagram submitted")
            root.quit()
            root.destroy()

        # make Esc exit the program
        root.bind('<Escape>', lambda e: closeWindow())

        # create a menu bar with an Exit command
        menubar = tk.Menu(root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Submit", command=lambda: closeWindow())
        filemenu.add_command(label="Exit", command=lambda: root.destroy())
        menubar.add_cascade(label="File", menu=filemenu)
        root.config(menu=menubar)

        root.mainloop()

        self.initializeGrid()

    def enter(self, event):
        if self.color == 0:
            self.canvas.create_rectangle(10,10,self.width-10,self.height-10, outline="pink")
        else:
            self.canvas.create_rectangle(10,10,self.width-10,self.height-10, outline="dark pink")
        self.grid[self.yRoot][self.xRoot] = self.grid[self.yRoot][self.xRoot][1] + self.grid[self.yRoot][self.xRoot][0]
        self.color = (self.color + 1) % 2

    def newComponent(self, a, b):
        self.grid[self.yRoot][self.xRoot] = self.grid[self.yRoot][self.xRoot][1] + self.grid[self.yRoot][self.xRoot][0]
        self.x = int(a)
        self.y = int(b)
        self.xRoot = int(a)
        self.yRoot = int(b)
        self.player((self.x * 10, self.y*10, self.x*10 + 10, self.y*10 + 10), outline=self.player_color)

    def relocateUp(self, event):
        self.player((self.x * 10, self.y*10, self.x*10 + 10, self.y*10 + 10), outline=self.my_color_light2)
        self.y -= 1
        self.yRoot -= 1
        self.player((self.x * 10, self.y*10, self.x*10 + 10, self.y*10 + 10), outline=self.player_color)

    def relocateDown(self, event):
        self.player((self.x * 10, self.y*10, self.x*10 + 10, self.y*10 + 10), outline=self.my_color_light2)
        self.y += 1
        self.yRoot += 1
        self.player((self.x * 10, self.y*10, self.x*10 + 10, self.y*10 + 10), outline=self.player_color)

    def relocateLeft(self, event):
        self.player((self.x * 10, self.y*10, self.x*10 + 10, self.y*10 + 10), outline=self.my_color_light2)
        self.x -= 1
        self.xRoot -= 1
        self.player((self.x * 10, self.y*10, self.x*10 + 10, self.y*10 + 10), outline=self.player_color)

    def relocateRight(self, event):
        self.player((self.x * 10, self.y*10, self.x*10 + 10, self.y*10 + 10), outline=self.my_color_light2)
        self.x += 1
        self.xRoot += 1
        self.player((self.x * 10, self.y*10, self.x*10 + 10, self.y*10 + 10), outline=self.player_color)

    def moveUp(self, event):
        if self.grid[self.y][self.x] == 'v':
            self.y -= 1
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'u'
            self.canvas.create_line(self.x * 10 + 5, self.y * 10 + 15, self.x * 10 + 5, self.y * 10 + 5, width=2)
        elif self.grid[self.y][self.x] == 'h':
            self.y -= 1
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'u'
            self.canvas.create_line(self.x * 10 + 5, self.y * 10 + 10, self.x * 10 + 5, self.y * 10 + 3, width=2)
        elif self.grid[self.y - 1][self.x] == '':
            self.canvas.create_line(self.x * 10 + 5, self.y * 10 + 5, self.x * 10 + 5, (self.y - 1) * 10 + 5, width=2)
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'u'
            self.y -= 1
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'u'
        elif self.x == self.xRoot and self.y - 1 == self.yRoot:
            self.canvas.create_line(self.x * 10 + 5, self.y * 10 + 5, self.x * 10 + 5, (self.y - 1) * 10 + 5, width=2)
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'u'
            self.y -= 1
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'u'
        else:
            self.canvas.create_rectangle(self.x * 10 + 2, self.y * 10 - 2, self.x * 10 + 8,
                                         self.y * 10 - 8, fill=self.my_color_light, outline=self.my_color_light)
            self.canvas.create_line(self.x * 10 + 5, self.y * 10 + 5, self.x * 10 + 5, self.y * 10 - 5, width=2)
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'u'
            self.y -= 1
            self.grid[self.y][self.x] = 'v'
            self.moveUp(event)

    def moveUpShift(self, event):
        if self.grid[self.y][self.x] == 'h':
            self.y -= 1
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'u'
            self.canvas.create_line(self.x * 10 + 5, self.y * 10 + 12, self.x * 10 + 5, self.y * 10 + 5, width=2)
        elif self.grid[self.y - 1][self.x] == '':
            self.canvas.create_line(self.x * 10 + 5, self.y * 10 + 5, self.x * 10 + 5, (self.y - 1) * 10 + 5, width=2)
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'u'
            self.y -= 1
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'u'
        elif self.x == self.xRoot and self.y - 1 == self.yRoot:
            self.canvas.create_line(self.x * 10 + 5, self.y * 10 + 5, self.x * 10 + 5, (self.y - 1) * 10 + 5, width=2)
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'u'
            self.y -= 1
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'u'
        else:
            self.canvas.create_line(self.x * 10 + 5, self.y * 10 + 5, self.x * 10 + 5, self.y * 10 - 2, width=2)
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'u'
            self.y -= 1
            self.grid[self.y][self.x] = 'h'
            self.moveUpShift(event)

    def moveDown(self, event):
        if self.grid[self.y][self.x] == 'v':
            self.y += 1
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'd'
            self.canvas.create_line(self.x * 10 + 5, self.y * 10 - 15, self.x * 10 + 5, self.y * 10 + 5, width=2)
        elif self.grid[self.y][self.x] == 'h':
            self.y += 1
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'd'
            self.canvas.create_line(self.x * 10 + 5, self.y * 10 - 5, self.x * 10 + 5, self.y * 10 + 5, width=2)
        elif self.grid[self.y + 1][self.x] == '':
            self.canvas.create_line(self.x * 10 + 5, self.y * 10 + 5, self.x * 10 + 5, (self.y + 1) * 10 + 5, width=2)
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'd'
            self.y += 1
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'd'
        elif self.x == self.xRoot and self.y + 1 == self.yRoot:
            self.canvas.create_line(self.x * 10 + 5, self.y * 10 + 5, self.x * 10 + 5, (self.y + 1) * 10 + 5, width=2)
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'd'
            self.y += 1
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'd'
        else:
            self.canvas.create_line(self.x * 10 + 5, self.y * 10 + 5, self.x * 10 + 5, (self.y + 1) * 10 + 5, width=2)
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'd'
            self.y += 1
            self.grid[self.y][self.x] = 'v'
            self.canvas.create_rectangle(self.x * 10 + 2, (self.y + 1) * 10 - 2, self.x * 10 + 8, (self.y + 1) * 10 - 8,
                                         fill=self.my_color_light, outline=self.my_color_light)
            self.moveDown(event)

    def moveDownShift(self, event):
        if self.grid[self.y][self.x] == 'h':
            self.y += 1
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'd'
            self.canvas.create_line(self.x * 10 + 5, self.y * 10 - 2, self.x * 10 + 5, self.y * 10 + 5, width=2)
        elif self.grid[self.y + 1][self.x] == '':
            self.canvas.create_line(self.x * 10 + 5, self.y * 10 + 5, self.x * 10 + 5, (self.y + 1) * 10 + 5, width=2)
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'd'
            self.y += 1
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'd'
        elif self.x == self.xRoot and self.y + 1 == self.yRoot:
            self.canvas.create_line(self.x * 10 + 5, self.y * 10 + 5, self.x * 10 + 5, (self.y + 1) * 10 + 5, width=2)
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'd'
            self.y += 1
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'd'
        else:
            self.canvas.create_line(self.x * 10 + 5, self.y * 10 + 5, self.x * 10 + 5, self.y * 10 + 12, width=2)
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'd'
            self.y += 1
            self.grid[self.y][self.x] = 'h'
            self.moveDownShift(event)

    def moveLeft(self, event):
        if self.grid[self.y][self.x] == 'h':
            self.x -= 1
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'l'
            self.canvas.create_line(self.x * 10 + 5, self.y * 10 + 5, self.x * 10 + 20, self.y * 10 + 5, width=2)
        elif self.grid[self.y][self.x] == 'v':
            self.x -= 1
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'l'
            self.canvas.create_rectangle(self.x * 10 + 10, self.y * 10, self.x * 10 + 20, self.y * 10 + 10,
                                         fill=self.my_color_light, outline=self.my_color_light)
            self.canvas.create_line(self.x * 10 + 12, self.y * 10 + 5, self.x * 10 + 20, self.y * 10 + 5,
                                    width=2)  # not sure about the 12
        elif self.grid[self.y][self.x - 1] == '':
            self.canvas.create_line(self.x * 10 + 5, self.y * 10 + 5, (self.x - 1) * 10 + 5, self.y * 10 + 5, width=2)
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'l'
            self.x -= 1
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'l'
        elif self.x - 1 == self.xRoot and self.y == self.yRoot:
            self.canvas.create_line(self.x * 10 + 5, self.y * 10 + 5, (self.x - 1) * 10 + 5, self.y * 10 + 5, width=2)
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'l'
            self.x -= 1
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'l'
        else:
            self.canvas.create_line(self.x * 10 + 5, self.y * 10 + 5, (self.x - 1) * 10 + 5, self.y * 10 + 5, width=2)
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'l'
            self.x -= 1
            self.grid[self.y][self.x] = 'h'
            self.canvas.create_rectangle((self.x - 1) * 10 + 12, self.y * 10 + 2, (self.x - 1) * 10 + 18,
                                         self.y * 10 + 8, fill=self.my_color_light, outline=self.my_color_light)
            self.moveLeft(event)

    def moveLeftShift(self, event):
        if self.grid[self.y][self.x] == 'h':
            self.x -= 1
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'l'
            self.canvas.create_rectangle(self.x * 10 + 10, self.y * 10, self.x * 10 + 20, self.y * 10 + 10,
                                         fill=self.my_color_light, outline=self.my_color_light)
            self.canvas.create_line(self.x * 10 + 5, self.y * 10 + 5, self.x * 10 + 20, self.y * 10 + 5, width=2)
        elif self.grid[self.y][self.x] == 'v':
            self.x -= 1
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'l'
            self.canvas.create_line(self.x * 10 + 5, self.y * 10 + 5, self.x * 10 + 12, self.y * 10 + 5, width=2)
        elif self.grid[self.y][self.x - 1] == '':
            self.canvas.create_line(self.x * 10 + 5, self.y * 10 + 5, (self.x - 1) * 10 + 5, self.y * 10 + 5, width=2)
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'l'
            self.x -= 1
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'l'
        elif self.x - 1 == self.xRoot and self.y == self.yRoot:
            self.canvas.create_line(self.x * 10 + 5, self.y * 10 + 5, (self.x - 1) * 10 + 5, self.y * 10 + 5, width=2)
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'l'
            self.x -= 1
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'l'
        else:
            self.canvas.create_line(self.x * 10 + 5, self.y * 10 + 5, self.x * 10 - 2, self.y * 10 + 5, width=2)
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'l'
            self.x -= 1
            self.grid[self.y][self.x] = 'v'
            self.moveLeftShift(event)

    def moveRight(self, event):
        if self.grid[self.y][self.x] == 'h':
            self.x += 1
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'r'
            self.canvas.create_line(self.x * 10 - 10, self.y * 10 + 5, self.x * 10 + 5, self.y * 10 + 5, width=2)
        elif self.grid[self.y][self.x] == 'v':
            self.x += 1
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'r'
            self.canvas.create_line(self.x * 10 - 2, self.y * 10 + 5, self.x * 10 + 5, self.y * 10 + 5, width=2)
        elif self.grid[self.y][self.x + 1] == '':
            self.canvas.create_line(self.x * 10 + 5, self.y * 10 + 5, (self.x + 1) * 10 + 5, self.y * 10 + 5, width=2)
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'r'
            self.x += 1
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'r'
        elif self.x + 1 == self.xRoot and self.y == self.yRoot:
            self.canvas.create_line(self.x * 10 + 5, self.y * 10 + 5, (self.x + 1) * 10 + 5, self.y * 10 + 5, width=2)
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'r'
            self.x += 1
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'r'
        else:
            self.canvas.create_line(self.x * 10 + 5, self.y * 10 + 5, (self.x + 1) * 10 + 5, self.y * 10 + 5, width=2)
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'r'
            self.x += 1
            self.grid[self.y][self.x] = 'h'
            self.canvas.create_rectangle((self.x + 1) * 10 - 2, self.y * 10 + 2, (self.x + 1) * 10 - 8, self.y * 10 + 8,
                                         fill=self.my_color_light, outline=self.my_color_light)
            self.moveRight(event)

    def moveRightShift(self, event):
        if self.grid[self.y][self.x] == 'h':
            self.x += 1
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'r'
            self.canvas.create_line(self.x * 10 - 10, self.y * 10 + 5, self.x * 10 + 5, self.y * 10 + 5, width=2)
        elif self.grid[self.y][self.x] == 'v':
            self.x += 1
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'r'
            self.canvas.create_line(self.x * 10 - 2, self.y * 10 + 5, self.x * 10 + 5, self.y * 10 + 5, width=2)
        elif self.grid[self.y][self.x + 1] == '':
            self.canvas.create_line(self.x * 10 + 5, self.y * 10 + 5, (self.x + 1) * 10 + 5, self.y * 10 + 5, width=2)
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'r'
            self.x += 1
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'r'
        elif self.x + 1 == self.xRoot and self.y == self.yRoot:
            self.canvas.create_line(self.x * 10 + 5, self.y * 10 + 5, (self.x + 1) * 10 + 5, self.y * 10 + 5, width=2)
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'r'
            self.x += 1
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'r'
        else:
            self.canvas.create_line(self.x * 10 + 5, self.y * 10 + 5, self.x * 10 + 12, self.y * 10 + 5, width=2)
            self.grid[self.y][self.x] = self.grid[self.y][self.x] + 'r'
            self.x += 1
            self.grid[self.y][self.x] = 'v'
            self.moveRightShift(event)

    def printGrid(self):
        print("")
        for i in range(0, len(self.grid)):
            print(self.grid[i])

    def initializeGrid(self):
        # change letters to ne, nw, se, sw, v, h (compatible with grid in Diagram class)
        for i in range(0, len(self.grid)):
            for j in range(0, len(self.grid[i])):
                if i == self.yRoot and j == self.xRoot:
                    self.grid[i][j] = self.grid[i][j][1] + self.grid[i][j][0]

                if self.grid[i][j] == 'dl' or self.grid[i][j] == 'ru':
                    self.grid[i][j] = 'nw'
                elif self.grid[i][j] == 'dr' or self.grid[i][j] == 'lu':
                    self.grid[i][j] = 'ne'
                elif self.grid[i][j] == 'ul' or self.grid[i][j] == 'rd':
                    self.grid[i][j] = 'sw'
                elif self.grid[i][j] == 'ur' or self.grid[i][j] == 'ld':
                    self.grid[i][j] = 'se'
                elif self.grid[i][j] != 'v' and self.grid[i][j] != 'h':
                    self.grid[i][j] = ''

        # reduce unnecessary rows/cols
        self.grid = [x for x in self.grid if any(x)]
        self.grid = list(zip(*self.grid))
        self.grid = [x for x in self.grid if any(x)]
        self.grid = list(zip(*self.grid))

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
            gen = Generator(self.diagram, binarySequence)
            for j in range(2**len(gen.strandSmoothingSequence)):
                generators.append(Generator(self.diagram, binarySequence, self.addPadding(bin(j).replace("0b", ""), len(gen.strandSmoothingSequence)).replace("0", "x")))
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
        dgen = Chain(self.diagram, dsmoothings, dcoefficients)
        binarySequence = generator.binarySequence
        for i in range(len(binarySequence)):
            if binarySequence[self.diagram.n - i - 1] == '0':
                j = self.diagram.n - i
                newBinarySequence = binarySequence[:self.diagram.n - i - 1] + '1' + binarySequence[j:]
                newGenerator = Generator(self.diagram, newBinarySequence)
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
        return Chain(self.diagram, dChain, dChainCoefficients)
        '''
        vec = self.dChainVector(chain)
        h = chain.getHomologicalGrading()
        q = chain.getQuantumGrading()
        imageGroup = self.getChainGroup(h+1,q)
        ch = Chain(self.diagram, [], [])
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
        dgen = Chain(self.diagram, dsmoothings, dcoefficients)
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

KhNoDe()