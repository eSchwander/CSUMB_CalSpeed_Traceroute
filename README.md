# CSUMB_CalSpeed_Traceroute

This script requires some setup to run. You will need to create the following folders: "ProcessedData", "UploadData", and "csvResults".

Additionally, for this parser to run you need to create a file called tcrtIPs.py.
This file holds the IP addresses of the California, Oregon, and East Coast servers.
These IPs are sensitive info, hence the x's.

CaliforniaIP = xxx.xxx.xxx.xxx

OregonIP = xxx.xxx.xxx.xxx

EastCoastIP = xxx.xxx.xxx.xxx

In order to run the script:
  1. Place test files in UploadData.
  2. Run the script from the terminal using the command "python parse_all_tcrts.py"
  3. The processed files will be moved to ProcessedData.
  4. The resulting csv will be created in csvResults.
