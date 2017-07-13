#!/usr/bin/env python

"""This module illustrates how to write 
GalaxyCommunication_data_manager.pyc
and ProtonCommunication_data_manager.py
Basically it is just a sphinx test for the documentation
"""

import argparse
import subprocess
import shutil
import os
import datetime
from bioblend.galaxy import GalaxyInstance
import string
import random
import logging

##########################
#URL GALAXY
##########################
from GlobalVariables import galaxy_base_url 
from GlobalVariables import apiKey
from GlobalVariables import inputAbsolutPath

__license__ = "grou "
__revision__ = " $Id: Main_data_manager.py 1586 2016-08-10 15:56:25 $"
__docformat__ = 'reStructuredText'
__author__ = 'William Digan, CARPEM'

logger = logging.getLogger(__name__)
##############################################
#~ connection to the galaxy server
##############################################
def galaxyConnection(base_url,apiKey): 
	""" 
	galaxyConnection(base_url,apiKey)
	returns (GalaxyInstance)
	
	**Descriptions**:
	
	This function aims to create a connection to the Galaxy server.
	
	**Parameters**:
	
        :param base_url: an url which point to your galaxy instance 
        :param apiKey: a valid galaxy API key
        :type base_url: string
        :type apiKey: string
        :returns: GalaxyInstance
        :rtype: GalaxyInstance         
	""" 
	try:
		gi = GalaxyInstance(url=base_url, key=apiKey)
	except StandardError:
		logger.error("An error occured. Verify the server connection.")
	return(gi)
##############################################
#~ Check the current users and return all users also
##############################################
def returnGalaxyUsers(galaxyWeb): 
	""" 
	returnGalaxyUsers(galaxyWeb)
	returns (usersDict)
	
	**Descriptions**:
	
	This function aims to return the galaxy users dictionnary.
	
	**Parameters**:
	
        :param galaxyWeb: a connection to your galaxy instance 
        :type galaxyWeb: GalaxyInstance
        :returns: usersDict
        :rtype: Dictionnary   

	.. note:: In this function I can not use the users.get_current_user()
		function from bioblend because I use the Galaxy Master ApiKey
	""" 
	usersDict=galaxyWeb.users.get_users()
	return(usersDict)

def createUserApikey(galaxyWeb,userID): 
	""" 
	createUserApikey(galaxyWeb,userID)
	returns (userApiKey)
	
	**Descriptions**:
	
	This function aims to return the galaxy users dictionnary.
	
	**Parameters**:
	
        :param galaxyWeb: a connection to your galaxy instance 
        :type galaxyWeb: GalaxyInstance
        :param userID: the current user ID in  Galaxy
        :type userID: string
        :returns: userApiKey
        :rtype: string   

	.. note:: In this function I can not use the users.get_current_user()
		function from bioblend because I use the Galaxy Master ApiKey
	"""
	userApiKey=galaxyWeb.users.create_user_apikey(userID)
	return(userApiKey)

##############################################
#~ load all existing workflow to the galaxy instance of the current user
##############################################
def addAllWorkflow(galaxyWeb,workflow_Dir): 
	""" 
	addAllWorkflow(galaxyWeb,workflow_Dir)
	returns (int)
	
	**Descriptions**:
	
	This function aims to load all workflows on a folder such as 
	'/nas_Dir/workflow' for the current users.
	
	**Parameters**:
	
        :param galaxyWeb: a connection to your galaxy instance 
        :type galaxyWeb: GalaxyInstance
        :param workflow_Dir: path to the workflow directory
        :type workflow_Dir: string
        :returns: 0 or 1
        :rtype: int   

	.. note:: This function need to be used only one time when the
	Galaxy user api key is generated
	"""	
	if galaxyWeb.workflows.get_workflows()==[]:
		#~ workflow_Dir="/nas_Dir/workflow"
		src_workflows = os.listdir(workflow_Dir)
		for workflow in src_workflows:
			#~ print "import workflow: " +workflow
			galaxyWeb.workflows.import_workflow_from_local_path(workflow_Dir+"/"+workflow)
		return(1)
	else:
		return(0)

