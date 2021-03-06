import xml.etree.ElementTree as  ET
from pprint import pprint
import os
import sys
import json
import argparse
import re
##########################
#LOGGER
##########################
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s -- %(name)s - %(levelname)s : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=logging.INFO)

galaxyTemplateString="""
<tool id="tool_ID" name="tool_Name" version="tool_Version">
	<description>tool_Description</description>
	<requirements>
		<container type="docker">container_Name</container>
	</requirements>
	<version_command>version_command</version_command>
	<stdio>
		<exit_code range="1:" level="warning" description="Error" />
		<exit_code range="2"   level="warning"   description="Out of Memory" />
		<exit_code range="3:5" level="warning" description="Low disk space" />
		<exit_code range="6:"  level="warning"   description="Bad input dataset" />
	</stdio>
	<command>exec_command</command>
	<inputs>
		<param name="input_name" type="data" format="input_format" label="input_label" />
	</inputs>
	<outputs>
		<data name="output_name" format="output_format" label="output_label" />
	</outputs>
	<help>
	help_text
	</help>
	<citations>
		<citation type="bibtex">
			@misc{SAM_def,
			title={Definition of SAM/BAM format},
			url = {https://samtools.github.io/hts-specs/SAMv1.pdf},}
		</citation>
		<citation type="doi">10.1093/bioinformatics/btp352</citation>
	</citations>
</tool>"""

def find_between( s, first, last ):
	try:
		start = s.index( first ) + len( first )
		end = s.index( last, start )
		return s[start:end]
	except ValueError:
		return ""

def find_between_r( s, first, last ):
	try:
		start = s.rindex( first ) + len( first )
		end = s.rindex( last, start )
		return s[start:end]
	except ValueError:
		return ""

def writeGalaxyTool(varDict,dataInspect):
	#~ read the input template file
	#~ treeTool= ET.ElementTree()
	#~ treeTool= ET.parse(galaxyTemplateFile)
	#~ toolRoot=treeTool.getroot()
	toolRoot=ET.fromstring(galaxyTemplateString)
	#~ <tool id="tool_ID" name="tool_Name" version="tool_Version">
	toolRoot.set('id',str(varDict['tool_ID']))
	toolRoot.set('name',str(varDict['tool_Name']))
	toolRoot.set('version',str(varDict['tool_Version']))
	#add the element
	nodeToremove=[]
	stdio=["1:","2","3:5" ,"6:"]
	for child in toolRoot: 
		if  str(child.tag) == "description":
			child.text=str(varDict['tool_Description'])
		if  str(child.tag) == "requirements":
			container=child.find('container')
			container.text=str(dataInspect[0]['RepoTags'][0])
		if  str(child.tag) == "version_command" :
			if 'version_command' in varDict:
				child.text=str(varDict['version_command'])
			else:
				nodeToremove.append("version_command")
		#~ if  str(child.tag) == "stdio":
			#~ stdio.remove(str(varDict['stdio']))
		if  str(child.tag) == "command":
			child.text=str(varDict['exec_command'].replace("\\n ","\n"))
		if  str(child.tag) == "inputs":
			allInputs = [x for x in varDict.keys() if re.match(r'input_\w_format',x)]
			if len(allInputs) == 0: 
				input1=child.find('param')
				input1.set('name',str(varDict['input_name']))
				input1.set('format',str(varDict['input_format']))
				input1.set('label',str(varDict['input_label']))
			else:
				input1=child.find('param')
				for element in range(1,len(allInputs)+1,1):
					if element== 1:
						input1.set('name',str(varDict['input_'+str(element)+'_name']))
						input1.set('format',str(varDict['input_'+str(element)+'_format']))
						input1.set('label',str(varDict['input_'+str(element)+'_label']))
					else:
						param=ET.Element('param')
						param.set('name',str(varDict['input_'+str(element)+'_name']))
						param.set('format',str(varDict['input_'+str(element)+'_format']))
						param.set('label',str(varDict['input_'+str(element)+'_label']))
						child.append(param)
		if  str(child.tag) == "outputs":
			allInputs = [x for x in varDict.keys() if re.match(r'output_\w_format',x)]
			if len(allInputs) == 0: 			
				output1=child.find('data')
				output1.set('name',str(varDict['output_name']))
				output1.set('format',str(varDict['output_format']))
				output1.set('label',str(varDict['output_label']))
			else:
				output1=child.find('data')
				for element in range(1,len(allInputs)+1,1):
					if element== 1:
						output1.set('name',str(varDict['output_'+str(element)+'_name']))
						output1.set('format',str(varDict['output_'+str(element)+'_format']))
						output1.set('label',str(varDict['output_'+str(element)+'_label']))	
					else:
						output1.set('name',str(varDict['output_'+str(element)+'_name']))
						output1.set('format',str(varDict['output_'+str(element)+'_format']))
						output1.set('label',str(varDict['output_'+str(element)+'_label']))
		if  str(child.tag) == "help":
			output1=child.find('data')
		if  str(child.tag) == "citations":
			output1=child.find('data')
	treeTool = ET.ElementTree(toolRoot)
	return(treeTool,toolRoot,nodeToremove,stdio)
	#~ tree.write('testy.xml')

