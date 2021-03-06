from xmlrpclib import ServerProxy, Error
import socket
import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__),"../common"))

from common import JOB_PENDING_START, JOB_IN_PROGRESS, JOB_FAILED, JOB_COMPLETE, JOB_NOT_FOUND, get_status_string

import xmlrpclib



def dcc2int(target_file,target_format,source_file,source_format,jobserverproxy):

	#Get drop location on network to submit jobs
	print "Querying drop dir"
	
	for attempts in range(1,5):
		try:	
			job_submission_drop = jobserverproxy.get_job_submission_dir()
			break
		except socket.error, (value,message): 
			time.sleep(15)
	for attempts in range(1,5):
		try:
			job_output_drop = jobserverproxy.get_job_output_dir()
			break
		except socket.error, (value,message): 
			time.sleep(15)
	print "Setting up a job"
	#Set up the job, to get a jobid
	for attempts in range(1,5):
		try:
			job_id = jobserverproxy.setup_job(source_format,target_format)
			break
		except socket.error, (value,message): 
			print "Unable to setup job, waiting 15 seconds to retry"
			time.sleep(15)
			
			

	#Copy the input file to the job submission drop
	#I use the system copy command because shutil.copyfile is slow for big files
	copy_cmd = "copy %s %s" % (source_file,job_submission_drop + '\\' + job_id+"."+source_format)
	print "Launching %s" % (copy_cmd)
	ret = os.system(copy_cmd)
	
	
	if ret <> 0:
		print "Unable to copy source to target"
		print " copy command is: %s" % copy_cmd
		sys.exit(-1) #or something kinder, like a catchable exception

	#If we have reached this point, assume copy succeeded
	#signal server to start job
	for attempts in range(1,5):
		try:
			jobserverproxy.start_job(job_id)
			break
		except socket.error, (value,message): 
			#Waiting for connection
			print "Unable to start job, will re-attempt in 15 seconds"
			time.sleep(15)
		

	while True:
		time.sleep(5) #So that we dont spin so fast
		try:
			response = jobserverproxy.query_job_status(job_id)
		except socket.error, (value,message):
			time.sleep(15)
			continue
		print "raw job status is %s" % (response)
		if (JOB_PENDING_START == response):
			print "Job waiting for client to signal start."
			#this is bad, we just sent start command
		if (JOB_IN_PROGRESS == response):
			print "Job in server queue for conversion."
		if (JOB_FAILED == response):
			print "Server was unable to complete conversion"
			sys.exit(-1) #Probably could do better than this, maybe return(-1)
		if (JOB_NOT_FOUND == response):
			print "Server lost our job, PANIC"
			sys.exit(-1) #Probably could do better than this, maybe return(-1)
		if (JOB_COMPLETE == response):
			print "Jobserver indicates conversion is complete"
			break #Leave loop

	#Job is complete, retrieve results
	job_output_path = os.path.join(job_output_drop,job_id+"."+target_format)
	retrieve_cmd = "copy %s %s" % (job_output_path,target_file)
	print "Launching %s" % retrieve_cmd
	ret = os.system(retrieve_cmd)

	#ideally the copy sets the proper name on the target intermediate file

	return

	
if __name__ == "__main__":
	test_input_file = '..\\test_data\\max\\box.max'
	test_output_file = '..\\box.ase'
	
	jobserverproxy = ServerProxy("http://localhost:8000")
	dcc2int(test_output_file,'ase',test_input_file,'max',jobserverproxy)
	# server = ServerProxy("http://localhost:8000") # local server
