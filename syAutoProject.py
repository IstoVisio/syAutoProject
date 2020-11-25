import sys
import os
import glob
import tkinter as tk
from tkinter import filedialog 
import syglass
from syglass import pyglass
import code

class Application(tk.Frame):
	outputFoldername = "Output Folder: "
	inputFoldername = "Input Folder: "
	screenMessages = []
	
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
		self.textbox['state'] = 'disabled'
		self.textbox['foreground'] = 'white'
		self.textbox['background'] = 'black'
		self.addTextLine('Choose your input and output directories and press convert.')

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
		
	def addTextLine(self, text):
		self.screenMessages.append(text)
		if len(self.screenMessages) > 6:
			self.screenMessages.pop()
		self.textbox['state'] = 'normal'
		self.textbox.insert('1.0',"\n ".join(self.screenMessages))
		self.textbox['state'] = 'disabled'
		self.update()

	def convert(self):
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
		
		if not os.path.exists(outputFoldername):
			os.makedirs(outputFoldername)
			
		for imagesetFullPath in dirs:
			basename =os.path.basename(imagesetFullPath)
			msg = "Found directory: " + basename
			self.addTextLine(msg)
			newPath = os.path.join(outputFoldername, basename)
			self.addTextLine("Creating...")
			try:
				project = pyglass.CreateProject(pyglass.path(outputFoldername), basename)
				dd = pyglass.DirectoryDescription()
				firstPNG = glob.glob(os.path.join(imagesetFullPath, "*.png"))[0]
				firstPNG = firstPNG.replace("\\", "/")
				dd.InspectByReferenceFile(firstPNG)
				dataProvider = pyglass.OpenPNGs(dd.GetFileList())
				cd = pyglass.ConversionDriver()
				cd.SetInput(dataProvider)
				cd.SetOutput(project)
				cd.StartAsynchronous()
			except Exception as e:
				self.addTextLine("Something went wrong...")
				self.addTextLine(str(e))
			else:
				self.addTextLine("Success...!")
			
		
		print(dirs)

def main():
	root = tk.Tk()
	ex = Application(root)
	root.mainloop()


if __name__ == '__main__':
	main()
	

