import os 
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
import tkinter as tk
from tkinter import font

class Drascii:

	__root = Tk()

	# default window width and height
	__thisTextArea = Text(__root)
	__thisMenuBar = Menu(__root)
	__thisFileMenu = Menu(__thisMenuBar, tearoff=0)
	__thisHelpMenu = Menu(__thisMenuBar, tearoff=0)

	# To add scrollbar
	__thisScrollBar = Scrollbar(__thisTextArea)	 
	__file = None

	def __init__(self,**kwargs):

		# Set icon
		#try:
		#		self.__root.wm_iconbitmap("Notepad.ico") 
		#except:
		#		pass

		try:
			self.__thisWidth = kwargs['width']
		except KeyError:
			pass

		try:
			self.__thisHeight = kwargs['height']
		except KeyError:
			pass

		# Set the window text
		self.__root.title("Untitled - Drascii")

		# Center the window
		screenWidth = self.__root.winfo_screenwidth()
		screenHeight = self.__root.winfo_screenheight()
	
		# For left-align
		left = (screenWidth / 2) - (self.__thisWidth / 2) 
		
		# For right-align
		top = (screenHeight / 2) - (self.__thisHeight /2) 
		
		# For top and bottom
		self.__root.geometry('%dx%d+%d+%d' % (self.__thisWidth,
											self.__thisHeight,
											left, top)) 

		# To make the textarea auto resizable
		self.__root.grid_rowconfigure(0, weight=1)
		self.__root.grid_columnconfigure(0, weight=1)

		# Add controls (widget)
		self.__thisTextArea.grid(sticky = N + E + S + W)
		
		# To open new file
		self.__thisFileMenu.add_command(label="New",
										command=self.__newFile) 
		
		# To open a already existing file
		self.__thisFileMenu.add_command(label="Open",
										command=self.__openFile)
		
		# To save current file
		self.__thisFileMenu.add_command(label="Save",
										command=self.__saveFile) 

		# To create a line in the dialog	 
		self.__thisFileMenu.add_separator()										 
		self.__thisFileMenu.add_command(label="Exit",
										command=self.__quitApplication)
		self.__thisMenuBar.add_cascade(label="File",
									menu=self.__thisFileMenu)	 
		
		# To create a feature of description of the notepad
		self.__thisHelpMenu.add_command(label="About Notepad",
										command=self.__showAbout) 
		self.__thisMenuBar.add_cascade(label="Help",
									menu=self.__thisHelpMenu)

		self.__root.config(menu=self.__thisMenuBar)

		self.__thisScrollBar.pack(side=RIGHT,fill=Y)				 
		
		# Scrollbar will adjust automatically according to the content	 
		self.__thisScrollBar.config(command=self.__thisTextArea.yview)	 
		self.__thisTextArea.config(yscrollcommand=self.__thisScrollBar.set)

		#######################################options (to be added on a menu later)#######################################################
		
		self.__thisTextArea.configure(font=("TkFixedFont", 12))
		self.__thisTextArea.bind('<Button-1>', self.__handle_click)

		self.setBackground("black")
		self.setForeground("white")
		self.setSelected("red")

		self.__root.bind("<Control-plus>", self.zoomIn)
		self.__root.bind("<Control-minus>", self.zoomOut)

		#########################################################################################################################################
		
	def __quitApplication(self):
		self.__root.destroy()
		# exit()

	def __showAbout(self):
		showinfo("Drascii","Mrinal Verma")

	def __openFile(self):
		
		self.__file = askopenfilename(defaultextension=".txt",
									filetypes=[("All Files","*.*"),
										("Text Documents","*.txt")])

		if self.__file == "":
			
			# no file to open
			self.__file = None
		else:
			
			# Try to open the file
			# set the window title
			self.__root.title(os.path.basename(self.__file) + " - Drascii")
			self.__thisTextArea.delete(1.0,END)

			file = open(self.__file,"r")

			self.__thisTextArea.insert(1.0,file.read())

			file.close()
	
	def __newFile(self):
		self.__root.title("Untitled - Notepad")
		self.__file = None
		self.__thisTextArea.delete(1.0,END)

	def __saveFile(self):

		if self.__file == None:
			# Save as new file
			self.__file = asksaveasfilename(initialfile='Untitled.txt',
											defaultextension=".txt",
											filetypes=[("All Files","*.*"),
												("Text Documents","*.txt")])

			if self.__file == "":
				self.__file = None
			else:
				
				# Try to save the file
				file = open(self.__file,"w")
				file.write(self.__thisTextArea.get(1.0,END))
				file.close()
				
				# Change the window title
				self.__root.title(os.path.basename(self.__file) + " - Drascii")
				
			
		else:
			file = open(self.__file,"w")
			file.write(self.__thisTextArea.get(1.0,END))
			file.close()

	def run(self):
		self.__root.mainloop()

	def setBackground(self, color):
		self.__thisTextArea.configure(bg=color)

	def setForeground(self, color):
		self.__thisTextArea.configure(fg=color)

	def setSelected(self, color):
		self.__thisTextArea.configure(selectbackground=color)	

	def zoomIn(self, event=None):
		current_size = int(self.__thisTextArea.cget("font").split()[1])
		new_size = current_size + 2
		self.__thisTextArea.configure(font=("TkFixedFont", new_size))

	def zoomOut(self, event=None):
		current_size = int(self.__thisTextArea.cget("font").split()[1])
		new_size = current_size - 2
		self.__thisTextArea.configure(font=("TkFixedFont", new_size))

	def __handle_click(self, event):
		font_name, font_size = self.__thisTextArea.cget("font").split()
		font_size = int(font_size)
		font_object = font.Font(family=font_name, size=font_size)
		font_height = font_object.metrics("linespace")
		font_width = font_object.measure(" ")

		click_line = int(event.y / font_height)
		click_column = int(event.x / font_width)

		# Add lines
		num_lines = int(self.__thisTextArea.index('end').split('.')[0]) - 2
		while click_line > num_lines:
			self.__thisTextArea.insert('end', "\n")
			num_lines += 1

		# Add columns
		num_columns = len(self.__thisTextArea.get(f"{click_line}.0", f"{click_line}.end"))
		while click_column > num_columns:
			self.__thisTextArea.insert(f"{click_line}.end", " ")
			num_columns += 1

		self.__thisTextArea.delete(f"{click_line}.{click_column}")
		self.__thisTextArea.insert(f"{click_line}.{click_column}", 'a')

drascii = Drascii(width=1280,height=720)
drascii.run()




