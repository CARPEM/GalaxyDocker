#!/usr/bin/env python
"""The module ProtonCommunication_data_manager.py was
designed to be able to connect to the HEGP Ion Proton and
copy Data easily. It can be used with GalaxyCommunication_data_manager.py which
assure the Data-Manager_Galaxy Job routine.

This script use the The Torrent Suite Software Development Kit
to communicate with the Ion Proton.
ProtonCommunication_data_manager fullfill three main goals:
- retrieve the Data
- Select the data you want to use
- Copy them throught the network 
"""
import json
import requests
from pprint import pprint
import paramiko
from scp import SCPClient
import os
import logging
import subprocess

##########################
#URL SEQUENCER
##########################
from GlobalVariables import sequencer_base_url 
from GlobalVariables import sequencer_user
from GlobalVariables import sequencer_password
from GlobalVariables import sequencer_severName
from GlobalVariables import sequencer_ExperimentLimit

__license__ = "grou "
__revision__ = " $Id: Main_data_manager.py 1586 2016-08-10 15:56:25 $"
__docformat__ = 'reStructuredText'
__author__ = 'William Digan, CARPEM'
#~ first function (retrieve the last experiment and the file name)
#~ second function ( find the data to download)
#~ third function ( download data)
logger = logging.getLogger(__name__)

def CheckExperiments(nb_limit,iduser,idpwd,base_url):
	"""
	CheckExperiments(nb_limit,iduser,idpwd,base_url)
	returns (dictionnary)
	
	**Descriptions**:
	
	This function aims to return a dictionnary, which contains the 'n'
	 last experiments. It also return the run status and if the run is Complete or not.
	 For that purpose you need to provide the following parameters.

	**Parameters**:
	
        :param nb_limit: the 'n' number of experiments to check out
        :param iduser: the user ID to connect to the proton
        :param idpwd: the user password to connect to the proton 
        :param base_url: the Ion Proton URL
        :type nb_limit: int
        :type iduser: string
        :type idpwd: string
        :type base_url: string
        :returns: dict
        :rtype: dict 
	 
	
	       This function retrieve the n last experiment of the Ion Proton.
	       it returns a dictionnary which contains 5 elements.
	       {RunName: {cnvFileName;status;ftpStatus;date;id;resultsQuery}}

			       
	     .. note:: Dictionnary structure: {RunName: {cnvFileName;status;ftpStatus;date;id;resultsQuery}}
          - RunName : the experiments run name
          - cnvFileName : the sting match for the bcsummary and bcmatrix file
          - status :  run status either 'pending' or 'run'
          - ftpStatus : if the data can be download, either 'Complete' or ''
          - date : project date
          - id : project id in the ion proton
          - resultsQuery: astring to the result folder `
	"""
	##############################################
	##############################################
	logger.info("##########################")
	logger.info("CHECK PARAMETERS")
	logger.info("##########################")
	logger.debug("CheckExperiments()")
	logger.debug("nb_limit:  %s",nb_limit)
	logger.debug("iduser:  %s",iduser)
	logger.debug("idpwd:  %s",idpwd)
	logger.debug("base_url:  %s",base_url)
	logger.debug("##########################")

	logger.info("START REQUEST")
	resp = requests.get(base_url+'/experiment/', auth=(iduser,idpwd), params={"format": "json", "limit": nb_limit,"order_by" : "-date"})
	#~ #will contains results folder name
	resultFolder=""
	CNVfile=""
	resp_json = resp.json()
	#~ logger.debug("Print REQUEST :\n %s",pprint(resp_json))
	experiments=dict()
	logger.info("##########################")
	logger.info("START LOOP AROUND REQUEST")
	logger.info("##########################")
	
	for item in resp_json['objects']:
		logger.debug("##########################")
		logger.debug("displayName:  %s",item['displayName'])
		logger.debug("expName:  %s",item['expName'])
		logger.debug("##########################\n")
		currentExp=dict()
		currentExp['cnvFileName']=str(item['expName'])+"_"
		currentExp['status']=item['status']
		currentExp['ftpStatus']=item['ftpStatus']
		currentExp['date']=item['date']  
		currentExp['id']= item['id'] 
		currentExp['resultsQuery']= str(item['displayName']).replace(" ","_")+"_"+ str(item['id'])
		experiments[item['expName']]=currentExp   
