import os,datetime,sys,json
from datamanagerpkg import ProtonCommunication_data_manager
from datamanagerpkg import GalaxyCommunication_data_manager
from sequencer.models import Experiments, GalaxyUsers ,savedNGSData
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
from GlobalVariables import nasBackupFolder
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
from sequencer.localFunctions import buildSampleNameDict,buildBamDict

today = datetime.date.today()
#~ nasbackup=nasBackupFolder+'/backupNGS_new'
nasbackup=nasBackupFolder
#~ print(os.path.isdir("/home/el"))
#faire se travail avec un fichier texte 
#plutot quavec 
#~ nasbackup=nasBackupFolder+'/backupNGS_new'
checkThisFolder=open(nasbackup+"/"+str(today)+"_NotCompleteDownloadFolder.txt","w")
for runfolder in os.listdir(nasbackup):
	print("treat "+runfolder)
	print('treat experiment')
	print(nasbackup+"/"+runfolder+"/CompletedDownload.txt")
	print(os.path.exists(nasbackup+"/"+runfolder+"/CompletedDownload.txt"))
	if(os.path.exists(nasbackup+"/"+runfolder+"/CompletedDownload.txt")):
		print "find an obect"
		try:
			thisNGSData = savedNGSData.objects.get(filesystempath=str(nasbackup)+"/"+runfolder.rstrip())
		except savedNGSData.DoesNotExist:
			thisNGSData = None
		if  thisNGSData == None: 
			thisNGSData = savedNGSData.objects.create(
			filesystempath=str(nasbackup)+"/"+runfolder.rstrip(),
			folder_name=runfolder.rstrip(),
			status="complete")
			thisNGSData.save()
			thisNGSData.dataDictionnary=json.dumps(buildSampleNameDict(thisNGSData.folder_name))
			thisNGSData.save()  
			buildBamDict(thisNGSData)
	else:
		print "check this folder"+runfolder



checkThisFolder.close()
