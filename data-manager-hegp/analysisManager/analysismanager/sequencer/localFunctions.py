from datamanagerpkg import ProtonCommunication_data_manager
from datamanagerpkg import GalaxyCommunication_data_manager
from .models import Experiments, GalaxyUsers ,toDownloads 
from .models import GalaxyJobs, ExperimentRawData , savedNGSData
from .models import UserCommonJobs,Supportedfiles, NGSBamData
from .models import Workflows,WorkflowsTools
from pprint import pprint
import logging
import json
import os
import time
import requests
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
#~ from .forms import UserForm
from bioblend.galaxy import GalaxyInstance

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

##########################
#URL SEQUENCER
##########################
from GlobalVariables import sequencer_base_url 
from GlobalVariables import sequencer_root_base_url 
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
##########################
#NAs DIr folder
##########################
from GlobalVariables import nasInput
from GlobalVariables import CNVfolderName
from GlobalVariables import plasmaFolderName
from GlobalVariables import nasResults
from GlobalVariables import workflowPath
from GlobalVariables import toolsInformation
from GlobalVariables import nasBackupFolder

##########################
#SMTP folder
##########################
from GlobalVariables import smtpServerAphp
from GlobalVariables import smtpPortServer
from GlobalVariables import fromAddrOfficial
#~ import Prod_performRunProtonBackup
import local_ProtonBackup
#~ pathtoNasbackup="/nas_backup/backupNGS_new/"
pathtoNasbackup="/nas_backup"
##########################
#LOGGER
##########################
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s -- %(name)s - %(levelname)s : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=logging.INFO)
#logger.setLevel(logging.DEBUG)
tools_default = ["ucsc_table_direct1","CONVERTER_wiggle_to_interval_0","MAF_To_BED1","ratmine","lped2fpedconvert","mousemine","join1","cbi_rice_mart","ucsc_table_direct_archaea1","CONVERTER_interval_to_bed6_0","CONVERTER_interval_to_bigwig_0","wig_to_bigWig","MAF_To_Fasta1","metabolicmine","CONVERTER_maf_to_interval_0","Extract_features1","upload1","wc_gnu","pbed2ldindepconvert","CONVERTER_interval_to_bed12_0","random_lines1","modENCODEfly","gff_filter_by_attribute","gtf2bedgraph","ChangeCase","__EXPORT_HISTORY__","wiggle2simple1","GeneBed_Maf_Fasta2","CONVERTER_len_to_linecount","trimmer","createInterval","gff_filter_by_feature_count","Interval2Maf1","genomespace_exporter","Show tail1","barchart_gnuplot","microbial_import1","axt_to_concat_fasta","tabular_to_dbnsfp","Interval2Maf_pairwise1","CONVERTER_interval_to_bedstrict_0","CONVERTER_gff_to_bed_0","maf_by_block_number1","modmine","CONVERTER_gff_to_fli_0","flymine","MAF_Thread_For_Species1","CONVERTER_fasta_to_len","pbed2lpedconvert","vcf_to_maf_customtrack1","__SET_METADATA__","__IMPORT_HISTORY__","biomart","Sff_extractor","CONVERTER_bed_to_fli_0","secure_hash_message_digest","CONVERTER_fasta_to_bowtie_base_index","ebi_sra_main","MAF_Reverse_Complement_1","mergeCols1","gff2bed1","Grouping1","CONVERTER_maf_to_fasta_0","maf_limit_size1","sort1","Convert characters1","MAF_To_Interval1","CONVERTER_fasta_to_bowtie_color_index","genomespace_file_browser_prod","lped2pbedconvert","MAF_filter","CONVERTER_fasta_to_2bit","CONVERTER_fasta_to_tabular","gene2exon1","Cut1","Count1","MAF_Limit_To_Species1","ucsc_table_direct_test1","wormbase","maf_stats1","zebrafishmine","Filter1","Paste1","Interval_Maf_Merged_Fasta2","modENCODEworm","gtf_filter_by_attribute_values_list","Summary_Statistics1","qual_stats_boxplot","cat1","axt_to_lav_1","Grep1","eupathdb","lav_to_bed1","comp1","bed_to_bigBed","liftOver1","bed2gff1","gramenemart","hbvar","CONVERTER_interval_to_bed_0","yeastmine","Show beginning1","CONVERTER_sam_to_bam","wormbase_test","CONVERTER_picard_interval_list_to_bed6","Extract genomic DNA 1","Remove beginning1","flymine_test","CONVERTER_bed_to_gff_0","axt_to_fasta","addValue","MAF_split_blocks_by_species1"]


