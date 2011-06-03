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
import psd2png
import png2dds
import max2ase
import traceback
import threading
from socket import getfqdn
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
	
	for i in range(len(jobs)):
		if (jobs[i].job_id == job_id):
			tmpjob = jobs[i]
			tmpjob.job_status = JOB_IN_PROGRESS
			jobs[i] = tmpjob
			return jobs[i].job_status
	return JOB_NOT_FOUND
	
def mark_job_complete(job_id):
	global jobs
	for i in range(len(jobs)):
		if (jobs[i].job_id == job_id):
			tmpjob = jobs[i]
			tmpjob.job_status = JOB_COMPLETE
			jobs[i] = tmpjob
			return jobs[i].job_status
	return JOB_NOT_FOUND

def pump():
	""" Do nothing now """
	return ""
	
working = True
	
class WorkerThread(threading.Thread):
	def run(self):
		global working
		global jobs
		new_jobs_list = []

		while working:
			try:

				#Run over jobs calling max2ase on them
				ready_jobs = filter(lambda x:x.job_status == JOB_IN_PROGRESS, jobs)
				other_jobs = filter(lambda x:x.job_status <> JOB_IN_PROGRESS, jobs)

				#Of the ready jobs, separate into formats I know how to convert
				ready_jobs_max2ase = filter(lambda x:(x.in_format == 'max') and (x.out_format == 'ase'), ready_jobs)
				ready_jobs_png2dds = filter(lambda x:(x.in_format == 'png') and (x.out_format == 'dds'), ready_jobs)
				ready_jobs_psd2png = filter(lambda x:(x.in_format == 'psd') and (x.out_format == 'png'), ready_jobs)
				
				
				#Process max2ase conversions
				if (len(ready_jobs_max2ase) > 0):
					##Get the list of input files
					input_files_max2ase = map(lambda job:os.path.abspath(os.path.join(get_job_submission_dir(),job.job_id + "." + job.in_format)),ready_jobs_max2ase)
					##Get the list of output files
					output_files_max2ase = map(lambda job:os.path.abspath(os.path.join(get_job_output_dir(),job.job_id + "." + job.out_format)),ready_jobs_max2ase)
					##Convert
					print "Launching (%s->%s) conversion of %s to %s" % ('max','ase',input_files_max2ase,output_files_max2ase)
					ret = max2ase.max2ase(input_files_max2ase,output_files_max2ase)
					##Process result
					if (ret == 0):
						for job in ready_jobs_max2ase:
							mark_job_complete(job.job_id)
							print "Setting job id %s to complete" % (job.job_id) 
							
				#Process png2dds conversions
				if (len(ready_jobs_png2dds) > 0):
					##Get the list of input files
					input_files_png2dds = map(lambda job:os.path.abspath(os.path.join(get_job_submission_dir(),job.job_id + "." + job.in_format)),ready_jobs_png2dds)
					##Get the list of output files
					output_files_png2dds = map(lambda job:os.path.abspath(os.path.join(get_job_output_dir(),job.job_id + "." + job.out_format)),ready_jobs_png2dds)
					##Convert
					print "Launching (%s->%s) conversion of %s to %s" % ('max','ase',input_files_png2dds,output_files_png2dds)
					ret = png2dds.png2dds(input_files_png2dds,output_files_png2dds)
					##Process result
					if (ret == 0):
						for job in ready_jobs_png2dds:
							mark_job_complete(job.job_id)
							print "Setting job id %s to complete" % (job.job_id) 

				#Process psd2png conversions
				if (len(ready_jobs_psd2png) > 0):
					##Get the list of input files
					input_files_max2ase = map(lambda job:os.path.abspath(os.path.join(get_job_submission_dir(),job.job_id + "." + job.in_format)),ready_jobs_psd2png)
					##Get the list of output files
					output_files_max2ase = map(lambda job:os.path.abspath(os.path.join(get_job_output_dir(),job.job_id + "." + job.out_format)),ready_jobs_psd2png)
					##Convert
					print "Launching (%s->%s) conversion of %s to %s" % ('max','ase',input_files_max2ase,output_files_max2ase)
					ret = max2ase.max2ase(input_files_max2ase,output_files_max2ase)
					##Process result
					if (ret == 0):
						for job in ready_jobs_psd2png:
							mark_job_complete(job.job_id)
							print "Setting job id %s to complete" % (job.job_id) 					
						

				
			except:
				traceback.print_exc(file=sys.stdout)
				

	
def query_job_status(job_id):
	global jobs
	
	for job in jobs:
		if (job.job_id == job_id):
			return job.job_status
	
	return JOB_NOT_FOUND

 
if __name__ == "__main__":
	job_submission_dir=os.path.abspath('..\\input_drop')
	job_output_dir=os.path.abspath('..\\output_drop')
	worker = WorkerThread()
	worker.start()
	server = SimpleXMLRPCServer((getfqdn(), 8000))
	
	print "Listening on port 8000..."
	server.register_function(setup_job, "setup_job")
	server.register_function(query_job_status, "query_job_status")
	server.register_function(start_job, "start_job")
	server.register_function(get_job_submission_dir, "get_job_submission_dir")
	server.register_function(get_job_output_dir, "get_job_output_dir")
	server.register_function(pump, "pump")
	server.serve_forever()
