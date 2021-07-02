import syglass
from syglass import pyglass
#import code
import re
import numpy as np
	
def main():	
	pv = pyglass.VolumeLibrary()
	pv.ReloadLibrary()	
	y = pv.GetLibraryEntries()
	
	for project in y:
		name = project.name
		proj = syglass.get_project(project.path)
		pyproj = proj.impl
		m = re.search(r'_[0-9]+ug_', name)
		print("-------")
		if m is not None:
			stri = m.group()
			print("Found weight for project: " + name)
			weight = (float(stri[1:-3]) / 1000000.0)
			pyproj.SetSampleWeight(weight)
			
		l = re.search(r'_[0-9]+m_', name)
		if l is not None:
			stri = l.group()
			print("Found voxel size for project: " + name + " " + stri)
			weight = float(stri[1:-2])
			dimensions = np.full(3, weight)
			proj.set_voxel_dimensions(dimensions)
			proj.set_voxel_unit('um')
			
		p = re.search(r'ug_.+', name)
		if p is not None:
			stri = p.group()
			citation = stri[3:-3]	
			print("Found citation for project: " + name + " " + citation)
			pyproj.SetCitation(citation)

if __name__ == '__main__':
	main()
	

