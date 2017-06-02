#!/usr/bin/env python

from datamanagerpkg import ProtonCommunication_data_manager
import requests
import json
import pprint
import os
import paramiko
from scp import SCPClient
import subprocess
import time 
from shutil import copyfile	

##########################
#URL PROTON
##########################
from protonprojects.GlobalVariables import proton_base_url 
from protonprojects.GlobalVariables import idpr
from protonprojects.GlobalVariables import proton_severName
##########################
#URL GALAXY
##########################
from protonprojects.GlobalVariables import  galaxy_base_url
from protonprojects.GlobalVariables import  apiKey
##########################
#NAs DIr folder
##########################
from protonprojects.GlobalVariables import nasInput
from protonprojects.GlobalVariables import CNVfolderName
from protonprojects.GlobalVariables import PlasmafolderName
from protonprojects.GlobalVariables import nasResults
from protonprojects.GlobalVariables import nasBackupFolder
import logging
##########################
#LOGGER
##########################
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s -- %(name)s - %(levelname)s : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=logging.INFO,filename='/nas_backup/log_copybackupnew/backupNGS_new_run156A160.log')
#~ logging.basicConfig(format='%(asctime)s -- %(name)s - %(levelname)s : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=logging.INFO)

#logger.setLevel(logging.DEBUG)

#~ inputrun=open("/data/mybackup20161121.txt","r")
#~ inputrun=open("/data/mybackup20161208.txt","r")
#~ inputrun=open("/data/mybackup20161216.txt","r")
#~ inputrun=open("/data/mybackup20161219.txt","r")
#~ #start line 93
inputFileToProcess="/data/mybackup20170117.txt"
absolutpath="/results/analysis/output/Home"

def CopydataAgain(inputData,outputData,filetocopy,originalchecksum,checksumBam,iterationNumb,sshProton):
	print "input data rich a timeout socket exception will retry the job"
	print "filename:"+inputData
	print "outputdata:"+outputData
	if os.path.exists(outputData):
		os.remove(outputData)
	print "sleep 10 seconds and redo the experiment"
	time.sleep(10)
	if iterationNumb>10 :
		print "maximum iteration reach"
		return 1
	#scp.close()
	scp=SCPClient(sshProton.get_transport())		
	print("Copy Failed for "+filetocopy+"redo the operation in copydataAGAIN from"+str(iterationNumb))
	try:
		scp.get(inputData,outputData)
	except Exception:
		print "rich a timeout socket exceptionfrom CopyDATAAGAIN"
		scp.close()
		scp=SCPClient(sshProton.get_transport())		
		CopydataAgain(inputData,outputData,filetocopy,originalchecksum,checksumBam,iterationNumb+1,sshProton)
		
	jobdone=False
	while jobdone!=True:
		print "This prints once a 10. and wait for data"
		time.sleep(10) 
		jobdone=True
	bashCommand1 = "md5sum "+outputData
	process1 = subprocess.Popen(bashCommand1.split(), stdout=subprocess.PIPE)
	checksumData=process1.communicate()[0].split(" ")[0]
	if	(checksumData== originalchecksum) :
		checksumBam.write(filetocopy+ " COMPLETE " +str(originalchecksum)+"\n")
	else :
		scp.close()
		scp=SCPClient(sshProton.get_transport())			
		CopydataAgain(inputData,outputData,filetocopy,originalchecksum,checksumBam,iterationNumb+1,sshProton)

#get checksum for one file			
def getmd5sum(pathdodata,sshProton):

	ssh_stdin, ssh_md5sum_stdout, ssh_stderr = sshProton.exec_command(" md5sum "+pathdodata)
	bamchecksum=""
	originalFile=""
	for checksum in ssh_md5sum_stdout.readlines():
		bamchecksum=str(checksum.rstrip().split(" ")[0])
		originalFile=str(checksum.rstrip().split(" ")[1])
	return([bamchecksum,originalFile])
				
