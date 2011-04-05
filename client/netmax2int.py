#from common import FLAGS
# simple test program (from the XML-RPC specification)
from xmlrpclib import ServerProxy, Error

"""


def max2ase(target,source,env):
	
	#For now, only process one file at a time
	source_max_file = str(source[0])
	target_intermediate_file = str(target[0])

	#Get drop location on network to submit jobs
	job_submission_drop = jobserverproxy.get_job_submission_dir()
	job_output_drop = jobserverpoxy.get_job_output_dir()

	#Set up the job, to get a jobid
	job_id = jobserverproxy.setup_job('ase','max')
 
	#Copy the input file to the job submission drop
	#I use the system copy command because shutil.copyfile is slow for big files
	ret = os.sytem("copy %s %s" % (source_max_file,job_submission_drop))

	if ret <> 0:
      sys.exit(-1) #or something kinder, like a catchable exception

	#If we have reached this point, assume copy succeeded
	#signal server to start job
	jobserverproxy.start_job(job_id)

	while True:
      time.sleep(5) #So that we dont spin so fast
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
    job_output_path = os.path.join(job_submission_dir,job_id)
    ret = os.system("copy %s %s" % (job_output_path,target_intermediate_file)

     #ideally the copy sets the proper name on the target intermediate file

    return
"""	
	
if __name__ == "__main__":
	#max2ase(["output.ase"],["input.max"],None)
	# server = ServerProxy("http://localhost:8000") # local server
	proxy = ServerProxy("http://localhost:8000")

	job_id = proxy.setup_job('max','ase')
	#status = proxy.query_job_status("BLAH")
	#print "Status: %s" % (status)
	