def sendmailwrapper(fromaddr,toaddr,subject,body) :
    try:
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        #~ msg['Subject'] = "SUBJECT OF THE EMAIL"
        msg['Subject'] = subject  
        body = body
        msg.attach(MIMEText(body, 'html'))
        server = smtplib.SMTP(smtpServerAphp, smtpPortServer)
        server.starttls()
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
    except Exception:
        logger.info("##########################")    
        logger.info("The smtp server is not avaiable please check your configuration")
def Download_Data_clean():
    #here again controle the state of the object
    toDownloadsData=toDownloads.objects.all()
    for dataRun in toDownloadsData :
        if dataRun.backupValidate == "en cours" :
            dataRun.backupValidate="en traitement"
            dataRun.save()
            #forced the copy of the run in order to be sure of the data integrity
            for runcopy in range(0,5):
                local_ProtonBackup.performWholeRunBackup(str(dataRun.folder_name))
            #~ create the file CompleteData.txt
            completData=open(pathtoNasbackup+str(dataRun.folder_name)+'/CompletedDownload.txt','w')
            completData.close()
            dataRun.backupValidate="Termin&egrave"
            dataRun.backupOnNas="True"
            dataRun.save()
            #~ Creation of the savedNGSData object
            try:
                thisNGSData = savedNGSData.objects.get(filesystempath=str(pathtoNasbackup)+"/"+str(dataRun.folder_name))
            except savedNGSData.DoesNotExist:
                thisNGSData = None
            if  thisNGSData == None: 
                thisNGSData = savedNGSData.objects.create(
                filesystempath=str(pathtoNasbackup)+"/"+str(dataRun.folder_name),
                folder_name=str(dataRun.folder_name),
                status="complete")
                thisNGSData.save()  
                thisNGSData.dataDictionnary=buildSampleNameDict(thisNGSData.folder_name)     
                thisNGSData.save()  
                buildBamDict(thisNGSData)
            users=GalaxyUsers.objects.all()
            body="""<p>Votre run  """+str(dataRun.folder_name) +""" est copi&eacute pour analyse plasma</p><p style="color:#2e1cb2";> """
            for thisUser in users :            
                sendmailwrapper(fromAddrOfficial,thisUser.user_email,"Copie de run Disponible",body)
            

#~ pathtoNasbackup
def updateBamStatus():
    AllNgsData=toDownloads.objects.all()
    for thisBackup in AllNgsData :
        #~ thisBackup.dataDictionnary=buildSampleNameDict(thisBackup.filesystempath+"/cov/",thisBackup.folder_name)
        thisBackup.dataDictionnary=buildSampleNameDict(folder_name)
        thisBackup.save()
    buildBamDict(thisBackup)
     
#######
def buildSampleNameDict(folderName):
    withoutAuto=str(folderName).replace("Auto_","").rstrip()
    #~ print(withoutAuto)
    withoutAutoTmp=withoutAuto.split('_')    
    cleanID=str("_".join(withoutAutoTmp[0:len(withoutAutoTmp)-1]))
    sampleNameDict=dict()
    try :
        resp = requests.get(sequencer_base_url+'/results/', auth=(sequencer_user,sequencer_password),params={"format": "json", "resultsName__endswith" : cleanID})
        resp_json = resp.json()
        #~ pprint(resp_json)
        adress=sequencer_root_base_url+str(resp_json['objects'][0]['eas'])
        #~ print 'this adress will be called to set up the sampleName'+adress
        resp_eas = requests.get(adress, auth=(sequencer_user,sequencer_password),params={"format": "json"})
        resp_eas_json = resp_eas.json()
        #~ pprint(resp_eas_json)
        for thisSampleName in resp_eas_json['barcodedSamples']:
            #~ print resp_eas_json['barcodedSamples'][thisSampleName]['barcodes']
            if len(resp_eas_json['barcodedSamples'][thisSampleName]['barcodes'])==1:
                sampleNameDict[resp_eas_json['barcodedSamples'][thisSampleName]['barcodes'][0]]=thisSampleName
            else:
                for ionTagElement in resp_eas_json['barcodedSamples'][thisSampleName]['barcodes'] :
                    sampleNameDict[ionTagElement]=thisSampleName
                    print "ionTagElement" +str(ionTagElement)   
    except requests.ConnectionError:
        print("Data server not available")
		
    bagOfBams=[f for f in os.listdir(nasBackupFolder+"/"+folderName+"/bam") if "bam" in f]	
    for fileBam in bagOfBams:
        thisfile=fileBam.split('.')[0]
        sampleNameDict[thisfile]=thisfile+'nomatchfromSequencer'
        
    return(sampleNameDict)