##############################################
#~ Create a new history name which will contains
#~ todayDate+workflowName+runName
##############################################
def Create_History(galaxyWeb,workflow_Name):
	""" 
	Create_History(galaxyWeb,workflow_Name)
	returns (historyDict)
	
	**Descriptions**:
	
	This function create a new galaxy history where the data will be load.

	**Parameters**:
	
        :param galaxyWeb: a connection to your galaxy instance 
        :type galaxyWeb: GalaxyInstance
        :param workflow_Name: part of the name of the history
        :type workflow_Name: string
        :returns: historyDict
        :rtype: dict   
	"""
	logger.info("##########################")
	logger.info("Create_History() for "+workflow_Name)
	logger.info("##########################")	
	today = datetime.date.today()
#	random.seed(datetime.date.now())
	random.seed(str(datetime.datetime.today()))
	#~ historyName= "".join(random.sample(list(string.ascii_uppercase),10))+"_"+str(today)+workflow_Name
	historyName= str(today)+workflow_Name
	galaxyWeb.histories.create_history(name=historyName)
	myNewHistory=galaxyWeb.histories.get_histories(name=historyName)
	logger.debug("##########################")
	logger.debug(historyName)
	logger.debug("##########################")		
	#~ return(myNewHistory[0]['id'])
	return({'today':str(today),'id':str(myNewHistory[0]['id']), 'name':str(historyName)})

##############################################
#~ Uploads data to a specific history
##############################################
#~ def upload_To_History(galaxyWeb,expDict,historyID,inputAbsolutPath):
def upload_To_History_CNV(galaxyWeb,expDict,historyID):
	""" 
	upload_To_History_CNV(galaxyWeb,expDict,historyID)
	returns (int)
	
	**Descriptions**:
	
	This function upload to a specific history the CNV data.

	**Parameters**:
	
        :param galaxyWeb: a connection to your galaxy instance 
        :type galaxyWeb: GalaxyInstance
        :param expDict: a result dictionnary output from the ProtonCommunication script
        :type expDict: dictionnary
        :param historyID: a galaxy history ID
        :type historyID: string
        :returns: 1
        :rtype: int   
	"""	
	galaxyWeb.tools.upload_file(path=expDict['bcmatrix'],history_id=historyID,file_type='txt',dbkey="hg19plasma")
	galaxyWeb.tools.upload_file(path=expDict['bcsummary'],history_id=historyID,file_type='txt',dbkey="hg19plasma")
	print "Data loaded to the current history"
	return 1

##############################################
#~ Retrieve the current history and build a 
#~ a dictionnary of the recent Uploaded data
##############################################
def CNV_Input_Dict(galaxyWeb,historyID):
	""" 
	CNV_Input_Dict(galaxyWeb,historyID)
	returns (data_Input_CNVID)
	
	**Descriptions**:
	
	This function return a dictionnary whitch contains datasets id for 
	CNV input files. This dictionnary contains a bcsummary and bcmatrix keys.
	
	**Parameters**:
	
        :param galaxyWeb: a connection to your galaxy instance 
        :type galaxyWeb: GalaxyInstance
        :param historyID: a galaxy history ID
        :type historyID: string
        :returns: data_Input_CNVID
        :rtype: dictionnary   
	"""	
	data_Input_CNVID=dict()
	for dataset in galaxyWeb.histories.show_history(historyID,contents=True):
		print dataset["name"]
		if ("bc_summary" in dataset["name"]):
			data_Input_CNVID["bcsummary"]= dataset["id"]
		else:
			data_Input_CNVID["bcmatrix"]= dataset["id"]
	return(data_Input_CNVID)

