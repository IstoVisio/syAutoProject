import sys
import os
import glob
import tkinter as tk
from tkinter import filedialog 
import syglass
from syglass import pyglass
import code

class Application(tk.Frame):
	outputFoldername = "Output Folder:"
	inputFoldername = "C:/mdm"
	
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		master.geometry("500x250")
		master.title("syGlass AutoCreator -- PNG Folders to syGlass Projects")
		self.pack()
		self.create_widgets()

	def create_widgets(self):
		self.input = tk.Button(self)
		self.input["text"] = self.inputFoldername
		self.input["width"] = 400
		self.input["command"] = self.inputBrowseFiles
		self.input.pack(side="top") 
		
		self.output = tk.Button(self)
		self.output["width"] = 400
		self.output["text"] = self.outputFoldername
		self.output["command"] = self.outputBrowseFiles
		self.output.pack(side="top") 
		
		self.textbox = tk.Text(self, height=10, width=70)
		self.textbox.pack(side="top")
		self.textbox.insert('1.0', 'Choose your input and output directories and press convert.')
		self.textbox['state'] = 'disabled'
		self.textbox['foreground'] = 'white'
		self.textbox['background'] = 'black'
		

		self.convert = tk.Button(self, text="CONVERT", fg="red", command=self.convert)
		self.convert.pack(side="bottom")

	def outputBrowseFiles(self): 
		self.outputFoldername = filedialog.askdirectory(initialdir = "/", title = "Select a Folder") 
		# Change label contents 
		self.output["text"] = "Output Folder: " + self.outputFoldername
	
	def inputBrowseFiles(self): 
		self.inputFoldername = filedialog.askdirectory(initialdir = "/", title = "Select a Folder") 
		# Change label contents 
		self.input["text"] = "Input Folder: " + self.inputFoldername
	
	def convert(self):
		print(self)

def createDirIfMissing(path):
	if not os.path.exists(path):
		os.makedirs(path)
		
def addTextLine(text):
	print(text)
	#txt = self.textbox.get()
	# gets everything in your textbox
	#self.textarea.insert(END,"\n"+text)

def convert():
	inputFoldername = "C:/Users/micha/Pictures/syGlass"
	outputFoldername = "C:/convert_output"
	dirs = []
	all = os.listdir(inputFoldername)
	for each in all:
		fullpath = os.path.join(inputFoldername, each)
		
		if os.path.isdir(fullpath):
			l = glob.glob(os.path.join(fullpath, "*.png"))
			if len(l) > 4:
				dirs.append(fullpath)
	
	createDirIfMissing(outputFoldername)
		
	for imagesetFullPath in dirs:
		basename =os.path.basename(imagesetFullPath)
		addTextLine("Found directory: " + basename)
		newPath = os.path.join(outputFoldername, basename)
		addTextLine("Creating...")
		try:
			project = pyglass.CreateProject(pyglass.path(outputFoldername), basename)
			dd = pyglass.DirectoryDescription()
			firstPNG = glob.glob(os.path.join(imagesetFullPath, "*.png"))[0]
			s = os.path.join(newPath, firstPNG)
			dd.InspectByReferenceFile(s)
			print(dd.GetFileList())
			dataProvider = pyglass.OpenTIFFs(dd.GetFileList(), False)
			cd = pyglass.ConversionDriver()
			cd.SetInput(dataProvider)
			cd.SetOutput(project)
			cd.StartAsynchronous()
		except Exception as e:
			print("An exception occurred")
			print(e)
		
	
	print(dirs)

def main():
	root = tk.Tk()
	ex = Application(root)
	root.mainloop()


if __name__ == '__main__':
	#main()
	convert()

