#!/usr/bin/env python
import argparse
import subprocess
import shutil
import os
import datetime
from bioblend.galaxy import GalaxyInstance
import string
import random

##############################################
#~ load all existing workflow to the galaxy instance of the current user
##############################################
def addAllWorkflow(galaxyWeb,workflow_Dir): 
	#~ workflow_Dir="/nas_Dir/workflow"
	src_workflows = os.listdir(workflow_Dir)
	for workflow in src_workflows:
		#~ print "import workflow: " +workflow
		galaxyWeb.workflows.import_workflow_from_local_path(workflow_Dir+"/"+workflow)

##############################################
#~ Create a new history name which will contains
#~ todayDate+workflowName+runName
##############################################
def Create_History(galaxyWeb,workflow_Name):
	today = datetime.date.today()
#	random.seed(datetime.date.now())
	random.seed(str(datetime.datetime.today()))
	historyName= "".join(random.sample(list(string.ascii_uppercase),10))+"_"+str(today)+workflow_Name
	galaxyWeb.histories.create_history(name=historyName)
	myNewHistory=galaxyWeb.histories.get_histories(name=historyName)
	return(myNewHistory[0]['id'])

##############################################
#~ Uploads data to a specific history
##############################################
def upload_To_History(galaxyWeb,filesPath,historyID,inputAbsolutPath):
	#~  add the data to the history
	for dataToLoad in filesPath:
		if dataToLoad.endswith('xls') :
		#~ gi.tools.upload_file(path='/nas_Dir/R_2016_07_05_14_24_05_user_proton-148-Recherche_CancerPanel04072016BEColon_And_Lung_V2_Proton_Auto_user_proton-148-Recherche_CancerPanel04072016BEColon_And_Lung_V2_Proton_505.bc_summary.xls',history_id=historyID,file_type='txt',dbkey="hg19plasma")
			galaxyWeb.tools.upload_file(path=inputAbsolutPath+"/"+dataToLoad,history_id=historyID,file_type='txt',dbkey="hg19plasma")
	print "Data loaded to the current history"

##############################################
#~ Retrieve the current history and build a 
#~ a dictionnary of the recent Uploaded data
##############################################
def CNV_Input_Dict(galaxyWeb,historyID):
	data_Input_CNVID=dict()
	for dataset in galaxyWeb.histories.show_history(historyID,contents=True):
		print dataset["name"]
		if ("bc_summary" in dataset["name"]):
			data_Input_CNVID["bcsummary"]= dataset["id"]
		else:
			data_Input_CNVID["bcmatrix"]= dataset["id"]
	return(data_Input_CNVID)

def Run_CNV_Workflow(galaxyWeb,data_Input_CNVID,historyID):
	CNVworkflowID=""
	for workflow in galaxyWeb.workflows.get_workflows():
		if "CNVtest" in workflow["name"]:
			CNVworkflowID=workflow['id']
			print "Workflow ID found"
	cnv_Workflow=galaxyWeb.workflows.show_workflow(CNVworkflowID)
	#~ cnv_Workflow['inputs']['1']['label']
	inputWorkflow=dict()
	for key,value in cnv_Workflow['inputs'].iteritems():
		#~ print key
		if ("bcsummary" in value['label']):
			inputWorkflow[key]= { 'src':'hda', 'id':data_Input_CNVID["bcsummary"] }
		else:
			inputWorkflow[key]= { 'src':'hda', 'id':data_Input_CNVID["bcmatrix"] }
	galaxyWeb.workflows.invoke_workflow(CNVworkflowID, inputs=inputWorkflow,history_id=historyID)

##############################################
#~  Main CNV script to call from the IonTorrent Browser
##############################################
def mainCNV(pathToFile,apiKey,inputAbsolutPath):
	gi = GalaxyInstance(url='http://gqlqxyserver', key=apiKey)
	#~ if a new user add all the workflow
	#~ workflow_Dir="/nas_Dir/workflow"
	#~ addAllWorkflow(gi,workflow_Dir)
	historyID=Create_History(gi,"_CNV")
	#~ Uploads data to a specific history
	upload_To_History(gi,pathToFile,historyID,inputAbsolutPath)
	#~ Retrieve the current history and build a 
	#~ a dictionnary of the recent Uploaded data
	dataCNVID=CNV_Input_Dict(gi,historyID)
	Run_CNV_Workflow(gi,dataCNVID,historyID)


if __name__ == "__main__":
	#~ parser = argparse.ArgumentParser(prog=".py",description='This script is a wrapper around polyweb/polydiag to faciliate\n the data management.')
	#~ parser = argparse.ArgumentParser(description='This script is a wrapper around galaxy/workflow to send data to galaxy')
	#~ parser.add_argument('-k','--apiKey', help='the user apikey (which will be used)',required=True)
	apiKey="qpykey"
	inputAbsolutPath="/nas_Dir"
	src_files = os.listdir(inputAbsolutPath)

	mainCNV(src_files,apiKey,inputAbsolutPath)
	#~ str(random.sample(list(string.ascii_uppercase),10))

	#~ gi.histories.create_history(name=)