##############################################
#~ Retrieve the CNV workflow and execute it
##############################################
def Run_CNV_Workflow(galaxyWeb,data_Input_CNVID,historyID):
	""" 
	Run_CNV_Workflow(galaxyWeb,data_Input_CNVID,historyID)
	returns (int)
	
	**Descriptions**:
	
	This function retrieve the CNV workflow and execute it. Use a dictionnary
	as input.
	
	**Parameters**:
	
        :param galaxyWeb: a connection to your galaxy instance 
        :type galaxyWeb: GalaxyInstance
        :param data_Input_CNVID: a dictionnary output from function CNV_Input_Dict
        :type data_Input_CNVID: dictionnary
        :param historyID: a galaxy history ID
        :type historyID: string
        :returns: 1
        :rtype: int   
	"""	
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
			inputWorkflow[key]= { 'src':'hda', 'id': data_Input_CNVID["bcsummary"] }
		else:
			inputWorkflow[key]= { 'src':'hda', 'id': data_Input_CNVID["bcmatrix"] }
	galaxyWeb.workflows.invoke_workflow(CNVworkflowID, inputs=inputWorkflow,history_id=historyID)
	return(1)

##############################################
#~  Main CNV script to call from the IonTorrent Browser
##############################################
def mainCNV(expDict,base_url,apiKey):
	""" 
	mainCNV(expDict,base_url,apiKey)
	returns (historyID)
	
	**Descriptions**:
	
	This function execute the CNV routine. From a run of the Ion Proton,
	The routine will connect the user to Galaxy, create an history,
	upload the CNV input files to it and run the CNV workflow.
	
	**Parameters**:
	
        :param expDict: a dictionnary output from ProtonCommunication_data_manager.copyData().
        :param base_url: an url which point to your galaxy instance 
        :param apiKey: a valid galaxy API key
        :type base_url: string
        :type apiKey: string
        :returns historyID: the galaxy history where the data and the CNV run are located
        :rtype historyID: a dictionnary

	"""	
	gi=galaxyConnection(base_url,apiKey)
	#~ if a new user add all the workflow
	print expDict["resultsName"]
	print "dictname"
	historyID=Create_History(gi,"_PLASMA_"+expDict["resultsName"])
	#~ Uploads data to a specific history
	upload_To_History_CNV(gi,expDict,str(historyID['id']))
	#~ upload_To_History(gi,expDict,historyID,inputAbsolutPath)
	#~ Retrieve the current history and build a 
	#~ a dictionnary of the recent Uploaded data
	dataCNVID=CNV_Input_Dict(gi,str(historyID['id']))
	Run_CNV_Workflow(gi,dataCNVID,str(historyID['id']))
	print "job done, hydrate yourself"
	return(historyID)
##############################################
#~  Main Plasma script to call from the IonTorrent Browser
##############################################
def mainPlasma(expDict,base_url,apiKey,inputDataFolder):
	""" 
	mainPlasma(expDict,base_url,apiKey)
	returns (historyID)
	
	**Descriptions**:
	
	This function execute the CNV routine. From a run of the Ion Proton,
	The routine will connect the user to Galaxy, create an history,
	upload the CNV input files to it and run the CNV workflow.
	
	**Parameters**:
	
        :param expDict: a dictionnary output from ProtonCommunication_data_manager.copyData().
        :param base_url: an url which point to your galaxy instance 
        :param apiKey: a valid galaxy API key
        :type base_url: string
        :type apiKey: string
        :returns historyID: the galaxy history where the data and the CNV run are located
        :rtype historyID: a dictionnary
	"""
	gi=galaxyConnection(base_url,apiKey)
	#~ if a new user add all the workflow
	logger.info("##########################")
	logger.info("mainPlasma for "+expDict["resultsName"])
	logger.info("##########################")	

	historyID=Create_History(gi,"_PLASMA_"+expDict["resultsName"])
	#~ Uploads data to a specific history
	upload_To_History_Plasma(gi,expDict,str(historyID['id']),inputDataFolder)
	logger.info("##########################")
	logger.info("mupload_From_Library_To_Plasma_History :")
	logger.info("##########################")		
	#~ upload_From_Library_To_Plasma_History(gi,expDict,str(historyID['id']),"/Plasma/")
	#~ Retrieve the current history and build a 
	#~ a dictionnary of the recent Uploaded data
	