def doitformykey(key,thisAnalysis,data,checksumcov,sshProton,scp):
	bamchecksum,originalFile=getmd5sum(data[key],sshProton)
	print(bamchecksum)
	if os.path.exists(thisAnalysis+"/"+data[key].split("/")[-1]) :
		bashCommand1 = "md5sum "+thisAnalysis+"/"+data[key].split("/")[-1]
		process1 = subprocess.Popen(bashCommand1.split(), stdout=subprocess.PIPE)
		copybam=process1.communicate()[0].split(" ")[0]			
		print("Check copy")
		if	(copybam==bamchecksum) :
			print("COMPLETE")
			checksumcov.write(data[key].split("/")[-1]+ " COMPLETE " +str(bamchecksum)+"\n")
		else :
			CopydataAgain(data[key],thisAnalysis,data[key].split("/")[-1],bamchecksum,checksumcov,1,sshProton)			

	else:
		try :
			scp.get(data[key],thisAnalysis)	
		except Exception: 
			print "this file failed to upload"+str(thisAnalysis)
			#failedFileToREDO.write("this file failed to upload :"+str(thisAnalysis)+"/"+data['bcmatrix'].split("/")[-1]+"\t"+str(bamchecksum)+"\n")
			scp.close()
			scp=SCPClient(sshProton.get_transport())
			CopydataAgain(data[key],thisAnalysis,data[key].split("/")[-1],bamchecksum,checksumcov,1,sshProton)			
			scp.close()
		jobdone=False
		while jobdone!=True:
			print "This prints once a 10sec. and wait for data"
			time.sleep(10) 
			jobdone=True
				

def buildcoverageAnalysisFile(sshProton,runNametobackup):	
	logger.debug("##########################")
	logger.debug("list coverageAnalysis folder")
	logger.debug("##########################")
	coverageAnalysisDict=dict()
	ssh_stdin, ssh_coverageAnalysis_stdout, ssh_stderr = sshProton.exec_command(" find "+absolutpath+"/"+runNametobackup.rstrip()+"/plugin_out -name 'coverageAnalysis_out*'")
	coverageAnalysisfolder=[]#contains coverage analysis folder
	for strfile in ssh_coverageAnalysis_stdout.readlines() :
		coverageAnalysisfolder.append(str(strfile.rstrip()))
		
	#~ #coverageAnalysisDict=dict()
	logger.debug("##########################")
	logger.debug("files to copy from coverageAnalysis")
	logger.debug("*.bcmatrix.xls,*.bc_summary.xls,startplugin.json,results.json")
	logger.debug("##########################")
	experiment_name=runNametobackup.rstrip()
	covAnalysisFile="_".join(experiment_name.split("_")[0:(len(experiment_name.split("_"))-1)])	
	for coverageAnalysis in coverageAnalysisfolder:
		mycoverage=dict()
		ssh_stdin, ssh_coverageAnalysis_stdout, ssh_stderr = sshProton.exec_command(" find "+coverageAnalysis+" -name '*"+covAnalysisFile+".bcmatrix.xls'")
		mycoverage['bcmatrix']=ssh_coverageAnalysis_stdout.readline().rstrip()
		ssh_stdin, ssh_coverageAnalysis_stdout, ssh_stderr = sshProton.exec_command(" find "+coverageAnalysis+" -name '*"+covAnalysisFile+".bc_summary.xls'")
		mycoverage['bc_summary']=ssh_coverageAnalysis_stdout.readline().rstrip()
		ssh_stdin, ssh_coverageAnalysis_stdout, ssh_stderr = sshProton.exec_command(" find "+coverageAnalysis+" -name 'startplugin.json'")
		mycoverage['startplugin']=ssh_coverageAnalysis_stdout.readline().rstrip()
		ssh_stdin, ssh_coverageAnalysis_stdout, ssh_stderr = sshProton.exec_command(" find "+coverageAnalysis+" -name 'results.json'")
		mycoverage['results']=ssh_coverageAnalysis_stdout.readline().rstrip()
		ssh_stdin, ssh_coverageAnalysis_stdout, ssh_stderr = sshProton.exec_command(" ls "+coverageAnalysis+"/local_beds/")
		local_beds=[]
		
		for bed in ssh_coverageAnalysis_stdout.readlines() :
			local_beds.append(coverageAnalysis+"/local_beds/"+str(bed.rstrip()))
		mycoverage['local_beds']=local_beds
		coverageAnalysisDict[coverageAnalysis]=mycoverage
		print(mycoverage)
		return(coverageAnalysisDict)

def buildVariantCallerFile(sshProton,runNametobackup):
	logger.debug("##########################")
	logger.debug("list variantCaller folder")
	logger.debug("##########################")
	experiment_name=runNametobackup.rstrip()