def buildBamDict(thisData):
    onlybamfiles = [thisData.filesystempath+"/bam/"+f for f in os.listdir(thisData.filesystempath+"/bam/") if os.path.isfile(thisData.filesystempath+"/bam/"+f)]
    onlybamfiles_clean = [f for f in onlybamfiles if f.endswith(".bam")]
    for thisBam in onlybamfiles_clean:
        try :
            tryBam = NGSBamData.objects.get(bam_path=str(thisBam))
        except NGSBamData.DoesNotExist:
            tryBam = None
        if  tryBam == None:
            ionExpressTag=str(thisBam).split("/")
            thisionTag=str(ionExpressTag[-1].split('.')[0])
            if thisionTag in json.loads(thisData.dataDictionnary):
                localDict=json.loads(thisData.dataDictionnary)
                newBam = NGSBamData(bam_path=str(thisBam),
                experienceName=thisData,
                ionTag=thisionTag,
                sampleName= localDict[thisionTag])
                newBam.save()
            else:
                print "key error, the key was not found on the dictionnary for sample"
                print thisBam+ "in run "+thisData.filesystempath
                newBam = NGSBamData(bam_path=str(thisBam),
                experienceName=thisData,
                ionTag=thisionTag,
                sampleName= thisionTag+"noSampleName")
                newBam.save()
    thisData.save()

def Download_NGS_RawData():
    logger.info("##########################")
    ticket_histories=GalaxyJobs.objects.all()
    for job in ticket_histories :
        #~ if job.progression=="suspendu":   
        #~ if job.progression=="suspendu":   
        if job.history_download==False:   
            if job.progression=="suspendu":
                job.progression="Download_in_progress"
                job.save()                
                bamtoDl=[]
                logger.info("Build the bamtoDL list for  : %s",job.tag_id )                 
                for bam in job.list_experimentRawData.all():
                    bamtoDl.append(bam.bam_path)
                #~ do not forgot to close the ssh connection()    
                #~ the data are downloaded, now you can create a new
                #~ Galaxy history
                job.history_download=True
                job.progression="Download_complete"
                #~ job.galaxy_dictionnary=json.dumps(z)
                job.save()
                job.progression="chargement_dans_galaxy"
                job.save()            
                logger.info("##########################")    
                logger.info("start Galaxy job")
                experimentsDict=json.loads(job.galaxy_dictionnary) 
                #~ z = experimentsDict.copy()
                #~ z.update(json.loads(job.galaxy_dictionnary)) 
                experimentsDict['resultsName']=job.resultsName
                experimentsDict['bamForPlasma']=bamtoDl
                job.galaxy_dictionnary=json.dumps(experimentsDict)                
                #~ confirmation telechargement 
                #~ sendmailwrapper(fromAddrOfficial,job.history_user_email.,subject,body)
                historyPlasma=GalaxyCommunication_data_manager.mainSamtools_fromNGSData(experimentsDict,galaxy_base_url,job.history_user_email.user_apikey,plasmaFolderName)
                #~ historyPlasma=GalaxyCommunication_data_manager.mainPlasma_fromNGSData(experimentsDict,galaxy_base_url,job.history_user_email.user_apikey,plasmaFolderName)
                job.history_id=historyPlasma['id']
                job.history_name=historyPlasma['name']
                job.history_today=historyPlasma['today']
                job.progression="chargement_dans_galaxy_complet"
                #~ confirmation lancement de galaxy
                job.save()
                body="""<p>Votre analyse &agrave; &eacute;t&eacute; ajout&eacute;e &agrave; l'historique:\n</p><p style="color:#2e1cb2";> """+job.history_name+""".\n</p>
                """+str(job.list_experimentRawData.count()) +""" &eacute;chantillon(s) est(sont) en cours de traitement. Vous pourrez les trouver en cliquant sur le lien
                <p><a href='"""+galaxy_base_url+"""/history/view_multiple'> <img src="http://www.carpem.fr/wp-content/themes/carpem/img/logo.gif" /></a></p>
                """
                sendmailwrapper(fromAddrOfficial,str(job.history_user_email.user_email)," Analyse Plasma dans Galaxy",body)
             #~ will be put in other function
            else:
                logger.info("##########################")    
                logger.info("Ce Job est deja pris en charge dans une task de telechargement de donnees")				
                continue



