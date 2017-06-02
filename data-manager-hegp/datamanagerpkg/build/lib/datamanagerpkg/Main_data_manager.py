#!/usr/bin/env python
import GalaxyCommunication_data_manager
import ProtonCommunication_data_manager
from bioblend.galaxy import GalaxyInstance

if __name__ == '__main__':
	base_url = 'http://yourprotoonserver/rundb/api/v1'
	idpr="psszd"
	severName="testproton"
	apiKey="qnqpykey"
	base_url_galaxy='http://yourgqlqxyserver.3'
	inputAbsolutPath="/nas_Dir"
	experimentLimit=2
	experiementdict=ProtonCommunication_data_manager.mainGetCNVData(base_url,idpr,severName,experimentLimit)
		#~ 1) connect with an api key and check if the workflows are here, if not copy every workflows
		#~ Run CNV 

	#~ gi=GalaxyCommunication_data_manager.galaxyConnection(base_url,apiKey)
	#~ 2) add workflow to current user
	#GalaxyCommunication_data_manager.addAllWorkflow(gi,"/nas_Dir/workflow")
	for key,currentExp in experiementdict.iteritems():
		print key
		#~ print currentExp["resultsName"]
		GalaxyCommunication_data_manager.mainCNV(currentExp,base_url_galaxy,apiKey)
	#~ src_files = os.listdir(inputAbsolutPath)
	#~ mainCNV(src_files,apiKey,inputAbsolutPath)
