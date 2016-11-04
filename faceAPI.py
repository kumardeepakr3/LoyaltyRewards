import httplib, urllib, base64, json, string


##### Working Fine #####
def faceDetectOctetStream(octet_stream, subscription_key):
    headers = {
         # Request headers
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }

    params = urllib.urlencode({
        'returnFaceId': 'true',
    })

    try:
        body = octet_stream
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/face/v1.0/detect?%s" % params, body, headers)
        response = conn.getresponse()
        response_status = response.status
        data = response.read()
        conn.close()

        if (response_status == 200):
            # print(data)
            jsonParsed = json.loads(data.decode('utf-8'))
            if(len(jsonParsed) > 0):
                faceId = jsonParsed[0]["faceId"]
                return faceId, 1
            else:
                print "Error in Json Parsing in faceDetectOctetStream"
                return "err", 0
        else:
            print response_status
            print data
            return "err", 0
    except Exception as e:
        print("Exception in function faceDetectOctetStream")
        return "err", 0



def faceDetectUrl(url, subscription_key):
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }

    params = urllib.urlencode({
        'returnFaceId': 'true',
    })

    try:
        body = '{"url": "' +url+ '"}'
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/face/v1.0/detect?%s" % params, body, headers)
        response = conn.getresponse()
        response_status = response.status
        data = response.read()
        conn.close()

        if (response_status == 200):
            print(data)
            jsonParsed = json.loads(data.decode('utf-8'))
            if(len(jsonParsed) > 0):
                faceId = jsonParsed[0]["faceId"]
                return faceId, 1
            else:
                print "Error in Json Parsing in faceDetectUrl"
                return "err", 0
        else:
            print response_status
            print data
            return "err", 0
    except Exception as e:
        print("Exception in function faceDetectUrl")
        return "err", 0



#### Working Fine ####
def createFaceList(uniqueListId, subscription_key):

    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }

    params = urllib.urlencode({
    })

    try:
        body = '''{
            "name" : "customer007",
            "userData" : "List of Customers is stored here"
        }'''

        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("PUT", "/face/v1.0/facelists/"+uniqueListId+"?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        response_status = response.status
        conn.close()

        if (response_status == 200):
            print "Created Face List Successfully"
        else:
            print "Error in Face List Creation"
            print(data)

    except Exception as e:
        print("Exception in createFaceList")
        return "err", 0




def addFaceToListUrl(url, uniqueListId, subscription_key):

    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }

    params = urllib.urlencode({
    })

    try:
        body = '{ "url": "' + url + '" }'
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/face/v1.0/facelists/"+uniqueListId+"/persistedFaces?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        response_status = response.status
        conn.close()

        if(response_status == 200):
            print "Face Added to List"
            jsonParsed = json.loads(data.decode('utf-8'))
            persistedId = jsonParsed["persistedFaceId"]
            return persistedId, 1
        else:
            print("Error in addFaceToListOctetStream function")
            print(data)
            return "err", 0

    except Exception as e:
        print("Exception Caught in Function addFaceToListUrl")
        return "err", 0



#Function Tested. Works Fine
def addFaceToListOctetStream(octet_stream, uniqueListId, subscription_key):

    headers = {
        # Request headers
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }

    params = urllib.urlencode({
    })

    try:
        body = octet_stream
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/face/v1.0/facelists/"+uniqueListId+"/persistedFaces?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        response_status = response.status
        conn.close()

        if(response_status == 200):
            print "Face Added to List"
            jsonParsed = json.loads(data.decode('utf-8'))
            persistedId = jsonParsed["persistedFaceId"]
            return persistedId, 1
        else:
            print("Error in addFaceToListOctetStream function")
            print(data)
            return "err", 0

    except Exception as e:
        print("Exception in addFaceToListOctetStream")
        return "err", 0




def faceSimilarity(faceId, faceListId, maxNumOfCandidatesReturned, subscription_key):

    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }

    params = urllib.urlencode({
    })

    try:
        body = '{"faceId" : "' +faceId+ '", "faceListId" : "' +faceListId+'", "maxNumOfCandidatesReturned" : '+str(maxNumOfCandidatesReturned)+'}'
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/face/v1.0/findsimilars?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        response_status = response.status
        conn.close()

        if (response_status == 200):
            return data, 1
        else:
            print(response_status)
            print("Error in function faceSimilarity Response")
            return "err", 0
    except Exception as e:
        print("Caught Exception in function faceSimilarity")
        return "err", 0