#~ def buildSampleNameDict(runPath):
    #~ onlyCovDir = [runPath+"/"+f for f in os.listdir(runPath) if os.path.isdir(runPath+"/"+f)]
    #~ bcsummaryfile = [onlyCovDir[0]+"/"+f for f in os.listdir(onlyCovDir[0]) if f.endswith('.bc_summary.xls')]
    #~ sampleNameDict=dict()
    #~ with open(onlyCovDir[0]+'/startplugin.json') as rawJson:
        #~ json_data = json.load(rawJson)
    #~ for sampleNameTag in json_data['plan']['barcodedSamples'] :
        #~ sampleNameDict[json_data['plan']['barcodedSamples'][sampleNameTag]['barcodes'][0]]=sampleNameTag
    #~ return(sampleNameDict)
    #~ d['plan']['barcodedSamples']['17PG289']['barcodes'][0]
     
    #~ with open(onlyCovDir[0]+'/results.json') as rawJson:
        #~ json_data = json.load(rawJson)
    #~ for ionXpressTag in json_data['barcodes'] :
        #~ sampleNameDict[ionXpressTag]=json_data['barcodes'][ionXpressTag]['Sample Name']

    
#~ d["barcodes"]['IonXpress_001']["Sample Name"]
    #~ bcsummary=open(bcsummaryfile[0],'r').readlines()
    #~ sampleNameDict=dict()
    #~ for line in bcsummary:
        #~ element=line.split("\t")
        #~ if "Barcode" not in element[0]:
            #~ sampleNameDict[element[0]]=element[1]
            
    #~ folder_name = models.TextField(primary_key=True)
    #~ filesystempath = models.TextField(default='no filesystempath')
    #~ reference = models.TextField(default='no reference')
    #~ status = models.TextField(default='no status')
    #~ timeStamp = models.TextField(default='no timeStamp')
    #~ timeToComplete = models.TextField( default='no timeToComplete')
    #~ backupOnNas = models.TextField(default='false')
    #~ backupValidate = models.TextField(default='false')
    #~ diskusage = models.TextField(default='data 0')
    

#~ def reloadStatus():
    #~ savedData_list = savedNGSData.objects.all() 
    #~ if len(savedData_list) != 0 :
        #~ for localDir in savedData_list:
            #~ thisDownloadData=""
            #~ try :
                #~ thisDownloadData=toDownloads.objects.get(folder_name=thisDownloadData['folder_name'])
                #~ thisDownloadData.backupOnNas="True"
                #~ thisDownloadData.save()
            #~ except toDownloads.DoesNotExist :
                #~ thisDownloadData = None
  
