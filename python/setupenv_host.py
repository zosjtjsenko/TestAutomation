''' ***********************************************************************
  This script wil automatically setup a testenvironment in a VM of choice.
  If the VM is running, a script on the guest will provoked.
  Flow of the program
   1. Ask user for ticket number
   4. Ask user for OS to test on
   6. Ask for single or single and multi server
   7. Take snapshot with the given ticketnumber as name
   8. Start snapshot
   9. Wait for guest to start up
   2. Ask user for TICS version number
   3. Ask user for TICS release number
   5. Download given TICS version and the lic.dat license
   10.
 ************************************************************************
'''
import virtualbox
import re
from subprocess import call
from subprocess import Popen
import time
import urllib
from xml.dom.minidom import parse
import xml.dom.minidom
import re
import os

#Create ticket data folder and add log file in the folder
def initializeTest(ticsversion):
    unused_cls_return_value= os.system('cls')
    ticketNumber = inputCheck("\nWhat ticket are you working on?")

    newfolder = "D:\\testDATA\\Ticket data\\" +str(ticketNumber)

    if not os.path.exists(newfolder):
        os.makedirs(newfolder)

	templateFile = newfolder + "\\" + str(ticketNumber) + "log"

    with open(templateFile, "wb") as f:
        f.write("TICS" + ticsversion + " Win7.1 32bit Chrome\n\n")
        f.write("Verified, seems to be working correctly.\n")
        f.write("Tested:\n")
        f.write("- Installed TICS 8.2.3.31019 in a clean VM\n")
	    		
    p = Popen(["notepad.exe", templateFile])
    #p.terminate()
	
    return ticketNumber

#InputVM method
def inputCheck(message):
    while True:
        try:
            userInput = int(input(message))   
        except ValueError:
            print("Enter a number please.")
            continue
        else:
            return userInput
            break	
			
#Create and start new snapshot
def startnewsnapshot(ticketNumber):
    # list of machines
    vbox = virtualbox.VirtualBox()
    vbox.machines 
    	
    #print menu for choosing the vm to snapshot
    unused_cls_return_value= os.system('cls') 
    print ("List of available test VM(s)")
    for idx, vm in enumerate(vbox.machines):
        print (str(idx)+ "  " + vm.name)
    
    #users input on what vm to take a snapshot from
    chosenVMnumber = inputCheck("\nFrom which VM do you want take a snapshot?")
    chosenVM = vbox.machines[chosenVMnumber]
    print "Chosen the VM:\n" + chosenVM.name
    
    #takes a snapshot of the chosen VM and starts the vm
    snapshotName = "Snapshot: "+ str(ticketNumber) 
    call (["VBoxManage", "snapshot", chosenVM.name, "take", snapshotName ])
    call (["VBoxManage", "startvm", chosenVM.name])
    
    # set size of vm
    call(["vboxmanage", "controlvm", chosenVM.name, "setvideomodehint", "2044", "1480", "32"]) 
    	
    #wait till the guest is booted. Need to do a <VBoxControl guestproperty set Wait_For_Logon_Event Event_Now_Set> on the guest	
    call(["VBoxManage", "guestproperty", "wait", chosenVM.name,  "Wait_For_Logon_Event"])	
    
    return snapshotName, chosenVM.name
	
#*****close restore previous and delete new snapshot***********************************
def closesnapshot(chosenVM,snapshotName):
     #Shutting down and deleting the snapshot
     print "Going to save the state"
     call(["VBoxManage", "controlvm", chosenVM, "savestate"]) 
     print "Going to restore snapshot "
     call(["VBoxManage", "snapshot", chosenVM, "restore", "Win7 +  VS 2015 (till 12-12-2016)(Only start by script)"])
     #delay is needed else it with produce error about a locked Snapshot
     time.sleep(5)
     print "Going to delete snaphot" + snapshotName
     call(["VBoxManage", "snapshot", chosenVM, "delete", snapshotName])
     
