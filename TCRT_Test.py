"""
------------------------------------------------------------------------
Evan_Test.PY

AUTHOR(S):    Evan Schwander		eschwander@csumb.edu

PURPOSE-  This class will hold an individual TraceRoute test.

VALUES TO CARE ABOUT (For the CSV): 
    HopCount - The amount of hops in a test.
    Hops[] - Holds Hop objects. Hops past HopCount hold 'NA' values
        Each Hop object holds its own number, name(Nm), IP(IP), and speed(D).
            
------------------------------------------------------------------------
"""

# IMPORTS
import sys
from tcrtIPs import * 
#END IMPORTS


class Hop:

    """A simple class for holding the information from a single hop"""

    '''
    # ------------------------------
    # ---- CLASS VARIABLES ----
    Number = ""
    Name = ""
    IP = ""
    Speed = ""
    # ------------------------------
    '''
    
    def __init__(self, dataString):
        tempDataString = dataString.split(" ")
        temp = [x for x in tempDataString if x]
        try:
            self.Number = temp.pop(0)
        except:
            self.Number = dataString

        # Checking if test timed out or was otherwise ended early
        try:
            #if Number can be converted into an int, everything is swell
            self.Number = int(self.Number)
            self.Name = temp.pop(0)
            self.IP = temp.pop(0)[1:-1]
            self.Speed = temp.pop(0)    
        except:
            #if Number cannot be convereted to an int the test ended early
            self.Number = self.Number
            self.Name = dataString
            self.IP = "NA"
            self.Speed = "NA"
                
        # Converts "*" to NA for csv purposes
        if self.IP == "":
            self.IP = "*"
        '''
		if self.Name == "*":
            self.Name = "NA" 
        if self.IP == "*":
            self.IP = "NA" 
        if self.Speed == "*":
            self.Speed = "NA" 
		'''

    
    def __str__(self):
        return("Hop number: {}\nDestination: {}\nDestination IP: {}\nSpeed: {} ms".format(self.Number, self.Name, self.IP, self.Speed))
    #END DEF


class TCRT_Test:
    
    """A TRCRT test, containing parsed information about TCRT hops"""
    '''
    # ---- CLASS ATTRIBUTES ----
    Hops = []
    HopCount = 0
    HopMin = -1
    HopMax = -1
    # ------------------------------
    '''

    def __init__(self, dataString="", destination = "unknown"):
        '''
        Used to initialize an object of this class
        ARGS:
            dataString: String, the text that is going to be parsed
        '''

        # Some variable initialization
        self.Hops = []
        self.Destination = ''
        self.HopMax = 40

        # Setting destination IP based on passed in value
        self.setDestination(destination)

        #Construct Hops list
        self.Hops.append(self.__parseHops(dataString))
        
        #Check Hops for any errors and deal with them accordingly
        error = False
        for x in self.Hops:
            if "Cancelled" in x.Name:
                self.HopCount = "error: Cancelled by user"
                error = True
            elif "Timed" in x.Name:
                self.HopCount = "error: Timed out"
                error = True
            elif "failed" in x.Name:
                self.HopCount = "error: Traceroute command failed"
                error = True
            elif "not complete" in x.Name:
                self.HopCount = "error: Traceroute did not complete"
                error = True
            elif "Quitting" in x.Name:
                self.HopCount = "error: Cancelled by user"
                error = True
        if error:
            self.__parseIndividualHops("")

        #Checking for incomplete tcrts
        if not error:
            # if the final hop's IP is not the destination IP, the trace route was incomplete
            if self.Hops[self.HopCount - 1].IP != self.Destination:
                if self.HopCount < 40:
                    self.Hops[self.HopCount].IP = "error: Traceroute did not complete"
                    self.Hops[self.HopCount].Name = "error: Traceroute did not complete"
                    self.Hops[self.HopCount].Speed = "error: Traceroute did not complete"
                elif self.HopCount == 40:
                    self.Hops[self.HopCount-1].IP = "error: Traceroute did not complete"
                    self.Hops[self.HopCount-1].Name = "error: Traceroute did not complete"
                    self.Hops[self.HopCount-1].Speed = "error: Traceroute did not complete"



    #END DEF

# INITIALIZATION FUNCTIONS -----------------------------------------------------

    def __parseHops(self, dataString):
        """ 
        Seperates first line from the hops and then passes off hops to be parsed.
        """
        # We start our function be splitting the data string into individual chunks,
        # which we will then parse individually
        data = dataString.splitlines()
        if self.__parseFirstLine(data[0]):
            data.pop(0)
        self.__parseIndividualHops(data)
        
    #END DEF

    def __parseIndividualHops(self, dataString):
        """ 
        Creates Hop objects that are parsed upon creation 
        These objects are then stored into an array 
        Additionally, this function will fill the Hops array up to the 40 hop max 
        """
        # This is where we creat Hop objects and store them into an array
        self.Hops = []
        while(dataString):
            self.Hops.append(Hop(dataString.pop(0)))
        #Here we determine the number of hops before completion
        if dataString != "":
            self.HopCount = len(self.Hops)
        # This loop fills the Hops array with fake Hop objects up to HopMax
        while(len(self.Hops) < self.HopMax):
            emptyHop = str(len(self.Hops)) + " NA (NA) NA"
            self.Hops.append(Hop(emptyHop))
    #END DEF

    def setDestination(self, destination):
        if destination == "california":
            self.ConnectionLoc = "California"
            self.Destination = CaliforniaIP
        elif destination == "oregon":
            self.ConnectionLoc = "Oregon"
            self.Destination = OregonIP
        elif destination == "east":
            self.ConnectionLoc = "East"
            self.Destination = EastCoastIP
        else:
            self.ConnectionLoc = "Unknown"
            self.Destination = "Unknown"
    #END DEF
            
    def __parseFirstLine(self, dataString):
        """ 
        Finds destination IP and HopMax 
        """

        #Sometimes this special first line will not exist
        # This if statement is for when it does not
        if "traceroute" not in dataString:
            return False

        dataString = dataString.split(" ") 
        
        # The following loop finds the hop max and destination IP in the first line
        flag = False
        for x in dataString:
            if flag:
                self.HopMax = int(x)
                break
            if '.' in x:
                self.Destination = x[0:-1]
                flag = True

        if(self.Destination == CaliforniaIP):
            self.ConnectionLoc = "California"
        elif(self.Destination == OregonIP):
            self.ConnectionLoc = "Oregon"
        elif(self.Destination == EastCoastIP):
            self.ConnectionLoc = "East"

        return True
    #END DEF

    def __str__(self):
        # converts test into csv
        csv = str(self.HopCount) + ","
        for hop in self.Hops:
            csv += hop.Name + ","
            csv += hop.IP + ","
            csv += hop.Speed + ","
        if self.ConnectionLoc == "Oregon":
            return csv[0:-1]
        return(csv)

