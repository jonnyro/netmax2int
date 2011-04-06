#from common import FLAGS
# simple test program (from the XML-RPC specification)
from xmlrpclib import ServerProxy, Error

import sys
import os
import time

sys.path.append("../common")
from common import get_status_string
from common import JOB_PENDING_START, JOB_IN_PROGRESS, JOB_FAILED, JOB_COMPLETE, JOB_NOT_FOUND, get_status_string
#XMLRPCLib sample from python docs
import xmlrpclib

proxy = xmlrpclib.ServerProxy("http://localhost:8000/")

"""
print "3 is even: %s" % str(proxy.is_even(3))
print "100 is even: %s" % str(proxy.is_even(100))

"""

def max2ase(target,source,env):
	global jobserverproxy
	#For now, only process one file at a time
	source_max_file = str(source[0])
	target_intermediate_file = str(target[0])

	#Get drop location on network to submit jobs
	print "Querying drop dir"
	job_submission_drop = jobserverproxy.get_job_submission_dir()
	job_output_drop = jobserverproxy.get_job_output_dir()
	print "Setting up a job"
	#Set up the job, to get a jobid
	job_id = jobserverproxy.setup_job('ase','max')

	#Copy the input file to the job submission drop
	#I use the system copy command because shutil.copyfile is slow for big files
	copy_cmd = "copy %s %s" % (source_max_file,os.path.join(job_submission_drop,job_id+'.max'))
	print "Launching %s" % (copy_cmd)
	ret = os.system(copy_cmd)
	
	
	if ret <> 0:
		print "Unable to copy source to target"
		print " copy command is: %s" % copy_cmd
		sys.exit(-1) #or something kinder, like a catchable exception

	#If we have reached this point, assume copy succeeded
	#signal server to start job
	jobserverproxy.start_job(job_id)

	while True:
		time.sleep(5) #So that we dont spin so fast
		jobserverproxy.pump() #Trigger conversion of active items
		response = jobserverproxy.query_job_status(job_id)
		if (JOB_PENDING_START == response):
			print "Job waiting for client to signal start."
			#this is bad, we just sent start command
		if (JOB_IN_PROGRESS == response):
			print "Job in server queue for conversion."
		if (JOB_FAILED == response):
			print "Server was unable to complete conversion"
			sys.exit(-1) #Probably could do better than this, maybe return(-1)
		if (JOB_COMPLETE == response):
			print "Jobserver indicates conversion is complete"
			break #Leave loop

	#Job is complete, retrieve results
	job_output_path = os.path.join(job_submission_drop,job_id+'.ase')
	retrieve_cmd = "copy %s %s" % (job_output_path,target_intermediate_file)
	print "Launching %s" % retrieve_cmd
	ret = os.system(retrieve_cmd)

	#ideally the copy sets the proper name on the target intermediate file

	return

	
if __name__ == "__main__":
	test_input_file = '..\\test_data\\max\\box.max'
	test_output_file = '..\\output\\box.ase'
	
	jobserverproxy = ServerProxy("http://localhost:8000")
	max2ase([test_output_file],[test_input_file],None)
	# server = ServerProxy("http://localhost:8000") # local server
	
"""
	job_id = proxy.setup_job('max','ase')
	print job_id
	status = proxy.query_job_status(job_id)
	status_str = get_status_string(status)
	print "Status: %s" % (status_str)
	#Start the job
	proxy.start_job(job_id)
	
	#Check the status again
	#status = proxy.query_job_status(job_id)
	status = proxy.query_job_status(job_id)
	status_str = get_status_string(status)
	print "Status: %s" % (status_str)
"""