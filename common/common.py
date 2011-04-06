#Flags shared by server and client
JOB_PENDING_START = 0
JOB_IN_PROGRESS   = 1
JOB_FAILED        = 2
JOB_COMPLETE      = 3
JOB_NOT_FOUND	  = 4

def get_status_string(status_code):
	global JOB_PENDING_START,JOB_IN_PROGRESS,JOB_FAILED,JOB_COMPLETE,JOB_NOT_FOUND
	
	if (status_code == JOB_PENDING_START):
		return "JOB_PENDING_START"
	elif (status_code == JOB_IN_PROGRESS):
		return "JOB_IN_PROGRESS"
	elif (status_code == JOB_FAILED):
		return "JOB_FAILED"
	elif (status_code == JOB_COMPLETE):
		return "JOB_COMPLETE"
	elif (status_code == JOB_NOT_FOUND):
		return "JOB_NOT_FOUND"