#~ #return a dictionnary
	logger.info("##########################")
	logger.info("RETURN RESULT DICTIONNARY")
	logger.info("##########################")
	logger.debug("experiments:  %s",str(experiments))
	return(experiments)   

##############################################
#~ Find the result folder absolut path
#~ query on the result api
#~ return also a dictionnary and add the filesystempath to the dict
##############################################
def QueryResults(resultsQuery,cnvFileName,iduser,idpwd,base_url):
	"""
	QueryResults(resultsQuery,idpwd,base_url)
	returns (dictionnary)
	
	**Descriptions**:
	
	This function find the result folder absolut path associated to an
	identified resultsQuery. it returns a dictionnary 
	and add the filesystempath to the current dictionnary.

	**Parameters**:
	
        :param resultsQuery: a string resultsQuery output from CheckExperiments() 
        :param iduser: the user ID to connect to the proton
        :param idpwd: the user ID to connect to the proton(To add) 
        :param base_url: the Ion Proton URL
        :type expDict: dict
        :type iduser: string
        :type idpwd: string
        :type base_url: string
        :returns: dict
        :rtype: dict 

	       This function retrieve the result path associated with an
	        experiments name from the Ion Proton.
	       it returns a dictionnary which contains 2 new elements
	        from the current dictionnary.
	       {RunName: {cnvFileName;resultsName;runPath;}}    
	       
	     .. note:: Dictionnary structure: {RunName: {resultsName;runPath;cnvFileName}}
          - resultsName; : the experiments result name
          - runPath : the path to the current result folder in the Ion Proton
	"""	
	##############################################
	##############################################
	logger.info("##########################")
	logger.info("CHECK PARAMETERS")
	logger.info("##########################")
	logger.debug("QueryResults()")
	logger.debug("resultsQuery:  %s",resultsQuery)
	logger.debug("cnvFileName:  %s",cnvFileName)
	logger.debug("iduser:  %s",iduser)
	logger.debug("idpwd:  %s",idpwd)
	logger.debug("base_url:  %s",base_url)
	logger.debug("##########################")

	logger.info("START REQUEST")	
	#~ for key,currentExp in expDict.iteritems():
	resultsPath=dict()
	#~ resp = requests.get(base_url+'/results/', auth=(idpr,idpr),params={"format": "json", "resultsName__endswith" : "r'*"+resultFolder+"'"})
	resp = requests.get(base_url+'/results/', auth=(iduser,idpwd),params={"format": "json", "resultsName__endswith" : resultsQuery})
	resp_json = resp.json()
	logger.info("##########################")
	logger.info("START LOOP AROUND REQUEST")
	logger.info("##########################")
		
	for item in resp_json['objects']:
		logger.info("##########################")
		logger.debug("resultsName:  %s",str(item['resultsName']))
		logger.info("runPath:  %s",str(item['filesystempath']))
		logger.info("##########################\n")
		
		resultsPath['resultsName']=str(item['resultsName'])
		resultsPath['cnvFileName']=cnvFileName+ str(item['resultsName'])
		resultsPath['runPath']=str(item['filesystempath'])
	logger.info("##########################")
	logger.info("RETURN RESULT DICTIONNARY")
	logger.info("##########################")
	logger.debug("resultsPath:  %s",str(resultsPath))
	return(resultsPath)

##############################################
#~ establish an ssh connection
##############################################
def sshConnection(severName,iduser,idpwd):
	"""
	sshConnection(severName,idpwd)
	returns (sshConnection)
	
	**Descriptions**:
	
	This function allow an ssh connection through the  pakito python module.
	the goal here is to establish a connection before performed an scp bash
	command.

	**Parameters**:
        :param severName: name of the linux machine to connect throught ssh
        :param iduser: the user ID to connect to the proton
        :param idpwd: the user password to connect to the proton
        :type severName: string
        :type iduser: string
        :type idpwd: string
        :returns: sshConnection
        :rtype: sshConnection 
	"""
	logger.info("##########################")
	logger.info("CHECK PARAMETERS")
	logger.info("##########################")
	logger.debug("sshConnection()")
	logger.debug("severName:  %s",severName)
	logger.debug("iduser:  %s",iduser)
	logger.debug("idpwd:  %s",idpwd)
	logger.debug("##########################")

	logger.info("Define an ssh connection")
	
	sshConnection = paramiko.SSHClient()
	logger.info("Allow connection to an external server")
	
	sshConnection.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
	logger.info("ssh connection to the server")
	
	sshConnection.connect(severName, username=iduser, password=idpwd)
	logger.info("##########################")
	logger.info("RETURN ssh connection")
	logger.info("##########################")
	return(sshConnection)

