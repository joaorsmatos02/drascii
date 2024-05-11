import os 
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter import font

class Drascii:

	root = Tk()

	textArea = Text(root, wrap=NONE)
	menuBar = Menu(root)
	fileMenu = Menu(menuBar, tearoff=0)
	helpMenu = Menu(menuBar, tearoff=0)
	verticalScroll = Scrollbar(textArea)
	horizontalScroll = Scrollbar(textArea, orient=HORIZONTAL) 
	file = None

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

		self.root.geometry('%dx%d+%d+%d' % (self.width,
											self.height,
											left, top)) 

		# To make the textarea auto resizable
		self.root.grid_rowconfigure(0, weight=1)
		self.root.grid_columnconfigure(0, weight=1)

		# Add controls (widget)
		self.textArea.grid(sticky = N + E + S + W)
		
		self.fileMenu.add_command(label="New",
										command=self.__newFile) 
		self.fileMenu.add_command(label="Open",
										command=self.__openFile)
		self.fileMenu.add_command(label="Save",
										command=self.__saveFile) 


		self.fileMenu.add_separator()										 
		self.fileMenu.add_command(label="Exit",
										command=self.__quitApplication)
		self.menuBar.add_cascade(label="File",
									menu=self.fileMenu)	 
		
		self.helpMenu.add_command(label="About Notepad",
										command=self.__showAbout) 
		self.menuBar.add_cascade(label="Help",
									menu=self.helpMenu)

		self.root.config(menu=self.menuBar)

		self.verticalScroll.pack(side=RIGHT,fill=Y) 
		self.verticalScroll.config(command=self.textArea.yview)	 
		self.textArea.config(yscrollcommand=self.verticalScroll.set)

		self.horizontalScroll.pack(side=BOTTOM,fill=X) 
		self.horizontalScroll.config(command=self.textArea.xview)	 
		self.textArea.config(xscrollcommand=self.horizontalScroll.set)

		#######################################options (to be added on a menu later)#######################################################
		
		self.textArea.configure(font=("Consolas", 12), cursor="tcross")

		self.textArea.bind("<Button-1>", self.__handle_click)
		self.textArea.bind("<B1-Motion>", self.__handle_click)

		self.setBackground("black")
		self.setForeground("white")
		self.setSelected("black")

		self.root.bind("<Control-plus>", self.zoomIn)
		self.root.bind("<Control-minus>", self.zoomOut)
		self.root.bind("<Control-MouseWheel>", self.zoomWithMouseWheel)

		#########################################################################################################################################
		
	def __quitApplication(self):
		self.root.destroy()
		# exit()

	def __showAbout(self):
		showinfo("Drascii","Mrinal Verma")

	def __openFile(self):
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
	
	def __newFile(self):
		self.root.title("Untitled - Notepad")
		self.file = None
		self.textArea.delete(1.0,END)

	def __saveFile(self):
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

	def run(self):
		self.root.mainloop()

	def setBackground(self, color):
		self.textArea.configure(bg=color)

	def setForeground(self, color):
		self.textArea.configure(fg=color)

	def setSelected(self, color):
		self.textArea.configure(selectbackground=color)	

	def zoomIn(self, event=None):
		current_size = int(self.textArea.cget("font").split()[1])
		new_size = current_size + 2
		self.textArea.configure(font=("Consolas", new_size))

	def zoomOut(self, event=None):
		current_size = int(self.textArea.cget("font").split()[1])
		new_size = current_size - 2
		self.textArea.configure(font=("Consolas", new_size))

	def zoomWithMouseWheel(self, event):
		if event.delta > 0:
			self.zoomIn()
		else:
			self.zoomOut()

	def __handle_click(self, event):
		font_name, font_size = self.textArea.cget("font").split()
		font_size = int(font_size)
		font_object = font.Font(family=font_name, size=font_size)
		font_height = font_object.metrics("linespace")
		font_width = font_object.measure(" ")

		# Calculate the visible portion of the text
		rowsPerColumn = [len(self.textArea.get(f"{x}.0", f"{x}.end")) for x in range(int(self.textArea.index('end').split('.')[0]))]
		outsideViewCols = int(max(rowsPerColumn) * self.textArea.xview()[0])
		outsideViewsLines = int(int(self.textArea.index('end').split('.')[0]) * self.textArea.yview()[0])

		# Calculate the click position relative to the text widget
		click_line = int(event.y / font_height) + outsideViewsLines + 1
		click_column = int(event.x / font_width) + outsideViewCols

		if click_line < 1 or click_column < 0:
			return

		# Add lines if necessary
		num_lines = int(self.textArea.index('end').split('.')[0]) - 1
		while click_line > num_lines:
			self.textArea.insert('end', "\n")
			num_lines += 1

		# Add columns if necessary
		num_columns = len(self.textArea.get(f"{click_line}.0", f"{click_line}.end"))
		while click_column > num_columns:
			self.textArea.insert(f"{click_line}.end", " ")
			num_columns += 1

		# If the click is not on a newline character, delete the existing character and insert 'x' at the click position
		if not self.textArea.get(f"{click_line}.{click_column}") == '\n':
			self.textArea.delete(f"{click_line}.{click_column}")
		self.textArea.insert(f"{click_line}.{click_column}", 'x')


drascii = Drascii(width=1280,height=720)
drascii.run()




