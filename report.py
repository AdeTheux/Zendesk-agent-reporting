class Report (object) :

     def __init__(self, agentData, fileName) :

        self. _data = "" + \
         "<html>" + \
           "<body>" + \
             "<h1> Report On Agents </h1>"

        for key in agentData :
          
            self._data = self._data + agentData[key].html ()           
       
        self._data     = self._data + " </body> </html>"

        self._fileName = fileName

     def generate (self) :
        
        try :

            outFile = open (self._fileName, "w")
            outFile.write (self._data)
        except UnicodeEncodeError :
            
            writeData = self._data.encode ('utf8', 'replace') 
            outFile.write (writeData)
            print "LOG : Could not write data so writing after converting to utf8."
