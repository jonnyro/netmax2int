import os


def max2ase(input_files,output_files):

	LOAD_MAX_FILE_TEMPLATE_STRING = """loadMaxFile "<input_file>" quiet:true;\n"""
	EXPORT_MAX_FILE_TEMPLATE_STRING = """exportFile "<output_file>" #noPrompt;\n"""
	QUIT_MAX_STRING = """QuitMax #noPrompt;\n"""
	#The template should be in the same folder as the module source.
	
	txt = ""  #String containing maxscript code
	for (input_file,output_file) in zip(input_files,output_files):
		#Convert possible relative paths to absolute paths
		input_file_abspath = os.path.abspath(input_file)
		output_file_abspath = os.path.abspath(output_file)
		
		#Delete the output file if it already exists
		if os.path.exists(output_file_abspath):
			os.unlink(output_file_abspath)
		
		
		#Escape backslashes
		input_file_escaped = input_file_abspath.replace("\\","\\\\")
		output_file_escaped = output_file_abspath.replace("\\","\\\\")
		
		
		#print (input_file,input_file_escaped,output_file,output_file_escaped)
		
		txt += LOAD_MAX_FILE_TEMPLATE_STRING.replace("<input_file>",input_file_escaped)
		txt += EXPORT_MAX_FILE_TEMPLATE_STRING.replace("<output_file>",output_file_escaped)
	
	
	txt += QUIT_MAX_STRING
	
	f = open("tmp.ms","w")
	f.write(txt)
	f.close()

	cmd = r'"C:\\Program Files\Autodesk\3ds Max 2009\3dsmax.exe" -U MAXScript tmp.ms'
	ret = os.system(cmd)
	
	if ret <> 0:
		print "Failure executing command"
		print cmd
		
	#Optionally delete maxscript
		
	return ret