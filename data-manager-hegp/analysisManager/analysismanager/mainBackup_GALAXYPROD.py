#~ import django
import performRunProtonBackup
import sequencer.localFunctions as localFunctions
import os

#BACKUP NAS TO NAS
nasroot='/nas_Dir'
nasbackup='/nas_backup/backupNGS_new'
fromadr="william.digan@aphp.fr"
#FROM nascarp1 to nasgalaxy1

inputFileToProcess="/nas_backup/ionprotonRunName.txt"
inputrun=open(inputFileToProcess,"r")

runtocopy=[]

for line in inputrun.readlines():
    print" this line "+line
    if "_tn" not in line.rstrip() :
        print "no tn:"+line.rstrip()
        if line.rstrip() != "":
            runtocopy.append(line.rstrip())
    else :
        print "not the right folerdname"
print runtocopy
for run in runtocopy:
    body="""backup de donnee du run """+str(run)+""" en cours
    """
    localFunctions.sendmailwrapper(fromadr,fromadr,"backup de donnee",body)
    performRunProtonBackup.performWholeRunBackup(str(run))
    body="""backup de donnee du run """+str(run)+""" terminee
    """
    localFunctions.sendmailwrapper(fromadr,fromadr,"backup du run terminee",body)
