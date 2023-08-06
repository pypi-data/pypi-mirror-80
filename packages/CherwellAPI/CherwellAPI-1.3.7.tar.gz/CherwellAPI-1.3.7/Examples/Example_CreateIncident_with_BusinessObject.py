from __future__ import print_function
from CherwellAPI import CherwellClient
import pickle

#########################################################################################
# This example demonstrates how the Cherwell API Connection object can be used to
# create a new business object using the 'BusinessObject Class
###########################################################################################

#############################################
# Change the following to suit your instance
#############################################

base_uri = "http://<Your Cherwell Host here>"
username = "<Your UserName Here>"
password = "<Your Password here>"
api_key = "<Your Cherwell REST API Client Key here>"

# Create a new CherwellClient connection
cherwell_client = CherwellClient.Connection(base_uri, api_key, username, password)

# Create a new instance of an Incident
incident = cherwell_client.get_new_business_object("Incident")

# show there is no Record saved currently
print("########################")
print("Before Saving new Record")
print("########################")
print("BusObId: {}".format(incident.busObId))
print("RecId: {}".format(incident.busObRecId))
print("PublicId: {}\n".format(incident.busObPublicId))

# Set the properties of the new incident
incident.CustomerDisplayName = "John Allard"
incident.Description = "This is a test incident"
incident.Priority = 5
incident.Service = "IT Service Desk"
incident.Category = "Report Outage or Error"
incident.Subcategory = "Submit Incident"
incident.Source = "Event"


# Save the new incident
incident.Save()

# show the record is now saved and has an id
print("########################")
print("Before Saving new Record")
print("########################")
print("BusObId: {}".format(incident.busObId))
print("RecId: {}".format(incident.busObRecId))
print("PublicId: {}\n".format(incident.busObPublicId))