##############################################
#~ check data consistency before Performed a
#~  scp cmd. 
#~ if I need to add more quality control around the data
#~ do it here
##############################################
def CheckResConsistency(expDict,ssh):
	"""
	CheckResConsistency(expDict,ssh)
	returns (dictionnary)
	
	**Descriptions**:
	
	This function  check data consistency for one dictionnary before performed a scp command.
	Quality control need to be handle in this function. add a key coverageAnalysis_out
	which point to the right folder coverageAnalysis_out which contains the bed file ColonLungV2.20140523

	**Parameters**:
	
        :param expDict: a dictionnary output from QueryResults() 
        :param ssh: sshConnection from sshConnection()
		:type expDict: dict
        :type ssh: sshConnection
        :returns: dict
        :rtype: dict 
	"""	
	logger.info("##########################")
	logger.info("CHECK PARAMETERS")
	logger.info("##########################")
	logger.debug("CheckResConsistency()")
	logger.debug("expDict:  %s",str(expDict))
	logger.debug("ssh:  %s",ssh)
	logger.debug("##########################")


	logger.info("##########################")
	logger.info("#SEARCH BAM FILE PATH")
	ssh_stdin_bam, ssh_coverageAnalysis_stdout_bam, ssh_stderr_bam = ssh.exec_command(" ls "+expDict['runPath']+"/download_links/IonXpress*bam")
	bamfileList=[]
	for bamfile in ssh_coverageAnalysis_stdout_bam.readlines() :
		logger.debug("##########################")
		logger.debug("bamfile:  %s",bamfile)
		logger.debug("##########################")
		bamfileList.append(str(bamfile.rstrip()))

	expDict['BAM_FILES']=bamfileList

	logger.info("##########################")
	logger.info("SEARCH COVERAGE ANALYSIS FILE")
	ssh_stdin, ssh_coverageAnalysis_stdout, ssh_stderr = ssh.exec_command(" find "+expDict['runPath']+"/plugin_out -name 'coverageAnalysis_out*'")
	#~ #In some cases the coverage Analysis folder do no exist  or the Bed is different?
	#~ #I have to treat this situation.
	workdone=False
	for folder in ssh_coverageAnalysis_stdout.readlines() :
		logger.debug("##########################")
		logger.debug("folder:  %s",folder)
		logger.debug("##########################")
		ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("ls "+folder.rstrip()+"/local_beds/")
		
		for bed in ssh_stdout.readlines():
			#print bed + "bed file"
			expDict['coverageAnalysis_out']=folder.rstrip()
			workdone=True
			break
				
	logger.info("##########################")
	logger.info("RETURN THE DICTIONNARY")
	logger.info("##########################")
#~ build the link between sample an Iontag
	if workdone==True:
		mysampleDict=dict()
		ssh_stdin, ssh_coverageAnalysis_stdout, ssh_stderr = ssh.exec_command(" cat "+expDict['coverageAnalysis_out']+'/'+expDict['cnvFileName']+".bc_summary.xls")
		for sample in ssh_coverageAnalysis_stdout.readlines() :
			print sample.split("\t")
			mysplit=sample.split("\t")
			mysampleDict[str(mysplit[0])]=str(str(mysplit[1]).replace(" ", "").upper())
			
		expDict['sampleKey']=	mysampleDict				
	return(expDict)

##############################################
#~ copy data trought scp and perform checksum 
##############################################
#need to add an argument which is file path
#~ resultDirPath=nas_Dir/INPUTS/
#~ analysisType=/BEDNAME/(CNV or SAFIR) or /PLASMA/
def copyDataCNV(currentExp,ssh,resultDirPath,analysisType):
#~ def copyDataCNV(currentExp,ssh):
	"""
	copyDataCNV(currentExp,ssh)
	returns (dictionnary)
	
	**Descriptions**:
	
	This function copy data trought scp and perform checksum. Add the key bcmatrix
	and bcsummary to the current directory. if some rename opperation need to be performed
	it as to been done here.
	
	**Parameters**:
	
        :param currentExp: a directory output from CheckResultsConsistency() 
        :param ssh: sshConnection from sshConnection()
        :type currentExp: dict
        :type ssh: sshConnection
        :returns: dict
        :rtype: dict 
	"""
	scp = SCPClient(ssh.get_transport())
	scp.get(currentExp['coverageAnalysis_out']+'/'+currentExp['cnvFileName']+".bcmatrix.xls",resultDirPath+currentExp['resultsName']+analysisType)
	scp.get(currentExp['coverageAnalysis_out']+'/'+currentExp['cnvFileName']+".bc_summary.xls",resultDirPath+currentExp['resultsName']+analysisType)
	currentExp['bcmatrix']=resultDirPath+currentExp['resultsName']+analysisType+currentExp['cnvFileName']+".bcmatrix.xls"
	currentExp['bcsummary']=resultDirPath+currentExp['resultsName']+analysisType+currentExp['cnvFileName']+".bc_summary.xls"
	scp.close()
	return(currentExp)
