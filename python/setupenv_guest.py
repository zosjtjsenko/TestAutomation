# This script will start the TICS installer and then will automatically click the 
# buttons and fills in the textfields in the installer
# AutoIt functions can be found here : https://www.autoitscript.com/autoit3/docs/functions/ 
#

import autoit
import time
import os
import sys

def singleServerInstall(exePath, pathToLic):
    #check if TICS setup is starting with the right window
    winId = autoit.control_get_text("TICS Setup", "Static13")
    if winId == 'Welcome to the TICS setup':
        print "Expected window"
    else:
        print "unexpected window"
    
    print "Single Server Install initialized\n\n"
    
    #1 welcome screen
    autoit.control_click("TICS Setup", "Button2")	
    print "Welcome screen passed",
    time.sleep(delay)
    print "[X]"
    
    #2 choose components -> default = single server
    autoit.control_click("TICS Setup", "Button2")
    print "Choose components passed",
    time.sleep(delay)
    print "[X]"	
    
    #3 Choose install location default = C:\Program Files (x86)\TIOBE\TICSBASIC4CS
    autoit.control_click("TICS Setup", "Button2")
    print "Choose install location passed",
    time.sleep(delay)
    print "[X]"
    
    #4 Company information and license enter path to lic.dat	
    autoit.win_activate("TICS Setup")
    autoit.control_set_text("TICS Setup", "Edit5", pathToLic)
    autoit.control_click("TICS Setup", "Button2")
    print "Company information passed",	
    time.sleep(delay)
    print "[X]"
        
    #5 Tics Add-ins
    autoit.control_click("TICS Setup", "Button2")
    print "Tics add-ins passed",
    time.sleep(delay)
    print "[X]"
    
    
    #6 Install Apache select "Yes, I want to install/upgrade Apache (recommended)" Second time running the installer this step has to be passed
    if autoit.win_exists("Install Apache/PHP5"):
        autoit.control_click("Install Apache/PHP5", "Button4")
        autoit.control_click("Install Apache/PHP5", "Button2")
        time.sleep(2)
        print "Apache installation passed",
        time.sleep(2)
        print "[X]"
    
    #7 Tics Enter TICSBuildService Username and Password
    autoit.win_wait_active("TICS Setup", 20)	
    autoit.control_click("TICS Setup", "Button2")	
    print "Username and Password passed",
    time.sleep(delay)
    print "[X]"
    
    #8 Tics The entered username is empty POP-UP	
    autoit.control_click("TICS Setup", "Button1")	
    print "Pop-up passed",
    time.sleep(delay)
    print "[X]"
    
    #9 Ready to install
    #autoit.control_click("TICS Setup", "Button2")	
    print "Ready to install",
    time.sleep(2)
    print "[X]"
    
    #9 Cancelling the install
    #autoit.control_click("TICS Setup", "Button3")	
    #print "Cancelling the install",
    #time.sleep(delay)
    #print "[X]"
    
	#9 Continuing the installer 
	#autoit.control_click("TICS Setup", "Button2")	
    print "Installer started",
    time.sleep(delay)
    print "[X]"
	
	#10 Instalation complete 
    autoit.control_click("TICS Setup", "Button2")	
    print "Next",
    autoit.control_click("TICS Setup", "Button2")    
    print "Finish"	
    time.sleep(2)
    print "[X]"

def multiServerInstall(exePath):

    print "Multi Server Install initialized\n\n"
    
    #1 welcome screen
    autoit.control_click("TICS Setup", "Button2")	
    print "Welcome screen passed",
    time.sleep(delay)
    print "[X]"
    
    #2 select multi server
    autoit.control_send("TICS Setup", "ComboBox1", "{down}")
    time.sleep(delay)
    #autoit.control_click("TICS Setup", "ComboBox1")	
    autoit.control_click("TICS Setup", "[CLASSNN:SysTreeView321]")
    time.sleep(delay)
    autoit.control_send("TICS Setup", "[CLASSNN:SysTreeView321]", "{SPACE}")
    time.sleep(delay)
    autoit.control_send("TICS Setup", "[CLASSNN:SysTreeView321]", "{UP}")
    time.sleep(delay)
    autoit.control_send("TICS Setup", "[CLASSNN:SysTreeView321]", "{SPACE}")	
    print "Multiserver choosen with \"TICS file server checkers\" and \"TICS file server configuration\" selected"
    #time.sleep(delay)
    #3 Pop up handling
    autoit.control_click("TICS Setup", "Button2")
    autoit.control_click("TICS Setup", "Button1")
    print "Pop up passed"
    #time.sleep(delay)
    #4 Choose install location
    autoit.control_click("TICS Setup", "Button2")	
    print "Install location choosen"
    #time.sleep(delay)
    #4 Company information and license enter path to lic.dat	
    autoit.win_activate("TICS Setup")
    autoit.control_set_text("TICS Setup", "Edit5", pathToLic)
    autoit.control_click("TICS Setup", "Button2")
    print "Company information passed",	
    time.sleep(delay)
    #5 Ready to install
    #autoit.control_click("TICS Setup", "Button2")	
    print "Ready to install",
    time.sleep(delay)
    ##6 Cancelling the install
    #autoit.control_click("TICS Setup", "Button3")	
    #print "Cancelling the install",
    #time.sleep(delay)
    #print "[X]"
    #autoit.control_click("TICS Setup", "Button2")	
    #print "Installer cancelled",
	#6 Continuing the install
    autoit.control_click("TICS Setup", "Button3")	
    print "Continuing the install",
    time.sleep(delay)
    print "[X]"
    autoit.control_click("TICS Setup", "Button2")	
    print "Installer Continuing",
    #7 Instalation complete 
    autoit.control_click("TICS Setup", "Button2")	
    print "Next",
    autoit.control_click("TICS Setup", "Button2")    
    print "Finish"	
    time.sleep(2)
    print "[X]"


#****Main program starts here*************************
	
if ( __name__ == "__main__"):

    installerType = int(sys.argv[1])
    print installerType
    #variables
    delay = 1
    exePath = "E:\\sharedFolder\\tics.exe"
    pathToLic = "E:\\sharedFolder\\lic.dat"
    
    time.sleep(15)
    #Run the application and wait till the application is actived
    autoit.run(exePath)
    autoit.win_wait_active("TICS Setup", 3)
    	
    unused_cls_return_value= os.system('cls')
    	
    #singleServerInstall(exePath, pathToLic)
    if installerType == True:
        print ("Installing multiserver")
        multiServerInstall(exePath)