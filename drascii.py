import os 
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter import font
import random

class Drascii:

	root = Tk()

	textArea = Text(root, wrap=NONE)
	menuBar = Menu(root)
	fileMenu = Menu(menuBar, tearoff=0)
	helpMenu = Menu(menuBar, tearoff=0)
	#verticalScroll = Scrollbar(textArea)
	#horizontalScroll = Scrollbar(textArea, orient=HORIZONTAL) 
	file = None

	mode = "draw"
	currentFont = "Consolas"
	fontSize = 12
	cursor = "tcross" # https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html

	currentChar = ' '
	currentIndex = 0
	randomChar = False
	mouseHistory = []

	drawBackgroundColor = "black"
	drawForegroundColor = "white"
	drawSelectedColor = "black"
	drawInsertColor = "black"

	writeBackgroundColor = "black"
	writeForegroundColor = "white"
	writeSelectedColor = "red"
	writeInsertColor = "white"

	def __init__(self,**kwargs):

		try:
			self.width = kwargs['width']
		except KeyError:
			pass

		try:
			self.height = kwargs['height']
		except KeyError:
			pass

		self.root.title("Untitled - Drascii")

		screenWidth = self.root.winfo_screenwidth()
		screenHeight = self.root.winfo_screenheight()
	
		left = (screenWidth / 2) - (self.width / 2) 
		top = (screenHeight / 2) - (self.height /2) 

		self.root.geometry('%dx%d+%d+%d' % (self.width, self.height, left, top)) 

		# To make the textarea auto resizable
		self.root.grid_rowconfigure(0, weight=1)
		self.root.grid_columnconfigure(0, weight=1)

		# Add controls (widget)
		self.textArea.grid(sticky = N + E + S + W)
		
		# File Menu
		self.fileMenu.add_command(label="New", command=self.newFile) 
		self.fileMenu.add_command(label="Open", command=self.openFile)
		self.fileMenu.add_command(label="Save", command=self.saveFile) 
		self.fileMenu.add_separator()
		self.fileMenu.add_command(label="Settings", command=self.settingsMenu)
		self.fileMenu.add_separator()								 
		self.fileMenu.add_command(label="Exit", command=self.quitApplication)
		self.menuBar.add_cascade(label="File", menu=self.fileMenu)	 
		
		# Help Menu
		self.helpMenu.add_command(label="About Notepad", command=self.showAbout) 
		self.menuBar.add_cascade(label="Help", menu=self.helpMenu)

		self.root.config(menu=self.menuBar)
		
		self.textArea.configure(font=(self.currentFont, self.fontSize), cursor=self.cursor)

		self.setBackground(self.drawBackgroundColor)
		self.setForeground(self.drawForegroundColor)
		self.setSelected(self.drawSelectedColor)
		self.setInsert(self.drawInsertColor)

		self.textArea.bind("<Button-1>", self.handleClick)
		self.textArea.bind("<B1-Motion>", self.handleClick)
		self.textArea.bind("<ButtonRelease-1>", self.handleRelease)
		self.textArea.bind("<KeyPress>", self.onKeyPressed)
		self.root.bind("<Control-plus>", self.zoomIn)
		self.root.bind("<Control-minus>", self.zoomOut)
		self.root.bind("<Control-MouseWheel>", self.zoomWithMouseWheel)
		
	def quitApplication(self):
		self.root.destroy()
		exit()

	def showAbout(self):
		showinfo("Drascii","Mrinal Verma")

	def openFile(self):
		self.file = askopenfilename(defaultextension=".txt",
									filetypes=[("All Files","*.*"),
										("Text Documents","*.txt")])
		if self.file == "":
			self.file = None
		else:
			self.root.title(os.path.basename(self.file) + " - Drascii")
			self.textArea.delete(1.0,END)
			file = open(self.file,"r")
			self.textArea.insert(1.0,file.read())
			file.close()
	
	def newFile(self):
		self.root.title("Untitled - Notepad")
		self.file = None
		self.textArea.delete(1.0,END)

	def saveFile(self):
		if self.file == None:
			self.file = asksaveasfilename(initialfile='Untitled.txt',
											defaultextension=".txt",
											filetypes=[("All Files","*.*"),
												("Text Documents","*.txt")])
			if self.file == "":
				self.file = None
			else:
				file = open(self.file,"w")
				file.write(self.textArea.get(1.0,END))
				file.close()
				self.root.title(os.path.basename(self.file) + " - Drascii")
				
			
		else:
			file = open(self.file,"w")
			file.write(self.textArea.get(1.0,END))
			file.close()

	def settingsMenu(self):
		newWindow = Toplevel(self.root)
		newWindow.title("Settings")
		newWindow.geometry("720x360")

		# Selector for mode
		mode_label = Label(newWindow, text="Mode:")
		mode_label.grid(row=0, column=0)
		modes = ["draw", "write"]
		self.mode_var = StringVar(newWindow)
		self.mode_var.set(self.mode)
		mode_selector = OptionMenu(newWindow, self.mode_var, *modes, command=self.setMode)
		mode_selector.grid(row=0, column=1)

		# Selector for current font
		font_label = Label(newWindow, text="Font:")
		font_label.grid(row=1, column=0)
		fonts = ["Consolas", "Arial", "Times New Roman"]
		self.font_var = StringVar(newWindow)
		self.font_var.set(self.currentFont)
		font_selector = OptionMenu(newWindow, self.font_var, *fonts, command=self.setFont)
		font_selector.grid(row=1, column=1)

		# Selector for font size
		size_label = Label(newWindow, text="Font Size:")
		size_label.grid(row=2, column=0)
		self.size_scale = Scale(newWindow, from_=8, to=24, orient=HORIZONTAL, command=self.onFontSizeDrag)
		self.size_scale.set(self.fontSize)
		self.size_scale.grid(row=2, column=1)

		# Selector for cursor
		cursor_label = Label(newWindow, text="Cursor:")
		cursor_label.grid(row=3, column=0)
		cursors = ["arrow", "tcross", "hand2", "crosshair"]
		self.cursor_var = StringVar(newWindow)
		self.cursor_var.set(self.cursor)
		cursor_selector = OptionMenu(newWindow, self.cursor_var, *cursors, command=self.setCursor)
		cursor_selector.grid(row=3, column=1)

		# Selector for current char
		char_label = Label(newWindow, text="Current Character:")
		char_label.grid(row=4, column=0)
		self.char_entry = Entry(newWindow)
		self.char_entry.insert(0, self.currentChar)
		self.char_entry.grid(row=4, column=1)
		self.char_entry.bind("<FocusOut>", self.setCurrentChar)

		# Checkbox for random char
		self.random_char_var = BooleanVar(value=self.randomChar)
		random_char_checkbox = Checkbutton(newWindow, text="Random Character", variable=self.randomChar, command=self.setRandomChar)
		random_char_checkbox.grid(row=4, column=2)

	def onFontSizeDrag(self, value):
		current_value = int(value)
		if current_value > self.fontSize:
			self.zoomIn()
		elif current_value < self.fontSize:
			self.zoomOut()
		self.fontSize = current_value

	def run(self):
		self.root.mainloop()

	def setCursor(self, value):
		self.cursor = value
		self.textArea.configure(cursor=self.cursor)

	def setFont(self, value):
		self.currentFont = value
		self.textArea.configure(font=(value, self.fontSize))

	def setBackground(self, color):
		self.textArea.configure(bg=color)

	def setForeground(self, color):
		self.textArea.configure(fg=color)

	def setSelected(self, color):
		self.textArea.configure(selectbackground=color)	

	def setInsert(self, color):
		self.textArea.configure(insertbackground=color)

	def setRandomChar(self):
		self.randomChar = not self.randomChar
		self.currentIndex = 0

	def zoomIn(self, event=None):
		self.fontSize += 2
		self.textArea.configure(font=(self.currentFont, self.fontSize))

	def zoomOut(self, event=None):
		self.fontSize -= 2
		self.textArea.configure(font=(self.currentFont, self.fontSize))

	def zoomWithMouseWheel(self, event):
		if event.delta > 0:
			self.zoomIn()
		else:
			self.zoomOut()

	def setMode(self, mode=None):
		if mode == "write" or (mode == None and self.mode == "draw"):
			self.mode = "write"
			self.setSelected(self.writeSelectedColor)
			self.setInsert(self.writeInsertColor)
		else:
			self.mode = "draw"
			self.setSelected(self.drawSelectedColor)
			self.setInsert(self.drawInsertColor)

	def setCurrentChar(self, event):
		self.currentChar = self.char_entry.get()
		self.currentIndex = 0
	
	def onKeyPressed(self, event):
		if event.keysym == "F1":
			self.setMode()
		if event.char and event.char.isprintable():
			self.currentChar = event.char
			self.currentIndex = 0
		if self.mode == "draw":
			return "break"
		return None

	def handleClick(self, event):
		fontObject = font.Font(family=self.currentFont, size=self.fontSize)
		fontHeight = fontObject.metrics("linespace")
		fontWidth = fontObject.measure(" ")

		# Calculate the visible portion of the text
		rowsPerColumn = [len(self.textArea.get(f"{x}.0", f"{x}.end")) for x in range(int(self.textArea.index('end').split('.')[0]))]
		outsideViewCols = int(max(rowsPerColumn) * self.textArea.xview()[0])
		outsideViewsLines = int(int(self.textArea.index('end').split('.')[0]) * self.textArea.yview()[0])

		# Calculate the click position relative to the text widget
		clickLine = int(event.y / fontHeight) + outsideViewsLines + 1
		clickColumn = int(event.x / fontWidth) + outsideViewCols
		if (clickLine, clickColumn) not in self.mouseHistory: # if position hasnt been visited before in current click

			self.mouseHistory.append((clickLine, clickColumn))

			if clickLine < 1 or clickColumn < 0:
				return

			# Add lines if necessary
			numLines = int(self.textArea.index('end').split('.')[0]) - 1
			while clickLine > numLines:
				self.textArea.insert('end', "\n")
				numLines += 1

			# Add columns if necessary
			numColumns = len(self.textArea.get(f"{clickLine}.0", f"{clickLine}.end"))
			while clickColumn > numColumns:
				self.textArea.insert(f"{clickLine}.end", " ")
				numColumns += 1

			if self.mode == "draw":
				if not self.textArea.get(f"{clickLine}.{clickColumn}") == '\n':
					self.textArea.delete(f"{clickLine}.{clickColumn}")
				if not self.randomChar:
					self.textArea.insert(f"{clickLine}.{clickColumn}", self.currentChar[self.currentIndex])
					self.currentIndex = (self.currentIndex + 1) % len(self.currentChar)
				else:
					self.textArea.insert(f"{clickLine}.{clickColumn}", chr(random.randint(33, 126)))

	def handleRelease(self, event=None):
		self.mouseHistory = []

		
drascii = Drascii(width=1280,height=720)
drascii.run()




