def max2ase(input_file,output_file):
	script_file = "max2ase_template.ms"
	f = open(script_file,"r")
	txt = f.read()
	f.close()
	txt = txt.replace("<input_file>",os.path.abspath(input_file))
	txt = txt.replace("<output_file>",os.path.abspath(output_file))
	
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