def Download_RawData():
    logger.info("##########################")
    ticket_histories=GalaxyJobs.objects.all()
    for job in ticket_histories :
        #~ if job.progression=="suspendu":   
        #~ if job.progression=="suspendu":   
        if job.history_download==False:   
            if job.progression=="suspendu":
                job.progression="Download_in_progress"
                job.save()                
                bamtoDl=[]
                logger.info("Build the bamtoDL list for  : %s",job.tag_id )                 
                for bam in job.list_experimentRawData.all():
                    bamtoDl.append(bam.bam_path)
                logger.info("Connect to the server : %s",sequencer_severName )     
                sshProton=ProtonCommunication_data_manager.sshConnection(
                sequencer_severName,sequencer_user,sequencer_password)
                logger.info("##########################")    
                logger.info("Copy data throught ssh and scp")
                experimentsDict=ProtonCommunication_data_manager.backgroundcopyDataBamtask(
                json.loads(job.galaxy_dictionnary),job.resultsName,bamtoDl,sshProton,nasInput,plasmaFolderName)
                z = experimentsDict.copy()
                z.update(json.loads(job.galaxy_dictionnary)) 
                experimentsDict['resultsName']=job.resultsName
                #~ do not forgot to close the ssh connection()    
                sshProton.close()
				#~  the data are downloaded, now you can create a new
				#~  Galaxy history
                job.history_download=True
                job.progression="Download_complete"
                job.galaxy_dictionnary=json.dumps(z)
                #~ job.galaxy_dictionnary=json.dumps(experimentsDict)
                job.save()
                #~ will be put in other function
            else:
                logger.info("##########################")    
                logger.info("Ce Job est deja pris en charge dans une task de telechargement de donnees")				
                continue
        elif job.progression=="Download_complete":                 
            job.progression="chargement_dans_galaxy"
            job.save()            
            logger.info("##########################")    
            logger.info("start Galaxy job")
            experimentsDict=json.loads(job.galaxy_dictionnary) 
            #confirmation telechargement 
            #~ sendmailwrapper(fromAddrOfficial,job.history_user_email.,subject,body)
            historyPlasma=GalaxyCommunication_data_manager.mainPlasma_fromNGSData(experimentsDict,galaxy_base_url,job.history_user_email.user_apikey,plasmaFolderName)
            job.history_id=historyPlasma['id']
            job.history_name=historyPlasma['name']
            job.history_today=historyPlasma['today']
            job.progression="chargement_dans_galaxy_complet"
            #confirmation lancement de galaxy
            job.save()
            body="""<p>Votre analyse &agrave; &eacute;t&eacute; ajout&eacute;e &agrave; l'historique:\n</p><p style="color:#2e1cb2";> """+job.history_name+""".\n</p>
            """ + str(job.list_experimentRawData.count()) +""" &eacute;chantillon(s) est(sont) en cours de traitement. Vous pourrez les trouver en cliquant sur le lien
            
           <p><a href='"""+galaxy_base_url+"""/history/view_multiple'> <img src="http://www.carpem.fr/wp-content/themes/carpem/img/logo.gif" /></a></p>

            """
            sendmailwrapper(fromAddrOfficial,str(job.history_user_email.user_email)," Analyse Plasma dans Galaxy",body)
            
        else:
            logger.info("##########################")    
            logger.info("Ce Job est deja fini ou pris en charge dans une task d'execution de Galaxy")			
            continue

def sendReminder_JobIsDone():
    logger.info("##########################")
    ticket_histories=GalaxyJobs.objects.all()  
    for job in ticket_histories :
        if job.progression=="chargement_dans_galaxy_complet":
            logger.info("##########################")    
            logger.info("Ce Job est en cours d'analyse")
            gi=GalaxyCommunication_data_manager.galaxyConnection(galaxy_base_url,job.history_user_email.user_apikey)
            if (gi.histories.get_status(str(job.history_id))['percent_complete']==100 ):
                logger.info("##########################")    
                logger.info("Un mail sera envoye a l'utilisateur")
                body="""<p>Votre analyse est termin&eacute;e. Les r&eacute;sultats sont disponibles dans votre historique:\n</p><p style="color:#2e1cb2";> """+job.history_name+""".\n</p>
                <p><b>Bilan:</b></p><table style="width:100%" border="1">
                <tr>
                <th>Information</th><th>R&eacute;sultats</th><th>R&eacute;sultats attendu</th>
                </tr>
                <tr>
                <td>Fichier(s) complet(s) </td><td>"""+str(gi.histories.get_status(str(job.history_id))['state_details']['ok']) +"""</td><td>"""+str((6*job.list_experimentRawData.count())+job.list_experimentRawData.count() )+ """</td>
                </tr>
                <tr>                
                <td>Fichier(s) en erreur </td><td>"""+str(gi.histories.get_status(str(job.history_id))['state_details']['error']) +"""</td><td>0</td>
                </tr>
                <tr>                
                <td>Fichier(s) vide </td><td>"""+str(gi.histories.get_status(str(job.history_id))['state_details']['empty']) +"""</td><td>0</td>
                </tr>
                </table>
                <p> Vous pourrez les trouver en cliquant sur le lien
                </p>
            <p><a href='"""+galaxy_base_url+"""/history/view_multiple'> <img src="http://www.carpem.fr/wp-content/themes/carpem/img/logo.gif" /></a></p>
                
            """
                sendmailwrapper(fromAddrOfficial,str(job.history_user_email.user_email),"Plasma Complet disponible dans Galaxy",body)
                job.progression="Complet"
                job.save()