##############################################
	dataPlasmaID=Plasma_Input_Dict(gi,str(historyID['id']))
	Run_Plasma_Workflow(gi,dataPlasmaID,str(historyID['id']))
	logger.info("job done, hydrate yourself")
	return(historyID)


def mainSamtools_fromNGSData(expDict,base_url,apiKey,inputDataFolder):
	""" 
	mainPlasma_fromNGSData(expDict,base_url,apiKey)
	returns (historyID)
	
	**Descriptions**:
	
	This function execute the CNV routine. From a run of the Ion Proton,
	The routine will connect the user to Galaxy, create an history,
	upload the CNV input files to it and run the CNV workflow.
	
	**Parameters**:
	
        :param expDict: a dictionnary output from ProtonCommunication_data_manager.copyData().
        :param base_url: an url which point to your galaxy instance 
        :param apiKey: a valid galaxy API key
        :type base_url: string
        :type apiKey: string
        :returns historyID: the galaxy history where the data and the CNV run are located
        :rtype historyID: a dictionnary
	"""
	gi=galaxyConnection(base_url,apiKey)
	#~ if a new user add all the workflow
	logger.info("##########################")
	logger.info("mainPlasma for "+expDict["resultsName"])
	logger.info("##########################")	

	historyID=Create_History(gi,"_Samtools_"+expDict["resultsName"])
	#~ Uploads data to a specific history
	#~ upload_To_History_Plasma_NGS_data(gi,expDict,str(historyID['id']),inputDataFolder)
	upload_To_History_Samtools_NGS_data(gi,expDict,str(historyID['id']),inputDataFolder)
	logger.info("##########################")
	logger.info("mupload_From_Library_To_Plasma_History :")
	logger.info("##########################")		
	#~ upload_From_Library_To_Plasma_History(gi,expDict,str(historyID['id']),"/Plasma/")
	#~ Retrieve the current history and build a 
	#~ a dictionnary of the recent Uploaded data
	
##############################################
	dataPlasmaID=Samtools_Input_Dict(gi,str(historyID['id']))
	Run_Samtools_Workflow(gi,dataPlasmaID,str(historyID['id']))
	logger.info("job done, hydrate yourself")
	return(historyID)
##############################################
#~ Uploads data to a specific history for NGS data
##############################################



def mainPlasma_fromNGSData(expDict,base_url,apiKey,inputDataFolder):
	""" 
	mainPlasma_fromNGSData(expDict,base_url,apiKey)
	returns (historyID)
	
	**Descriptions**:
	
	This function execute the CNV routine. From a run of the Ion Proton,
	The routine will connect the user to Galaxy, create an history,
	upload the CNV input files to it and run the CNV workflow.
	
	**Parameters**:
	
        :param expDict: a dictionnary output from ProtonCommunication_data_manager.copyData().
        :param base_url: an url which point to your galaxy instance 
        :param apiKey: a valid galaxy API key
        :type base_url: string
        :type apiKey: string
        :returns historyID: the galaxy history where the data and the CNV run are located
        :rtype historyID: a dictionnary
	"""
	gi=galaxyConnection(base_url,apiKey)
	#~ if a new user add all the workflow
	logger.info("##########################")
	logger.info("mainPlasma for "+expDict["resultsName"])
	logger.info("##########################")	

	historyID=Create_History(gi,"_PLASMA_"+expDict["resultsName"])
	#~ Uploads data to a specific history
	upload_To_History_Plasma_NGS_data(gi,expDict,str(historyID['id']),inputDataFolder)
	logger.info("##########################")
	logger.info("mupload_From_Library_To_Plasma_History :")
	logger.info("##########################")		
	#~ upload_From_Library_To_Plasma_History(gi,expDict,str(historyID['id']),"/Plasma/")
	#~ Retrieve the current history and build a 
	#~ a dictionnary of the recent Uploaded data
	
##############################################
	dataPlasmaID=Plasma_Input_Dict(gi,str(historyID['id']))
	Run_Plasma_Workflow(gi,dataPlasmaID,str(historyID['id']))
	logger.info("job done, hydrate yourself")
	return(historyID)
