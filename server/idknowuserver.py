'''
idKnowU Server
Copyright 2018 Seth Persigehl (KK4TEE)
Released under the MIT Licence
See LICENSE for more details

This script receives JSON wrapped base64 encoded JPG
streaming images from an AR device (e.g. HoloLens)
and then hands it off to OpenFace to see if any faces
in the picture can be recognized. If there are any
matches, the metadata and user inputed data are
returned to the HoloLens as a JSON file for display
to the user.

CherryPy is used as the web server, and HTTPS
transport can optionally be enabled if you provide
the required certificates.

This program was originally created during the
2018 Creating Reality Hackathon in Los Angeles, CA

'''

import cherrypy
import simplejson
import os
from time import sleep
from time import strftime
import datetime
import binascii


protocol = "http"
host = "0.0.0.0"
port = "8088"

imagesRootPath = 'images'
openFaceOutputpath = 'currentFace.txt'
userStoredDataparentPath = '../training-images/'

global goldImages
goldImages = {
    "name":"idKnowUServer1",
    "devices": {},
    
    "name": "name",
    "socialMedia": "socialMedia",
    "role": "role",
    "funFact": "funFact",
    "accuracy": "accuracy",
    "counter": "0"
    }
    
global goldUsers
goldUsers = {
    "name":"idKnowUServer1",
    "users": {}
    }
    
input_json = {}

def readData(path, cs):
    filestring = open(path, "r")
    s = str(filestring.read())
    filestring.close()
    entries = s.split(cs)

    return entries

def dictofpacking():
    facelist = readData(openFaceOutputpath, "&")
    userdata = readData(userStoredDataparentPath + facelist[0] +
                        '/' + facelist[0] + '.txt', "\n")
    goldImages["name"] = userdata[0]
    goldImages["socialMedia"] = userdata[1]
    goldImages["role"] = userdata[2]
    goldImages["funFact"] = userdata[3]
    goldImages["accuracy"] = facelist[1]
    goldImages["counter"] = str(int(goldImages["counter"]) + 1)
    return goldImages
    
class Root:
        
    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def uploadjpg(self):
        global goldImages
        print("PICTURE UPLOADED")
        result = {"operation": "request", "result": "success", "data":"IF you can read this, sending arbitrary data works"}
        input_json = cherrypy.request.json
        print("DeviceUniqueID: " + str(input_json["settings"]["deviceUniqueIdentifier"]))
        dt = datetime.datetime.utcnow()
        filename = (imagesRootPath 
            + "/" + str(dt.year) 
            + "/" + str(dt.month) 
            + "/" + str(dt.day) 
            + "/" + str(dt.hour)
            + "/" + str(dt.minute )
            + "/" + str(input_json["settings"]["deviceUniqueIdentifier"]) 
            + "-" + str(dt.year) 
            + "-" + str(dt.month) 
            + "-" + str(dt.day) 
            + "-" + str(dt.hour)
            + "-" + str(dt.minute )
            + "-" + str(dt.second) 
            + "-" + str(dt.microsecond).zfill(6)
            + ".jpg"
            )
            
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        
        f = open( filename,'wb') # Archive a copy of the image
        f.write(binascii.a2b_base64(input_json["image"]["0"]["base64"]))
        f.close()
        
        filename = imagesRootPath + "/latest_capture.jpg"
        f = open( filename,'wb') # Update the latest image
        f.write(binascii.a2b_base64(input_json["image"]["0"]["base64"]))
        f.close()
        
        input_json["image"]["0"]["base64"] = "stored to disk"
        input_json["image"]["0"]["URL"] = protocol + "://" + host + ":" + port + "/" + filename
        print(input_json["image"]["0"]["URL"])
        goldImages["devices"][str(input_json["settings"]["deviceUniqueIdentifier"])] = input_json
        
        ''' If the user is new, create a settings dictionary for their visualizations'''
        ''' # Feature add in progress. Probably won't finish in time, so cutting it out.
        goldUsers["users"][str(input_json["settings"]["deviceUniqueIdentifier"])] = \
            CreateRemoteSettings(str(input_json["settings"]["deviceUniqueIdentifier"]), KnownDevices)
            '''
            
        return result
    
    @cherrypy.expose
    def index(self):
        s = "<h1>idKnowU Server</h1><br>"
        s += "Client IP: "
        s += str(cherrypy.request.remote.ip)
        s += "<br>Server Socket: "
        s += str(cherrypy.server.socket_host)
        return s
        
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def jsonImages(self):
        #return readData(openFaceOutputpath)
        try:
            r = dictofpacking()
        except:
            r = ""
        return r
        #return goldImages
        
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def jsonUsers(self):
        return goldUsers

if __name__ == '__main__':
    
    cherrypy.config.update({'server.socket_host': host,
                        'server.socket_port': int(port),
                            # The bellow sections are used for HTTPS
                        #'server.ssl_module':  'builtin',
                        #'server.ssl_certificate': 'cert.pem',
                        #'server.ssl_certificate': 'fullchain.pem',
                        #'server.ssl_private_key': 'privkey.pem',
                        #'server.ssl_certificate_chain': 'chain.perm',
                       })
    cherrypy.config.update("Root.conf")
    #cherrypy.quickstart(Root(), '/')
    #cherrypy.quickstart(Root())
   
    cherrypy.tree.mount(Root(), "/", config="Root.conf")
    cherrypy.engine.start()