def download_data_Histories():
    logger.info("##########################")
    histories=GalaxyJobs.objects.all()
    base_url=galaxy_base_url   
    
    for job in histories :
        if job.history_download==False:
            currentuser=GalaxyUsers.objects.get(user_email=job.history_user_email)
            gi=GalaxyCommunication_data_manager.galaxyConnection(base_url,currentuser.user_apikey)
            status=gi.histories.get_status(job.history_id)
            history_info=gi.histories.show_history(job.history_id, contents=True)
            datasetslist=""
            for dataset in history_info:
                datasetslist=datasetslist+str(dataset['dataset_id'])+";"            
  
            job.history_state=status['state']
            job.history_percent_complete=str(status['percent_complete'])
            job.history_datasets_id=datasetslist
            
            job.save()
            logger.info(str(job.history_percent_complete))
            logger.info(str(job.history_state))
            logger.info(str(datasetslist))
            
            if job.history_percent_complete == "100" :
                logger.info( "job found at 100")
                for dataset in job.history_datasets_id.split(';'):
                    if dataset != '' :
                        logger.info( "dataset is downloading")
                        logger.info( str(dataset))
                        gi.datasets.download_dataset(dataset,
                        file_path="/nas_Dir/results/",
                        use_default_filename=True, wait_for_completion=True)
                job.history_download=True

     
def buildJobHistory(currentuser,historyCNV):
    logger.info("##########################")
    base_url=galaxy_base_url   
    gi=GalaxyCommunication_data_manager.galaxyConnection(base_url,currentuser.user_apikey)
    status=gi.histories.get_status(historyCNV['id'])
    history_info=gi.histories.show_history(historyCNV['id'], contents=True)
    #~ print str(gi.histories.get_status(historyCNV['id']))
    #~ print str(gi.histories.show_history(historyCNV['id'], contents=True))
    datasetslist=""
    for dataset in history_info:
        datasetslist=datasetslist+str(dataset['dataset_id'])+";"
    try:
        local_history = GalaxyJobs.objects.get(history_id=historyCNV['id'])
    except GalaxyJobs.DoesNotExist:
        local_history = None
#~ #if none create a new user

    if  local_history == None:
        logger.info( "a none value create a new local_history")
        local_history=GalaxyJobs(history_id=historyCNV['id'],
        history_name=historyCNV['name'], history_today=historyCNV['today'],
        history_user_email=currentuser.user_email,
        history_analyse_type="CNV", history_state=status['state'],
        history_percent_complete=status['percent_complete'],
        history_datasets_id=datasetslist
        )
        local_history.save()
        if local_history.history_percent_complete != 100 :
            buildJobHistory(currentuser,historyCNV)
        else :
            for dataset in local_history.history_datasets_id.split(';'):
                if dataset != '' :
                    gi.datasets.download_dataset(dataset,
                    file_path="/nas_Dir/results/",
                    use_default_filename=True, wait_for_completion=True)

    else:
        local_history=GalaxyJobs(history_state=status['state'],
        history_percent_complete=status['percent_complete'],
        history_datasets_id=datasetslist
        )
        local_history.save()
        if local_history.history_percent_complete != 100 :
            buildJobHistory(currentuser,historyCNV)
        else :
            for dataset in local_history.history_datasets_id.split(';'):
                if dataset != '' :
                    gi.datasets.download_dataset(dataset,
                    file_path="/nas_Dir/results/",
                    use_default_filename=True, wait_for_completion=True)
    logger.info( "##########################")
    logger.info( "checkusers from getGalaxyUsers")
    logger.info( "##########################")
    #~ # Always return an HttpResponseRedirect after successfully dealing
    #~ with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
    return (1)  