##############################################
#~ Uploads data to a specific history for NGS data
##############################################
def upload_To_History_Samtools_NGS_data(galaxyWeb,expDict,historyID,analysisType):
	""" 
	upload_To_History_Plasma(galaxyWeb,expDict,historyID)
	returns (int)
	
	**Descriptions**:
	
	This function upload to a specific history the CNV data.

	**Parameters**:
	
        :param galaxyWeb: a connection to your galaxy instance 
        :type galaxyWeb: GalaxyInstance
        :param expDict: a result dictionnary output from the ProtonCommunication script
        :type expDict: dictionnary
        :param historyID: a galaxy history ID
        :type historyID: string
        :returns: 1
        :rtype: int   
	"""
	logger.info("##########################")
	logger.info("upload_To_History_Plasma() for "+expDict["resultsName"])
	logger.info("##########################")		
	for bampath in expDict['bamForPlasma']:		
		galaxyWeb.tools.upload_file(path=bampath,history_id=historyID,file_type='bam',dbkey="hg19")
		ionTagnobam=str("".join(str(bampath.split("/")[-1]).split(".")[0]))
		absPath=bampath.split("/")
		outputtxt = open("/".join(absPath[0:len(absPath)-1])+"/"+ionTagnobam+".txt",'w')
		if ionTagnobam in expDict: 
			outputtxt.write(expDict[str(ionTagnobam)])
		else:
			outputtxt.write(str(ionTagnobam))
		outputtxt.close()
		logger.debug("##########################")
		logger.debug("bampath "+bampath)
		logger.debug("ionTagnobam "+ionTagnobam)
		logger.debug("##########################")				
		#~ galaxyWeb.tools.upload_file(path="/".join(absPath[0:len(absPath)-1])+"/"+ionTagnobam+".txt",history_id=historyID,file_type='txt',dbkey="hg19plasma")
	return 1
	
	

def upload_To_History_Plasma_NGS_data(galaxyWeb,expDict,historyID,analysisType):
	""" 
	upload_To_History_Plasma(galaxyWeb,expDict,historyID)
	returns (int)
	
	**Descriptions**:
	
	This function upload to a specific history the CNV data.

	**Parameters**:
	
        :param galaxyWeb: a connection to your galaxy instance 
        :type galaxyWeb: GalaxyInstance
        :param expDict: a result dictionnary output from the ProtonCommunication script
        :type expDict: dictionnary
        :param historyID: a galaxy history ID
        :type historyID: string
        :returns: 1
        :rtype: int   
	"""
	logger.info("##########################")
	logger.info("upload_To_History_Plasma() for "+expDict["resultsName"])
	logger.info("##########################")		
	for bampath in expDict['bamForPlasma']:		
		galaxyWeb.tools.upload_file(path=bampath,history_id=historyID,file_type='bam',dbkey="hg19plasma")
		ionTagnobam=str("".join(str(bampath.split("/")[-1]).split(".")[0]))
		absPath=bampath.split("/")
		outputtxt = open("/".join(absPath[0:len(absPath)-1])+"/"+ionTagnobam+".txt",'w')
		if ionTagnobam in expDict: 
			outputtxt.write(expDict[str(ionTagnobam)])
		else:
			outputtxt.write(str(ionTagnobam))
		outputtxt.close()
		logger.debug("##########################")
		logger.debug("bampath "+bampath)
		logger.debug("ionTagnobam "+ionTagnobam)
		logger.debug("##########################")				
		galaxyWeb.tools.upload_file(path="/".join(absPath[0:len(absPath)-1])+"/"+ionTagnobam+".txt",history_id=historyID,file_type='txt',dbkey="hg19plasma")
	return 1

