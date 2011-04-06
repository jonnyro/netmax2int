"""
#Pseudocode for server.  This is going to need some work.
while running
  Obtain a list of all jobs that are queued up (start has been signaled)
  Compose a maxscript that will process all of these jobs
  Launch max with script
  Wait for results, max will close on complete
  Update job status for results. Removing from queue
"""
import xmlrpclib
import sys
import os
sys.path.append("../common")
from common import JOB_PENDING_START, JOB_IN_PROGRESS, JOB_FAILED, JOB_COMPLETE, JOB_NOT_FOUND, get_status_string
import uuid

from SimpleXMLRPCServer import SimpleXMLRPCServer

"""
1. get_job_output_dir
2. get_job_submission_dir
3. setup_job(input_format_name,output_format_name) returns (jobid)
4. start_job(job_id)
5. query_job_status(job_id) returns (JOB_PENDING_START,JOB_IN_PROGRESS,JOB_FAILED,JOB_COMPLETE,JOB_NOT_FOUND)
"""


class ExportJob:
	def __init__(self,in_format,out_format):
		self.job_id = str(uuid.uuid4())
		self.in_format = in_format
		self.out_format = out_format
		self.job_status = JOB_PENDING_START
	

jobs = []

def get_job_output_dir():
	global job_output_dir
	return job_output_dir
	
def get_job_submission_dir():
	global job_submission_dir
	return job_submission_dir
	
def setup_job(input_format_name,output_format_name):
	global jobs
	job = ExportJob(input_format_name,output_format_name)
	jobs.append(job)
	print "Created job(%s): %s->%s" % (job.job_id,job.in_format,job.out_format)
	return job.job_id
	
def start_job(job_id):
	global jobs
	for job in jobs:
		if (job.job_id == job_id):
			job.job_status = JOB_IN_PROGRESS
			break
	return job.job_status

	
"""
Until I set up a processing thread.  This is the only way i can trigger the conversions to run
"""	
def pump():
	global jobs
	new_jobs_list = []
	#Run over jobs calling max2ase on them
	for job in jobs:
		status = job.job_status
		
		if (status == JOB_IN_PROGRESS):
			input_file = os.path.join(get_job_submission_dir(),job.job_id + ".max")
			output_file = os.path.join(get_job_output_dir(),job.job_id + ".ase")
			max2ase(input_file,output_file)
			
			#if completed ok
			job.job_status = JOB_COMPLETE
			new_jobs_list.append(job)
		else:
			new_jobs_list.append(job)
	
	jobs = new_jobs_list
	
	return ""
	
def query_job_status(job_id):
	global jobs
	
	for job in jobs:
		if (job.job_id == job_id):
			return job.job_status
	
	return JOB_NOT_FOUND
		
def max2ase(input_file,output_file):
	script_file = "max2ase_template.ms"
	f = open(script_file,"r")
	txt = f.read()
	f.close()
	txt = txt.replace("<input_file>",input_file)
	txt = txt.replace("<output_file>",output_file)
	
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
if __name__ == "__main__":
	job_submission_dir='..\\input_drop'
	job_output_dir='..\\output_drop'
	
	server = SimpleXMLRPCServer(("localhost", 8000))
	print "Listening on port 8000..."
	server.register_function(setup_job, "setup_job")
	server.register_function(query_job_status, "query_job_status")
	server.register_function(start_job, "start_job")
	server.register_function(get_job_submission_dir, "get_job_submission_dir")
	server.register_function(get_job_output_dir, "get_job_output_dir")
	server.register_function(pump, "pump")
	server.serve_forever()
