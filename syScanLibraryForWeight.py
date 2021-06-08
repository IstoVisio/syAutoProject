import sys
import os
import glob
import tkinter as tk
from tkinter import filedialog 
import tkinter.scrolledtext as tkscrolled
import syglass
from syglass import pyglass
import code
import re


			
def main():	
	#afterward, use pyglass::VolumeLibrary to reload, Call VolumeLibrary::ReloadLibrary(), Call VolumeLibrary::PutEntry()
	pv = pyglass.VolumeLibrary()
	pv.ReloadLibrary()
	#code.interact(local=locals())
	
	y = pv.GetLibraryEntries()
	
	for project in y:
		#print(project.name)
		name = project.name
		m = re.search(r'_[0-9]+ug_', name)
		if bool(m):
			stri = m.group()
			print("Found weight for project: " + name)
			weight = (float(stri[1:-3]) / 1000000.0)
			proj = syglass.get_project(project.path)
			pyproj = proj.impl
			pyproj.SetSampleWeight(weight)


if __name__ == '__main__':
	main()
	