def parsedDockerInspect(dockerInspect):
	with open(dockerInspect) as data_file:    
		dataInspect = json.load(data_file)
	environmentDocker=dataInspect[0]['Config']['Env']
	varDict=dict()
	for envVariable in environmentDocker:
		logging.debug(str(envVariable).split('='))
		xmlVar=str(envVariable).split('=')
		varDict[xmlVar[0]]=xmlVar[1]
	logging.debug("varDict :\n"+str(varDict))
	logging.debug("##################")
	logging.debug("environmentDocker :\n"+str(environmentDocker))
	logging.debug("##################")	
	logging.debug(dataInspect)	
	return(varDict,environmentDocker,dataInspect)

def cleaningOutput(checkoutput,thisPath):
	outputwrite=open(thisPath,"w")
	for line in checkoutput:
		if "&lt;" in line:
			logging.debug(line)
			outputwrite.write(line.replace("&lt;","<"))
		elif "&gt;" in line:
			logging.debug(line)
			outputwrite.write(line.replace("&gt;",">"))
		else:
			outputwrite.write(line)
			
	outputwrite.close()

if __name__=="__main__":
	parser = argparse.ArgumentParser(description='Process a docker inspect output in order to generate a galaxy tool.xml file',epilog='the name of the output file is the same as the galaxy tool_id')
	parser.add_argument('-i','--inputFile',help='a input file output from the docker inspect command')
	# Optional positional argument
	parser.add_argument('-o','--outputName', nargs='?',help='An optional output name for the .xml file. if not specified,\n the output file will be the tool_id')
	parser.add_argument('-v','--version', action='version', version='%(prog)s 0.2')
	args = parser.parse_args()
	logging.debug(args)
	logging.debug(args.inputFile)
	logging.debug(args.outputName)
	#####check the input parameter
	if args.inputFile==None:
		logging.info("not input file selected")
		parser.print_help()
		sys.exit("-----input file not found-----")
	#~ check if the file exist
	elif os.path.isfile(args.inputFile) :
		logging.info("will proceed your input")
		if args.outputName==None :
			logging.info("output file not specified. \n The output will have the name \n of the tool id specified.")

	else:
		logging.info("the file do not exist")
		parser.print_help()
		sys.exit("-----input file not found-----")
	##Parse the docker inspect input file 
	varDict,environmentDocker,dataInspect=parsedDockerInspect(args.inputFile)
	treeTool,toolRoot,nodeToremove,stdio=writeGalaxyTool(varDict,dataInspect)

	for node in nodeToremove: 
		deleteNode=toolRoot.findall("./"+str(node))
		for element in deleteNode: 
			toolRoot.remove(element)

	#~ stdioRoot=toolRoot.find('stdio')
	#~ for node in stdio: 
		#~ deleteNode=toolRoot.findall("./stdio/exit_code[@range='"+str(node)+"']")
		#~ logging.debug(deleteNode)	
		#~ for element in deleteNode: 
			#~ stdioRoot.remove(element)
	treeTool.write("tmpfile.xml")
	checktmp=open("tmpfile.xml","r").readlines()
	
	if args.outputName != None :
		cleaningOutput(checktmp,str(args.outputName))
		logging.info("################## \n Do not forget to add :\n - "+str(args.outputName)+" \n to the tool_conf.xml file")
	else:
		cleaningOutput(checktmp,str(varDict['tool_ID'])+".xml")
		logging.info("################## \n Do not forget to add :\n - "+str(varDict['tool_ID'])+".xml \n to the tool_conf.xml file")

