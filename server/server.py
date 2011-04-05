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
from SimpleXMLRPCServer import SimpleXMLRPCServer

def is_even(n):
    return n%2 == 0

server = SimpleXMLRPCServer(("localhost", 8000))
print "Listening on port 8000..."
server.register_function(is_even, "is_even")
server.serve_forever()
"""
1. get_job_output_dir
2. get_job_submission_dir
3. setup_job(input_format_name,output_format_name) returns (jobid)
4. start_job(job_id)
5. query_job_status(job_id) returns (JOB_PENDING_START,JOB_IN_PROGRESS,JOB_FAILED,JOB_ COMPLETE)
"""


class ExportJob:
	def __init__:
	

jobs = []

def get_job_output_dir():
	pass
	
def get_job_submission_dir():
	pass
	
def setup_job(input_format_name,output_format_name):
	pass
	
def start_job(job_id):
	pass

def query_job_status(job_id):
	pass