##############################################
#~ Uploads data to a specific history
##############################################
def upload_To_History_Plasma(galaxyWeb,expDict,historyID,analysisType):
	""" 
	upload_To_History_Plasma(galaxyWeb,expDict,historyID)
	returns (int)
	
	**Descriptions**:
	
	This function upload to a specific history the CNV data.

	**Parameters**:
	
        :param galaxyWeb: a connection to your galaxy instance 
        :type galaxyWeb: GalaxyInstance
        :param expDict: a result dictionnary output from the ProtonCommunication script
        :type expDict: dictionnary
        :param historyID: a galaxy history ID
        :type historyID: string
        :returns: 1
        :rtype: int   
	"""
	logger.info("##########################")
	logger.info("upload_To_History_Plasma() for "+expDict["resultsName"])
	logger.info("##########################")		
	for bampath in expDict['bamForPlasma']:		
		galaxyWeb.tools.upload_file(path=bampath,history_id=historyID,file_type='bam',dbkey="hg19plasma")
		ionTagnobam=str("".join(str(bampath.split("/")[-1]).split(".")[0]))
		logger.debug("##########################")
		logger.debug("bampath "+bampath)
		logger.debug("ionTagnobam "+ionTagnobam)
		logger.debug("##########################")				
		galaxyWeb.tools.upload_file(path="/nas_Dir/INPUT/"+expDict["resultsName"]+analysisType+ionTagnobam+".txt",history_id=historyID,file_type='txt',dbkey="hg19plasma")
	
	return 1


##############################################
#~ Uploads data to a specific history
##############################################
def upload_From_Library_To_Plasma_History(galaxyWeb,expDict,historyID,analysisType):
	""" 
	upload_To_History_Plasma(galaxyWeb,expDict,historyID)
	returns (int)
	
	**Descriptions**:
	
	This function upload to a specific history the CNV data.

	**Parameters**:
	
        :param galaxyWeb: a connection to your galaxy instance 
        :type galaxyWeb: GalaxyInstance
        :param expDict: a result dictionnary output from the ProtonCommunication script
        :type expDict: dictionnary
        :param historyID: a galaxy history ID
        :type historyID: string
        :returns: 1
        :rtype: int   
	"""
	logger.info("##########################")
	logger.info("try to found the temporary library" )
	logger.info("##########################")
	#if the library does not exist, create a tmp library
	today = datetime.date.today()
	mytmpLibrary=galaxyWeb.libraries.get_libraries(str(today)+"temporarylibrary_"+expDict["resultsName"])
	myuploadfolder=""
	if mytmpLibrary == [] :
		mytmpLibrary=galaxyWeb.libraries.create_library(name=str(today)+"temporarylibrary_"+expDict["resultsName"],
		description="use to load link easily the data to galaxy")
		myuploadfolder=galaxyWeb.libraries.create_folder(str(mytmpLibrary["id"]),"_PLASMA_"+expDict["resultsName"])[0]
	else:
		myuploadfolder=galaxyWeb.libraries.create_folder(str(mytmpLibrary["id"]),"_PLASMA_"+expDict["resultsName"])[0]

	logger.info("##########################")
	logger.info("Upload all the file into the temporarylibrary as symbolic link" )
	logger.info("##########################")
	
	simpleBamName=[]
	for bampath in expDict['bamForPlasma']:
		galaxyWeb.libraries.upload_from_galaxy_filesystem(library_id=str(mytmpLibrary["id"]),folder_id=str(myuploadfolder['id']),
		filesystem_paths=bampath,file_type='bam',dbkey="hg19plasma",link_data_only='link_to_files')
		ionTagnobam=str("".join(str(bampath.split("/")[-1]).split(".")[0]))
		simpleBamName.append(ionTagnobam+".bam")
		simpleBamName.append(ionTagnobam+".txt")
		galaxyWeb.libraries.upload_from_galaxy_filesystem(library_id=str(mytmpLibrary["id"]),folder_id=str(myuploadfolder['id']),
		filesystem_paths="/nas_Dir/INPUT/"+expDict["resultsName"]+analysisType+ionTagnobam+".txt",file_type='txt',dbkey="hg19plasma",link_data_only='link_to_files')		
		

	logger.info("##########################")
	logger.info("add all the data into the history" )
	logger.info("##########################")
	for data in galaxyWeb.libraries.show_library(library_id=str(mytmpLibrary["id"]),contents=True):
		if str(data['name']).split("/")[-1] in simpleBamName:
			galaxyWeb.histories.upload_dataset_from_library(history_id=historyID,
			lib_dataset_id=str(data['id']))
			
	return 1