#~ xls.zip _vcf.zip local_parameters.json startplugin.json
#~ bed	 (many files)
#In variantCaller perform checksum on each following files
	ssh_stdin, ssh_variantCaller_stdout, ssh_stderr = sshProton.exec_command(" find "+absolutpath+"/"+runNametobackup.rstrip()+"/plugin_out -name 'variantCaller_out*'")				
	variantCallerFolder=[]
	variantCallerDict=dict()
	for strfile in ssh_variantCaller_stdout.readlines() :
		variantCallerFolder.append(str(strfile.rstrip()))
		
	varCallerFile="_".join(experiment_name.split("_")[1:(len(experiment_name.split("_"))-2)])				
	for variantCaller in variantCallerFolder:
		mycoverage=dict()
		ssh_stdin, ssh_coverageAnalysis_stdout, ssh_stderr = sshProton.exec_command(" find "+variantCaller+" -name '*"+varCallerFile+"*.vcf.zip'")
		mycoverage['vcf']=ssh_coverageAnalysis_stdout.readline().rstrip()
		ssh_stdin, ssh_coverageAnalysis_stdout, ssh_stderr = sshProton.exec_command(" find "+variantCaller+" -name '*"+varCallerFile+"*.xls.zip'")
		mycoverage['xls']=ssh_coverageAnalysis_stdout.readline().rstrip()
		ssh_stdin, ssh_coverageAnalysis_stdout, ssh_stderr = sshProton.exec_command(" find "+variantCaller+" -name 'local_parameters.json'")
		mycoverage['local_parameters']=ssh_coverageAnalysis_stdout.readline().rstrip()
		ssh_stdin, ssh_coverageAnalysis_stdout, ssh_stderr = sshProton.exec_command(" find "+variantCaller+" -name 'startplugin.json'")
		mycoverage['startplugin']=ssh_coverageAnalysis_stdout.readline().rstrip()
		ssh_stdin, ssh_coverageAnalysis_stdout, ssh_stderr = sshProton.exec_command(" ls "+variantCaller+"/*bed")
		local_beds=[]
		
		for bed in ssh_coverageAnalysis_stdout.readlines() :
			#~ print(str(bed.rstrip()))
			local_beds.append(str(bed.rstrip()))
		mycoverage['local_beds']=local_beds
		variantCallerDict[variantCaller]=mycoverage
		
	logger.debug("##########################")
	logger.debug("return variantCaller ditionnary")
	logger.debug("##########################")
	return(variantCallerDict)

def backupAllCovariantAnalysis(coverageAnalysisDict,pathtocov,sshProton,checksumcov,failedFileToREDO):
		#copy the cov data
	for Analysis,data in coverageAnalysisDict.iteritems():
		print("key")
		scp=SCPClient(sshProton.get_transport())
		thisAnalysis=pathtocov+"/"+str(Analysis).split("/")[-1]
		if not os.path.exists(thisAnalysis):
			os.makedirs(thisAnalysis)
		bamchecksum,originalFile=getmd5sum(data['bcmatrix'],sshProton)
		print(bamchecksum)
		print "check if the file "+thisAnalysis+"/"+data['bcmatrix'].split("/")[-1]
		print "already exist"
		if os.path.exists(thisAnalysis+"/"+data['bcmatrix'].split("/")[-1]):
			bashCommand1 = "md5sum "+thisAnalysis+"/"+data['bcmatrix'].split("/")[-1]
			process1 = subprocess.Popen(bashCommand1.split(), stdout=subprocess.PIPE)
			copybam=process1.communicate()[0].split(" ")[0]			
			print("Check copy")
			if	(copybam==bamchecksum) :
				print("COMPLETE:"+str(bamchecksum))
				checksumcov.write(data['bcmatrix'].split("/")[-1]+ " COMPLETE " +str(bamchecksum)+"\n")
			else :
				CopydataAgain(data['bcmatrix'],thisAnalysis,data['bcmatrix'].split("/")[-1],bamchecksum,checksumcov,1,sshProton)			
		else:
			try :
				scp.get(data['bcmatrix'],thisAnalysis)
			except Exception: 
				print "this file failed to upload"+str(thisAnalysis)
				failedFileToREDO.write("this file failed to upload :"+str(thisAnalysis)+"/"+data['bcmatrix'].split("/")[-1]+"\t"+str(bamchecksum)+"\n")
				scp.close()
				scp=SCPClient(sshProton.get_transport())
				CopydataAgain(data['bcmatrix'],thisAnalysis,data['bcmatrix'].split("/")[-1],bamchecksum,checksumcov,1,sshProton)
				scp.close()
			jobdone=False
			while jobdone!=True:
				print "This prints once a 10sec. and wait for data"
				time.sleep(10) 
				jobdone=True
				
			
		scp.close()
		scp=SCPClient(sshProton.get_transport())
		doitformykey('bc_summary',thisAnalysis,data,checksumcov,sshProton,scp)
		scp.close()
		scp=SCPClient(sshProton.get_transport())
		doitformykey('startplugin',thisAnalysis,data,checksumcov,sshProton,scp)
		scp.close()

		scp=SCPClient(sshProton.get_transport())
		doitformykey('results',thisAnalysis,data,checksumcov,sshProton,scp)
		scp.close()