# Ask user what version of TICS he want to install (single or single + multi)***********************************
def getTicsInstaller(installerPath,licPath):
    maxVersion = 100
    urlList = []
    versionList = []
    dlURLList = []
    numberList = []
    installerType = ''
    
    unused_cls_return_value= os.system('cls')
    print "0. Single server install\n"
    print "1. Single and Multi server install\n"
    installerType = inputCheck("Select installer type\n")
    	
    # Receive the data from the xml api from Jenkins
    viewAll = "http://192.168.1.88:8080/view/All/api/xml"
    data = urllib.urlopen(viewAll)
    
    # Open XML document using minidom parser
    DOMTree = xml.dom.minidom.parse(data)
    collection = DOMTree.documentElement
    
    # Get all the jobs in allView 
    jobs = collection.getElementsByTagName("job")
    
    # Print detail of each build.
    for job in jobs:   
        name = job.getElementsByTagName('name')[0]
        #print "name: %s" % name.childNodes[0].data
        matchObj = re.match(r'TICS 8.[0-5].x$',name.childNodes[0].data)
        if matchObj:
            url = job.getElementsByTagName('url')[0]
            #print "url: %s" % url.childNodes[0].data			
            urlList.append( url.childNodes[0].data)
            versionList.append(name.childNodes[0].data)
        	
    # Output all version equals 8.0.x and above
    unused_cls_return_value= os.system('cls')
    for count, version in enumerate(versionList):		
        print str(count) + ".  " + version + " \n"		
    
    # Ask user what release he wants
    chosenRelease = inputCheck("\nSelect a TICS release?")
	
    # Add 
    artiLink = urlList[chosenRelease]
    ticsRelease = urlList[chosenRelease] + "api/xml"
    
    unused_cls_return_value= os.system('cls') 
    print "Chosen Release Version:\n" + versionList[chosenRelease] + "\n\n"
    	
    # Find out which builds are present for the chosen version 	
    dataticsversion = urllib.urlopen(str(ticsRelease))		
    DOMTree = xml.dom.minidom.parse(dataticsversion)
    collection = DOMTree.documentElement
    
    # Get all the builds from the job
    builds = collection.getElementsByTagName("build")
    			
    for count, build in enumerate(builds):
        buildNr = build.getElementsByTagName('number')[0]
        numberList.append(buildNr.childNodes[0].data)
        buildUrl = build.getElementsByTagName('url')[0]
        
        #print buildUrl.childNodes[0].data
        				
        buildInfoUrl = buildUrl.childNodes[0].data + "api/xml"
        #print buildInfoUrl + "\n"
        
        buildData = urllib.urlopen(buildInfoUrl)
        DOMTree = xml.dom.minidom.parse(buildData)
        collection = DOMTree.documentElement
        		
        artifactData = collection.getElementsByTagName("artifact")
        		
        for co, arti in enumerate(artifactData):
            artiName = arti.getElementsByTagName('fileName')[0]
             
            if co%2 == 1:
                print str(count) + ". " + artiName.childNodes[0].data + "\n\n"
                artil = arti.getElementsByTagName('relativePath')[0]
                artinode = artil.childNodes[0].data
                dlURLList.append(artinode)
        
        if count >=maxVersion:
            break
        	
    chosenVersion = inputCheck("\nSelect a TICS version?")
    ticsVersion = dlURLList[chosenVersion]
	
    # Prepare the downloadlocation for the urlretrieve function
    downloadLocation = artiLink + numberList[chosenVersion] + "/artifact/" + ticsVersion
    downloadLocationLic = artiLink + numberList[chosenVersion] + "/artifact/lic.dat"
    
    unused_cls_return_value= os.system('cls') 
    print "Chosen Version:\n" + downloadLocation
    
    # Download the installer and the lic.dat file	
    urllib.urlretrieve(downloadLocation, installerPath)
    urllib.urlretrieve(downloadLocationLic, licPath)
    
    # Returns the TICS version and the installerType (single or single + multi)
    return ticsVersion, installerType
    
    		
#************************** MAIN program starts here **************************
if (__name__ == "__main__"):
	#Download the right version of TICS from the Jenkins build servers
    ticsInstallerPath = "D:\\testDATA\sharedFolder\\tics.exe"
    licPath = "D:\\testDATA\sharedFolder\\lic.dat"	
	pythonPath = "C:\Python27\python.exe"
	setupGuestScriptPath = "E:\_Joppe\TestAutomating\python\setupenv_guest.py"
    ticsversion, installerType = getTicsInstaller(ticsInstallerPath, licPath)
     
    #ask ticketnumber and create folder in ticket data. add logfile (template) in the created folder 	
    ticketNumber = initializeTest(ticsversion)
     	
    #takesnapshot and start VM	
    snapshotName, chosenVM = startnewsnapshot(ticketNumber)	
	
	#vboxmanage guestcontrol "Win7 +  VS 2015  (Only start by script)" run --exe "C:\Python27\python.exe" --username "ieuser" --password "Passw0rd!" -- "python.exe" "E:\_Joppe\TestAutomating\python\setupenv_guest.py"
	call(["vboxmanage", "guestcontrol", chosenVM, "run",  "--exe", pythonPath, "--username","ieuser", "--password", "Passw0rd!", "--", "python.exe", setupGuestScriptPath, installerType])
	
          
     #if all the work on the guest is done
     #closesnapshot(chosenVM, snapshotName)
     
    # Run python script on guest
    vboxmanage guestcontrol "Win7 +  VS 2015  (Only start by script)" run --exe "C:\Python27\python.exe" --username "ieuser" --password "Passw0rd!" -- "python.exe" "E:\_Joppe\TestAutomating\python\setupenv_guest.py"
     