def AddaWorkflowTool(this_tool):
    try:
        tryexp = WorkflowsTools.objects.get(primary_name=str(this_tool[0]['id']+"_"+this_tool[0]['version']+".json"))
    except WorkflowsTools.DoesNotExist:
        tryexp = None
        logger.info("tool found was not added to the DB. We Add now this new tool")
        newtool=WorkflowsTools(primary_name=str(this_tool[0]['id']+"_"+this_tool[0]['version']+".json"),
        name=str(this_tool[0]['id']),
        version=str(this_tool[0]['version']))
        newtool.save()
        logger.info("Add the tool definition to the Workflow and link it to the current workflow.")
        logger.info("Name of the json file where the tool is define:" +str(this_tool[0]['id']+"_"+this_tool[0]['version']+".json"))
        #create a tool 
        with open(toolsInformation+str(this_tool[0]['id']+"_"+this_tool[0]['version']+".json")) as data_file_tool:    
            tool = json.load(data_file_tool)
            logger.info("#######################INPUT")
            for dataInput in tool['function'][0]['input'] :
                try:
                    tryexp = Supportedfiles.objects.get(dataDescription=str(dataInput['dataDescription']))
                except Supportedfiles.DoesNotExist:
                    tryexp = None
                    newfile=Supportedfiles(dataHandle=str(dataInput['dataHandle']),dataDescription=str(dataInput['dataDescription']),dataFormatEdamOntology=str(dataInput['format'][0]['uri'])) 
                    newfile.save()
                    newtool.inputlist.add(newfile)
                    newtool.save()
                       #~ print("#######################dataInpty")
            logger.info("#######################OUTPUT")
            for dataInput in tool['function'][0]['input'] :
                try:
                    tryexp = Supportedfiles.objects.get(dataDescription=str(dataInput['dataDescription']))
                except Supportedfiles.DoesNotExist:
                    tryexp = None
                    newfile=Supportedfiles(dataHandle=str(dataInput['dataHandle']),dataDescription=str(dataInput['dataDescription']),dataFormatEdamOntology=str(dataInput['format'][0]['uri']) )
                    newfile.save()  
                    newtool.outputlist.add(newfile)
                    newtool.save()



def updateJobStatus(userGalaxy):
    gi=GalaxyCommunication_data_manager.galaxyConnection(galaxy_base_url,str(userGalaxy.user_apikey))
    jobsList=gi.jobs.get_jobs()
    for currentJob in jobsList:
        #check if the job exist if not create a new job
        logger.info("#######################")
        newJob=gi.jobs.show_job(str(currentJob['id']), full_details=True)
        print(newJob)    
        tryGetJob = None
        try:
            tryGetJob = UserCommonJobs.objects.get(job_id=str(newJob['id']))
            logger.info(" the job exist already")
        except UserCommonJobs.DoesNotExist:
            tryGetJob = None
            if (tryGetJob == None):
                logger.info("Add a new Galaxy Job") 
                if str(newJob['tool_id']) not in  tools_default:
                    logger.info("add a new tool")
                    this_tool=gi.tools.get_tools(newJob['tool_id'])
                    AddaWorkflowTool(this_tool)
                else:
                    logger.info("Add a default tool which is not linked to edam Ontology. They are not treated by Regate")
                    this_tool=gi.tools.get_tools(newJob['tool_id'])
                    try:
                        tryexp = WorkflowsTools.objects.get(primary_name=str(this_tool[0]['id']+"_"+this_tool[0]['version']+".json"))
                    except WorkflowsTools.DoesNotExist:
                        tryexp = None
                        logger.info("tool found was not added to the DB. We Add now this new tool")
                        newtool=WorkflowsTools(primary_name=str(this_tool[0]['id']+"_"+this_tool[0]['version']+".json"),
                        name=str(this_tool[0]['id']),
                        version=str(this_tool[0]['version']))
                        newtool.save()
                        
                theTool=None
                this_tool=gi.tools.get_tools(newJob['tool_id'])
                try:
                    theTool = WorkflowsTools.objects.get(primary_name=str(this_tool[0]['id']+"_"+this_tool[0]['version']+".json"))
                except WorkflowsTools.DoesNotExist:
                    logger.info("No tool here")
                    continue
                logger.info("Add a new Galaxy Job") 
                job_local=UserCommonJobs(
                job_user_email = userGalaxy,job_id = str(newJob['id']),
                job_create_time =str(newJob['create_time']),job_state = str(newJob['state']),
                job_exit_code = str(newJob['exit_code']),job_tool_id = theTool,
                job_stderr = str(newJob['stderr']),job_stdout = str(newJob['stdout']),
                job_params = str(newJob['params']),job_outputs = str(newJob['outputs']),
                job_inputs = str(newJob['inputs']))
                job_local.save()




def checkUsersJobs():
    if GalaxyUsers.objects.count()!=0:
        for local_user in GalaxyUsers.objects.all():
            logger.info("#######################")
            logger.info("check user :"+str(local_user.user_email))
            updateJobStatus(local_user)
    else:
        logger.info("no user in the DB")
