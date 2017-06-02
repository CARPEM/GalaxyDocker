import os
import sys

import json


from datamanagerpkg import ProtonCommunication_data_manager
from datamanagerpkg import GalaxyCommunication_data_manager



from sequencer.models import Experiments, GalaxyUsers 
from sequencer.models import GalaxyJobs, ExperimentRawData

##########################
#URL SEQUENCER
##########################
from GlobalVariables import sequencer_base_url 
from GlobalVariables import sequencer_user
from GlobalVariables import sequencer_password
from GlobalVariables import sequencer_severName
from GlobalVariables import sequencer_ExperimentLimit
from GlobalVariables import toolsInformation

##########################
#URL GALAXY
##########################
from GlobalVariables import  galaxy_base_url
from GlobalVariables import  apiKey

##########################
#NAs DIr folder
##########################
from GlobalVariables import nasInput
from GlobalVariables import CNVfolderName
from GlobalVariables import plasmaFolderName
from GlobalVariables import nasResults
from GlobalVariables import workflowPath

##########################
#SMTP folder
##########################
from GlobalVariables import smtpServerAphp
from GlobalVariables import smtpPortServer
from GlobalVariables import fromAddrOfficial

from sequencer.views import getDataPath
from datamanagerpkg import ProtonCommunication_data_manager
from datamanagerpkg import GalaxyCommunication_data_manager
from pprint import pprint

#open a workflow
with open('/nas_Dir/workflow/Galaxy-Workflow-Plasma_mutation.ga') as data_file:    
    data = json.load(data_file)

pprint(data)

#now I have the key in order
stepkey=data['steps'].keys()
stepkey = [int(x) for x in stepkey]
stepkey.sort()

#create a workflow object
#~ u'annotation': u'plasma workflow to generates all the data',
#~ u'name': u'Plasma_mutation',
from sequencer.models import Workflows,WorkflowsTools,Supportedfiles
tryexp = None
try:
   tryexp = Workflows.objects.get(name=str(data['name']))
except Workflows.DoesNotExist:
   tryexp = None
   if (tryexp == None):
      workflow_local=Workflows(name=str(data['name']),description=str(data['name']))
      workflow_local.save()

workflow_local = Workflows.objects.get(name=str(data['name']))
for step in stepkey:

   if data['steps'][str(step)]['tool_id']!=None:
      #create a tool
      print("grou1")
      try:
         tryexp = WorkflowsTools.objects.get(primary_name=str(data['steps'][str(step)]['tool_id']+"_"+data['steps'][str(step)]['tool_version']+".json"))
      except WorkflowsTools.DoesNotExist:
         tryexp = None
      #~ if tryexp == None:
         print("grou2")
         newtool=WorkflowsTools(primary_name=str(data['steps'][str(step)]['tool_id']+"_"+data['steps'][str(step)]['tool_version']+".json"),
         name=str(data['steps'][str(step)]['tool_id']),
         version=str(data['steps'][str(step)]['tool_version']))
         newtool.save()
         print("grou3")
         workflow_local.tools_list.add(newtool)
         print("grou4")
         workflow_local.save()
         print( data['steps'][str(step)]['tool_id']+"_"+data['steps'][str(step)]['tool_version']+".json")
      #create a tool 
         with open(toolsInformation+data['steps'][str(step)]['tool_id']+"_"+data['steps'][str(step)]['tool_version']+".json") as data_file_tool:    
            tool = json.load(data_file_tool)
            #~ print(tool['function'][0])
            print("#######################input")
            #~ print(tool['function'][0]['input'])
            for dataInput in tool['function'][0]['input'] :
               try:
                  tryexp = Supportedfiles.objects.get(dataDescription=str(dataInput['dataDescription']))
               except Supportedfiles.DoesNotExist:
                  tryexp = None
                  newfile=Supportedfiles(dataHandle=str(dataInput['dataHandle']),
                  dataDescription=str(dataInput['dataDescription']),
                  dataFormatEdamOntology=str(dataInput['dataFormat'][0]['uri'])) 
                  newfile.save()      
                  newtool.inputlist.add(newfile)
                  newtool.save()
               #~ print("#######################dataInpty")
            print("#######################output")
            for dataInput in tool['function'][0]['input'] :
               try:
                  tryexp = Supportedfiles.objects.get(dataDescription=str(dataInput['dataDescription']))
               except Supportedfiles.DoesNotExist:
                  tryexp = None
               #~ if tryexp == None:
                  newfile=Supportedfiles(dataHandle=str(dataInput['dataHandle']),
                  dataDescription=str(dataInput['dataDescription']),
                  dataFormatEdamOntology=str(dataInput['dataFormat'][0]['uri']) )
                  newfile.save()  
                  newtool.outputlist.add(newfile)
                  newtool.save()
