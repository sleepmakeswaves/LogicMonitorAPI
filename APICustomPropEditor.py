#!/bin/env python3
import requests
import json
import hashlib
import base64
import time
import hmac
#Account Info
AccessId =''
AccessKey =''
Company = ''

Oldlabel = input("Enter Device Property Name: ")
Newlabel = input("Enter New property Name: ")
#Request Info
httpVerb ='GET'
resourcePath = '/device/devices'
queryParams = '?filter=customProperties.name:' + Oldlabel + '&fields=id,customProperties'+ '&size=1000'
#Construct URL
url = 'https://'+ Company +'.logicmonitor.com/santaba/rest' + resourcePath + queryParams
#Get current time in milliseconds
epoch = str(int(time.time() * 1000))
#Concatenate Request details
requestVars = httpVerb + epoch + resourcePath
#Construct signature
hmac1 = hmac.new(AccessKey.encode(),msg=requestVars.encode(),digestmod=hashlib.sha256).hexdigest()
signature = base64.b64encode(hmac1.encode())
#Construct headers
auth = 'LMv1 ' + AccessId + ':' + signature.decode() + ':' + epoch
headers = {'Content-Type':'application/json','Authorization':auth}
#Make request
response = requests.get(url, headers=headers)
#Parse response
jsonResponse = json.loads((response.content).decode('utf-8'))
#Loop through each device & update Collector Id
for i in jsonResponse['data']['items']:
    deviceId = str(i['id'])
    for j in i['customProperties']:
        if str(j['name']) == Oldlabel:
            # change the property name
            j['name'] = Newlabel
    #Request Info
    httpVerb ='PATCH'
    resourcePath = '/device/devices/'+deviceId
    queryParams = '?patchFields=customProperties&filter=customProperties.name:' +Oldlabel+ '&opType=refresh'
    #data = '{"customProperties":[{"name":"'+ Newlabel + '","value":"' +cpvalue+ '"}]}'
    # json to string except id field, GET API load id field
    data = json.dumps(i)
    #print('data=',data)
    #Construct URL
    url = 'https://'+ Company +'.logicmonitor.com/santaba/rest' + resourcePath + queryParams
    #Get current time in milliseconds
    epoch = str(int(time.time() * 1000))
    #Concatenate Request details
    requestVars = httpVerb + epoch + data + resourcePath
    #Construct signature
    hmac2 = hmac.new(AccessKey.encode(),msg=requestVars.encode(),digestmod=hashlib.sha256).hexdigest()
    signature = base64.b64encode(hmac2.encode())
    #Construct headers
    auth = 'LMv1 ' + AccessId + ':' + signature.decode() + ':' + epoch
    headers = {'Content-Type':'application/json','Authorization':auth}
    #Make request
    response = requests.patch(url, data=data, headers=headers)
    print ('Response Status:',response.status_code)
    #print ('Response Body:', str(response.content))