#############
#around bed
#############
		for bam in data['local_beds']:
			scp=SCPClient(sshProton.get_transport())
			ssh_stdin, ssh_md5sum_stdout, ssh_stderr = sshProton.exec_command(" md5sum "+bam)
			bamchecksum=""
			originalFile=""
			for checksum in ssh_md5sum_stdout.readlines():
				bamchecksum=str(checksum.rstrip().split(" ")[0])
				originalFile=str(checksum.rstrip().split(" ")[1])
			print "copy Beds files"
			
			
			if os.path.exists(thisAnalysis+"/"+bam.split("/")[-1]):
				bashCommand1 = "md5sum "+thisAnalysis+"/"+bam.split("/")[-1]
				process1 = subprocess.Popen(bashCommand1.split(), stdout=subprocess.PIPE)
				copybam=process1.communicate()[0].split(" ")[0]
				if	(copybam==bamchecksum) :
					print("COMPLETE")				
					checksumcov.write(bam.split("/")[-1]+ " COMPLETE " +str(bamchecksum)+"\n")
				else :
					scp=SCPClient(sshProton.get_transport())
					CopydataAgain(bam,thisAnalysis,bam.split("/")[-1],bamchecksum,checksumcov,1,sshProton)
					scp.close()
					scp=SCPClient(sshProton.get_transport())
							
			else:
				try :
					scp.get(bam,thisAnalysis)
					jobdone=False
					while jobdone!=True:
						print "This prints 10sec. and wait for data"
						time.sleep(10) 
						jobdone=True					
				except Exception: 
					print "this file failed to upload"+str(thisAnalysis)
					failedFileToREDO.write("this file failed to upload :"+str(thisAnalysis)+"/"+ bam.split("/")[-1]  +"\t"+str(bamchecksum)+"\n")
					scp.close()
					scp=SCPClient(sshProton.get_transport())
					CopydataAgain(bam,thisAnalysis,bam.split("/")[-1],bamchecksum,checksumcov,1,sshProton)
					scp.close()					
				scp.close()



def backupAllVariantAnalysis(variantCallerDict,sshProton,pathtovcf,failedFileToREDO,checksumvcf):

	for variantCall,data in variantCallerDict.iteritems():
		scp=SCPClient(sshProton.get_transport())
		print("key")
		print "Variant CAller starts"
		thisvariant=pathtovcf+"/"+str(variantCall).split("/")[-1]
		if not os.path.exists(thisvariant):
			os.makedirs(thisvariant)
		bamchecksum,originalFile=getmd5sum(data['vcf'],sshProton)
		print(bamchecksum)

		if os.path.exists(thisvariant+"/"+data['vcf'].split("/")[-1]):
			bashCommand1 = "md5sum "+thisvariant+"/"+data['vcf'].split("/")[-1]
			process1 = subprocess.Popen(bashCommand1.split(), stdout=subprocess.PIPE)
			copybam=process1.communicate()[0].split(" ")[0]			
			print("Check copy")
			if	(copybam==bamchecksum) :
				print("COMPLETE")
				checksumvcf.write(data['vcf'].split("/")[-1]+ " COMPLETE " +str(bamchecksum)+"\n")
			else :
				scp.close()
				scp=SCPClient(sshProton.get_transport())				
				CopydataAgain(data['vcf'],thisvariant,data['vcf'].split("/")[-1],bamchecksum,checksumvcf,1,sshProton)			
				scp.close()
				scp=SCPClient(sshProton.get_transport())
						
		else:
			try :
				scp.get(data['vcf'],thisvariant)
				jobdone=False
				while jobdone!=True:
					print "This prints 10sec. and wait for data"
					time.sleep(10) 
					jobdone=True
			except Exception:
					print "this file failed to upload"+str(thisvariant)
					failedFileToREDO.write("this file failed to upload :"+str(thisvariant)+"/"+ data['vcf'].split("/")[-1]  +"\t"+str(bamchecksum)+"\n")
					scp.close()
					scp=SCPClient(sshProton.get_transport())
					CopydataAgain(data['vcf'],thisvariant,data['vcf'].split("/")[-1],bamchecksum,checksumvcf,1,sshProton)
					scp.close()
					scp=SCPClient(sshProton.get_transport())
		scp.close()	
		scp=SCPClient(sshProton.get_transport())
		doitformykey('xls',thisvariant,data,checksumvcf,sshProton,scp)
		scp.close()	
		scp=SCPClient(sshProton.get_transport())		
		doitformykey('startplugin',thisvariant,data,checksumvcf,sshProton,scp)
		scp.close()	
		scp=SCPClient(sshProton.get_transport())		
		doitformykey('local_parameters',thisvariant,data,checksumvcf,sshProton,scp)
		scp.close()	
		scp=SCPClient(sshProton.get_transport())