##############################################
#~ copy data trought scp and perform checksum 
#~ copyDataBam(currentExp,ssh,"/nas_Dir"+something)
##############################################
#need to add an argument which is file path
#~ resultDirPath=nas_Dir/INPUTS/
#~ analysisType=/BEDNAME/(CNV or SAFIR) or /PLASMA/
def copyDataBam(currentExp,bamtoDownload,ssh,resultDirPath,analysisType):
#~ def copyDataCNV(currentExp,ssh):
	"""
	copyDataBam(currentExp,ssh)
	returns (dictionnary)
	
	**Descriptions**:
	
	This function copy data trought scp and perform checksum. Add the key bcmatrix
	and bcsummary to the current directory. if some rename opperation need to be performed
	it as to been done here.
	
	**Parameters**:
	
        :param currentExp: a directory output from CheckResultsConsistency() 
        :param ssh: sshConnection from sshConnection()
        :type currentExp: dict
        :type ssh: sshConnection
        :returns: dict
        :rtype: dict 
	"""
	logger.info("##########################")
	logger.info("CHECK PARAMETERS")
	logger.info("##########################")
	logger.debug("copyDataBam()")
	scp = SCPClient(ssh.get_transport())
	pathToPlasmaBam=[]
	bammd5sum=dict()
	for bamPath in bamtoDownload:
		scp.get(str(bamPath),resultDirPath+currentExp['resultsName']+analysisType)
		ionTag=str("_".join(str(bamPath.split("/")[-1]).split("_")[0:2]))+".bam"
		ionTagnobam=str("_".join(str(bamPath.split("/")[-1]).split("_")[0:2]))
		#~ ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("md5sum "+str(bamPath))		
		#~ bammd5sum[ionTag]=str("_".join(ssh_stdout.readlines()).rstrip()).split(" ")[0]
		bammd5sum[ionTag]="gg"

		logger.debug("##########################")
		logger.debug("Bam File rename"+ionTag)
		logger.debug("path to bam " +resultDirPath+currentExp['resultsName']+analysisType+ionTag)
		#~ logger.debug(bammd5sum[ionTag])
		logger.debug("##########################")
		os.rename(resultDirPath+currentExp['resultsName']+analysisType+str(bamPath.split("/")[-1]),
		resultDirPath+currentExp['resultsName']+analysisType+ionTag)
		#~ bashCommand1 = "md5sum "+resultDirPath+currentExp['resultsName']+analysisType+ionTag
		#~ process1 = subprocess.Popen(bashCommand1.split(), stdout=subprocess.PIPE)
		#~ copybam=process1.communicate()[0].split(" ")[0]
		copybam="gg"
		filetowrite = open(resultDirPath+currentExp['resultsName']+analysisType+ionTagnobam+".txt", 'w')
		filetowrite.write(ionTagnobam)
		filetowrite.close()
		if (copybam==bammd5sum[ionTag]):
			bammd5sum[ionTag]=bammd5sum[ionTag]+";Valid;"+resultDirPath+currentExp['resultsName']+analysisType+ionTag
		else:
			bammd5sum[ionTag]=bammd5sum[ionTag]+";Corrupted;"+resultDirPath+currentExp['resultsName']+analysisType+ionTag
		#~ print copybam
		pathToPlasmaBam.append(resultDirPath+currentExp['resultsName']+analysisType+ionTag)
		
	json.dump(bammd5sum, open(resultDirPath+currentExp['resultsName']+analysisType+currentExp['resultsName']+"_bamReport.txt",'a'))
	currentExp['bamForPlasma']=pathToPlasmaBam
	currentExp['bammd5sum']=bammd5sum
	scp.close()
	return(currentExp)

