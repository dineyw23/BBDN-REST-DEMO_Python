"""
Copyright (C) 2016, Blackboard Inc.
All rights reserved.
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
Neither the name of Blackboard Inc. nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY BLACKBOARD INC ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL BLACKBOARD INC. BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import json
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import ssl
import sys
from constants import *

requests.packages.urllib3.disable_warnings()

#Tls1Adapter allows for connection to sites with non-CA/self-signed
#  certificates e.g.: Learn Dev VM
class Tls1Adapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)

class Membership():

    def __init__(self, target_url, token):
        self.target_url = target_url
        self.token = token
        self.memberships_Path = '/learn/api/public/v1/courses/courseId/users' #create(POST)/get(GET)
        self.membership_Path = '/learn/api/public/v1/courses/courseId/users/userId'
        self.dskExternalId = 'BbDN-DSK'
        self.courseExternalId = "BbDN-Python-REST_Demo"
        self.termExternalId = 'BbDN-TERM'
        self.usrExternalId = 'bbdnrestdemouser'


    def execute(self, command, dsk, token):
        if "create" in command:
            print('[Membership:execute] : ' + command)
            self.createMembership(dsk, token)
        elif "read" in command:
            print('[Membership:execute] : ' + command)
            self.getMembership(token)
        elif "read_all" in command:
            print('[Membership:execute] : ' + command)
            self.getMemberships(token)
        elif "update" in command:
            print('[Membership:execute] : ' + command)
            self.updateMembership(dsk, token)
        elif "delete" in command:
            print('[Membership:execute] : ' + command)
            self.deleteMembership(token)


    def getMemberships(self, token):
        #GET /learn/api/public/v1/courses/{courseId}/users

        print('[Membership:getMemberships] token: ' + token)
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + token
        print('[Membership:getMemberships] authStr: ' + authStr)
        session = requests.session()
        session.mount('https://', Tls1Adapter()) # remove for production

        replacement = "externalId:"+COURSEEXTERNALID
        memberships_Path = self.memberships_Path
        memberships_Path = memberships_Path.replace("courseId", replacement)

        r = session.get("https://" + self.target_url + memberships_Path, headers={'Authorization':authStr}, verify=False)
        #r = session.get("https://" + self.target_url + self.memberships_Path+self.courseId+"/users", headers={'Authorization':authStr}, verify=False)
        print("[Membership:getMemberships()] STATUS CODE: " + str(r.status_code) )
        print("[Membership:getMemberships()] RESPONSE: " + r.text)


    def createMembership(self, dsk, token):
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + token

        print ("[Membership:createMembership()] Starting")

        self.PAYLOAD = {
            "dataSourceId":dsk, #self.dskExternalId, supported soon.
            "availability": {
                "available":"Yes"
            },
            "courseRoleId":"Instructor"
        }

        session = requests.session()
        session.mount('https://', Tls1Adapter()) # remove for production with commercial cert

        #self.membership_Path = '/learn/api/public/v1/courses/courseId/users/userId'
        replacement = "externalId:"+COURSEEXTERNALID
        membership_Path = self.membership_Path
        membership_Path = membership_Path.replace("courseId", replacement)

        replacement = "externalId:" + USEREXTERNALID
        membership_Path = membership_Path.replace("userId", replacement)

        r = session.put("https://" + self.target_url + membership_Path, data=json.dumps(self.PAYLOAD), headers={'Authorization':authStr, 'Content-Type':'application/json'}, verify=False)
        print("[Membership:createMembership()] STATUS CODE: " + str(r.status_code) )
        print("[Membership:createMembership()] RESPONSE: " + r.text)


    def getMembership(self, token):
        #GET /learn/api/public/v1/courses/{courseId}/users/{userId}
        print('[Membership:getMemberships] token: ' + token)
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + token
        print('[Membership:getMemberships] authStr: ' + authStr)
        session = requests.session()
        session.mount('https://', Tls1Adapter()) # remove for production

        replacement = "externalId:"+COURSEEXTERNALID
        membership_Path = self.membership_Path
        membership_Path = membership_Path.replace("courseId", replacement)

        replacement = "externalId:" + USEREXTERNALID
        membership_Path = membership_Path.replace("userId", replacement)

        r = session.get("https://" + self.target_url + membership_Path, headers={'Authorization':authStr},  verify=False)

        print("[Membership:getMembership()] STATUS CODE: " + str(r.status_code) )
        print("[Membership:getMembership()] RESPONSE: " + r.text)


    def updateMembership(self, dsk, token):
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + token

        self.PAYLOAD = {
            "dataSourceId":dsk,
            "availability": {
                "available":"No"
            },
            "courseRoleId":"Student"
        }

        session = requests.session()
        session.mount('https://', Tls1Adapter()) # remove for production with commercial cert

        replacement = "externalId:"+ COURSEEXTERNALID
        membership_Path = self.membership_Path
        membership_Path = membership_Path.replace("courseId", replacement)

        replacement = "externalId:" + USEREXTERNALID
        membership_Path = membership_Path.replace("userId", replacement)

        r = session.patch("https://" + self.target_url + membership_Path, data=json.dumps(self.PAYLOAD), headers={'Authorization':authStr, 'Content-Type':'application/json'}, verify=False)

        print("[Membership:updateMembership()] STATUS CODE: " + str(r.status_code) )
        print("[Membership:updateMembership()] RESPONSE: " + r.text)


    def deleteMembership(self, token):
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + token

        session = requests.session()
        session.mount('https://', Tls1Adapter()) # remove for production with commercial cert

        replacement = "externalId:"+ COURSEEXTERNALID
        membership_Path = self.membership_Path
        membership_Path = membership_Path.replace("courseId", replacement)

        replacement = "externalId:" + USEREXTERNALID
        membership_Path = membership_Path.replace("userId", replacement)

        r = session.delete("https://" + self.target_url + membership_Path, headers={'Authorization':authStr}, verify=False)

        print("[Membership:deleteMembership()] STATUS CODE: " + str(r.status_code) )
        print("[Membership:deleteMembership()] RESPONSE: " + r.text)