#~ #############
#~ #around bed
#~ #############
		for bam in data['local_beds']:
			scp=SCPClient(sshProton.get_transport())
			print "get local beds for variant caller"
			ssh_stdin, ssh_md5sum_stdout, ssh_stderr = sshProton.exec_command(" md5sum "+bam)
			bamchecksum=""
			originalFile=""
			for checksum in ssh_md5sum_stdout.readlines():
				bamchecksum=str(checksum.rstrip().split(" ")[0])
				originalFile=str(checksum.rstrip().split(" ")[1])

				if os.path.exists(thisvariant+"/"+bam.split("/")[-1]):
					bashCommand1 = "md5sum "+thisvariant+"/"+bam.split("/")[-1]
					process1 = subprocess.Popen(bashCommand1.split(), stdout=subprocess.PIPE)
					copybam=process1.communicate()[0].split(" ")[0]			
					print("Check copy")
					if	(copybam==bamchecksum) :
						print("COMPLETE")
						checksumvcf.write(bam.split("/")[-1]+ " COMPLETE " +str(bamchecksum)+"\n")
					else :
						scp.close()
						scp=SCPClient(sshProton.get_transport())				
						CopydataAgain(bam,thisvariant,bam.split("/")[-1],bamchecksum,checksumvcf,1,sshProton)
						scp.close()
						scp=SCPClient(sshProton.get_transport())
								
				else:
					try :
						scp.get(bam,thisvariant)
						jobdone=False
						while jobdone!=True:
							print "This prints 10sec. and wait for data"
							time.sleep(10) 
							jobdone=True
					except Exception:
						failedFileToREDO.write("this file failed to upload :"+str(thisvariant)+"/"+ bam.split("/")[-1]  +"\t"+str(bamchecksum)+"\n")
						scp.close()
						scp=SCPClient(sshProton.get_transport())
						CopydataAgain(bam,thisvariant,bam.split("/")[-1],bamchecksum,checksumvcf,1,sshProton)
						scp.close()
						scp=SCPClient(sshProton.get_transport())