##############################################
#~ copy data trought scp and perform checksum 
#~ return a dictionnary with the path to the file
##############################################
def mainGetCNVData(base_url,idpr,iduser,severName,experimentLimit) :
	print "##########################"
	print "Query Experiments\n"
	experimentsDict=CheckExperiments(experimentLimit,iduser,idpr,base_url) 
	print "##########################" 
	print "Find Results folder Path\n"
	experimentsDict=FindResults(experimentsDict,idpr,base_url)
	print "##########################" 
	print "Connect to the server "+	severName
	sshProton=sshConnection(severName,idpr,idpr)
	print "##########################" 
	print "check coverage data consistency "
	experimentsDict=CheckResultsConsistency(experimentsDict,sshProton) 
	print "##########################" 
	print "Copy data throught scp"
	for key,currentExp in experimentsDict.iteritems():
		if not os.path.exists("/nas_Dir/"+currentExp['resultsName']+"/CNV"):
			os.makedirs("/nas_Dir/"+currentExp['resultsName']+"/CNV")
			#~ copyData(currentExp,ssh,"/nas_Dir/"+currentExp['resultsName']+"/CNV")
		print "##########################" 
		print "Treat experiment "+key
		currentExp=copyDataCNV(currentExp,sshProton,"/nas_Dir/","/CNV")
	#~ do not forgot to close the ssh connection()    
	sshProton.close()
	return(experimentsDict)


##############################################
#~ Find the result folder absolut path
#~ query on the result api
#~ return also a dictionnary and add the filesystempath to the dict
##############################################
def FindResults(expDict,idpwd,base_url):
	"""
	FindResults(expDict,idpwd,base_url)
	returns (dictionnary)
	
	**Descriptions**:
	
	This function find the result folder absolut path. it retuns a dictionnary 
	and add the filesystempath to the current dictionnary.

	**Parameters**:
	
        :param expDict: a directory output from the the CheckExperiments() function
        :param idpwd: the user ID to connect to the proton
        :param idpwd: the user ID to connect to the proton(To add) 
        :param base_url: the Ion Proton URL
        :type expDict: dict
        :type idpwd: string
        :type idpwd: string
        :type base_url: string
        :returns: dict
        :rtype: dict 
	 
	       This function retrieve the result path associated with an
	        experiments name from the Ion Proton.
	       it returns a dictionnary which contains 2 new elements
	        from the current dictionnary.
	       {RunName: {resultsName;runPath;...}}

			       
	     .. note:: Dictionnary structure: {RunName: {resultsName;runPath;cnvFileName;status;ftpStatus;date;id;resultsQuery}}
          - resultsName; : the experiments result name
          - runPath : the path to the current result folder in the Ion Proton
	"""	
	for key,currentExp in expDict.iteritems():
		resp = requests.get(base_url+'/results/', auth=(idpwd,idpwd),params={"format": "json", "resultsName__endswith" : currentExp['resultsQuery']})
		resp_json = resp.json()
		for item in resp_json['objects']:
			#~ if item['status'] == "Completed":
			currentExp['resultsName']=str(item['resultsName'])
			currentExp['cnvFileName']=currentExp['cnvFileName']+ str(item['resultsName'])
			currentExp['runPath']=str(item['filesystempath'])
	return(expDict)   
	
	
def CheckResultsConsistency(expDict,ssh):
	"""
	CheckResultsConsistency(expDict,ssh)
	returns (dictionnary)
	
	**Descriptions**:
	
	This function  check data consistency for a a dict of dictionnary before performed a scp command.
	Quality control need to be handle in this function. add a key coverageAnalysis_out
	which point to the right folder coverageAnalysis_out which contains the bed file ColonLungV2.20140523

	**Parameters**:
	
        :param expDict: a dictionnary output from QueryResults() 
        :param ssh: sshConnection from sshConnection()
		:type expDict: dict
        :type ssh: sshConnection
        :returns: dict
        :rtype: dict 
	"""	
	for key,currentExp in expDict.iteritems():
		ssh_stdin, ssh_coverageAnalysis_stdout, ssh_stderr = ssh.exec_command(" find "+currentExp['runPath']+"/plugin_out -name 'coverageAnalysis_out*'")
		#~ rightcoverageAnalysis_out=""
		for folder in ssh_coverageAnalysis_stdout.readlines() :
			print folder.rstrip()
			ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("ls "+folder.rstrip()+"/local_beds/")
			for bed in ssh_stdout.readlines():
				#print bed + "bed file" 
				if "ColonLungV2.20140523" in bed:
					print "right folder found"
					#~ rightcoverageAnalysis_out=folder.rstrip()
					currentExp['coverageAnalysis_out']=folder.rstrip()
	return(expDict)
	
	



