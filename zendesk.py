# TODO 
# Connect to Zendesk api of one account.
# Dump the contents to an html v1

## INPUTS have ZD_USER and ZD_PASS as environment variable with your Zendesk
#  username and password. (eg export ZD_USER=abc@gmail export ZD_PASS=password)

import requests
import os
import json
import datetime
import user
import report

from string import Template
from datetime import date


"""
Our own custom print function for fixing unicode issues.
"""
def myPrint(myPrintData) :

    try :

        print str(myPrintData)

    except UnicodeEncodeError :
            
        print "Unicode encode occured but was handled"
        newData = myPrintData.encode ('utf8', 'replace')
        print newData

"""
Parse the json and 
create the html tables.
"""

## Keeping prefixes separate to avoid
## hard quoting as much as possible

PREFIXES = {
   'USERS'    : "users",
   'TICKETS'  : "tickets",
   'USERSURL' : "/api/v2/users.json?&role[]=admin&role[]=agent",
   'TICKURL'  : "/api/v2/tickets.json",
   'AUDITS'   : "/api/v2/tickets/$ticket_id/audits.json",
   'METRICS'  : "/api/v2/ticket_metrics.json",
}

"""
Representation of a ZendeskClient which stores info 
about users.

TODO Add tickets if required
"""
class ZendeskClient (object) :

     def __init__ (self, compName, userName, password) :
  
         self._compName   = compName
         self._user       = userName
         self._pass       = password
         self._compUrl    = "https://" + compName + ".zendesk.com"
         self._userUrl    = self._compUrl + PREFIXES['USERSURL']
         self._tickUrl    = self._compUrl + PREFIXES['TICKURL']
         self._metricsUrl = self._compUrl + PREFIXES['METRICS']
         self._auditsUrl  = self._compUrl + PREFIXES['AUDITS']
         
         # This is a map between ticketId and userId
         self._ticketMap  = {} 
            
         # This will be a dictionary of Id and data
         # should get updated while learning takes place
         self._agentData = {} 

     def checkAuth (self) :

	 reqData     = requests.get (self._userUrl, auth=(self._user, self._pass))
         if reqData.status_code == 200:
              myPrint("Authorization Succesful")
              return True
         else : 
              myPrint("Status Code =" + str(reqData.status_code) + "Url hit was" + self._userUrl)
              return False
                
 
     def formUsers (self) :
   
         myPrint("Parsing the the user json to get information of users " + self._userUrl)
	 reqData     = requests.get (self._userUrl, auth=(self._user, self._pass))
         if reqData.status_code != 200:
             myPrint("Error Occured" + str (reqData))
             return
         decodedJson = json.loads (reqData.text)
         
         #If users are found, form objects
         if PREFIXES['USERS'] in decodedJson :
             myPrint("Total number of users= " + str(len(decodedJson [PREFIXES['USERS']])))
             for item in decodedJson [PREFIXES['USERS']] : 

                 self.learnFromUser (item)

         if "next_page" in decodedJson :

	      if decodedJson["next_page"] is not None :

                  self._userUrl = decodedJson["next_page"]
                  self.formUsers()
              else :    
                  
                  print "Last page of users" 
         
         return

     def formTicks (self) :

         myPrint("Parsing the ticket information " + self._tickUrl)
	 reqData     = requests.get (self._tickUrl, auth=(self._user, self._pass))
         if reqData.status_code != 200:
             myPrint("Error Occured" + str (reqData))
             return

         decodedJson = json.loads (reqData.text)
          
         #If users are found, form objects
         if PREFIXES['TICKETS'] in decodedJson :
             myPrint("Total number of tickets= " + str(len(decodedJson [PREFIXES['TICKETS']])))
             for item in decodedJson [PREFIXES['TICKETS']] : 

                self.learnFromTick (item)
         self.formMetrics ()

         if "next_page" in decodedJson :

	      if decodedJson["next_page"] is not None :

                  self._tickUrl = decodedJson["next_page"]
                  self.formTicks()
              else :    
                  
                  print "Last page of tickets" 
         return

     def formMetrics (self) :

         myPrint("Parsing the metrics information " + self._metricsUrl)
	 reqData     = requests.get (self._metricsUrl, auth=(self._user, self._pass))
         if reqData.status_code != 200:
             myPrint("Error Occured" + str (reqData))
             return

         decodedJson = json.loads (reqData.text)
         
         if "ticket_metrics" in decodedJson :
             for item in decodedJson ["ticket_metrics"] :
                 
                 if "ticket_id" in item and item["ticket_id"] in self._ticketMap : 
                     agentData = self._agentData[self._ticketMap[item["ticket_id"]]]
                     if "full_resolution_time_in_minutes" in item :
                         resTime = item ["full_resolution_time_in_minutes"]
                         myPrint("Result time -->" + str(resTime))
                         if "calendar" in resTime :
                             if resTime["calendar"] is not None :
                                 agentData.updateCalMins(int (resTime["calendar"]))
                         if "business" in resTime :
                             if resTime["business"] is not None :
                                 agentData.updateBusMins(int (resTime["business"]))
                  
                 # Update if the no of groups it has gone
                 # through is greater than 1       
                 if "group_stations" in item :
                     if int(item["group_stations"]) > 1 :
                         agentData.updateEsc () 

	 if decodedJson["next_page"] is not None :

	     self._metricsUrl = decodedJson["next_page"]
             self.formMetrics()
	 else :    

	     print "Last page of metrics" 
	
         return


     def learnFromUser (self, userDict) :

        if "id" in userDict :
       
           if "role" in userDict :

               if "name" in userDict :

                   myPrint(userDict["name"] + " is an " + userDict["role"])

               if userDict["role"] == "agent" or userDict["role"] == "admin" :

                   if not userDict["id"] in self._agentData : 
               
                      self._agentData[userDict["id"]] = user.AgentData ()

                   self._agentData[userDict["id"]].setRole(userDict["role"])

                   if "name" in userDict :
               
                      self._agentData[userDict["id"]].setName (userDict["name"])
    
                   if "last_login_at" in userDict :

                      timeToday = datetime.datetime.now()
                      if userDict["last_login_at"] is None :
                   
                         lastLogin = "Never Logged In"
                      else :

                         logInTime = datetime.datetime.strptime (userDict["last_login_at"], "%Y-%m-%dT%H:%M:%SZ")
                         delta = timeToday - logInTime
                         lastLogin = str(delta.days) + " days " + str(delta.seconds/3600) + " hours ago" 

                      self._agentData[userDict["id"]].setLastLogin(lastLogin) 

     def learnFromAudits (self, userId, auditUrl) :
        
          # Create has a field name assignId 
          #  
	 reqData     = requests.get (auditUrl, auth=(self._user, self._pass))
         if reqData.status_code != 200:
             myPrint("Error Occured" + str (reqData))
             return

         decodedJson = json.loads (reqData.text)
         myPrint("Checking audits for ticket at url " + auditUrl)
         if "audits" in decodedJson :
            noComment = True
            noView    = True
            authorId  = ""
            for audit in decodedJson ["audits"] :
                if "author_id" in audit :
                   authorId = audit["author_id"]
                auditCreated = object ()
                if "created_at" in audit :
                    auditCreated = datetime.datetime.strptime (audit["created_at"], "%Y-%m-%dT%H:%M:%SZ")
                if "events" in audit :
                    for event in audit["events"] :

                        if str (userId) == str (authorId) :
                            if type (self._agentData[userId]) != type (object()) :
                               aTime = self._agentData[userId].getAssignedTime()
                               if type (aTime) != type (object()) : 
                                   if auditCreated > aTime :
                                       noView = False 
                            
                        if "type" in event and "field_name" in event:
                            if "Create" == event["type"] or "Change" == event["type"]:
                               if "assignee_id" in event["field_name"] and "value" in event:
                                   if str (userId) == str (event["value"]) :
                                       self._agentData[userId].setAssignedTime(auditCreated)
                        if "public" in event :
                            if "Comment" == event["type"]  :
                               if "author_id" in event and event ["author_id"] == userId :
                                   noComment = False
                                   self._agentData[userId].updateComments ()
                                   if False == event["public"] :
                                       self._agentData[userId].updatePriComments()
                                   else :
                                       self._agentData[userId].updatePubComments()

                            if "CommentPrivacyChange" == event["type"] :
                               noComment = False
                               if "public" in event :
                                   if event["public"] == False :
                                       self._agentData[userId].updatePriComments()
                                       self._agentData[userId].decPubComments() 
                else : 
                   myPrint("Log: No events found in audit")
         if noComment is True :
 
              self._agentData[userId].updateNoComments ()
 
         if noView is True :
 
              self._agentData[userId].updateNoView () 

	 if decodedJson["next_page"] is not None :

	     auditUrl = decodedJson["next_page"]
             self.learnFromAudits(userId, auditUrl)
	 else :    

	     print "Last page of audits for ticket" 
	
         return
         
     def learnFromTick (self, ticketDict) :
        
        if "assignee_id" in ticketDict :
            
            userId = ticketDict ['assignee_id']
            toPrint = ""

            if userId is None :
                   
                if "id" in ticketDict : 
                     myPrint("Ticket not assigned to anyone : " + str(ticketDict["id"]))
                return
            
            if "id" in ticketDict :
                self._ticketMap [ticketDict["id"]] = userId
                toPrint = "Ticket Id = " + str(ticketDict["id"])

	    if userId in self._agentData :
	        self._agentData[userId].updateAssigned ()
	    else :
                print "Warning : Adding new assignee : " + str(userId)
                print  "Check the url below to see if he is a member"
                print self._compUrl + "/api/v2/users/" + str(userId) + ".json" 
	        self._agentData[userId] = user.AgentData()
            
            toPrint = " Assignee Id = " + str(userId) + " Name = " + self._agentData[userId].getName()
            myPrint(toPrint)  
            if "via" in ticketDict :
                if "channel" in ticketDict["via"] :
                    if ticketDict["via"]["channel"] == "web" :
                        self._agentData[userId].updateWeb ()
 
            if "status" in ticketDict :
                if ticketDict["status"] == "solved" :
                    self._agentData[userId].updateSolved ()
                elif ticketDict["status"] == "closed" :
                    self._agentData[userId].updateClosed ()

            # Doing this here to ensure that dict entry is created         
            if "id" in ticketDict :
                urlTemp  = Template (self._auditsUrl)
                auditUrl = urlTemp.substitute (ticket_id=ticketDict["id"])
                self.learnFromAudits (userId, auditUrl)
           
     def getAgentData (self) :

        return self._agentData 

     def finalize (self) :
          
         for userId in self._agentData :
             self._agentData[userId].calCommentAvg ()
             self._agentData[userId].calAvgLife ()

     def display (self) :
       
        for key in self._agentData :
             try :
                 myPrint("\n\nDetails for key --" + str(key)) 
                 myPrint(str(self._agentData[key]))
             except UnicodeEncodeError :
             
                 myPrint("Could not print Data on the screen.")

    
"""
Global function which return help contents.
"""
def usage () : 

   return "Help \n \n" + \
          "Invoke script with username, password, domain name and \n" + \
          "htmlfile name as arguments \n\n" + \
          "You can also use environment variables ZD_USER, ZD_PASS,\n" + \
          "ZD_REPORT and ZD_DOMAIN to set the inputs"

if __name__ == "__main__" :

    userName   = ""
    password   = ""
    repName    = ""
    domainName = ""
 
    try :
       userName   = os.environ ['ZD_USER']
       password   = os.environ ['ZD_PASS']
       repName    = os.environ ['ZD_REPORT']
       domainName = os.environ ['ZD_DOMAIN']
    except (KeyError) :
       import sys 
       if len (sys.argv) < 5 :
             myPrint(usage ())
             sys.exit (1)
       userName   = sys.argv[1]
       password   = sys.argv[2]
       domainName = sys.argv[3]
       repName    = sys.argv[4]

    zenCli = ZendeskClient (domainName, userName, password)
    if not zenCli.checkAuth () :
        sys.exit(1)
    zenCli.formUsers()
    zenCli.formTicks()
    zenCli.finalize ()
    zenCli.display()
    rep = report.Report (zenCli.getAgentData(), repName)
    rep.generate()
    
