import sys
import datetime
from subprocess import Popen, PIPE
import json

#container ID extraction
container_id = sys.argv[1]

print("Check :"+container_id)
cmd=['docker', 'inspect', "--format='{{json .State}}'", container_id]

print(cmd)
process = Popen(cmd, stdout=PIPE, stderr=PIPE)
stdout, stderr = process.communicate()

status=json.loads(stdout)
print(status['StartedAt'])
print(stdout)

shinyAppStartDate=datetime.datetime.strptime(status['StartedAt'].split('.')[0], "%Y-%m-%dT%H:%M:%S")
today=datetime.datetime.now()

print(shinyAppStartDate)


deltaTime = (today-shinyAppStartDate).total_seconds()
print(deltaTime)
cmdstop=['docker', 'stop', container_id]
cmdrm=['docker', 'rm', container_id]


process = Popen(cmd, stdout=PIPE, stderr=PIPE)
stdout, stderr = process.communicate()
#everything is compare in seconds
if(deltaTime>300):
	print("delete containers")
	print("docker stop "+container_id)
	process = Popen(cmdstop, stdout=PIPE, stderr=PIPE)
	stdout, stderr = process.communicate()
	print("docker rm "+container_id)
	process = Popen(cmdrm, stdout=PIPE, stderr=PIPE)
	stdout, stderr = process.communicate()