##############################################
#~ copy data trought scp and perform checksum 
#~ copyDataBam(currentExp,ssh,"/nas_Dir"+something)
##############################################
#need to add an argument which is file path
#~ resultDirPath=nas_Dir/INPUTS/
#~ analysisType=/BEDNAME/(CNV or SAFIR) or /PLASMA/
def backgroundcopyDataBamtask(Expdict,currentExp,bamtoDownload,ssh,resultDirPath,analysisType):
#~ def copyDataCNV(currentExp,ssh):
	"""
	backgroundcopyDataBamtask(currentExp,ssh)
	returns (dictionnary)
	
	**Descriptions**:
	
	This function copy data trought scp and perform checksum. Add the key bcmatrix
	and bcsummary to the current directory. if some rename opperation need to be performed
	it as to been done here.
	
	**Parameters**:
	
        :param currentExp: a directory output from CheckResultsConsistency() 
        :param ssh: sshConnection from sshConnection()
        :type currentExp: dict
        :type ssh: sshConnection
        :returns: dict
        :rtype: dict 
	"""	
	logger.info("##########################")
	logger.info("CHECK PARAMETERS")
	logger.info("##########################")
	logger.debug("backgroundcopyDataBamtask()")
	scp = SCPClient(ssh.get_transport())
	pathToPlasmaBam=[]
	bammd5sum=dict()
	#for each bam to download.
	ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("md5sum "+Expdict['coverageAnalysis_out']+'/'+Expdict['cnvFileName']+".bc_summary.xls")
	scp.get(Expdict['coverageAnalysis_out']+'/'+Expdict['cnvFileName']+".bc_summary.xls",resultDirPath+Expdict['resultsName']+analysisType)
	bashCommand1 = "md5sum "+resultDirPath+Expdict['resultsName']+analysisType+'/'+Expdict['cnvFileName']+".bc_summary.xls"
	process1 = subprocess.Popen(bashCommand1.split(), stdout=subprocess.PIPE)
	#~ store the copy bam md5
	copybam=process1.communicate()[0].split(" ")[0]
	fileTagChecksum = open(resultDirPath+Expdict['resultsName']+analysisType+'/'+Expdict['cnvFileName']+"_checksum.txt", 'w')
	#~ CopyBamAgain(scp,copybam,bammd5sum[ionTag],fileTagChecksum,str(bamPath),resultDirPath+currentExp+analysisType+ionTag,ionTag)
	fileTagChecksum.write(Expdict['cnvFileName']+".bc_summary.xls"+ " COMPLETE " +copybam+"\n")
	fileTagChecksum.close()

	#~ Read the sumarry.xls file to have the proper sample name.
	mysampleDict=dict()
	summaryFile=open(resultDirPath+Expdict['resultsName']+analysisType+'/'+Expdict['cnvFileName']+".bc_summary.xls",'r') 
	for sample in summaryFile.readlines() :
		print sample.split("\t")
		mysplit=sample.split("\t")
		mysampleDict[mysplit[0]]=str(mysplit[1]).replace(" ", "").upper()
	
	for bamPath in bamtoDownload:
		scp = SCPClient(ssh.get_transport())
		ionTag=str("_".join(str(bamPath.split("/")[-1]).split("_")[0:2]))+".bam"
		ionTagkey=str("_".join(str(bamPath.split("/")[-1]).split("_")[0:2]))
		#~ if (os.path.exists(resultDirPath+currentExp+analysisType+ionTag) != True ):
		if (os.path.exists(resultDirPath+currentExp+analysisType+mysampleDict[ionTagkey]+".bam") != True ):
		#Perform the bamfile original checksum ando store  it in the bammd5sum dict
			ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("md5sum "+str(bamPath))
			#perform the data copy
			#~ //copy the data with thr right file name
			#~ scp.get(str(bamPath),resultDirPath+currentExp+analysisType+ionTag)
			scp.get(str(bamPath),resultDirPath+currentExp+analysisType+mysampleDict[ionTagkey]+".bam")
			#~ wait for n seconds)
			#~ while (os.path.exists(resultDirPath+currentExp+analysisType+ionTag) != True ):
			while (os.path.exists(resultDirPath+currentExp+analysisType+mysampleDict[ionTagkey]+".bam") != True ):
				logger.debug("##########################")
				logger.debug("wait for data to be downloaded")
				time.sleep(15) 
			ionTagnobam=str("_".join(str(bamPath.split("/")[-1]).split("_")[0:2]))
			#store the original bam md5
			bammd5sum[ionTag]=str("_".join(ssh_stdout.readlines()).rstrip()).split(" ")[0]
			#~ bammd5sum[ionTag]=tmporiginalbammd5sum
			logger.debug("##########################")
			#~ logger.debug("Bam File rename"+ionTag)
			#~ logger.debug("path to bam " +resultDirPath+currentExp+analysisType+ionTag)
			logger.debug("Bam File rename"+mysampleDict[ionTagkey])
			logger.debug("path to bam " +resultDirPath+currentExp+analysisType+mysampleDict[ionTagkey]+".bam")
			#~ logger.debug(bammd5sum[ionTag])
			logger.debug("##########################")				
			#~ run the MD5sum again the copy data
			#~ bashCommand1 = "md5sum "+resultDirPath+currentExp+analysisType+ionTag
			bashCommand1 = "md5sum "+resultDirPath+currentExp+analysisType+mysampleDict[ionTagkey]+".bam"
			process1 = subprocess.Popen(bashCommand1.split(), stdout=subprocess.PIPE)
			#~ store the copy bam md5
			copybam=process1.communicate()[0].split(" ")[0]	
			#~ fileTagChecksum = open(resultDirPath+currentExp+analysisType+ionTagnobam+"_checksum.txt", 'w')			

			fileTagChecksum = open(resultDirPath+currentExp+analysisType+mysampleDict[ionTagkey]+"_checksum.txt", 'w')			
			#~ CopyBamAgain(scp,copybam,bammd5sum[ionTag],fileTagChecksum,str(bamPath),resultDirPath+currentExp+analysisType+ionTag,ionTag)
			CopyBamAgain(scp,copybam,bammd5sum[ionTag],fileTagChecksum,str(bamPath),resultDirPath+currentExp+analysisType+mysampleDict[ionTagkey]+".bam",mysampleDict[ionTagkey]+".bam")
			filetowrite = open(resultDirPath+currentExp+analysisType+mysampleDict[ionTagkey]+".txt", 'w')
			#~ filetowrite.write(ionTagnobam)
			filetowrite.write(mysampleDict[ionTagkey])
			filetowrite.close()
			fileTagChecksum.close()
			#~ pathToPlasmaBam.append(resultDirPath+currentExp+analysisType+ionTag)
			pathToPlasmaBam.append(resultDirPath+currentExp+analysisType+mysampleDict[ionTagkey]+".bam")
		else:
			#~ pathToPlasmaBam.append(resultDirPath+currentExp+analysisType+ionTag)
			pathToPlasmaBam.append(resultDirPath+currentExp+analysisType+mysampleDict[ionTagkey]+".bam")			
			continue
		scp.close()			
	#END loop and close all port
	#~ writechecksum.close()
	newdict=dict()
	newdict['bamForPlasma']=pathToPlasmaBam
	newdict['bammd5sum']=bammd5sum
	#~ scp.close()
	return(newdict)
	

def CopyBamAgain(scp,copyBam_MD5,originalBam_MD5,outputFile_MD5,originalBamPath,copyBamBath,Tag):
	if(copyBam_MD5== originalBam_MD5) :
		outputFile_MD5.write(Tag+ " COMPLETE " +originalBam_MD5+"\n")
		return(1)
	else :
		#~ scp.get(str(bamPath),resultDirPath+currentExp['resultsName']+analysisType+ionTag)
		scp.get(originalBamPath,copyBamBath)
		#~ wait for n seconds)
		while (os.path.exists(copyBamBath) != True ):
			print "wait for data"
			time.sleep(15)
		CopyBamAgain(scp,copyBam_MD5,originalBam_MD5,outputFile_MD5,originalBamPath,copyBamBath,Tag)

if __name__ == '__main__':

	mainGetCNVData(sequencer_base_url,sequencer_password,sequencer_user,sequencer_severName,sequencer_ExperimentLimit)

	print "Sans audace pas de gloire"
	print "yippee A ki-yay !"