##############################################
#~ Retrieve the current history and build a 
#~ a dictionnary of the recent Uploaded data
##############################################
def Plasma_Input_Dict(galaxyWeb,historyID):
	""" 
	Plasma_Input_Dict(galaxyWeb,historyID)
	returns (data_Input_CNVID)
	
	**Descriptions**:
	
	This function return a dictionnary whitch contains datasets id for 
	Plasma input files. This dictionnary contains a bcsummary and bcmatrix keys.
	
	**Parameters**:
	
        :param galaxyWeb: a connection to your galaxy instance 
        :type galaxyWeb: GalaxyInstance
        :param historyID: a galaxy history ID
        :type historyID: string
        :returns: data_Input_CNVID
        :rtype: dictionnary   
	"""	

	logger.info("##########################")
	logger.info("Plasma_Input_Dict() for "+historyID)
	logger.info("##########################")
	idPlasmalist=[]
	plasmadicttxt=dict()
	plasmadictbam=dict()
	for dataset in galaxyWeb.histories.show_history(historyID,contents=True):
		print dataset["name"]
		patientkey=dataset["name"].split(".")[0]
		logger.debug("##########################")
		logger.debug("name "+dataset["name"])
		logger.debug("patientkey "+patientkey)
		logger.debug("##########################")
		newdict=dict()
		if dataset["name"].split(".")[1]=="bam":
			plasmadictbam[patientkey]=dataset["id"]
		else:
			plasmadicttxt[patientkey]=dataset["id"]
		idPlasmalist.append(dataset["id"])
	return({'bam':plasmadictbam,'txt':plasmadicttxt})

def Samtools_Input_Dict(galaxyWeb,historyID):
	""" 
	Samtools_Input_Dict(galaxyWeb,historyID)
	returns (data_Input_CNVID)
	
	**Descriptions**:
	
	This function return a dictionnary whitch contains datasets id for 
	Plasma input files. This dictionnary contains a bcsummary and bcmatrix keys.
	
	**Parameters**:
	
        :param galaxyWeb: a connection to your galaxy instance 
        :type galaxyWeb: GalaxyInstance
        :param historyID: a galaxy history ID
        :type historyID: string
        :returns: data_Input_CNVID
        :rtype: dictionnary   
	"""	

	logger.info("##########################")
	logger.info("Samtools_Input_Dict() for "+historyID)
	logger.info("##########################")
	idPlasmalist=[]
	plasmadicttxt=dict()
	plasmadictbam=dict()
	for dataset in galaxyWeb.histories.show_history(historyID,contents=True):
		print dataset["name"]
		patientkey=dataset["name"].split(".")[0]
		logger.debug("##########################")
		logger.debug("name "+dataset["name"])
		logger.debug("patientkey "+patientkey)
		logger.debug("##########################")
		newdict=dict()
		if dataset["name"].split(".")[1]=="bam":
			plasmadictbam[patientkey]=dataset["id"]
		idPlasmalist.append(dataset["id"])
	return({'bam':plasmadictbam})







