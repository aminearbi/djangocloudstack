from CloudStack import *
from random import randint
import sys,random,datetime 



secret="4eBiewVZVlsynJ3hZAd1dTC0K-4AMZRhbGsZjvQtCSIMIWSkVa4gQkmTKw2LeFnNz_AOGAJlEmCodsVmnZ9A6g"
api="http://172.16.206.31:8080/client/api"
api2="http://196.203.216.18:5555/client/api"
apikey="qt2tNBaxT9L6Eo-0SVbPMQgMAgATP6CW6AV4jF3_QavPF-_E9ucz07lYkBkMcQEMXUQ470JNLprKtTOqJ8Y2Cw"
cloudclient = Client(api2,apikey,secret);
CentOSserver="22cff7e4-af82-408f-a400-221b5fb4ae2a"
Ubuntuserver="26dcfbfe-bad9-4bce-924d-9898bb54a5c8"
DebianServer="62a3d073-c843-48fb-a06a-94c5ae6c9987"


    


def createVM():
    print "#######################################"
    print "     Starting VM Creation Process      "
    print "#######################################"
    logger= open('logfile.log', 'a+')
    print "Please Select service offering"
    i=0
    soss= cloudclient.listServiceOfferings()
    for so in soss:
        i=i+1
        print "%s - Service Offering Name is : %s" %(i,so['name'])
    soffnumber = int(raw_input())
    servoff=soss[soffnumber-1]['id']
    templates=cloudclient.listTemplates({'templatefilter':'community'})
    counter=0
    print "Please Select a Template"
    for temp in templates:
        counter+=1
        print "%s - Template Name is : %s" %(counter,temp['name'])

    osnum=int(raw_input())
    osid =templates[osnum-1]['id']
    zones=cloudclient.listZones()
    ii=0
    for zo in zones :
        ii=ii+1
        print "%s - Zone Name is : %s" %(ii,zo['name'])
    zonenum= int(raw_input())
    zoneid=zones[zonenum-1]['id']
    print zoneid
    print "Please name your VM"
    thename=raw_input()
    print "your vm details are:\n name = %s\n zoneID = %s\n osId=%s\n service offering id is = %s" %(thename,zoneid,os,servoff)
    logger.write ("your vm details are:\n name = %s\n zoneID = %s\n osId=%s\n service offering id is = %s" %(thename,zoneid,os,servoff))
    sysdate = datetime.datetime.now()
    logger.write (str(sysdate))
    loger.close()
    
    print cloudclient.deployVirtualMachine({'serviceofferingid':servoff,'templateid':osid,'zoneid':zoneid,'displayname':thename,'name':thename,'networkids':'8f01e7e7-2130-4916-ba37-054bc7decf11'})
def DestroyVM():
    print "#######################################"
    print "     Starting VM Destroying Process    "
    print "#######################################"
    logger= open('logfile.log', 'a+')
    vms = cloudclient.listVirtualMachines({})
    i=0
    print "Please Pick the VM you want to destroy"
    for vm in vms:
        i=i+1
        print "%s - VM Name is : %s" %(i,vm['name'])
    vmnum=int(raw_input())
    vmid=vms[vmnum-1]['id']
    vmname = vms[vmnum-1]['name']
    cloudclient.destroyVirtualMachine({'id':vmid})
    logger.write ( "The machine Named %s is now : %s destroyed" %s(vmname,datetime.datetime.now()))
    logger.close()
