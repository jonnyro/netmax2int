import os

def max2ase(input_file,output_file):
	#The template should be in the same folder as the module source.
	script_file = os.path.join(os.path.dirname(__file__),"max2ase_template.ms")
	f = open(script_file,"r")
	txt = f.read()
	f.close()
	
	#Convert possible relative paths to absolute paths
	input_file_abspath = os.path.abspath(input_file)
	output_file_abspath = os.path.abspath(output_file)
	
	#Delete the output file if it already exists
	if os.path.exists(output_file_abspath):
		os.unlink(output_file_abspath)
	
	
	#Escape backslashes
	input_file_escaped = input_file_abspath.replace("\\","\\\\")
	output_file_escaped = output_file_abspath.replace("\\","\\\\")
	
	
	print (input_file,input_file_escaped,output_file,output_file_escaped)
	
	txt = txt.replace("<input_file>",input_file_escaped)
	txt = txt.replace("<output_file>",output_file_escaped)
	
	
	
	f = open("tmp.ms","w")
	f.write(txt)
	f.close()

	cmd = r'"C:\\Program Files\Autodesk\3ds Max 2009\3dsmax.exe" -U MAXScript tmp.ms'
	ret = os.system(cmd)
	
	if ret <> 0:
		print "Failure executing command"
		print cmd
		
	#Optionally delete maxscript
		
	return