##############################################
#~ Retrieve the Plasma workflow and execute it
##############################################
def Run_Samtools_Workflow(galaxyWeb,data_Input_PLASMAID,historyID):
	""" 
	Run_Plasma_Workflow(galaxyWeb,data_Input_PLASMAID,historyID)
	returns (int)
	
	**Descriptions**:
	
	This function retrieve the CNV workflow and execute it. Use a dictionnary
	as input.
	
	**Parameters**:
	
        :param galaxyWeb: a connection to your galaxy instance 
        :type galaxyWeb: GalaxyInstance
        :param data_Input_CNVID: a dictionnary output from function CNV_Input_Dict
        :type data_Input_CNVID: dictionnary
        :param historyID: a galaxy history ID
        :type historyID: string
        :returns: 1
        :rtype: int   
	"""
	logger.info("##########################")
	logger.info("Run_Samtools_Workflow() for "+historyID)
	logger.info("##########################")	
	PlasmaworkflowID=""
	for workflow in galaxyWeb.workflows.get_workflows():
		if "demo_samtools" in workflow["name"]:
			PlasmaworkflowID=workflow['id']
			logger.debug("##########################")
			logger.debug("Workflow ID found "+PlasmaworkflowID)
			logger.debug("##########################")				
	Plasma_Workflow=galaxyWeb.workflows.show_workflow(PlasmaworkflowID)
	#~ cnv_Workflow['inputs']['1']['label']
	inputWorkflow=dict()
	for bamName,historyidBam in data_Input_PLASMAID['bam'].iteritems():
		for key,value in Plasma_Workflow['inputs'].iteritems():
			#~ print key
			if ("bam file" in value['label']):
				inputWorkflow[key]= { 'src':'hda', 'id': historyidBam }
				logger.debug("##########################")
				logger.debug("inputWorkflow[key] "+str(inputWorkflow[key]))
				logger.debug("[key] "+str(key))
				logger.debug("##########################")					

				#~#Run a plasma analysis for each bam 
		galaxyWeb.workflows.invoke_workflow(PlasmaworkflowID, inputs=inputWorkflow,history_id=historyID)
	return(1)
	
##############################################
#~ Retrieve the Plasma workflow and execute it
##############################################
def Run_Plasma_Workflow(galaxyWeb,data_Input_PLASMAID,historyID):
	""" 
	Run_Plasma_Workflow(galaxyWeb,data_Input_PLASMAID,historyID)
	returns (int)
	
	**Descriptions**:
	
	This function retrieve the CNV workflow and execute it. Use a dictionnary
	as input.
	
	**Parameters**:
	
        :param galaxyWeb: a connection to your galaxy instance 
        :type galaxyWeb: GalaxyInstance
        :param data_Input_CNVID: a dictionnary output from function CNV_Input_Dict
        :type data_Input_CNVID: dictionnary
        :param historyID: a galaxy history ID
        :type historyID: string
        :returns: 1
        :rtype: int   
	"""
	logger.info("##########################")
	logger.info("Run_Plasma_Workflow() for "+historyID)
	logger.info("##########################")	
	PlasmaworkflowID=""
	for workflow in galaxyWeb.workflows.get_workflows():
		if "Plasma_mutation" in workflow["name"]:
			PlasmaworkflowID=workflow['id']
			logger.debug("##########################")
			logger.debug("Workflow ID found "+PlasmaworkflowID)
			logger.debug("##########################")				
	Plasma_Workflow=galaxyWeb.workflows.show_workflow(PlasmaworkflowID)
	#~ cnv_Workflow['inputs']['1']['label']
	inputWorkflow=dict()
	for bamName,historyidBam in data_Input_PLASMAID['bam'].iteritems():
		for key,value in Plasma_Workflow['inputs'].iteritems():
			#~ print key
			if ("plasmabam" in value['label']):
				inputWorkflow[key]= { 'src':'hda', 'id': historyidBam }
				logger.debug("##########################")
				logger.debug("inputWorkflow[key] "+str(inputWorkflow[key]))
				logger.debug("[key] "+str(key))
				logger.debug("##########################")					
			else:
				inputWorkflow[key]= { 'src':'hda', 'id':  data_Input_PLASMAID['txt'][bamName] }
				logger.debug("##########################")
				logger.debug("inputWorkflow[key] "+str(inputWorkflow[key]))
				logger.debug("[key] "+str(key))
				logger.debug("##########################")
				#~#Run a plasma analysis for each bam 
		galaxyWeb.workflows.invoke_workflow(PlasmaworkflowID, inputs=inputWorkflow,history_id=historyID)
	return(1)

if __name__ == "__main__":
	src_files = os.listdir(inputAbsolutPath)
	mainCNV(src_files,galaxy_base_url,apiKey)
