import logging
from django.shortcuts import get_object_or_404,render
from .forms import MyForm
#from .forms import MyFormbool
from django.urls import reverse
# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
#my package
from datamanagerpkg import ProtonCommunication_data_manager
from datamanagerpkg import GalaxyCommunication_data_manager

from .models import Experiments, GalaxyUsers ,toDownloads
from .models import GalaxyJobs, ExperimentRawData, savedNGSData
from .models import Workflows,WorkflowsTools,Supportedfiles,NGSBamData
import json
import os
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
#~ from .forms import UserForm
from bioblend.galaxy import GalaxyInstance
import tasks
import string
import random
import requests
from pprint import pprint
import paramiko
from scp import SCPClient

##############################################
#MAIN PARAMETERS

##########################
#LOGGER
##########################
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s -- %(name)s - %(levelname)s : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=logging.INFO)
#logger.setLevel(logging.DEBUG)

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

def id_generator(size=50, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
    
##############################################
#~#HOME PAGE
def getExperiments(request):
    logger.info("##########################")
    logger.info("START getExperiments() view")
    logger.info("##########################")
    logger.debug("Load Template sequencer/projects.html ")   
    template = loader.get_template('sequencer/projects.html')
    logger.info("Return all Experiments ")    
     #~ #define in models.py
    experiments_list = Experiments.objects.all() 
  
    logger.debug("##########################")
    logger.debug("apiKey and base_url define below")
    logger.debug("##########################")    

    logger.info("Get GalaxyUsers()")
     #~ #define in models.py 
    usersFromGalaxy=GalaxyUsers.objects.all()
    bams=ExperimentRawData.objects.all()
    logger.debug("usersFromGalaxy: %s ",str(usersFromGalaxy))
    logger.debug("##########################")    
    logger.debug("Build context with experiments and users information")    
    context = {
        'experiments_list': experiments_list,
        'users' :usersFromGalaxy,
        'bams' :bams,
    }
    logger.info("##########################")
    logger.info("END getExperiments() view")
    logger.info("##########################")    
    return HttpResponse(template.render(context, request)) 	


def downloads(request):
    logger.info("##########################")
    logger.info("START getExperiments() view")
    logger.info("##########################")
    logger.debug("Load Template sequencer/downloads.html ")   
    template = loader.get_template('sequencer/downloads.html')
    logger.info("Return all Experiments ")    
     #~ #define in models.py
    todownload_list = toDownloads.objects.all() 
    logger.debug("##########################")
    logger.debug("apiKey and base_url define below")
    logger.debug("##########################")    
    logger.info("Get GalaxyUsers()")
     #~ #define in models.py 
    usersFromGalaxy=GalaxyUsers.objects.all()
    #~ bams=ExperimentRawData.objects.all()
    logger.debug("usersFromGalaxy: %s ",str(usersFromGalaxy))
    logger.debug("##########################")    
    logger.debug("Build context with experiments and users information")    
    context = {
        'todownload_list': todownload_list,
        'users' :usersFromGalaxy,
        #~ 'bams' :bams,
    }
    logger.info("##########################")
    logger.info("END getExperiments() view")
    logger.info("##########################")    
    return HttpResponse(template.render(context, request)) 

def locateDataToDownload(nbLimit,toMatch):
    sshProton=ProtonCommunication_data_manager.sshConnection(sequencer_severName,sequencer_user,sequencer_password)
    ssh_stdin, ssh_coverageAnalysis_stdout, ssh_stderr = sshProton.exec_command("ls /results/analysis/output/Home/ |sort -ur |grep -m "+str(nbLimit)+" '"+toMatch +"'")
    getData=ssh_coverageAnalysis_stdout.readlines()	
    print(getData)
    sshProton.close()
    return (getData)
  

def actualizeDownloads(request):
    logger.info("##########################")
    logger.info("START actualizeDownloads() view")
    logger.info("##########################")
    experimentLimit=request.POST.get('sliderDataInput')
    if (experimentLimit != None):
        logger.info("##########################") 
        logger.info("Query the %s last experiments",str(experimentLimit))        
        info=locateDataToDownload(experimentLimit,"Auto_user")
        actualizedparsedInformation(info)
        info=locateDataToDownload(experimentLimit,"reanalyz")
        actualizedparsedInformation(info)

    logger.info("END actualizeDownloads() view")
    logger.info("##########################")
    return HttpResponseRedirect(reverse('sequencer:downloadsdata'))    

def actualizedparsedInformation(info) :
    for element in info:
        if not "_tn_" in element :
            withoutAuto=str(element).replace("Auto_","").rstrip()
            print(withoutAuto)
            withoutAutoTmp=withoutAuto.split('_')
            cleanID=str("_".join(withoutAutoTmp[0:len(withoutAutoTmp)-1]))
            resp = requests.get(sequencer_base_url+'/results/', auth=(sequencer_user,sequencer_password),params={"format": "json", "resultsName__endswith" : cleanID})
            resp_json = resp.json()
            pprint(resp_json)
            try:
                todown = toDownloads.objects.get(folder_name=str(element).rstrip())
            except toDownloads.DoesNotExist:
                todown = None
            if  todown == None:        
                for item in resp_json['objects']:  
                    todown = toDownloads.objects.create(folder_name=str(element).rstrip(),
                    filesystempath=item['filesystempath'],
                    reference=item['reference'],
                    status=item['status'],
                    backupOnNas="false",
                    backupValidate="non",
                    timeToComplete=item['timeToComplete'],                        
                    timeStamp=item['timeStamp'])
                    try:
                        checkNGSBackup = savedNGSData.objects.get(folder_name=str(element).rstrip())
                    except savedNGSData.DoesNotExist:
                        checkNGSBackup = None
                    if  checkNGSBackup != None:
                        todown.backupOnNas="True"
                        todown.backupValidate="Termin&egrave;"
                    if item['diskusage']== None :
                        todown.diskusage=str(0) 
                    else:
                        todown.diskusage=str(item['diskusage'])                       
                    todown.save()
                        
                        
                        
def showSavedData(request):
    logger.info("##########################")
    logger.info("START showSavedData() view")
    logger.info("##########################")
    logger.debug("Load Template sequencer/ngsData.html ")   
    template = loader.get_template('sequencer/ngsData.html')
    logger.info("Return all Experiments ")    
     #~ #define in models.py
    todownload_list = savedNGSData.objects.all() 
    logger.debug("##########################")
    logger.debug("apiKey and base_url define below")
    logger.debug("##########################")    
    logger.info("Get GalaxyUsers()")
     #~ #define in models.py 
    usersFromGalaxy=GalaxyUsers.objects.all()
    #~ bams=ExperimentRawData.objects.all()
    logger.debug("usersFromGalaxy: %s ",str(usersFromGalaxy))
    logger.debug("##########################")    
    logger.debug("Build context with experiments and users information")    
    context = {
        'todownload_list': todownload_list,
        'users' :usersFromGalaxy,
        #~ 'bams' :bams,
    }
    logger.info("##########################")
    logger.info("END getExperiments() view")
    logger.info("##########################")    
    return HttpResponse(template.render(context, request)) 
##############################################
#~#USER LOG IN 
def showSavedDataLogs(request,user_name):
    logger.info("##########################")
    logger.info("START showSavedData() view")
    logger.info("##########################")
    logger.debug("Load Template sequencer/ngsData.html ")   
    template = loader.get_template('sequencer/ngsData.html')
    logger.info("Return all Experiments ")    
    #~ latest_question_list = Experiments.objects.all()
    #~ experiments_list = Experiments.objects.all()    
    todownload_list = savedNGSData.objects.all()     
    ##############################################    
    gi=GalaxyCommunication_data_manager.galaxyConnection(galaxy_base_url,apiKey)
    users=GalaxyUsers.objects.all() #return a list of dictionnary
    currentUser=GalaxyUsers.objects.get(user_id=user_name)
    logger.debug( "##########################")
    logger.debug( "checkusers")
    logger.debug( "##########################")    
    user = authenticate(username=currentUser.user_email, password=currentUser.user_email)
    if user is not None:
        login(request, user)
    context = {
        #~ 'latest_question_list': latest_question_list,
        'todownload_list': todownload_list,
        'users' :users,
        'user_name':currentUser.user_email,
        'current_user_name':currentUser.user_email,
    }
    logger.debug("##########################")
    logger.debug("job done getExperiments")
    logger.debug("##########################")
    return HttpResponse(template.render(context, request))

def getSequenceData(request,experiment_name):
    logger.info("##########################")
    logger.info("START getBamReviewed() view")
    logger.info("##########################")
    logger.info("Check User autentification")
    logger.info("##########################")
    logger.info("Parsed User Request")
    logger.info("##########################")    
    UserRequest=request.POST
    try :
        thisDownloadData = toDownloads.objects.get(folder_name=experiment_name)
        thisDownloadData.backupOnNas="en cours"
        thisDownloadData.backupValidate="en cours"
        thisDownloadData.save()
    except toDownloads.DoesNotExist :
        thisDownloadData = None
    #~ current_exp = toDownloads.objects.get(folder_name=experiment_name)
    #~ for key, val in UserRequest.iteritems():
        #~ print str(key)
        #~ print str(val)
    logger.info("##########################")
    logger.info("##########################")    
    logger.info("Copy data throught ssh and scp")
    logger.debug("##########################")        
    #~ logger.debug(experimentsDict['bammd5sum'])
    template = loader.get_template('sequencer/download_Main.html')    
    logger.debug("##########################")           
    logger.debug("##########################")      
    context = {
        'current_exp': thisDownloadData,
        'experimentsDict':UserRequest,
    }      
    #this tasks will be run before by celery as a baground event
    return HttpResponse(template.render(context, request)) 


##############################################
#~#USER LOG IN 
def getExperimentsLogs(request,user_name):
    experimentLimit=10
    logger.info("##########################")
    logger.debug("start work getExperiments")
    logger.debug("create dict getExperiments")    
    template = loader.get_template('sequencer/projects.html')
    #~ latest_question_list = Experiments.objects.all()
    experiments_list = Experiments.objects.all()    
    ##############################################    
    gi=GalaxyCommunication_data_manager.galaxyConnection(galaxy_base_url,apiKey)
    users=GalaxyUsers.objects.all() #return a list of dictionnary
    currentUser=GalaxyUsers.objects.get(user_id=user_name)
    logger.debug( "##########################")
    logger.debug( "checkusers")
    logger.debug( "##########################")    
    user = authenticate(username=currentUser.user_email, password=currentUser.user_email)
    if user is not None:
        login(request, user)

    context = {
        #~ 'latest_question_list': latest_question_list,
        'experiments_list': experiments_list,
        'users' :users,
        'user_name':currentUser.user_email,
        'current_user_name':currentUser.user_email,
    }
    logger.debug("##########################")
    logger.debug("job done getExperiments")
    logger.debug("##########################")
    return HttpResponse(template.render(context, request)) 
        
def checkUsersKey(usersdict,galaxyWeb):
    #~ inputAbsolutPath="/nas_Dir/workflow"
    for userinfo in usersdict:
        #~  #Check if the user is not the admin
        logger.debug(str(userinfo['email']))
        logger.debug("checkUsersKey function what the pb")
        if  (str(userinfo['email']) != "admin@galaxy.org"):
            logger.debug("check if the email already on the DB")
            try:
                user = GalaxyUsers.objects.get(user_email=userinfo['email'])
            except GalaxyUsers.DoesNotExist:
                user = None
            logger.debug("user info:"+ str(userinfo['id']))
            #~ #if none create a new user
            if  user == None:
                logger.debug( "a none value create a new user")
                user=GalaxyUsers(user_id=userinfo['id'],
                user_email=userinfo['email'],user_aphid=userinfo['username'],
                user_apikey=GalaxyCommunication_data_manager.createUserApikey(galaxyWeb,str(userinfo['id']))                
                )
                logger.info("Add WOrkflow to users")
                gi=GalaxyCommunication_data_manager.galaxyConnection(galaxy_base_url,user.user_apikey)
                GalaxyCommunication_data_manager.addAllWorkflow(gi,workflowPath)                
                user.save()   
            #~ #else print user apikey                      
            else:
                logger.info( "user.apikey:"+str(user.user_apikey) )

def djangoUsers(usersdict):
    for userinfo in usersdict:
        try:
            user = User.objects.get(username=userinfo.user_email)
        except User.DoesNotExist:
            user = None
        if  user == None:
            user = User.objects.create_user(username=userinfo.user_email,password= userinfo.user_email)
            user.save()
            

def QueryExperiments(request, user_id):

    #~ #question = get_object_or_404(Question, pk=question_id)
    #~ #currentuser = get_object_or_404(GalaxyUsers, pk=user_id)
    currentuser = GalaxyUsers.objects.get(user_id=user_id)
    logger.debug("##########################")
    logger.debug("get n experiments for user"+str(currentuser.user_email))    
    #~ # Always return an HttpResponseRedirect after successfully dealing
    #~ #with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
    return HttpResponseRedirect(reverse('sequencer:showdatalogs', args=(currentuser.user_id,)))   
    #~ #return HttpResponseRedirect(reverse('sequencer:projectslogs', args=(currentuser.user_id,)))   
      
def vote(request, user_id):
    #~ question = get_object_or_404(Question, pk=question_id)
    #~ currentuser = get_object_or_404(GalaxyUsers, pk=user_id)
    currentuser = GalaxyUsers.objects.get(user_id=user_id)
    logger.debug("##########################")
    logger.debug("get n experiments for user"+str(currentuser.user_email)) 
    #~ # Always return an HttpResponseRedirect after successfully dealing
    #~ with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
    return HttpResponseRedirect(reverse('sequencer:showdatalogs', args=(currentuser.user_id,)))    
    #~ #return HttpResponseRedirect(reverse('sequencer:projectslogs', args=(currentuser.user_id,)))    


    
def actualize(request):
    logger.info("##########################")
    logger.info("START actualize() view")
    logger.info("##########################")
    experimentLimit=request.POST.get('sliderDataInput')
    if (experimentLimit != None):
        logger.info("##########################") 
        logger.info("Query the %s last experiments",str(experimentLimit)) 
        dataexp=ProtonCommunication_data_manager.CheckExperiments(experimentLimit,sequencer_user,sequencer_password,sequencer_base_url)
        inputdata = json.dumps(dataexp)
        logger.info("DONE")
        logger.info("##########################")         
    #~ #loop around the experiments query
    #~ #will be refresh automatically
        for run, expdict in dataexp.iteritems():
            logger.debug("run_name : %s ",run)
            logger.info("check in the DB if the Experiments is already saved")
            logger.info("##########################")            
            try:
                tryexp = Experiments.objects.get(run_name=run)
            except Experiments.DoesNotExist:
                tryexp = None
                
            if  (tryexp == None) and (expdict["ftpStatus"]=='Complete'):
				#add only the one with a complete status
				exp = Experiments(run_name=run,cnvFileName=expdict["cnvFileName"],ftpStatus=expdict["ftpStatus"],status=expdict["status"],resultsQuery=expdict["resultsQuery"],dateIonProton=str(str(expdict["date"]).split("T")[0]))
				exp.save()
				logger.debug("install and search bam file  associated to the run  : %s ",run)
				getDataPath(exp)                     

    else :
        logger.warning("##########################")
        logger.warning("No experiments found")
        logger.warning("##########################")     
                  
    logger.info("END actualize() view")
    logger.info("##########################")
    return HttpResponseRedirect(reverse('sequencer:projects'))    

def getDataPath(experiment_Complete):
##########################
#START ROUTINE GET EXPERIMENTS INFORMATIONS 
#GET DATA FOR SAFIR PLASMA AND CNV
##########################
    logger.info("##########################")
    logger.info("Find Results folder Path\n")    
    experimentsDict=ProtonCommunication_data_manager.QueryResults(
    experiment_Complete.resultsQuery,experiment_Complete.cnvFileName,sequencer_user,sequencer_password,sequencer_base_url) 
    logger.info("##########################")
    logger.info("Connect to the server : %s",sequencer_severName )     
    sshProton=ProtonCommunication_data_manager.sshConnection(
    sequencer_severName,sequencer_user,sequencer_password)   
    logger.info("##########################")
    logger.info("check coverage data consistency : %s",sequencer_severName )     
    experimentsDict=ProtonCommunication_data_manager.CheckResConsistency(experimentsDict,sshProton)    
    logger.info("##########################")    
    logger.info("CREATE INPUT FOLDER FROM PROTON NAS_DIR/%s/CNV",experimentsDict['resultsName'])     
    if not os.path.exists(nasInput+experimentsDict['resultsName']+CNVfolderName):
        os.makedirs(nasInput+experimentsDict['resultsName']+CNVfolderName)
        
    logger.info("CREATE RESULTS FOLDER FROM GALAXY NAS_DIR/RESULTS/%s/CNV",experimentsDict['resultsName'])     
    if not os.path.exists(nasResults+experimentsDict['resultsName']):
        os.makedirs(nasResults+experimentsDict['resultsName'])
    experiment_Complete.dictionnary = json.dumps(experimentsDict)
    #~experiment objet reactualization 
    experiment_Complete.save()
    sshProton.close()
    for bamfile in experimentsDict['BAM_FILES']:
        sshProton=ProtonCommunication_data_manager.sshConnection(sequencer_severName,sequencer_user,sequencer_password)
        try :
            tryBam = ExperimentRawData.objects.get(bam_path=str(bamfile))
        except ExperimentRawData.DoesNotExist:
            tryBam = None
            
        if  tryBam == None:
            try:
                mykey=experimentsDict.keys()
            except ValueError:
             # decoding failed
                logger.error("This run is not avaible now"+str(experiment_Complete.run_name))     
                logger.error("It will be deleted from hour database")
                experiment_Complete.delete()   
                sshProton.close()  
                continue
            ionExpressTag=str(bamfile).split("/")
            try :     
                logger.debug("something "+str(experimentsDict['sampleKey']))
                logger.debug(nasResults+experimentsDict['resultsName'])                         
                newBam = ExperimentRawData(bam_path=str(bamfile),
                experienceName=experiment_Complete,
                ionTag=str("_".join(ionExpressTag[len(ionExpressTag)-1].split("_")[0:2])),
                sampleName=experimentsDict['sampleKey'][str("_".join(ionExpressTag[len(ionExpressTag)-1].split("_")[0:2]))])
                newBam.save()
            except  KeyError:
                logger.error("This run as a Sample key but a patient is missing"+str(ionExpressTag[len(ionExpressTag)-1].split("_")[0:2]))     
                logger.error("This bam is not not avaible in run "+str(experiment_Complete.run_name))     
                sshProton.close()
                continue
                
        sshProton.close()
        
    logger.info("##########################\nGO DICTIONNARY input") 
    logger.info(str(experiment_Complete.dictionnary)) 
    logger.info("##########################")     
    return(1)    

##########################
#END ROUTINE GET EXPERIMENTS INFORMATIONS 
#GET DATA FOR SAFIR PLASMA AND CNV
##########################  

def getGalaxyUsers(request): 
    gi=GalaxyCommunication_data_manager.galaxyConnection(galaxy_base_url,apiKey)
    users=GalaxyCommunication_data_manager.returnGalaxyUsers(gi) #return a list of dictionnary
    logger.info( "##########################")
    logger.info( "checkusers from getGalaxyUsers")
    checkUsersKey(users,gi)
    djangoUsers( GalaxyUsers.objects.all())  
    logger.info( "##########################")
    #~ # Always return an HttpResponseRedirect after successfully dealing
    #~ with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
    return HttpResponseRedirect(reverse('sequencer:savedData'))
    #~ return HttpResponseRedirect(reverse('sequencer:projects'))

def getBamReviewed(request,experiment_name):
    logger.info("##########################")
    logger.info("START getBamReviewed() view")
    logger.info("##########################")
    logger.info("Check User autentification")
    usermail=request.user.username
    if request.user.is_authenticated():
        logger.debug("User logged as ; %s",request.user.username)    
    else:
        logger.error("No user autentificated, No able to pursue further the analysis")
    logger.info("##########################")
    logger.info("Parsed User Request")
    logger.info("##########################")    
    UserRequest=request.POST
    myCheckedBam=[]
    for key, val in UserRequest.iteritems():
        #~ print str(key)
        #~ print str(val)
        if 'plasmaCheckboxValue' in str(key):
            myCheckedBam.append(str(val))
    current_exp = Experiments.objects.get(run_name=experiment_name)
    experimentsDict=json.loads(current_exp.dictionnary)
    bamtoDl=[]
    #create here the local history
    #add the bam like this throught the experiments
    currentuser= GalaxyUsers.objects.get(user_email=usermail)
    PlasmaWorkflow= Workflows.objects.get(name='Plasma_mutation')   
    local_history=GalaxyJobs(tag_id=id_generator(),
    history_user_email=currentuser,
    resultsName=experimentsDict['resultsName'],
    history_analyse_type=PlasmaWorkflow,
    progression="suspendu",
    history_download=False,
    galaxy_dictionnary=json.dumps(experimentsDict))
    logger.info("save the galaxyJobs object")    
    local_history.save()     
    for bamfileTag in myCheckedBam:
        try:
            currentBam=current_exp.experimentrawdata_set.get(ionTag=bamfileTag)
            local_history.list_experimentRawData.add(currentBam)
            bamtoDl.append(str(currentBam.bam_path))
            local_history.save()        
        except ExperimentRawData.DoesNotExist:
            currentBam = None
            logger.error("This bam is not not avaible in this experiment")     
        logger.info(str(currentBam.bam_path).split("/")[len(str(currentBam.bam_path).split("/"))-1])
        logger.info("##########################")
    logger.info("##########################")    
    logger.info("CREATE INPUT FOLDER FROM PROTON NAS_DIR/%s/bam",experimentsDict['resultsName'])     
    if not os.path.exists(nasInput+experimentsDict['resultsName']+plasmaFolderName):
        os.makedirs(nasInput+experimentsDict['resultsName']+plasmaFolderName)
        
    logger.info("CREATE RESULTS FOLDER FROM GALAXY NAS_DIR/RESULTS/%s/bam",experimentsDict['resultsName'])     
    if not os.path.exists(nasResults+experimentsDict['resultsName']+plasmaFolderName):
        os.makedirs(nasResults+experimentsDict['resultsName']+plasmaFolderName)
    local_history.save()    
    logger.info("##########################")
    logger.info("Connect to the server : %s",sequencer_severName )     
    logger.info("##########################")    
    logger.info("Copy data throught ssh and scp")
    logger.debug("##########################")        
    #~ logger.debug(experimentsDict['bammd5sum'])
    template = loader.get_template('sequencer/plasma_Main.html')    
    logger.debug("##########################")           
    logger.debug("go the GalaxyUser"+currentuser.user_email)   
    logger.debug("##########################")      
    bamFileName=bamtoDl
    context = {
        'current_exp': current_exp,
        #~ 'experimentsDict':experimentsDict['bamForPlasma'], #will print the bam absolut path
        'experimentsDict':bamFileName,
        #~ 'historyPlasma': "yoyo",
    }      
    #this tasks will be run before by celery as a baground event
    #~ tasks.task_Download_RawData() 
    return HttpResponse(template.render(context, request)) 


def getBamFromNgsData(request,experiment_name):
    logger.info("##########################")
    logger.info("START getBamFromNgsData() view")
    logger.info("##########################")
    logger.info("Check User autentification")
    usermail=request.user.username
    if request.user.is_authenticated():
        logger.debug("User logged as ; %s",request.user.username)
    else:
        logger.error("No user autentificated, No able to pursue further the analysis")
        
    logger.info("##########################")
    logger.info("Parsed User Request")
    logger.info("##########################")    
    UserRequest=request.POST
    myCheckedBam=[]
    for key, val in UserRequest.iteritems():
        #~ print str(key)
        #~ print str(val)
        if 'plasmaCheckboxValue' in str(key):
            myCheckedBam.append(str(val))
    current_exp = savedNGSData.objects.get(folder_name=experiment_name)
    #~ experimentsDict=json.loads(current_exp.dictionnary)
    bamtoDl=[]
    #create here the local history
    #add the bam like this throught the experiments
    currentuser= GalaxyUsers.objects.get(user_email=usermail)
    #~ PlasmaWorkflow= Workflows.objects.get(name='Plasma_mutation')   
    PlasmaSamtools= Workflows.objects.get(name='demo_samtools')   
    local_history=GalaxyJobs(tag_id=id_generator(),
    history_user_email=currentuser,
    resultsName=current_exp.folder_name,
    history_analyse_type=PlasmaSamtools,
    progression="suspendu",
    history_download=False,
    galaxy_dictionnary=json.dumps(json.loads(current_exp.dataDictionnary)))
    logger.info("save the galaxyJobs object")
    local_history.save()
    for bamfileTag in myCheckedBam:
        try:
            currentBam=current_exp.ngsbamdata_set.get(ionTag=bamfileTag)
            local_history.list_experimentRawData.add(currentBam)
            bamtoDl.append(str(currentBam.bam_path))
            local_history.save()        
        except NGSBamData.DoesNotExist:
            currentBam = None
            logger.error("This bam is not not avaible in this experiment")     
        logger.info(str(currentBam.bam_path).split("/")[len(str(currentBam.bam_path).split("/"))-1])
        logger.info("##########################")
    logger.info("##########################")    
    local_history.save()    
    logger.info("##########################")
    logger.info("Connect to the server : %s",sequencer_severName )     
    logger.info("##########################")    
    logger.info("Copy data throught ssh and scp")
    logger.debug("##########################")        
    #~ logger.debug(experimentsDict['bammd5sum'])
    template = loader.get_template('sequencer/plasma_Main.html')    
    logger.debug("##########################")           
    logger.debug("go the GalaxyUser"+currentuser.user_email)   
    logger.debug("##########################")      
    bamFileName=bamtoDl
    context = {
        'current_exp': current_exp,
        'experimentsDict':bamFileName,
    }      
    #this tasks will be run before by celery as a baground event
    #~ tasks.task_Download_RawData() 
    return HttpResponse(template.render(context, request)) 
 
         #~ 'historyPlasma': "yoyo",
   
        #~ 'experimentsDict':experimentsDict['bamForPlasma'], #will print the bam absolut path
    
    #~ logger.info("CREATE INPUT FOLDER FROM PROTON NAS_DIR/%s/bam",experimentsDict['resultsName'])     
    #~ if not os.path.exists(nasInput+experimentsDict['resultsName']+plasmaFolderName):
        #~ os.makedirs(nasInput+experimentsDict['resultsName']+plasmaFolderName)
        #~ 
    #~ logger.info("CREATE RESULTS FOLDER FROM GALAXY NAS_DIR/RESULTS/%s/bam",experimentsDict['resultsName'])     
    #~ if not os.path.exists(nasResults+experimentsDict['resultsName']+plasmaFolderName):
        #~ os.makedirs(nasResults+experimentsDict['resultsName']+plasmaFolderName)