def backupAllBamFileAnalysis(bamfileList,sshProton,checksumBam,pathtobam,failedFileToREDO):
	for bam in bamfileList:
		scp=SCPClient(sshProton.get_transport())
		print ("Treat Bam file")
		ssh_stdin, ssh_md5sum_stdout, ssh_stderr = sshProton.exec_command(" md5sum "+bam)
		bamchecksum=""
		originalFile=""
		for checksum in ssh_md5sum_stdout.readlines():
			bamchecksum=str(checksum.rstrip().split(" ")[0])
			originalFile=str(checksum.rstrip().split(" ")[1])
			
		ionTag=str("_".join(str(bam.split("/")[-1]).split("_")[0:2]))+".bam"

		if os.path.exists(pathtobam+"/"+ionTag):			
			bashCommand1 = "md5sum "+pathtobam+"/"+ionTag
			#~ time.sleep(40)
			print "path exist check the file again"
			process1 = subprocess.Popen(bashCommand1.split(), stdout=subprocess.PIPE)
			copybam=process1.communicate()[0].split(" ")[0]			
					
			print("Check copy")
			if	(copybam==bamchecksum) :
				print("COMPLETE checksum for the same file")
				checksumBam.write(ionTag+ " COMPLETE " +str(bamchecksum)+"\n")
			else :
				print"Not the same bam will redo tge analysis"
				scp.close()
				print("copybam:"+copybam)
				print("bamchecksum:"+bamchecksum)
				scp=SCPClient(sshProton.get_transport())				
				CopydataAgain(bam,pathtobam+"/"+ionTag,ionTag,bamchecksum,checksumBam,1,sshProton)
				scp.close()
				scp=SCPClient(sshProton.get_transport())
						
		else:
			try :
				scp.get(bam,pathtobam+"/"+ionTag)
				jobdone=False
				while jobdone!=True:
					print "This prints 50sec. and wait for data get bam. Made a new copy"
					time.sleep(10) 
					jobdone=True
					
				bashCommand1 = "md5sum "+pathtobam+"/"+ionTag
				time.sleep(10)
				print "Made a new copy now process the data checksum of the data hope no bug"
				process1 = subprocess.Popen(bashCommand1.split(), stdout=subprocess.PIPE)
				copybam=process1.communicate()[0].split(" ")[0]			
				print("Check copy")
				if	(copybam==bamchecksum) :
					print("COMPLETE")
					checksumBam.write(ionTag+ " COMPLETE " +str(bamchecksum)+"\n")
				else :
					CopydataAgain(bam,pathtobam+"/"+ionTag,ionTag,bamchecksum,checksumBam,1,sshProton)
			except Exception:
				failedFileToREDO.write("this file failed to upload :"+str(pathtobam)+"/"+ionTag +"\t"+str(bamchecksum)+"\n")
				print ("data transfer failed, for "+str(pathtobam)+"/"+ionTag)
				print ("try to do it again")
				scp.close()
				scp=SCPClient(sshProton.get_transport())
				CopydataAgain(bam,pathtobam+"/"+ionTag,ionTag,bamchecksum,checksumBam,1,sshProton)
				scp.close()
				scp=SCPClient(sshProton.get_transport())
		scp.close()


	
def performWholeRunBackup(runNametobackup):
	logger.debug("##########################")
	logger.debug("Start to perform the backup of :"+runNametobackup)
	logger.debug("##########################")
	logger.debug("##########################")
	logger.debug("Start connection to our proton :")
	logger.debug("##########################")	
	sshProton=ProtonCommunication_data_manager.sshConnection(
	proton_severName,idpr,idpr)
	logger.debug("##########################")
	logger.debug("list Bamfile")
	logger.debug("##########################")
	
	#list all the file to take from the NAS
	ssh_stdin_bam, ssh_coverageAnalysis_stdout_bam, ssh_stderr_bam = sshProton.exec_command(" ls "+absolutpath+"/"+runNametobackup.rstrip()+"/download_links/IonXpress*bam")
	bamfileList=[] #contains bamfile list
	for bamfile in ssh_coverageAnalysis_stdout_bam.readlines() :
		bamfileList.append(str(bamfile.rstrip()))
		
	coverageAnalysisDict=buildcoverageAnalysisFile(sshProton,runNametobackup)
	variantCallerDict=buildVariantCallerFile(sshProton,runNametobackup)

	#create run folder
	pathtoResult="/nas_backup/backupNGS_new/"+runNametobackup.rstrip()
	if not os.path.exists(pathtoResult):
		os.makedirs(pathtoResult)
	#create bam folder
	pathtobam=pathtoResult+"/bam"
	if not os.path.exists(pathtobam):
		os.makedirs(pathtobam)
	#checksum and copybam
	print("pathtofile")
	print(pathtoResult+"/checksumbam.txt")
	checksumBam=open(pathtoResult+'/checksumbam.txt','w')
	failedFileToREDO=open(pathtoResult+'/FailedFiles.txt','w')
	pathtocov=pathtoResult+"/cov"
	if not os.path.exists(pathtocov):
		os.makedirs(pathtocov)		
	checksumcov=open(pathtocov+'/checksumcov.txt','w')	
	pathtovcf=pathtoResult+"/vcf"
	if not os.path.exists(pathtovcf):
		os.makedirs(pathtovcf)
	checksumvcf=open(pathtovcf+'/checksumvcf.txt','w')
	
	backupAllCovariantAnalysis(coverageAnalysisDict,pathtocov,sshProton,checksumcov,failedFileToREDO) 
	backupAllVariantAnalysis(variantCallerDict,sshProton,pathtovcf,failedFileToREDO,checksumvcf)
	backupAllBamFileAnalysis(bamfileList,sshProton,checksumBam,pathtobam,failedFileToREDO)
	checksumBam.close()
	checksumcov.close()
	checksumvcf.close()
	sshProton.close()




