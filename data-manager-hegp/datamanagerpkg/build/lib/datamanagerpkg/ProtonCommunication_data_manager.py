#!/usr/bin/env python
"""The module ProtonCommunication_data_manager.py was
designed to be abe able to connect to the HEGP Ion Proton and
copy Data easily. It can be used with GalaxyCommunication_data_manager.py which
assure the Data-Manager_Galaxy Job routine.

This script use the The Torrent Suite Software Development Kit
to communicate with the Ion Proton.
ProtonCommunication_data_manager fullfill three main goals:
- retrieve the Data
- Select the Data you want to use
- Copy them throught the network 
"""
import json
import requests
from pprint import pprint
import paramiko
from scp import SCPClient
import os

__license__ = "grou "
__revision__ = " $Id: Main_data_manager.py 1586 2016-08-10 15:56:25 $"
__docformat__ = 'reStructuredText'
__author__ = 'William Digan, CARPEM'
#~ first function (retrieve the last experiment and the file name)
#~ second function ( find the data to download)
#~ third function ( download data)

def CheckExperiments(nb_limit,idpwd,base_url):
	"""
	CheckExperiments(nb_limit,idpwd,base_url)
	returns (dictionnary)
	
	**Descriptions**:
	       This is a longer explanation, which may include math with latex syntax
        :math:`\\alpha`.
        Then, you need to provide optional subsection in this order (just to be
        consistent and have a uniform documentation. Nothing prevent you to
        switch the order):
	retrieve the n last experiment and the file name
	and check if the run is complete
	return a dictionnary as key the expName
	and for value an other dict wich contains display name frtpstatus and status
	check if status is complete
	experiments=dict()
	CheckExperiments(1,"ionadmin") 
          - parameters using ``:param <name>: <description>``
          - type of the parameters ``:type <name>: <description>``
          - returns using ``:returns: <description>``
          - examples (doctest)
          - seealso using ``.. seealso:: text``
          - notes using ``.. note:: text``
          - warning using ``.. warning:: text``
          - todo ``.. todo:: text``

	**Parameters**:
        :param arg1: the first value
        :param arg2: the first value
        :param arg3: the first value
        :type arg1: int, float,...
        :type arg2: int, float,...
        :type arg3: int, float,...
        :returns: arg1/arg2 +arg3
        :rtype: int, float

        .. note:: Descripte the dictionnary structure
	"""
	##############################################
	##############################################

	resp = requests.get(base_url+'/experiment/', auth=(idpwd,idpwd), params={"format": "json", "limit": nb_limit,"order_by" : "-date"})
	#will contains results folder name
	resultFolder=""
	CNVfile=""
	resp_json = resp.json()
	experiments=dict()
	print "look at last run"
	for item in resp_json['objects']:
		#~ if item['status'] == "Complete":
		print "##########################" 
		currentExp=dict()
		#~ exp['displayName']=i['displayName']
		currentExp['cnvFileName']=str(item['expName'])+"_"
		currentExp['status']=item['status']
		currentExp['ftpStatus']=item['ftpStatus']
		currentExp['date']=item['date']  
		currentExp['id']= item['id'] 
		currentExp['resultsQuery']= str(item['displayName']).replace(" ","_")+"_"+ str(item['id'])
		#~ resultFolder=str(i['displayName']).replace(" ","_")+"_"+ str(i['id'])
		experiments[item['expName']]=currentExp   
#~ return a dictionnary
	return(experiments)   

##############################################
#~ Find the result folder absolut path
#~ query on the result api
#~ FindResults(grouexp,"ionadmin",base_url)
#~ return also a dictionnary and add the filesystempath to the dict
##############################################
def FindResults(expDict,idpwd,base_url):
	for key,currentExp in expDict.iteritems():
		#~ resp = requests.get(base_url+'/results/', auth=(idpr,idpr),params={"format": "json", "resultsName__endswith" : "r'*"+resultFolder+"'"})
		resp = requests.get(base_url+'/results/', auth=(idpwd,idpwd),params={"format": "json", "resultsName__endswith" : currentExp['resultsQuery']})
		runPath=""
		resp_json = resp.json()
		for item in resp_json['objects']:
			#~ if item['status'] == "Completed":
			currentExp['resultsName']=str(item['resultsName'])
			currentExp['cnvFileName']=currentExp['cnvFileName']+ str(item['resultsName'])
			currentExp['runPath']=str(item['filesystempath'])
	return(expDict)   			
			#~ print item['timeStamp']

##############################################
#~ establish an ssh connection
##############################################
def sshConnection(severName,idpwd):
	sshConnection = paramiko.SSHClient()
	sshConnection.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
	sshConnection.connect(severName, username=idpwd, password=idpwd)
	return(sshConnection)

##############################################
#~ check data consistency before Performed a
#~  scp cmd. 
#~ if I need to add more quality control around the data
##############################################
def CheckResultsConsistency(expDict,ssh):
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
#~ copyData(currentExp,ssh,"/nas_Dir"+something)
##############################################
def copyData(currentExp,ssh):
	scp = SCPClient(ssh.get_transport())
	#~ scp.get(rightcoverageAnalysis_out+'/'+currentExp['cnvFileName']+".bcmatrix.xls",resultPath)
	#~ scp.get(rightcoverageAnalysis_out+'/'+currentExp['cnvFileName']+".bc_summary.xls",resultPath)
	scp.get(currentExp['coverageAnalysis_out']+'/'+currentExp['cnvFileName']+".bcmatrix.xls","/nas_Dir/"+currentExp['resultsName']+"/CNV")
	scp.get(currentExp['coverageAnalysis_out']+'/'+currentExp['cnvFileName']+".bc_summary.xls","/nas_Dir/"+currentExp['resultsName']+"/CNV")
	currentExp['bcmatrix']="/nas_Dir/"+currentExp['resultsName']+"/CNV/"+currentExp['cnvFileName']+".bcmatrix.xls"
	currentExp['bcsummary']="/nas_Dir/"+currentExp['resultsName']+"/CNV/"+currentExp['cnvFileName']+".bc_summary.xls"
	scp.close()
	return(currentExp)

##############################################
#~ copy data trought scp and perform checksum 
#~ return a dictionnary with the path to the file
##############################################
def mainGetCNVData(base_url,idpr,severName,experimentLimit) :

	print "##########################"
	print "Query Experiments\n"
	experimentsDict=CheckExperiments(experimentLimit,idpr,base_url) 
	print "##########################" 
	print "Find Results folder Path\n"
	experimentsDict=FindResults(experimentsDict,idpr,base_url)
	print "##########################" 
	print "Connect to the server "+	severName
	sshProton=sshConnection(severName,idpr)
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
		currentExp=copyData(currentExp,sshProton)
	#~ do not forgot to close the ssh connection()    
	sshProton.close()
	return(experimentsDict)

if __name__ == '__main__':
	base_url = 'http://yourprotonserver/rundb/api/v1'
	idpr="pqsszordtest"
	severName="test6proton"
	experimentLimit=2
	mainGetCNVData(base_url,idpr,severName,experimentLimit)

