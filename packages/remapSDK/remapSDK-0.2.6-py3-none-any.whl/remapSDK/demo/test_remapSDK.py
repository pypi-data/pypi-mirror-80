#!/usr/bin/python


'''
   Copyright © 2019  Atos Spain SA. All rights reserved.
  
   This file is part of the ReMAP platform.
  
   The ReMAP platform is free software: you can redistribute it 
   and/or modify it under the terms of GNU GPL v3.
   
   THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT ANY WARRANTY OF ANY KIND, 
   EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
   MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT, 
   IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY 
   CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN ACTION OF CONTRACT, TORT 
   OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
   OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
  
   See README file for the full disclaimer information and LICENSE file 
   for full license information in the project root.  
  '''


# Import ReMAP SDK module
from remapSDK import remapSDK

print('################# ReMAP WP5 Model PoC #################')

# Instantiate ReMAP SDK
remapSdk = remapSDK.Sdk()

# Get parameters and metadata
start = remapSdk.getStartTime()
print(start)

end_date = remapSdk.getEndTime()
print(end_date)

tailno = remapSdk.getTailNumber()
print(tailno)

partNo = remapSdk.getParamPartNumber("param1")
print(partNo)

metadata = remapSdk.getMetadata()
print(metadata)

replacements = remapSdk.getReplacements()
print(replacements)

# Get dataset path
datasetPath = remapSdk.getDataset()
print(datasetPath)

### Process the CSV to estimate RUL ###

# Export RUL estimation
jsonoutput = {"rulUnit": "test_rul_unit", "rulValue": 5,
              "probabilityOfFailure": 44, "confidenceInterval": 55}
output = remapSdk.sendOutput(jsonoutput)
print(output)