def BackupDataAndChecksum(pathToOrign,pathToOutput,inputFilename):
#~ def BackupDataAndChecksum(key,thisAnalysis,data,checksumcov,sshProton,scp):
	#~PERFORM ORIGINAL MD5SUM 
	md5sumInput = "md5sum "+pathToOrign+"/"+inputFilename
	md5sumOutput = "md5sum "+pathToOutput+"/"+inputFilename
	process1 = subprocess.Popen(md5sumInput.split(), stdout=subprocess.PIPE)
	inputFilemd5sum=process1.communicate()[0].split(" ")[0]
	#~ bamchecksum,originalFile=getmd5sum(data[key],sshProton)
	logger.info(inputFilemd5sum)
	#~ EXECUTE COPY DATA
	inputDataSize=os.path.getsize(pathToOrign+"/"+inputFilename)
	#COPY DONE IN PYTHON
	copyfile(pathToOrign+"/"+inputFilename,pathToOutput+"/"+inputFilename)
	#COPY DONE IN BASH
	#~ copyTheData = "cp "+pathToOrign+"/"+inputFilename+" "+pathToOutput+"/"+inputFilename
	#~ process1 = subprocess.Popen(copyTheData.split(), stdout=subprocess.PIPE)
	#~ inputFilemd5sum=process1.communicate()[0].split(" ")[0]
	
	#~ scp.get(data[key],thisAnalysis)	
	jobdone=False
	

	while jobdone!=True:
		logger.info("This print every 30 seconds and wait for the copy to be done")
		time.sleep(10) 
		if inputDataSize==os.path.getsize(pathToOutput+"/"+inputFilename):
			jobdone=True
			
	md5sumOutput = "md5sum "+pathToOutput+"/"+inputFilename
	process1 = subprocess.Popen(md5sumOutput.split(), stdout=subprocess.PIPE)
	outputFilemd5sum=process1.communicate()[0].split(" ")[0]

	#~ print(originalFile)

	logger.info("Check copy md5sum")
	if	(inputFilemd5sum==outputFilemd5sum) :
		logger.info("COMPLETE the copy of the data")
		writechesumoftheData=open(pathToOutput+"/checksum_"+inputFilename+"md5sum.txt",'w')
		writechesumoftheData.write(pathToOrign+"/"+inputFilename+"\t"+ "COMPLETE\t" +str(inputFilemd5sum)+"\n")
		writechesumoftheData.close()
	else :
		BackupDataAndChecksum(pathToOrign,pathToOutput,inputFilename)
		#~ CopydataAgain(data[key],thisAnalysis,data['bcmatrix'].split("/")[-1],bamchecksum,checksumcov)	
				
#~ def BackupAllFiles(inputfolder,outputFolder)


def listfolder(path,copyData):
	logger.info("Check folder is not @aeDir")
	if path !='@eaDir':
		subfolder=os.listdir(path)
		if len(subfolder) > 1:
			logger.info("subfolder :"+str(subfolder))
			for subsubfolder in subfolder:
				if os.path.isdir(path+"/"+subsubfolder):
					logger.info("subfolder Go deeper :"+str(path+"/"+subsubfolder)) 
					if os.path.isdir(copyData+"/"+subsubfolder) ==False :
						logger.info("create a results folder :"+str(copyData+"/"+subsubfolder))
						os.makedirs(str(copyData+"/"+subsubfolder))
					listfolder(str(path+"/"+subsubfolder),str(copyData+"/"+subsubfolder)) 
				else:
					logger.info("only a file to copy :"+str(path+"/"+subsubfolder))
					BackupDataAndChecksum(path,copyData,subsubfolder)
		else:
			logger.info("only a file :"+str(subfolder))
			BackupDataAndChecksum(path,copyData,subfolder)
