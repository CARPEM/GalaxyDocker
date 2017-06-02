from __future__ import unicode_literals

from django.db import models

# Create your models here.
import datetime
from django.utils import timezone
from django.contrib.postgres.fields import JSONField

# Create your models here.
class Experiments(models.Model):
	#~ text do not have limits
    run_name = models.TextField(primary_key=True)
    ftpStatus = models.TextField(default='no ftpstatus')
    status = models.TextField(default='no status')
    cnvFileName = models.TextField(default='no cnv')
    resultsQuery = models.TextField( default='no results')
    dateIonProton = models.TextField(default='no date')
    #~ dictionnary = JSONField(default='')
    dictionnary = models.TextField( default='no dict')


    def __str__(self):
        return self.run_name
 
class ExperimentRawData(models.Model):
    #~ text do not have limits
    ionTag = models.TextField(default='no tag')
    sampleName = models.TextField(default='no sample name')
    bam_path = models.TextField(default='no path')
    
    experienceName = models.ForeignKey(Experiments, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.bam_path
       
class GalaxyUsers(models.Model):
    #~ text do not have limits
    user_id = models.CharField(max_length=200)
    user_email = models.CharField(max_length=200,primary_key=True)
    user_aphid = models.CharField(max_length=200)
    user_apikey = models.CharField(max_length=200,default='no_apikey')
    
    
    def __str__(self):
        return self.user_email

class Supportedfiles(models.Model):
    #~ text do not have limits
    dataHandle = models.TextField(default='dataHandle')
    dataDescription = models.TextField(default='dataDescription')
    dataFormatEdamOntology = models.TextField(default='dataFormatEdamOntology')
   
    def __str__(self):
        return (self.dataDescription +" "+self.dataFormatEdamOntology)
 
class WorkflowsTools(models.Model):
    #~ text do not have limits
    primary_name = models.CharField(max_length=200,default='no_name',primary_key=True)
    name = models.CharField(max_length=200,default='no_name')
    version = models.CharField(max_length=200,default='version')
    inputlist= models.ManyToManyField(Supportedfiles,related_name='inputlist')
    outputlist = models.ManyToManyField(Supportedfiles,related_name='outputlist')
    def __str__(self):
        return (self.name +" "+self.version)
        
class Workflows(models.Model):
    #~ text do not have limits
    name = models.TextField(default='no_name',primary_key=True)
    description = models.TextField(default='description')
    tools_list= models.ManyToManyField(WorkflowsTools)
    
    def __str__(self):
        return (self.name +" "+self.description)

class UserCommonJobs(models.Model):
    #~ text do not have limits
    job_id = models.TextField(default='no job ID',primary_key=True)
    job_user_email = models.ForeignKey(GalaxyUsers,on_delete=models.CASCADE)
    job_create_time = models.TextField(default='no create_time')
    job_state = models.TextField(default='no status')
    job_exit_code = models.TextField(default='no exit_code')
#   job_tool_id = models.TextField( default='no tool_id')
    job_tool_id = models.ForeignKey(WorkflowsTools, on_delete=models.CASCADE)
    job_stderr = models.TextField( default='stderr')
    job_stdout = models.TextField( default='stdout')
    job_params = models.TextField( default='params')
    job_outputs = models.TextField( default='outputs')
    job_inputs = models.TextField( default='inputs')
    
    def __str__(self):
        return (self.job_user_email.user_email +" "+self.job_tool_id.primary_name+" "+self.job_params)

class GalaxyJobs(models.Model):
    #~ Put here info about tools state tools info tools id such as version and so and so
    tag_id=models.CharField(max_length=200,default='no_tag',primary_key=True) #personal
    resultsName = models.TextField(default='no_resultsName') #from Proton
    history_id = models.CharField(max_length=200,default='no_id') #from GALAXY
    history_name = models.CharField(max_length=200,default='no_name') #from GALAXY
    #~ history_user_email = models.CharField(max_length=200,default='no_email')
    history_user_email = models.ForeignKey(GalaxyUsers, on_delete=models.CASCADE) #from GalaxyUsers
    #~ history_analyse_type = models.CharField(max_length=200,default='no_type') #from Workflows
    history_analyse_type = models.ForeignKey(Workflows) #from Workflows
    history_state = models.CharField(max_length=200,default='no_state')#from GALAXY
    history_today = models.CharField(max_length=200,default='no_day')#from GALAXY
    history_percent_complete = models.CharField(max_length=200,default='no_complete')#from GALAXY
    #a comma separated list of ids
    list_experimentRawData = models.ManyToManyField(ExperimentRawData) #from ExperimentRawData
    history_datasets_id = models.TextField(default='no_datasets')#from GALAXY
    history_download = models.BooleanField(default=False)#from GALAXY (download results)
    #~ history_upload = models.BooleanField(default=False)#from GALAXY (upload rawdata)
    #~ #suspendu,en_cours,en_upload, complet
    #~suspendu -->et history_download=False le job a ete creer par l'utilisateur
    #~ en_cours --> et history_download=False le telechargement des donnees sur le nas est en train de s'effectuer
    #~ en_upload--> et history_download=True et history_upload=True le telechargement des donnees sur le nas est effectuer
    #~ Les donnees sont chargees dans galaxy
    progression = models.CharField(max_length=200,default='suspendu') 
    galaxy_dictionnary=  models.TextField( default='no dict')
    
    
    def __str__(self):
        return ("JOB TAG :"+self.tag_id+"\nHISTORY NAME : "+self.history_name+"\nCREATED FOR USER : "+self.history_user_email.user_email)
