#!/usr/bin/env python
import GalaxyCommunication_data_manager
import ProtonCommunication_data_manager
from bioblend.galaxy import GalaxyInstance
import logging

##########################
#URL SEQUENCER
##########################
from GlobalVariables import sequencer_base_url 
from GlobalVariables import sequencer_user
from GlobalVariables import sequencer_password
from GlobalVariables import sequencer_severName
from GlobalVariables import sequencer_ExperimentLimit

##########################
#URL GALAXY
##########################
from GlobalVariables import galaxy_base_url 
from GlobalVariables import apiKey
from GlobalVariables import inputAbsolutPath

if __name__ == '__main__':
	experiementdict=ProtonCommunication_data_manager.mainGetCNVData(sequencer_base_url,sequencer_password,sequencer_user,sequencer_severName,sequencer_ExperimentLimit)
		#~ 1) connect with an api key and check if the workflows are here, if not copy every workflows
		#~ Run CNV 
	#~ gi=GalaxyCommunication_data_manager.galaxyConnection(base_url,apiKey)
	#~ 2) add workflow to current user
	#GalaxyCommunication_data_manager.addAllWorkflow(gi,"/nas_Dir/workflow")
	for key,currentExp in experiementdict.iteritems():
		print key
		#~ print currentExp["resultsName"]
		GalaxyCommunication_data_manager.mainCNV(currentExp,galaxy_base_url,apiKey)
	#~ src_files = os.listdir(inputAbsolutPath)
	#~ mainCNV(src_files,apiKey,inputAbsolutPath)
