from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
import localFunctions

from celery.decorators import task
logger = get_task_logger(__name__)
#~ tuto celery
#~ http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html#using-celery-with-django
#~ http://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html#first-steps
#~ http://docs.celeryproject.org/en/latest/userguide/tasks.html#custom-states
@task(name="sum_two_numbers")
def add(x, y):
    return x + y

@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="task_Download_RawData",
    ignore_result=True
)
def task_Download_RawData():
    """
    start download rawdata from sequencer
    """
    logger.info("start download history")

    localFunctions.Download_NGS_RawData()
    logger.info("end download")

#~ @periodic_task(
    #~ run_every=(crontab(minute='*/1')),
    #~ name="task_Download_RawData",
    #~ ignore_result=True
#~ )
#~ def task_Download_RawData():
    #~ """
    #~ start download rawdata from sequencer
    #~ """
    #~ logger.info("start download history")
#~ 
    #~ localFunctions.Download_RawData()
    #~ logger.info("end download")
    #~ 

@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="task_sendReminder",
    ignore_result=True
)
def task_sendReminder():
    """
    Send email if the data are ready for the user
    """
    logger.info("Review Galaxy Jobs")
    localFunctions.sendReminder_JobIsDone()
    logger.info("end Galaxy Jobs")

@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="task_Download_Data_clean",
    ignore_result=True
)
def task_Download_Data_clean():
    """
    Start to download data from the proton directly by looking at the file name.
    """
    logger.info("Review state of data to download")
    localFunctions.Download_Data_clean()
    logger.info("end of the review")





#~ 
#~ @periodic_task(
    #~ run_every=(crontab(minute='*/1')),
    #~ name="task_checkUsersJobs",
    #~ ignore_result=True
#~ )
#~ def task_checkUsersJobs_cron():
    #~ """
    #~ check each user jobs
    #~ """
    #~ logger.info("check user galaxy Jobs")
    #~ localFunctions.checkUsersJobs()
    #~ logger.info("check user galaxy Jobs")