def Portforwarding():
    print "##################################################"
    print "     Starting PortForwarding Process      "
    print "##################################################"
    publicip="bd873c0f-f166-471c-a4d7-9314c16ee9ac"
    forwardingnet="12ae4a18-e661-429e-b9b7-c65393fd3b7f"
    logger= open('logfile.log', 'a+')
    vms = cloudclient.listVirtualMachines({})
    i=0
    print "Please Pick the VM you want to do a portforwarding for"
    for vm in vms:
        i=i+1
        print "%s - VM Name is : %s" %(i,vm['name'])
    #vmnum=int(raw_input())
    vmid=vms[vmnum-1]['id']
    vmname=vms[vmnum-1]['name']
    print vmid
    print "Please enter a Private port"
    privateport=raw_input()
    print "Please enter a Public port"
    #publicport=raw_input()
    print "Please Pick the communication Protocol\n 1 - TCP\n 2 - UDP"
    #pick=raw_input()
    protocol="TCP"
    if(pick=="2"):
        protocol="UDP"
    print "You are about to create a portforwarding rule for the vm named :%s with the id: %s using the following paramaters" %(vmname,vmid)
    print "used protocol: %s\n public port: %s\n private port: %s" %(protocol,publicport,privateport)
    print "Do You Want To Continue?"
    #response=raw_input().lower()
    if(response=="yes" or response=="y"):
        cloudclient.createPortForwardingRule({
        'ipaddressid':publicip,
        'privateport':privateport,
        'protocol':protocol,
        'publicport':publicport,
        'virtualmachineid':vmid,
        #'cidrlist':'172.16.2.2/16',
        'openfirewall': 'true'
        #'networkid':'12ae4a18-e661-429e-b9b7-c65393fd3b7f'
        })
        logger.write("a port forwarding rule for the VM named : %s on the private port : %s to the public port : %s has been created at %s" %(vmname,privateport,publicport,datetime.datetime.now()))
        logger.close()
def StopVM():
    print "##################################################"
    print "                 Stoping VM Process               "
    print "##################################################"
    logger= open('logfile.log', 'a+')
    vms = cloudclient.listVirtualMachines({'state':'Running'})
    i=0
    if (len(vms)==0):
        print "There's no VM that can be stopped right now"
    else:
        print "Please Pick the VM you want to stop"
        for vm in vms:
            i=i+1
            print "%s - VM Name is : %s" %(i,vm['name'])
        vmnum=int(raw_input())
        vmstate=vms[vmnum-1]['state']
        vmid=vms[vmnum-1]['id']
        vmname=vms[vmnum-1]['name']
        if(vmstate.lower()=="running"):
            cloudclient.stopVirtualMachine({'id':vmid})
        logger.write ( "The machine Named %s is stopped at : %s\n" %(vmname,datetime.datetime.now()))
        print "The machine Named %s is stopped at : %s\n" %(vmname,datetime.datetime.now())
        logger.close()
def StartVM():
    print "##################################################"
    print "                 Starting VM Process               "
    print "##################################################"
    logger= open('logfile.log', 'a+')
    vms = cloudclient.listVirtualMachines({'state':'Stopped'})
    i=0
    if (len(vms)==0):
        print "there's no VM that can be Started right now"
        return
    else:
        print "Please Pick the VM you want to Start"
        for vm in vms:
            i=i+1
            print "%s - VM Name is : %s" %(i,vm['name'])
        vmnum=int(raw_input())
        vmstate=vms[vmnum-1]['state']
        vmid=vms[vmnum-1]['id']
        vmname=vms[vmnum-1]['name']
        if(vmstate.lower()!="running"):
            cloudclient.startVirtualMachine({'id':vmid})
        logger.write ( "The machine Named %s is Started at : %s \n" %(vmname,datetime.datetime.now()))
        print "The machine Named %s is Started at : %s \n" %(vmname,datetime.datetime.now())
        logger.close()
def getPortForwardingRules():
    usedport=[]
    prule=cloudclient.listPortForwardingRules()
    for rule in prule:
        usedport.append(rule['publicport'])
    return usedport
def setForwardingPort(usedport=[]):
   while True:
       port=randint(0,60000)
       if not port in usedport:
           return str(port)
