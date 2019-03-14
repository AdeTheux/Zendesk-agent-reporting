class AgentData (object) :

    def __init__ (self): 

        # Use ticketId/audits for getting this done.
        #done 
        self._privateCmnts    = 0
        self._publicCmnts     = 0
        self._tickNoComments  = 0
        self._tickCommentsAvg = 0
        self._webFormCreated  = 0
        self._tickSolved      = 0
        self._tickClosed      = 0
        self._noTickEsc       = 0
        self._avgCalMins      = 0
        self._avgBusMins      = 0
        self._lastLogin       = ""
	self._role            = ""
  
        self._viewed          = 0 
        self._notViewed       = 0 #No update done since assigning 
        #Nice to have
        self._autoUpdated     = 0
        self._autoSolved      = 0
        self._avgCallTimes    = 0
        self._slowCalls       = 0
        self._phoneTime       = 0
        
        ## Some processing stuff 
        self._assignedTicks   = 0
        self._name            = ""
        self._totalCalMins    = 0
        self._totalBusMins    = 0
        self._totalComments   = 0
        self._assignedTime    = object()
  
        """
        If this is to be done 
        This should be a list of timeX 
        and timeY
           
        """   
       
        self._phoneGraph      = []
        return
 
    def setAssignedTime (self, assignedTime) :

        self._assignedTime = assignedTime

    def setLastLogin (self, lastLogin) :

        self._lastLogin = lastLogin

    def setRole (self, role) :

        self._role = role

    def getAssignedTime (self) :
       
        return self._assignedTime

    def getName (self) :

        return self._name
 
    def updateAssigned (self) :
      
        self._assignedTicks = self._assignedTicks + 1

    def setName (self, name) :

        self._name = name

    def updateWeb (self) :

        self._webFormCreated = self._webFormCreated + 1
 
    def updateSolved (self) :

        self._tickSolved = self._tickSolved + 1

    def updateClosed (self) :
        
        self.updateSolved ()
        self._tickClosed = self._tickClosed + 1
    
    def updateComments (self) :
         
        self._totalComments = self._totalComments + 1
 
    def updatePriComments (self) :
 
        self._privateCmnts  = self._privateCmnts + 1
   
    def decPubComments (self) :
 
        self._publicCmnts = self._publicCmnts - 1

    def updatePubComments (self) :

        self._publicCmnts  = self._publicCmnts + 1
 
    def updateNoComments (self) :

        self._tickNoComments = self._tickNoComments + 1

    def updateNoView (self) :
  
       self._notViewed = self._notViewed + 1

    def updateEsc (self) :
  
        self._noTickEsc = self._noTickEsc + 1 
 
    def updateCalMins (self, tickMins) :
 
        self._totalCalMins = self._totalCalMins + tickMins
    
    def updateBusMins (self, tickMins) :
 
        self._totalBusMins = self._totalBusMins + tickMins
 
    def calCommentAvg (self) :
 
        if self._assignedTicks != 0 :
            self._tickCommentsAvg = self._totalComments / self._assignedTicks
 
    def calAvgLife (self) :
        # Assuming all closed tickets to be solved.
        
        if self._tickSolved != 0 :
            self._avgCalMins = self._totalCalMins / self._tickSolved
            self._avgBusMins = self._totalBusMins / self._tickSolved
    
    def html (self) :

       return " <h2>" + self._name + \
          "</h2> " + \
          "<table> " + \
          "<tr><td> Number of assigned tickets </td><td>" + str (self._assignedTicks) + \
          "</td></tr><tr><td>Agent name</td><td>" + self._name +  \
          "</td></tr><tr><td>Role</td><td>" + self._role +  \
          "</td></tr><tr><td>Tickets created using web form</td><td>" + str (self._webFormCreated) + \
          "</td></tr><tr><td>Number of tickets solved</td><td>" + str (self._tickSolved) + \
          "</td></tr><tr><td>Number of tickets closed</td><td>" + str (self._tickClosed) + \
          "</td></tr><tr><td>Total number of comments</td><td>" + str (self._totalComments) + \
          "</td></tr><tr><td>Number of tickets not updated(No changes made)</td><td>" + str (self._notViewed) + \
          "</td></tr><tr><td>Number of private comments</td><td>" + str (self._privateCmnts) + \
          "</td></tr><tr><td>Number of public comments</td><td>" + str (self._publicCmnts) + \
          "</td></tr><tr><td>Number of tickets with no comments</td><td>" + str (self._tickNoComments) + \
          "</td></tr><tr><td>Average number of comments in assigned tickets</td><td>" + str (self._tickCommentsAvg) + \
          "</td></tr><tr><td>Number of tickets escalated</td><td>" + str (self._noTickEsc) + \
          "</td></tr><tr><td>Total number of minutes to respond</td><td>" + str (self._totalCalMins) + \
          "</td></tr><tr><td>Total number of business minutes to respond</td><td>" + str (self._totalBusMins) + \
          "</td></tr><tr><td>Average minutes to respond to a ticket</td><td>" + str (self._avgCalMins) + \
          "</td></tr><tr><td>Average business minutes to respond</td><td>" + str (self._avgBusMins) + \
          "</td></tr><tr><td> Number of days since last login</td><td>" + str (self._lastLogin) + \
          "</td></tr> </table>"



      
    
    def __str__ (self): 

	return "\n Assigned Tickets            :" + str (self._assignedTicks) + \
		    "\n Name                   :" + self._name + \
		    "\n Role                   :" + self._role + \
                    "\n Web Form               :" + str (self._webFormCreated) + \
                    "\n Solved                 :" + str (self._tickSolved) + \
                    "\n Closed                 :" + str (self._tickClosed) + \
                    "\n Tickets Not Updated    :" + str (self._notViewed) + \
                    "\n Tot Comments           :" + str (self._totalComments) + \
                    "\n Pri Comments           :" + str (self._privateCmnts) + \
                    "\n Pub Comments           :" + str (self._publicCmnts) + \
                    "\n No Comments            :" + str (self._tickNoComments) + \
                    "\n Comments Avg(assigned) :" + str (self._tickCommentsAvg) + \
                    "\n Tick Esc               :" + str (self._noTickEsc) + \
                    "\n Total Cal Resp Mins    :" + str (self._totalCalMins) + \
                    "\n Total Bus Resp Mins    :" + str (self._totalBusMins) + \
                    "\n Avg Cal Resp Mins      :" + str (self._avgCalMins) + \
                    "\n Avg Bus Resp Mins      :" + str (self._avgBusMins) + \
                    "\n Last Logged in         :" + str (self._lastLogin)


