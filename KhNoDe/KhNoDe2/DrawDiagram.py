import tkinter as tk


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
