# -*- coding: utf-8 -*-
"""End-to-end API Data getting and cleaning practice

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1D9EsHmkeERo71HaeUAVzfPLDvlBFKjgS

# How to Connect and call APIs in Python?


## What is an API ?
API is an acronym for Application programming Interface. It can be understood as a composition of rules that enables us to access an external service on web through our systems.



An API is considered as a data source available on web which can be accessed through particular libraries of a programming language.

## Types of requests to an API
for detail-https://requests.readthedocs.io/en/latest/user/quickstart/

list of common instructions or commands we use to do certain sort of actions on the API-

1.GET command: It enables the users to fetch the data from the APIs onto their system in a specific format that is usually JSON.

2.POST command: This command enables us to add data to the API i.e. to the service on web.

3.DELETE command: It enables us to delete certain information from the API service on web.

4.PUT command: Using PUT command, we can update an existing data or information in the API service on web.

## Status/Response codes of an API
 On connecting  to an API, It return cetain response code which determines the status of our connection that is made to the API on web:

 1. 200: OK - It means we have a healthy connection  with the API on web.

 2.204: It depicts that we can successfully made a connection to the API, but did not return any data from the service.

 3.401: Authentication failed1

 4.403: Access is forbidden by the API service.

 5.404: The request API  service is not found on the server/web.

 6.500: Internal Server Error has occurred.

## Steps to Connect and Call APIs using Python

the steps to make a healthy connection to an API using Python as the scripting language.

###1. Import the necessary library

In order to connect to and API  and perform actions on it, we need to import `python requests library` itno the environment.
"""

import requests

"""###2. Perform an action to connect to the API
Here, we have used GET command to connnect to the API as shown-
`requests.get(" url link")`

the url to which the connection needs to be made into the get() function.
"""

response_API = requests.get()

"""###3. Print the response code
The status_code variable enables us to have a look at the status of our connection to the API.
"""

response_API.status_code

"""### Examples

## 1. Connecting to a GMAIL API
In this example, we would form a healthy connection to an Open Source GMAIL API from this link.
https://developers.google.com/gmail/api/reference/rest

Discovery Document : https://gmail.googleapis.com/$discovery/rest?version=v1
"""

import requests
response_API = requests.get('https://gmail.googleapis.com/$discovery/rest?version=v1')

print(response_API.status_code)



"""##2. Pulling data from an Open source COVID API

In this example, we would be connecting to an Open source COVID API just to extract and parse the json information in an customized manner

we have used the COVID19-India API to fetch the data of the cases from the state-wise list.
https://data.covid19india.org/


https://api.covid19india.org/state_district_wise.json

"""

import requests
import json
response_API2 = requests.get('https://api.covid19india.org/state_district_wise.json')

print(response_API2.status_code)

"""after making connection with the API ,the next task is to pull the data from the API


The `requests.get(api_path).text` helps us pull the data from the mentioned API.
"""

data = response_API2.text

"""### Parse the data into JSON format

having the extracted data, its now the time to convert and decode the data into perper JSON format as shown-

the `json.loads() ` function parse the data into a JSON format
"""

parse_json=json.loads(data)

# print the data
parse_json['Chhattisgarh']

active_case = parse_json['Andaman and Nicobar Islands']['districtData']['South Andaman']['active']
print("Active cases in South Andaman:", active_case)

"""##3.Example Searches from FBI Most Wanted Site:

These search examples are the extent of the documentation the FBI Most Wanted website gives as documentation for how to use its API

https://www.evanmarie.com/apis-json-and-data-cleaning/


url-https://api.fbi.gov/wanted/v1/list
"""

# Data from Atlanta field office
response = requests.get('https://api.fbi.gov/wanted/v1/list', params={ 'field_offices': 'atlanta'})

data = json.loads(response.content)
print("From the Atlanta field office: ", data['total'])
print(data['items'][0]['title'], "\n")

# Second page of data from entire list
response = requests.get('https://api.fbi.gov/wanted/v1/list', params={'page': 2})

data = json.loads(response.content)
print("Page No.: ", data['page'])
print(data['items'][0]['title'], "\n")

# Entire list, which is imported only 1 page at a time
response = requests.get('https://api.fbi.gov/wanted/v1/list')
data = json.loads(response.content)

database_length = data['total']

print("Length of entire most wanted list: ", data['total'])
print(data['items'][0]['title'], "\n")

# JSON data before converted to Pandas:
data['items'][0]

# check the data type after creating dataframe:
print("json.loads() has decoded the data to: ", type(json.loads(response.content)))