def CreateVMwithPortForwarding():
    print "#######################################"
    print "     Starting VM Creation Process      "
    print "#######################################"
    logger= open('logfile.log', 'a+')
    print "Please Select service offering"
    i=0
    soss= cloudclient.listServiceOfferings()
    for so in soss:
        i=i+1
        print "%s - Service Offering Name is : %s" %(i,so['name'])
    soffnumber = int(raw_input())
    servoff=soss[soffnumber-1]['id']
    print "Please select a template"
    templates=cloudclient.listTemplates({'templatefilter':'community'})
    counter=0
    print "Please Select a Template"
    for temp in templates:
        counter+=1
        print "%s - Template Name is : %s" %(counter,temp['name'])
    osnum=int(raw_input())
    osid =templates[osnum-1]['id']
    zones=cloudclient.listZones()
    ii=0
    for zo in zones :
        ii=ii+1
        print "%s - Zone Name is : %s" %(ii,zo['name'])
    zonenum= int(raw_input())
    zoneid=zones[zonenum-1]['id']
    print zoneid
    print "Please name your VM"
    thename=raw_input()
    logger.write( "your vm details are:\n name = %s\n zoneID = %s\n osId=%s\n service offering id is = %s created at : %s" %(thename,zoneid,os,servoff,datetime.datetime.now()))
    print cloudclient.deployVirtualMachine({'serviceofferingid':servoff,'templateid':osid,'zoneid':zoneid,'displayname':thename,'name':thename,'networkids':'8f01e7e7-2130-4916-ba37-054bc7decf11'})
    vms= cloudclient.listVirtualMachines({'name':thename})
    newvmid=None
    for vm in vms:
        newvmid=vm['id']
    print "##################################################"
    print "     Starting PortForwarding Process      "
    print "##################################################"
    publicip="bd873c0f-f166-471c-a4d7-9314c16ee9ac"
    forwardingnet="12ae4a18-e661-429e-b9b7-c65393fd3b7f"
    privateportslist=["22","80","3000"]
    for portprivate in privateportslist:
        publicport=setForwardingPort(getPortForwardingRules())
        cloudclient.createPortForwardingRule({
        'ipaddressid':publicip,
        'privateport':portprivate,
        'protocol':'TCP',
        'publicport':publicport,
        'virtualmachineid':newvmid,
        #'cidrlist':'172.16.2.2/16',
        'openfirewall': 'true'
        #'networkid':'12ae4a18-e661-429e-b9b7-c65393fd3b7f'
        })
        logger.write("a port forwarding rule for the VM named : %s on the private port : %s to the public port : %s has been created at %s" %(thename,portprivate,publicport,datetime.datetime.now()))
    logger.close()
def TemplateCreation():
    print "##########################################"
    print "     CentOS Template Creation Process     "
    print "##########################################"
    logger= open('logfile.log', 'a+')
    print 'Please Enter a Name for The Template'
    name= raw_input()
    i=0
    vls=cloudclient.listVolumes()
    for vl in vls :
        i+=1
        print "%s - Machine name is %s and volume name is %s id : %s" %(i,vl['vmname'],vl['name'],vl['id'])
    inpt= int(raw_input())
    volumeid=vls[inpt-1]['id']
    cloudclient.createTemplate({
    'displaytext':name,
    'name':name,
    'ostypeid':'a01b94c6-a166-11e4-b2ef-005056847688',
    'bits':'64',
    'isfeatured':'true',
    'ispublic':'true',
    'volumeid':volumeid
}
)


def listtemplates():
    templates=cloudclient.listTemplates({'templatefilter':'community'})
    counter=0
    listtemplate=[]
    for temp in templates:
        counter+=1
        print "%s - Template Name is : %s" %(counter,temp['name'])
        listtemplate.append(temp['name'])
    return listtemplate

def listvms():
    vms=cloudclient.listVirtualMachines()
    listvms=[]
    for vm in vms:
        v=(vm['id'],vm['name'])
        listvms.append(v)
    return listvms









    




    
    


