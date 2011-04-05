
#Pseudocode for server.  This is going to need some work.
while running
  Obtain a list of all jobs that are queued up (start has been signaled)
  Compose a maxscript that will process all of these jobs
  Launch max with script
  Wait for results, max will close on complete
  Update job status for results. Removing from queue