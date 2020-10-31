# REST API app
## Overview
This app written using Flask, swagger and connexion to work in kubernetes. It has 3 endpoints:
* /api/health - supports GET HTTP requests, returns HTTP code 204 (no content). Uses for liveness Kubernetes probe
* /api/encrypt - supports POST HTTP requests, receive user data json, and calculate hash using base64
* /api/decrypt - supports POST HTTP requests, receive user data json, and calculate the original string 
based in the base64 hash

## swaggler UI
The app supports swaggler UI for automaticly generate documentation for endpoints. Also it can be helpful to 
generate HTTP requests for API endpoints in the webinterface - more convinient way than do RAW cli requests 
via curl

![swaggler UI](https://i.imgur.com/Tl7K2ai.png
)

## swaggler 2.0 configuration, and Validation input/output data 
The API itself described in the yaml file [windriver_api.py](/windriver_api.py)
regarding data validation, it's work of connexion, swaggler(work via declaration schema in the YAML). 
But for double check I also use strict types (modern python3.8 feature) and, of cource, unit tests

## Installation in the Docker
I've attached a [Dockerfile](/Dockerfile). So, you can run the app inside it. But unit and end2end tests require
envinronment variables:
 
* serviceName - use here IP address of docker container (for example, 127.0.0.1 if you have docker locally) 
* servicePort - use here HTTP port 
* minimumScore - I use pylint for part of tests(to check code quality). So, this is the minimum amount of points,
which code can have. Example: 9.0
 
### /api/encrypt endpoint
It receives 
```json
{"Input": "string"}
```` 
Json dict via POST with headers (application/json), and returns an encrypted string in the output like:
```json
{
  "Input": "string",
  "Message": "",
  "Output": "c3RyaW5n",
  "Status": "success"
}
```
In a case of error, it returns an empty Output, status 'error' and, in the key Message the value with exact error

 ### /api/decrypt endpoint
 It receives 
```json
{"Input": "c3RyaW5n"}
```` 
Json dict via POST with headers (application/json), and returns an encrypted string in the output like:
```json
{
  "Input": "c3RyaW5n",
  "Message": "",
  "Output": "string",
  "Status": "success"
}
```
In a case of error, it returns an empty Output, status 'error' and, in the key Message the value with exact error

### Kubernetes and helm3
In order to use this app in the helm, you have to install the [helm3 chart](helm_package), additional information can be
find in the link above

### unit tests
Unit tests covers this app. The app has 14 unit, e2e and codestyle tests. Additionally, tests provides validation for
REST API data schema. Tests can be find in the [file](utest_windriver-api.py)
In order to use tests in the kubernetes, you can get list of pods:
```shell script
windriver-rest-api-69fddc7f8b-hfs8h     1/1     Running   0          76m
windriver-rest-api-69fddc7f8b-kxrgp     1/1     Running   0          76m
```
And than launch them:
```shell script
microk8s.kubectl exec -it windriver-rest-api-69fddc7f8b-kxrgp -- python3 -m unittest utest_windriver-api.py
************* Module api.string_processing
<....>
----------------------------------------------------------------------
Ran 14 tests in 3.636s
OK
```

