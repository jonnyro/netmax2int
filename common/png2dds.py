import os

def png2dds(input_file,output_file):
	path_to_nvdxt = '../third_party/nvdxt.exe'
	
	#Convert path into windows form
	path_to_nvdxt = os.path.normpath(path_to_nvdxt)
	
	cmd = "%s -file %s -output %s" % (path_to_nvdxt,input_file,output_file)
	print cmd
	ret = os.system(cmd)
	
	return ret