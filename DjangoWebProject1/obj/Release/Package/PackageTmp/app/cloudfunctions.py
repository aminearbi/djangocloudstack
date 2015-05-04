from CloudStack import *
from random import randint
import sys,random,datetime 
secret="4eBiewVZVlsynJ3hZAd1dTC0K-4AMZRhbGsZjvQtCSIMIWSkVa4gQkmTKw2LeFnNz_AOGAJlEmCodsVmnZ9A6g"
api="http://172.16.206.31:8080/client/api"
api2="http://196.203.216.18:5555/client/api"
apikey="qt2tNBaxT9L6Eo-0SVbPMQgMAgATP6CW6AV4jF3_QavPF-_E9ucz07lYkBkMcQEMXUQ470JNLprKtTOqJ8Y2Cw"
cloudclient = Client(api2,apikey,secret);


def serviceoffering():
    soss= cloudclient.listServiceOfferings()
    listof =[]
    for so in soss:
        listof.append((so['id'],so['name']))
    return listof

def listzones():
    soss= cloudclient.listZones()
    listof =[]
    for zo in soss:
        
        listof.append((zo['id'],zo['name']))
    return listof


def listtemplates():
    templates=cloudclient.listTemplates({'templatefilter':'community'})
    counter=0
    listtemplate=[]
    for temp in templates:
        
        listtemplate.append((temp['id'],temp['name']))
    return listtemplate
