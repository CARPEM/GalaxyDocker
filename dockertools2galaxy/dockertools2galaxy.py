import xml.etree.ElementTree as  ET
from pprint import pprint
import os
import sys
import json
import argparse
##########################
#LOGGER
##########################
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s -- %(name)s - %(levelname)s : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=logging.INFO)

galaxyTemplateFile='template_GalaxyTool.xml'
galaxyTemplateString="""
<tool id="tool_ID" name="tool_Name" version="tool_Version">
	<description>tool_Description</description>
	<requirements>
		<container type="docker">container_Name</container>
	</requirements>
	<version_command>version_command</version_command>
	<stdio>
		<exit_code range="1:" level="fatal" description="Error" />
		<exit_code range="2"   level="fatal"   description="Out of Memory" />
		<exit_code range="3:5" level="warning" description="Low disk space" />
		<exit_code range="6:"  level="fatal"   description="Bad input dataset" />
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

def writeGalaxyTool(varDict,environmentDocker,dataInspect):
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
		if  str(child.tag) == "stdio":
			stdio.remove(str(varDict['stdio']))
		if  str(child.tag) == "command":
			child.text=str(varDict['exec_command'].replace("\\n ","\n"))
		if  str(child.tag) == "inputs":
			input1=child.find('param')
			input1.set('name',str(varDict['input_name']))
			input1.set('format',str(varDict['input_format']))
			input1.set('label',str(varDict['input_label']))
		if  str(child.tag) == "outputs":
			output1=child.find('data')
			output1.set('name',str(varDict['output_name']))
			output1.set('format',str(varDict['output_format']))
			output1.set('label',str(varDict['output_label']))
		if  str(child.tag) == "help":
			output1=child.find('data')
		if  str(child.tag) == "citations":
			output1=child.find('data')
	treeTool = ET.ElementTree(toolRoot)
	return(treeTool,toolRoot,nodeToremove,stdio)
	#~ tree.write('testy.xml')

def parsedDockerInspect(dockerInspect):
	#~ print("hello you")
	#~ with open("testsamtools.txt") as data_file:    
	with open(dockerInspect) as data_file:    
		dataInspect = json.load(data_file)
	#~ logging.debug(pprint(dataInspect))
	environmentDocker=dataInspect[0]['Config']['Env']
	varDict=dict()

	for envVariable in environmentDocker:
		logging.debug(str(envVariable).split('='))
		xmlVar=str(envVariable).split('=')
		varDict[xmlVar[0]]=xmlVar[1]
	logging.debug(varDict)
	return(varDict,environmentDocker,dataInspect)
	

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

	#~ check if the file exist
	if os.path.isfile(args.inputFile) :
		logging.info("will proceed your input")
	else:
		logging.info("the file do not exist")
		parser.print_help()
		sys.exit("-----input file not found-----")
	#~ varDict,environmentDocker,dataInspect=parsedDockerInspect("testsamtools.txt")
	varDict,environmentDocker,dataInspect=parsedDockerInspect(args.inputFile)
	treeTool,toolRoot,nodeToremove,stdio=writeGalaxyTool(varDict,environmentDocker,dataInspect)

	for node in nodeToremove: 
		deleteNode=toolRoot.findall("./"+str(node))
		for element in deleteNode: 
			toolRoot.remove(element)

	stdioRoot=toolRoot.find('stdio')
	for node in stdio: 
		deleteNode=toolRoot.findall("./stdio/exit_code[@range='"+str(node)+"']")
		logging.debug(deleteNode)
		
		for element in deleteNode: 
			stdioRoot.remove(element)
	if args.outputName != None :
		treeTool.write(args.outputName)
	else:
		treeTool.write(str(varDict['tool_ID'])+".xml")
