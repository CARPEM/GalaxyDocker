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



__license__ = "grou "
__revision__ = " $Id: Main_data_manager.py 1586 2016-08-10 15:56:25 $"
__docformat__ = 'reStructuredText'
__author__ = 'William Digan, CARPEM'

##############################################
#~ connection to the galaxy server
##############################################
def galaxyConnection(base_url,apiKey): 
	""" bla
		returns (arg1 / arg2) + arg3

        This is a longer explanation, which may include math with latex syntax
        :math:`\\alpha`.
        Then, you need to provide optional subsection in this order (just to be
        consistent and have a uniform documentation. Nothing prevent you to
        switch the order):

          - parameters using ``:param <name>: <description>``
          - type of the parameters ``:type <name>: <description>``
          - returns using ``:returns: <description>``
          - examples (doctest)
          - seealso using ``.. seealso:: text``
          - notes using ``.. note:: text``
          - warning using ``.. warning:: text``
          - todo ``.. todo:: text``

        **Advantages**:
         - Uses sphinx markups, which will certainly be improved in future
           version
         - Nice HTML output with the See Also, Note, Warnings directives


        **Drawbacks**:
         - Just looking at the docstring, the parameter, type and  return
           sections do not appear nicely

        :param arg1: the first value
        :param arg2: the first value
        :param arg3: the first value
        :type arg1: int, float,...
        :type arg2: int, float,...
        :type arg3: int, float,...
        :returns: arg1/arg2 +arg3
        :rtype: int, float

        :Example:

        >>> import template
        >>> a = template.MainClass1()
        >>> a.function1(1,1,1)
        2

        .. note:: can be useful to emphasize
            important feature
        .. seealso:: :class:`MainClass2`
        .. warning:: arg2 must be non-zero.
        .. todo:: check that arg2 is non zero.
        """
	try:
		gi = GalaxyInstance(url=base_url, key=apiKey)
	except StandardError:
		print ("An error occured. Verify the server connection.")
	return(gi)

##############################################
#~ load all existing workflow to the galaxy instance of the current user
##############################################
def addAllWorkflow(galaxyWeb,workflow_Dir): 
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
	today = datetime.date.today()
#	random.seed(datetime.date.now())
	random.seed(str(datetime.datetime.today()))
	#~ historyName= "".join(random.sample(list(string.ascii_uppercase),10))+"_"+str(today)+workflow_Name
	historyName= str(today)+workflow_Name
	galaxyWeb.histories.create_history(name=historyName)
	myNewHistory=galaxyWeb.histories.get_histories(name=historyName)
	return(myNewHistory[0]['id'])

##############################################
#~ Uploads data to a specific history
##############################################
#~ def upload_To_History(galaxyWeb,expDict,historyID,inputAbsolutPath):
def upload_To_History(galaxyWeb,expDict,historyID):
	galaxyWeb.tools.upload_file(path=expDict['bcmatrix'],history_id=historyID,file_type='txt',dbkey="hg19plasma")
	galaxyWeb.tools.upload_file(path=expDict['bcsummary'],history_id=historyID,file_type='txt',dbkey="hg19plasma")
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
			inputWorkflow[key]= { 'src':'hda', 'id': data_Input_CNVID["bcsummary"] }
		else:
			inputWorkflow[key]= { 'src':'hda', 'id': data_Input_CNVID["bcmatrix"] }
	galaxyWeb.workflows.invoke_workflow(CNVworkflowID, inputs=inputWorkflow,history_id=historyID)

##############################################
#~  Main CNV script to call from the IonTorrent Browser
##############################################
def mainCNV(expDict,base_url,apiKey):
	gi=galaxyConnection(base_url,apiKey)
	#~ if a new user add all the workflow
	#~ workflow_Dir="/nas_Dir/workflow"
	#~ addAllWorkflow(gi,workflow_Dir)
	print expDict["resultsName"]
	print "dictname"
	historyID=Create_History(gi,"_CNV_"+expDict["resultsName"])
	#~ historyID=Create_History(gi,"_CNV_")
	#~ Uploads data to a specific history
	upload_To_History(gi,expDict,historyID)
	#~ upload_To_History(gi,expDict,historyID,inputAbsolutPath)
	#~ Retrieve the current history and build a 
	#~ a dictionnary of the recent Uploaded data
	dataCNVID=CNV_Input_Dict(gi,historyID)
	Run_CNV_Workflow(gi,dataCNVID,historyID)
	print "job done, hydrate yourself"


if __name__ == "__main__":
	#~ parser = argparse.ArgumentParser(prog=".py",description='This script is a wrapper around polyweb/polydiag to faciliate\n the data management.')
	#~ parser = argparse.ArgumentParser(description='This script is a wrapper around galaxy/workflow to send data to galaxy')
	#~ parser.add_argument('-k','--apiKey', help='the user apikey (which will be used)',required=True)
	apiKey="qr2gulqrqpykey"
	base_url='http://gqlqxyserver'
	inputAbsolutPath="/nas_Dir"
	src_files = os.listdir(inputAbsolutPath)
	#~ gi=galaxyConnection(base_url,apiKey)
	#~ mainCNV(src_files,gi,inputAbsolutPath)
	mainCNV(src_files,base_url,apiKey)
