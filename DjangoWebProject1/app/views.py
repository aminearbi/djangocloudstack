"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from django.http import HttpResponse
from datetime import datetime
from django.template.loader import get_template
from django.template import Context
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from CloudStack import *
from random import randint



import sys,random 
import crud
import socket




secret="4eBiewVZVlsynJ3hZAd1dTC0K-4AMZRhbGsZjvQtCSIMIWSkVa4gQkmTKw2LeFnNz_AOGAJlEmCodsVmnZ9A6g"
api="http://172.16.206.31:8080/client/api"
api2="http://196.203.216.18:5555/client/api"
apikey="qt2tNBaxT9L6Eo-0SVbPMQgMAgATP6CW6AV4jF3_QavPF-_E9ucz07lYkBkMcQEMXUQ470JNLprKtTOqJ8Y2Cw"
cloudclient = Client(api2,apikey,secret);



def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        context_instance = RequestContext(request,
        {
            'title':'Home Page',
            'year':datetime.now().year,
        })
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        context_instance = RequestContext(request,
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        })
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        context_instance = RequestContext(request,
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        })
    )



def hello(request):
    return HttpResponse("Hello world")

'''
def current(request):
    now = datetime.now()
    t = get_template('current.html')
    html = t.render(Context({'date': now}))
    return HttpResponse(html)
    '''
def template(request):
    t = get_template('port.html')
    html = t.render(Context({
            'templates':crud.listtemplates()
        }))
    return HttpResponse(html)

@csrf_exempt
def SetPortforwarding(request):
    vms=crud.listvms()
    prule=cloudclient.listPortForwardingRules()
    rules=[]
    for vm in prule:
        v=(vm['ipaddress'],vm['privateport'],vm['publicport'],vm['protocol'],vm['state'],vm['virtualmachinedisplayname'])
        rules.append(v)
        
    t = get_template('port.html')
    html = t.render(Context({
            'rules':rules,
            'vms':vms,
            'dport':crud.setForwardingPort(crud.getPortForwardingRules())
        }))

    return HttpResponse(html)

@csrf_exempt
def CreatePortForwardingRule(request):
    vmid= request.POST['id']
    privateport = request.POST['sport']
    protocol= request.POST['protocol']
    publicport = request.POST['dport']
    #dport=crud.setForwardingPort(crud.getPortForwardingRules())

    publicip="bd873c0f-f166-471c-a4d7-9314c16ee9ac"
    forwardingnet="12ae4a18-e661-429e-b9b7-c65393fd3b7f"
    logger= open('logfile.log', 'a+')

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
    logger.write("a port forwarding rule for the VM named : %s on the private port : %s to the public port : %s has been created at %s" %(vmid,privateport,publicport,datetime.now()))
    logger.close()

    return HttpResponseRedirect('/port/')
@csrf_exempt
def startvm(request):
    vms = cloudclient.listVirtualMachines({'state':'Stopped'})
    listvms=[]
    for vm in vms:
        v=(vm['id'],vm['name'])
        listvms.append(v)
    
    t = get_template('startvm.html')
    html = t.render(Context({
            'vms':listvms
        }))
    
    return HttpResponse(html)
@csrf_exempt
def startvmresult(request):
    vmid = request.POST['id']
    cloudclient.startVirtualMachine({'id':vmid})
    return HttpResponseRedirect('/startvm/')
@csrf_exempt
def stopvm(request):
    vms = cloudclient.listVirtualMachines({'state':'Running'})
    listvms=[]
    for vm in vms:
        v=(vm['id'],vm['name'])
        listvms.append(v)
    
    t = get_template('stopvm.html')
    html = t.render(Context({
            'vms':listvms
        }))
    return HttpResponse(html)
@csrf_exempt
def stopvmresult(request):
    vmid = request.POST['id']
    cloudclient.stopVirtualMachine({'id':vmid})
    return HttpResponseRedirect('/stopvm/')



def destroyvm(request):
    vms = crud.listvms()
    t = get_template('destroyvm.html')
    html = t.render(Context({
            'vms':vms
        }))
    return HttpResponse(html)
@csrf_exempt
def destroyvmresult(request):
    vmid = request.POST['id']
    cloudclient.destroyVirtualMachine({'id':vmid})
    return HttpResponseRedirect('/destroyvm/')
@csrf_exempt
def chat(request):
    vms = cloudclient.listVirtualMachines({'state':'Running'})
    t = get_template('chat.html')
    html = t.render(Context({
            'vms':vms
        }))
    return HttpResponse(html)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
@csrf_exempt
def chatlive(request):
    if 'id' in request.POST:
        vmid = request.POST['id']

        prule=cloudclient.listPortForwardingRules()
        for crule in prule:
            if crule['virtualmachineid'] == vmid and crule['privateport'] == '3000':
                rule = crule
        dport = int(rule['publicport']);
        print dport
        global s 
        
        p=s.connect(('196.203.216.18', dport))
        msg = s.recv(2048)
        t = get_template('chatlive.html')
        html = t.render(Context({
                'msg':msg
            }))
        return HttpResponse(html)
    elif 'input' in request.POST:
        msg = request.POST['input']
        s.send(msg)
        output = s.recv(2048)
        t = get_template('chatlive.html')
        html = t.render(Context({
                'msg':output
            }))
        return HttpResponse(html)
    else:
        t = get_template('chatlive.html')
        html = t.render(Context())
        return HttpResponse(html)
@csrf_exempt
def template(request):
    import app.cloudfunctions as funct
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/vmcreation.html',
         context_instance = RequestContext(request,
        {
            'title':'Create Virtual Machine',
            'message':'You Can Create a Virtual machine from Here.',
            'templates':funct.listtemplates(),
            'ostypes':funct.serviceoffering(),
            'zones':funct.listzones(),
        })
    )
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
@csrf_exempt
def createvm(request):

    cloudclient.deployVirtualMachine({'serviceofferingid':request.POST['os'],'templateid':request.POST['templates'],'zoneid':request.POST['zones'],'displayname':request.POST['vmname'],'name':request.POST['vmname'],'networkids':'8f01e7e7-2130-4916-ba37-054bc7decf11'})
    vms= cloudclient.listVirtualMachines({'name':request.POST['vmname']})
    newvmid=None
    for vm in vms:
        newvmid=vm['id']
   
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
@csrf_exempt
def listvm(request):
    vms = cloudclient.listVirtualMachines();
    listvms=[]
    for vm in vms:
        listvms.append((vm['id'],vm['name'],vm['state'],vm['templatename'],vm['created'],vm['hypervisor'],vm['memory']))
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/vmdetails.html',
         context_instance = RequestContext(request,
        {
            'vms':listvms
        })
    )
