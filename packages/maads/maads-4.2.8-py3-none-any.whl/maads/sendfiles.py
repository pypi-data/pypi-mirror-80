#############################################################
#
#  Author: Sebastian Maurice, PhD
#  Copyright by Sebastian Maurice 2018
#  All rights reserved.
#  Email: Sebastian.maurice@otics.ca
#
#############################################################

import json, urllib
import requests
import csv
import os
import imp
import re
import urllib.request
import asyncio
import validators
from urllib.parse import urljoin
from urllib.parse import urlsplit
from aiohttp import ClientSession



def formaturl(maindata,host,microserviceid,prehost,port):

    if len(microserviceid)>0:    
      mainurl=prehost + "://" + host +  ":" + str(port) +"/" + microserviceid + "/?hyperpredict=" + maindata
    else:
      mainurl=prehost + "://" + host + ":" + str(port) +"/?hyperpredict=" + maindata
        
    return mainurl
    
async def tcp_echo_client(message, loop,host,port,usereverseproxy,microserviceid):

    hostarr=host.split(":")
    hbuf=hostarr[0]
   # print(hbuf)
    hbuf=hbuf.lower()
    domain=''
    if hbuf=='https':
       domain=host[8:]
    else:
       domain=host[7:]
    host=domain  

    if usereverseproxy:
        geturl=formaturl(message,host,microserviceid,hbuf,port) #host contains http:// or https://
        message="GET %s\n\n" % geturl 

    reader, writer = await asyncio.open_connection(host, port, loop=loop)
    try:
      mystr=str.encode(message)
      writer.write(mystr)
      datam=''
      while True:
        data = await reader.read(1024)
      #  print(data)
        datam=datam+data.decode("utf-8")
       # print(datam)
        if not data:
           break
        
        await writer.drain()
   #   print(datam)  
      prediction=("%s" % (datam))
      writer.close()
    except Exception as e:
      print(e)
      return e
    
    return prediction

def hyperpredictions(maadstoken,pkey,theinputdata,host,port,usereverseproxy=0,microserviceid='',username='',password='',company='',email=''):
    if '_nlpclassify' not in pkey:
      theinputdata=theinputdata.replace(",",":")
    else:  
      buf2 = re.sub('[^a-zA-Z0-9 \n\.]', '', theinputdata)
      buf2=buf2.replace("\n", "").strip()
      buf2=buf2.replace("\r", "").strip()
      theinputdata=buf2

    if usereverseproxy:
       theinputdata=urllib.parse.quote(theinputdata)
  
    value="%s,[%s],%s" % (pkey,theinputdata,maadstoken)
    loop = asyncio.get_event_loop()
    val=loop.run_until_complete(tcp_echo_client(value, loop,host,port,usereverseproxy,microserviceid))
    return val
#########################################################
#######################VIPER Functions

def formaturlviper(maindata,host,microserviceid,prehost,port):

    if len(microserviceid)>0:    
      mainurl=prehost + "://" + host +  ":" + str(port) +"/" + microserviceid + "/" + maindata
    else:
      mainurl=prehost + "://" + host + ":" + str(port) +"/" + maindata
        
    return mainurl


async def fetch(client,url):
    async with client.get(url) as resp:
        assert resp.status == 200
        return await resp.text()

#############################VIPER API CALLS ################    
async def tcp_echo_clientviper(message, loop,host,port,microserviceid):

    hostarr=host.split(":")
    hbuf=hostarr[0]
   # print(hbuf)
    hbuf=hbuf.lower()
    domain=''
    if hbuf=='https':
       domain=host[8:]
    else:
       domain=host[7:]
    host=domain  

    #if len(microserviceid)>0:
    geturl=formaturlviper(message,host,microserviceid,hbuf,port) #host contains http:// or https://
    message="%s" % geturl 

    async with ClientSession() as session:
        html = await fetch(session,message)
        return html

def viperstats(vipertoken,host,port=-999,brokerhost='',brokerport=-999,microserviceid=''):

    if len(vipertoken)==0 or len(host)==0 or port==-999:
       return "Please enter vipertoken,host and port"

    value="viperstats?vipertoken="+vipertoken + "&brokerhost="+brokerhost+"&brokerport="+str(brokerport)
    loop = asyncio.get_event_loop()
    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))
    return val


def viperlisttopics(vipertoken,host,port=-999,brokerhost='',brokerport=-999,microserviceid=''):

    if len(vipertoken)==0 or len(host)==0 or port==-999:
       return "Please enter vipertoken,host and port"
    
    value="listtopics?vipertoken="+vipertoken + "&brokerhost="+brokerhost+"&brokerport="+str(brokerport)
    loop = asyncio.get_event_loop()
    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))
    return val

def vipersubscribeconsumer(vipertoken,host,port,topic,companyname,contactname,contactemail,location,description,brokerhost='',brokerport=-999,groupid='',microserviceid=''):

    if len(host)==0 or len(vipertoken)==0 or port==-999 or len(topic)==0 or len(companyname)==0 or len(contactname)==0 or len(contactemail)==0 or len(location)==0 or len(description)==0:
         return "Please enter host,port,vipertoken,topic, companyname,contactname,contactemail,location and description"
        
    value=("subscribeconsumer?vipertoken="+vipertoken + "&topic="+topic + "&companyname=" + companyname + "&contactname="+contactname +
           "&contactemail="+contactemail + "&location="+location+"&description="+description+ "&brokerhost="+brokerhost + "&brokerport="+str(brokerport) + "&groupid=" + groupid)
    loop = asyncio.get_event_loop()
    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))
    return val

def viperunsubscribeconsumer(vipertoken,host,port,consumerid,brokerhost='',brokerport=-999,microserviceid=''):

    if len(vipertoken)==0 or len(consumerid)==0 or len(host)==0:
         return "Please enter vipertoken,consumerid,host and port"
        
    value=("unsubscribeconsumer?vipertoken="+vipertoken + "&consumerid="+consumerid + "&brokerhost="+brokerhost +"&brokerport="+str(brokerport))
    loop = asyncio.get_event_loop()
    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))
    return val

def viperproducetotopic(vipertoken,host,port,topic,producerid,enabletls=0,delay=100,inputdata='',maadsalgokey='',maadstoken='',getoptimal=0,externalprediction='',brokerhost='',brokerport=-999,microserviceid=''):

    if len(host)==0 or len(vipertoken)==0 or port==-999 or len(topic)==0 or len(producerid)==0:
         return "Please enter host,port,vipertoken,topic, producerid"
        
    value=("producetotopic?vipertoken="+vipertoken + "&topic="+topic + "&producerid=" + producerid + "&getoptimal="+str(getoptimal) +
          "&delay=" + str(delay) +  "&enabletls="+str(enabletls)+ "&externalprediction="+externalprediction + "&inputdata="+inputdata + "&maadsalgokey="+maadsalgokey +"&maadstoken="+maadstoken + "&brokerhost="+brokerhost+"&brokerport="+str(brokerport)) 
    loop = asyncio.get_event_loop()
    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))
    return val

def viperconsumefromtopic(vipertoken,host,port,topic,consumerid,companyname,enabletls=0,delay=100,offset=0,brokerhost='',brokerport=-999,microserviceid=''):

    if len(host)==0 or len(vipertoken)==0 or port==-999 or len(topic)==0 or len(consumerid)==0 or len(companyname)==0:
         return "Please enter host,port,vipertoken,topic, consumerid,companyname"
        
    value=("consumefromtopic?vipertoken="+vipertoken + "&topic="+topic + "&consumerid=" + consumerid + "&offset="+str(offset) +
        "&delay=" + str(delay) +  "&enabletls=" + str(enabletls) + "&brokerhost="+brokerhost + "&brokerport="+str(brokerport)+"&companyname="+companyname)
    loop = asyncio.get_event_loop()
    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))
    return val

def viperhpdepredict(vipertoken,host,port,consumefrom,produceto,companyname,consumerid,producerid,hpdehost,enabletls=0,delay=0,hpdeport=-999,brokerhost='',brokerport=9092,
                     timeout=120,usedeploy=0,microserviceid=''):

    #reads the fieldnames and gets latest data from each stream (or fieldname)
    
    if (len(host)==0 or len(vipertoken)==0 or port==-999 or len(consumefrom)==0 or len(produceto)==0 or len(companyname)==0 or len(consumerid)==0
                 or len(producerid)==0 or len(hpdehost)==0 or hpdeport==-999):
         return "Please enter host,port,vipertoken,consumefrom,produceto,companyname,consumerid,producerid,hpdehost,hpdeport"
        
    value=("viperhpdepredict?vipertoken="+vipertoken + "&consumefrom="+consumefrom + "&produceto=" + produceto + "&consumerid="+consumerid +
           "&delay=" + str(delay) + "&enabletls=" + str(enabletls) + "&producerid="+producerid + "&usedeploy=" +str(usedeploy) +"&companyname="+companyname + "&hpdehost=" +hpdehost +"&hpdeport="+str(hpdeport)+"&brokerhost="+brokerhost + "&brokerport="+str(brokerport))
    loop = asyncio.get_event_loop()
    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))
    return val

def viperhpdeoptimize(vipertoken,host,port,consumefrom,produceto,companyname,consumerid,producerid,hpdehost,enabletls=0,delay=100,hpdeport=-999,usedeploy=0,
                      ismin=1,constraints='best',stretchbounds=20,constrainttype=1,epsilon=10,brokerhost='',brokerport=9092,
                     timeout=120,microserviceid=''):

    #reads the fieldnames and gets latest data from each stream (or fieldname)
    
    if (len(host)==0 or len(vipertoken)==0 or port==-999 or len(consumefrom)==0 or len(produceto)==0 or len(companyname)==0 or len(consumerid)==0
                 or len(producerid)==0 or len(hpdehost)==0 or hpdeport==-999):
         return "Please enter host,port,vipertoken,consumefrom,produceto,companyname,consumerid,producerid,hpdehost,hpdeport"
        
    value=("viperhpdeoptimize?vipertoken="+vipertoken + "&consumefrom="+consumefrom + "&produceto=" + produceto + "&consumerid="+consumerid +
         "&delay=" + str(delay) + "&enabletls=" + str(enabletls) + "&producerid="+producerid + "&companyname="+companyname + "&hpdehost=" +hpdehost +"&hpdeport="+str(hpdeport))
    loop = asyncio.get_event_loop()
    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))
    return val

def viperhpdetraining(vipertoken,host,port,consumefrom,produceto,companyname,consumerid,producerid,hpdehost,hpdeport=-999,offset=0,islogistic=0,
                      brokerhost='',brokerport=9092,timeout=120,microserviceid=''):

    #reads the fieldnames and gets latest data from each stream (or fieldname)
    
    if (len(host)==0 or len(vipertoken)==0 or port==-999 or len(consumefrom)==0 or len(produceto)==0 or len(companyname)==0 or len(consumerid)==0
                 or len(producerid)==0 or len(hpdehost)==0 or hpdeport==-999):
         return "Please enter host,port,vipertoken,consumefrom,produceto,companyname,consumerid,producerid,hpdehost,hpdeport"
        
    value=("viperhpdetraining?vipertoken="+vipertoken + "&consumefrom="+consumefrom + "&produceto=" + produceto + "&consumerid="+consumerid +
           "&producerid="+producerid + "&companyname="+companyname + "&hpdehost=" +hpdehost +"&hpdeport="+str(hpdeport)+"&brokerhost="+brokerhost+
           "&brokerport="+str(brokerport))
    loop = asyncio.get_event_loop()
    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))
    return val

def viperproducetotopicstream(vipertoken,host,port,topic,producerid,offset,enabletls=0,delay=100,brokerhost='',brokerport=-999,microserviceid=''):
    if (len(host)==0 or len(vipertoken)==0 or port==-999 or len(topic)==0 or len(producerid)==0):
         return "Please enter host,port,vipertoken,topic,producerid"
        
    value=("producetotopicstream?vipertoken="+vipertoken + "&topicname="+topic + "&delay=" + str(delay) + "&enabletls="+str(enabletls) +"&brokerhost="+brokerhost + "&brokerport="+str(brokerport) + "&producerid="+producerid + "&offset="+str(offset))
    loop = asyncio.get_event_loop()
    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))
    return val

def vipercreatetrainingdata(vipertoken,host,port,consumefrom,produceto,dependentvariable,independentvariables,
                            consumerid,producerid,offset,companyname,enabletls=0,delay=100,maxrows=-1,brokerhost='',brokerport=-999,microserviceid=''):

    if (len(host)==0 or len(vipertoken)==0 or port==-999 or len(consumefrom)==0 or len(produceto)==0 or len(dependentvariable)==0 or
        len(independentvariables)==0 or len(companyname)==0 or len(consumerid)==0 or len(producerid)==0):
         return "Please enter host,port,vipertoken,consumefrom,produceto,companyname,consumerid,producerid"
        
    value=("createtrainingdata?vipertoken="+vipertoken + "&consumefrom="+consumefrom + "&produceto="+produceto +
           "&dependentvariable="+dependentvariable+"&independentvariables="+independentvariables +"&offset="+str(offset)+
           "&delay=" + str(delay) + "&enabletls=" + str(enabletls) + "&consumerid="+consumerid + "&producerid="+producerid+"&companyname="+companyname + "&maxrows="+str(maxrows) + "&brokerhost="+brokerhost + "&brokerport="+str(brokerport))
    loop = asyncio.get_event_loop()
    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))
    return val

def vipercreatetopic(vipertoken,host,port,topic,companyname,contactname,contactemail,location,description,brokerhost='',brokerport=-999,numpartitions=1,replication=1,microserviceid=''):

    if len(host)==0 or len(vipertoken)==0 or port==-999 or len(topic)==0 or len(companyname)==0 or len(contactname)==0 or len(contactemail)==0 or len(location)==0 or len(description)==0:
         return "Please enter host,port,vipertoken,topic, companyname,contactname,contactemail,location and description"
        
    value=("createtopics?vipertoken="+vipertoken + "&topic="+topic + "&companyname=" + companyname + "&contactname="+contactname +
           "&contactemail="+contactemail + "&location="+location+"&description="+description+"&numpartitions="+str(numpartitions)+
           "&replicationfactor="+str(replication) + "&brokerhost="+brokerhost + "&brokerport=" + str(brokerport) )
    loop = asyncio.get_event_loop()
    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))
    return val

def viperconsumefromstreamtopic(vipertoken,host,port,topic,consumerid,companyname,enabletls=0,delay=100,offset=0,brokerhost='',brokerport=-999,microserviceid=''):

    if len(host)==0 or len(vipertoken)==0 or port==-999 or len(topic)==0 or len(consumerid)==0 or len(companyname)==0:
         return "Please enter host,port,vipertoken,topic, consumerid,companyname"
        
    value=("consumefromstreamtopic?vipertoken="+vipertoken + "&topic="+topic + "&consumerid=" + consumerid + "&offset="+str(offset) +
         "&delay=" + str(delay) + "&enabletls=" + str(enabletls) + "&brokerhost="+brokerhost + "&brokerport="+str(brokerport)+ "&companyname="+companyname)
    loop = asyncio.get_event_loop()
    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))
    return val


def vipercreatejointopicstreams(vipertoken,host,port,topic,topicstojoin,companyname,contactname,contactemail,description,
                                location,enabletls=0,brokerhost='',brokerport=-999,replication=1,numpartitions=1,microserviceid=''):
    if (len(host)==0 or len(vipertoken)==0 or port==-999 or len(contactname)==0 or len(contactemail)==0 or len(description)==0 or
        len(location)==0 ):
         return "Please enter host,port,vipertoken,contactname,contactemail,companyname,description,location"
        
    value=("createjointopicstreams?vipertoken="+vipertoken + "&topicname="+topic + "&topicstojoin="+topicstojoin +
           "&companyname="+companyname+"&contactname="+contactname +"&contactemail="+contactemail+"&brokerhost="+brokerhost+"&brokerport="+str(brokerport)+
           "&enabletls=" + str(enabletls) + "&description="+description + "&location="+location+"&replicationfactor="+str(replication)+"&numpartitions="+str(numpartitions))
    loop = asyncio.get_event_loop()
    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))
    return val

def vipercreateconsumergroup(vipertoken,host,port,topic,groupname,companyname,contactname,contactemail,description,
                                location,brokerhost='',brokerport=-999,microserviceid=''):
    if (len(host)==0 or len(vipertoken)==0 or port==-999 or len(contactname)==0 or len(contactemail)==0 or len(description)==0 or
        len(location)==0 or len(groupname)==0):
         return "Please enter host,port,vipertoken,contactname,contactemail,companyname,description,location,groupname"
        
    value=("createconsumergroup?vipertoken="+vipertoken + "&topic="+topic + "&groupname="+groupname +
           "&companyname="+companyname+"&contactname="+contactname +"&contactemail="+contactemail+
           "&description="+description + "&location="+location+"&brokerhost="+brokerhost+"&brokerport="+str(brokerport))
    loop = asyncio.get_event_loop()
    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))
    return val

def viperconsumergroupconsumefromtopic(vipertoken,host,port,topic,consumerid,groupid,companyname,enabletls=0,delay=100,offset=0,brokerhost='',brokerport=-999,microserviceid=''):
    if (len(host)==0 or len(vipertoken)==0 or port==-999 or len(companyname)==0 or len(consumerid)==0 or len(groupid)==0):
         return "Please enter host,port,vipertoken,consumerid,companyname,groupid"
        
    value=("consumergroupconsumefromtopic?vipertoken="+vipertoken + "&topic="+topic + "&consumerid="+consumerid +
          "&delay=" + str(delay) + "&enabletls=" + str(enabletls) + "&brokerhost="+brokerhost+"&brokerport="+str(brokerport) +"&offset="+str(offset) +"&companyname="+companyname+"&groupid="+groupid)
    loop = asyncio.get_event_loop()
    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))
    return val

def vipermodifyconsumerdetails(vipertoken,host,port,topic,companyname,consumerid,contactname='',contactemail='',location='',brokerhost='',brokerport=9092,microserviceid=''):
    if (len(host)==0 or len(vipertoken)==0 or port==-999 or len(companyname)==0 or len(consumerid)==0 ):
         return "Please enter host,port,vipertoken,consumerid,companyname,consumerid"
        
    value=("modifyconsumerdetails?vipertoken="+vipertoken + "&topic="+topic + "&consumerid="+consumerid +"&brokerhost="+brokerhost+"&brokerport="+str(brokerport)
            +"&companyname="+companyname+"&contactname="+contactname+"&contactemail="+contactemail+"&location="+location)
    loop = asyncio.get_event_loop()
    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))
    return val

def vipermodifytopicdetails(vipertoken,host,port,topic,companyname,isgroup=0,contactname='',contactemail='',location='',brokerhost='',brokerport=9092,microserviceid=''):
    if (len(host)==0 or len(vipertoken)==0 or port==-999 or len(companyname)==0 or len(topic)==0):
         return "Please enter host,port,topic,vipertoken,consumerid,companyname"
        
    value=("modifytopicdetails?vipertoken="+vipertoken + "&topic="+topic +"&brokerhost="+brokerhost+"&brokerport="+str(brokerport)
          + "&isgroup=" + str(isgroup)  +"&companyname="+companyname+"&contactname="+contactname+"&contactemail="+contactemail+"&location="+location)
    loop = asyncio.get_event_loop()
    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))
    return val

def viperactivatetopic(vipertoken,host,port,topic,microserviceid=''):
    if (len(host)==0 or len(vipertoken)==0 or port==-999 or len(topic)==0  ):
         return "Please enter host,port,vipertoken,topic"
        
    value=("activatetopic?vipertoken="+vipertoken + "&topic="+topic )
    loop = asyncio.get_event_loop()
    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))
    return val

def viperdeactivatetopic(vipertoken,host,port,topic,microserviceid=''):
    if (len(host)==0 or len(vipertoken)==0 or port==-999 or len(topic)==0  ):
         return "Please enter host,port,vipertoken,topic"
        
    value=("deactivatetopic?vipertoken="+vipertoken + "&topic="+topic )
    loop = asyncio.get_event_loop()
    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))
    return val

def vipergroupactivate(vipertoken,host,port,groupname,groupid,microserviceid=''):
    if (len(host)==0 or len(vipertoken)==0 or port==-999 or len(groupname)==0   or len(groupid)==0 ):
         return "Please enter host,port,vipertoken,groupname,groupid"
        
    value=("activategroup?vipertoken="+vipertoken + "&groupname="+groupname +"&groupid="+groupid)
    loop = asyncio.get_event_loop()
    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))
    return val

def vipergroupdeactivate(vipertoken,host,port,groupname,groupid,microserviceid=''):
    if (len(host)==0 or len(vipertoken)==0 or port==-999 or len(groupname)==0   or len(groupid)==0 ):
         return "Please enter host,port,vipertoken,groupname,groupid"
        
    value=("deactivategroup?vipertoken="+vipertoken + "&groupname="+groupname +"&groupid="+groupid)
    loop = asyncio.get_event_loop()
    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))
    return val

#val = viperstats('hivmg1TMR1zS1ZHVqF4s83Zq1rDtsZKh9pEULHnLR0BXPlaPEMZBEAyC7TY0','http://localhost',8000)
#print(val)

#val = viperlisttopics('hivmg1TMR1zS1ZHVqF4s83Zq1rDtsZKh9pEULHnLR0BXPlaPEMZBEAyC7TY0','http://localhost',8000)
#print(val)


#val=vipergroupdeactivate('hivmg1TMR1zS1ZHVqF4s83Zq1rDtsZKh9pEULHnLR0BXPlaPEMZBEAyC7TY0','http://localhost',8000,'stream-group',
                       #'GroupId-GBFXtNW7z325Pq56AMlU4Lh9HedQwV')

#val=vipergroupactivate('hivmg1TMR1zS1ZHVqF4s83Zq1rDtsZKh9pEULHnLR0BXPlaPEMZBEAyC7TY0','http://localhost',8000,'stream-group',
 #                      'GroupId-GBFXtNW7z325Pq56AMlU4Lh9HedQwV')
#http://localhost:8000/activategroup?groupname=demouser_r6w1_csv-demouser_r1w3_csv-Min11&groupid=GroupId-GBFXtNW7z325Pq56AMlU4Lh9HedQwV&
#vipertoken=hivmg1TMR1zS1ZHVqF4s83Zq1rDtsZKh9pEULHnLR0BXPlaPEMZBEAyC7TY0

#val=viperdeactivatetopic('hivmg1TMR1zS1ZHVqF4s83Zq1rDtsZKh9pEULHnLR0BXPlaPEMZBEAyC7TY0','http://localhost',8000,'kafka-test11')

#http://localhost:8000/deactivatetopic?topic=kafka-test11&vipertoken=hivmg1TMR1zS1ZHVqF4s83Zq1rDtsZKh9pEULHnLR0BXPlaPEMZBEAyC7TY0
#val=viperactivatetopic('hivmg1TMR1zS1ZHVqF4s83Zq1rDtsZKh9pEULHnLR0BXPlaPEMZBEAyC7TY0','http://localhost',8000,'kafka-test11')
#http://localhost:8000/activatetopic?topic=kafka-test11&vipertoken=hivmg1TMR1zS1ZHVqF4s83Zq1rDtsZKh9pEULHnLR0BXPlaPEMZBEAyC7TY0

# vipermodifytopicdetails(vipertoken,host,port,topic,companyname,contactname='',contactemail='',location='',brokerhost='',brokerport=9092,microserviceid=''):
   
#val=vipermodifytopicdetails('hivmg1TMR1zS1ZHVqF4s83Zq1rDtsZKh9pEULHnLR0BXPlaPEMZBEAyC7TY0','http://localhost',8000,'kafka-test11','OTICS')
#print(val)
#http://localhost:8000/modifytopicdetails?topic=kafka-test11&companyname=OTICS 2&brokerport=1000&brokerhost=localhost&location=Canada&contactemail=sebastian.maurice@gmail.com&vipertoken=hivmg1TMR1zS1ZHVqF4s83Zq1rDtsZKh9pEULHnLR0BXPlaPEMZBEAyC7TY0


#val=vipermodifyconsumerdetails('hivmg1TMR1zS1ZHVqF4s83Zq1rDtsZKh9pEULHnLR0BXPlaPEMZBEAyC7TY0','http://localhost',8000,'kafka-test11','OTICS',
 #                            'ConsumerId--OSSaepBXTLnehbqJ1aWlFuFCybX-2')


#http://localhost:8000/modifyconsumerdetails?topic=kafka-test11&companyname=OTICS 2&brokerport=1000&consumerid=
#ConsumerId--OSSaepBXTLnehbqJ1aWlFuFCybX-2&brokerhost=localhost&location=Canada&contactemail=sebastian.maurice@otics.ca&
#vipertoken=hivmg1TMR1zS1ZHVqF4s83Zq1rDtsZKh9pEULHnLR0BXPlaPEMZBEAyC7TY0

#viperconsumergroupconsumefromtopic(vipertoken,host,port,topic,consumerid,groupid,companyname,offset=0,brokerhost='',brokerport=-999,microserviceid=''):
    
#val=viperconsumergroupconsumefromtopic('hivmg1TMR1zS1ZHVqF4s83Zq1rDtsZKh9pEULHnLR0BXPlaPEMZBEAyC7TY0','http://localhost',8000,'demouser_r6w1_csv-demouser_r1w3_csv-Min11',
 #                            'ConsumerId-HY0Du9QohdgHKgiRFEacYNmPsAdQuy','GroupId-GBFXtNW7z325Pq56AMlU4Lh9HedQwV','OTICS')

#print(val)
#val=vipercreateconsumergroup('hivmg1TMR1zS1ZHVqF4s83Zq1rDtsZKh9pEULHnLR0BXPlaPEMZBEAyC7TY0','http://localhost',8000,'demouser_r6w1_csv-demouser_r1w3_csv-Min11',
 #                            'stream-group 7','OTICS','Sebastian Maurice','sebastian.maurice@otics.ca','test group','Toronto','',-999)
#print(val)
#http://localhost:8000/consumergroupconsumefromtopic?topic=demouser_r6w1_csv-demouser_r1w3_csv-Min11&consumerid=
#ConsumerId-HY0Du9QohdgHKgiRFEacYNmPsAdQuy&protocol=tcp&offset=0&companyname=OTICS&vipertoken=
#hivmg1TMR1zS1ZHVqF4s83Zq1rDtsZKh9pEULHnLR0BXPlaPEMZBEAyC7TY0&groupid=GroupId-GBFXtNW7z325Pq56AMlU4Lh9HedQwV

#http://localhost:8000/createconsumergroup?topic=demouser_r6w1_csv-demouser_r1w3_csv-Min11&groupname=stream-group 5&
#vipertoken=hivmg1TMR1zS1ZHVqF4s83Zq1rDtsZKh9pEULHnLR0BXPlaPEMZBEAyC7TY0&numpartitions=1&replicationfactor=1&
#companyname=OTICS test&contactname=sebastian maurice&
#contactemail=sebastian.maurice@otics.ca&description=This algorithm has optimal values for the topic&location=Toronto Ontario
#val=vipercreatejointopicstreams('hivmg1TMR1zS1ZHVqF4s83Zq1rDtsZKh9pEULHnLR0BXPlaPEMZBEAyC7TY0','http://localhost',8000,'joined-streamsmain10',
 #                               'dependentvariable,independentvariable1,independentvariable2,independentvariable3,independentvariable4,independentvariable5',\
  #                              'OTICS','Sebastian Maurice','sebastian.maurice@otics.ca','stream topics','Toronot','',-999,1,1)
#print(val)
#http://localhost:8000/createjointopicstreams?topicname=joined-streamsmain4&topicstojoin=dependentvariable,independentvariable1,independentvariable2,
#independentvariable3,independentvariable4,independentvariable5&companyname=OTICS advanced analytics&contactname=Sebastian Maurice&
#contactemail=sebastian.maurice@otics.ca&description=streamed topic&location=Toronto&replicationfactor=1&numpartitions=1&
#vipertoken=hivmg1TMR1zS1ZHVqF4s83Zq1rDtsZKh9pEULHnLR0BXPlaPEMZBEAyC7TY0

#val=viperconsumefromstreamtopic('hivmg1TMR1zS1ZHVqF4s83Zq1rDtsZKh9pEULHnLR0BXPlaPEMZBEAyC7TY0','http://localhost',8000,'joined-streamsmain4',
 #                               'ConsumerId-y9PHKDxbMRCu5U5eX0CPbEVto7Mc7C','OTICS',0)
#print(val)
#http://localhost:8000/consumefromstreamtopic?topic=joined-streamsmain4&consumerid=ConsumerId-y9PHKDxbMRCu5U5eX0CPbEVto7Mc7C&offset=0&
#protocol=tcp&companyname=OTICS&vipertoken=hivmg1TMR1zS1ZHVqF4s83Zq1rDtsZKh9pEULHnLR0BXPlaPEMZBEAyC7TY0

#vipercreatetopic(vipertoken,host,port,topic,companyname,contactname,contactemail,location,description,brokerhost='',brokerport=-999,numpartitions=1,replication=1,microserviceid=''):

#val=vipercreatetopic('hivmg1TMR1zS1ZHVqF4s83Zq1rDtsZKh9pEULHnLR0BXPlaPEMZBEAyC7TY0','http://localhost',8000,'python-topic2','OTICS',
 #                          'sebastian maurice','sebastian.maurice@otics.ca','Toronto','test subscription','',-999,1,1)

#print(val)

#http://localhost:8000/createtopics?topic=hpde-optimal2&vipertoken=hivmg1TMR1zS1ZHVqF4s83Zq1rDtsZKh9pEULHnLR0BXPlaPEMZBEAyC7TY0&
#numpartitions=1&replicationfactor=1&companyname=OTICS test&contactname=sebastian maurice&contactemail=sebastian.maurice@otics.ca&
#description=This holds the estimated parameter from HPDE for Real-time machine learning&location=Toronto Ontario


#val=vipercreatetrainingdata('hivmg1TMR1zS1ZHVqF4s83Zq1rDtsZKh9pEULHnLR0BXPlaPEMZBEAyC7TY0','http://localhost',8000,'joined-streamsmain4',
                            #  'training-datamain5','dependentvariable','independentvariable1,independentvariable2,independentvariable3,independentvariable4,independentvariable5','ConsumerId-y9PHKDxbMRCu5U5eX0CPbEVto7Mc7C','ProducerId-SqsojxPxXXtV4fcs-bSQsAZXDZV238',0,'OTICS')
#print(val)

#http://localhost:8000/createtrainingdata?consumefrom=joined-streamsmain4&produceto=training-datamain5&vipertoken=
#hivmg1TMR1zS1ZHVqF4s83Zq1rDtsZKh9pEULHnLR0BXPlaPEMZBEAyC7TY0&dependentvariable=dependentvariable&
#independentvariables=independentvariable1,independentvariable2,independentvariable3,independentvariable4,
#independentvariable5&offset=5&companyname=OTICS test&consumerid=ConsumerId-y9PHKDxbMRCu5U5eX0CPbEVto7Mc7C&
#producerid=ProducerId-SqsojxPxXXtV4fcs-bSQsAZXDZV238

#val=viperproducetotopicstream('hivmg1TMR1zS1ZHVqF4s83Zq1rDtsZKh9pEULHnLR0BXPlaPEMZBEAyC7TY0','http://localhost',8000,'joined-streamsmain4',
                             # 'ProducerId-qKBZL9pfE6Vlu258nLd4nrIMw4ABDj',0)
#print(val)

#http://localhost:8000/producetotopicstream?topicname=joined-streamsmain4&producerid=ProducerId-qKBZL9pfE6Vlu258nLd4nrIMw4ABDj&offset=0&
#vipertoken=hivmg1TMR1zS1ZHVqF4s83Zq1rDtsZKh9pEULHnLR0BXPlaPEMZBEAyC7TY0

#val=viperhpdetraining('hivmg1TMR1zS1ZHVqF4s83Zq1rDtsZKh9pEULHnLR0BXPlaPEMZBEAyC7TY0','http://localhost',8000,'training-datamain5',
 #                       'hpde-estimated-params3','OTICS','ConsumerId-gRy5mXjfEVYIyULprtyYE4RoCKcWUW','ProducerId-E2VObYiLwQ1szos42zjASD3K9YIZYP',
  #                      'http://localhost',8001,0,0,'localhost')

#http://localhost:8000/viperhpdetraining?consumefrom=training-datamain5&produceto=hpde-estimated-params3&timeout=120&
#vipertoken=hivmg1TMR1zS1ZHVqF4s83Zq1rDtsZKh9pEULHnLR0BXPlaPEMZBEAyC7TY0&offset=0&companyname=OTICS &brokerhost=localhost&brokerport=9092&
#consumerid=ConsumerId-gRy5mXjfEVYIyULprtyYE4RoCKcWUW&producerid=ProducerId-E2VObYiLwQ1szos42zjASD3K9YIZYP&hpdehost=http://localhost&hpdeport=8001

#val=viperhpdeoptimize('hivmg1TMR1zS1ZHVqF4s83Zq1rDtsZKh9pEULHnLR0BXPlaPEMZBEAyC7TY0','http://localhost',8000,'hpde-estimated-params3',
 #                       'hpde-predictions2','OTICS','ConsumerId-ArNNhxsy68wtQgOPE2p-JwpOELWVtg','ProducerId-mD6eZwVEPZZnHeAqwejgejDrg7WiQk',
  #                      'http://localhost',8001)

#http://localhost:8000/viperhpdeoptimize?consumefrom=hpde-estimated-params3&produceto=hpde-optimal2&timeout=120&
#vipertoken=hivmg1TMR1zS1ZHVqF4s83Zq1rDtsZKh9pEULHnLR0BXPlaPEMZBEAyC7TY0&companyname=OTICS &brokerhost=localhost&
#brokerport=9092&consumerid=ConsumerId-ArNNhxsy68wtQgOPE2p-JwpOELWVtg&producerid=ProducerId-6oSI2nINLgWFx2DkOcaJAfVr8LDJMD&
#hpdehost=http://localhost&hpdeport=8001


#val=viperhpdepredict('hivmg1TMR1zS1ZHVqF4s83Zq1rDtsZKh9pEULHnLR0BXPlaPEMZBEAyC7TY0','http://localhost',8000,'hpde-estimated-params3',
                       # 'hpde-predictions2','OTICS','ConsumerId-ArNNhxsy68wtQgOPE2p-JwpOELWVtg','ProducerId-mD6eZwVEPZZnHeAqwejgejDrg7WiQk',
                        #'http://localhost',8001,'',-999,120,0)
#print(val)

#http://localhost:8000/viperhpdepredict?consumefrom=hpde-estimated-params3&produceto=hpde-predictions2&timeout=120&
#vipertoken=hivmg1TMR1zS1ZHVqF4s83Zq1rDtsZKh9pEULHnLR0BXPlaPEMZBEAyC7TY0&companyname=OTICS &brokerhost=localhost&brokerport=9092&
#consumerid=ConsumerId-ArNNhxsy68wtQgOPE2p-JwpOELWVtg&producerid=ProducerId-mD6eZwVEPZZnHeAqwejgejDrg7WiQk&hpdehost=http://localhost&hpdeport=8001

#http://localhost:8000/viperhpdepredict?consumefrom=hpde-estimated-params3&produceto=hpde-predictions2&timeout=120&
#vipertoken=hivmg1TMR1zS1ZHVqF4s83Zq1rDtsZKh9pEULHnLR0BXPlaPEMZBEAyC7TY0&companyname=OTICS &brokerhost=localhost&
#brokerport=9092&consumerid=ConsumerId-ArNNhxsy68wtQgOPE2p-JwpOELWVtg&producerid=ProducerId-mD6eZwVEPZZnHeAqwejgejDrg7WiQk&
#hpdehost=http://localhost&hpdeport=8001
#val=viperconsumefromtopic('hivmg1TMR1zS1ZHVqF4s83Zq1rDtsZKh9pEULHnLR0BXPlaPEMZBEAyC7TY0','http://localhost',8000,'demouser_r6w1_csv-demouser_r1w3_csv-Min11',
                     #   'ConsumerId-HY0Du9QohdgHKgiRFEacYNmPsAdQuy',"OTICS")

#print(val)
#http://localhost:8000/consumefromtopic?topic=demouser_r6w1_csv-demouser_r1w3_csv-Min11&consumerid=ConsumerId-HY0Du9QohdgHKgiRFEacYNmPsAdQuy&
#offset=4&protocol=tcp&companyname=OTICS&vipertoken=hivmg1TMR1zS1ZHVqF4s83Zq1rDtsZKh9pEULHnLR0BXPlaPEMZBEAyC7TY0

#val=viperproducetotopic('hivmg1TMR1zS1ZHVqF4s83Zq1rDtsZKh9pEULHnLR0BXPlaPEMZBEAyC7TY0','http://localhost',8000,'demouser_r6w1_csv-demouser_r1w3_csv-Min11',
 #                       'ProducerId-V0FZEmkBj6rkyUbArgDSRH3uxapItJ',"",
  #                      'gAAAAABeXTRS0-qksslIbPqWUG1KXTdMmOAnSBe-JhrNUKhoSJ1I05zizDwilL4vKRBvq2ZaEAi2_RMG_YaVJ5g7bgqSRc0HyUhUSGj46ZbfpllR09K1zNhN65Zs0tOGLO_KBxeadrxGLWgeLvtHoHrEAyfF_ju-pg==',1)
#print(val)
#val=viperunsubscribeconsumer('hivmg1TMR1zS1ZHVqF4s83Zq1rDtsZKh9pEULHnLR0BXPlaPEMZBEAyC7TY0','http://localhost',8000,'ConsumerId-4UINvAP5dNRPACshoqktQn9rNtISvb','',-999)
#print(val)
#val=vipersubscribeconsumer('hivmg1TMR1zS1ZHVqF4s83Zq1rDtsZKh9pEULHnLR0BXPlaPEMZBEAyC7TY0','http://localhost',8000,'training-data','OTICS',
#                           'sebastian maurice','sebastian.maurice@otics.ca','Toronto','test subscription','',-999,'')
#print(val)
#http://localhost:8000/producetotopic?topic=demouser_r6w1_csv-demouser_r1w3_csv-Min11&producerid=ProducerId-V0FZEmkBj6rkyUbArgDSRH3uxapItJ&
#getoptimal=1&externalprediction=this is cool3mmmmm mmnnkllmlm;&vipertoken=hivmg1TMR1zS1ZHVqF4s83Zq1rDtsZKh9pEULHnLR0BXPlaPEMZBEAyC7TY0&
#maadstoken=gAAAAABeXTRS0-qksslIbPqWUG1KXTdMmOAnSBe-JhrNUKhoSJ1I05zizDwilL4vKRBvq2ZaEAi2_RMG_YaVJ5g7bgqSRc0HyUhUSGj46ZbfpllR09K1zNhN65Zs0tOGLO_KBxeadrxGLWgeLvtHoHrEAyfF_ju-pg==

#http://localhost:8000/unsubscribeconsumer?consumerid=ConsumerId-Eoa1ZHVORmmoaFpqqgUx0u1d8pNJX5
#&vipertoken=hivmg1TMR1zS1ZHVqF4s83Zq1rDtsZKh9pEULHnLR0BXPlaPEMZBEAyC7TY0

#http://localhost:8000/createtopics?topic=training-data&vipertoken=hivmg1TMR1zS1ZHVqF4s83Zq1rDtsZKh9pEULHnLR0BXPlaPEMZBEAyC7TY0&
#numpartitions=1&replicationfactor=1&companyname=OTICS test&contactname=sebastian maurice&contactemail=sebastian.maurice@otics.ca&
#description=This algorithm has optimal values for the topic&location=Toronto Ontario

#val=viperlisttopics('hivmg1TMR1zS1ZHVqF4s83Zq1rDtsZKh9pEULHnLR0BXPlaPEMZBEAyC7TY0','http://localhost',8000)
#print(val)
#######################################################################################

def returndata(buffer,label):
      #print("LABEL: %s" % (label))
    try:
      if label=='PKEY:':
         val=""
         pattern = re.compile('\s*[,\n]\s*')
         fixed = pattern.sub(', ', buffer)
         listvalues=fixed.split(', ')
         val=[s for s in listvalues if label in s]      
         rval=val[0].split(':')[1]
      elif label=='ALGO0:':
         val=""
         pattern = re.compile('\s*[,\n]\s*')
         fixed = pattern.sub(', ', buffer)
         listvalues=fixed.split(', ')
         #print(listvalues)
         val=[s for s in listvalues if label in s]
         #print(val)
         rval=val[0].split(':')[1]
      elif label=='ACCURACY0:':
         val=""
         pattern = re.compile('\s*[,\n]\s*')
         fixed = pattern.sub(', ', buffer)
         listvalues=fixed.split(', ')
         val=[s for s in listvalues if label in s]      
         rval=val[0].split(':')[1]
      elif label=='SEASON0:':
         val=""
         pattern = re.compile('\s*[,\n]\s*')
         fixed = pattern.sub(', ', buffer)
         listvalues=fixed.split(', ')
         val=[s for s in listvalues if label in s]      
         rval=val[0].split(':')[1]         

      elif label=='ALGO1:':
         val=""
         pattern = re.compile('\s*[,\n]\s*')
         fixed = pattern.sub(', ', buffer)
         listvalues=fixed.split(', ')
         #print(listvalues)
         val=[s for s in listvalues if label in s]
         #print(val)
         rval=val[0].split(':')[1]
      elif label=='ACCURACY1:':
         val=""
         pattern = re.compile('\s*[,\n]\s*')
         fixed = pattern.sub(', ', buffer)
         listvalues=fixed.split(', ')
         val=[s for s in listvalues if label in s]      
         rval=val[0].split(':')[1]
      elif label=='SEASON1:':
         val=""
         pattern = re.compile('\s*[,\n]\s*')
         fixed = pattern.sub(', ', buffer)
         listvalues=fixed.split(', ')
         val=[s for s in listvalues if label in s]      
         rval=val[0].split(':')[1]         
      elif label=='ALGO2:':
         val=""
         pattern = re.compile('\s*[,\n]\s*')
         fixed = pattern.sub(', ', buffer)
         listvalues=fixed.split(', ')
         #print(listvalues)
         val=[s for s in listvalues if label in s]
         #print(val)
         rval=val[0].split(':')[1]
      elif label=='ACCURACY2:':
         val=""
         pattern = re.compile('\s*[,\n]\s*')
         fixed = pattern.sub(', ', buffer)
         listvalues=fixed.split(', ')
         val=[s for s in listvalues if label in s]      
         rval=val[0].split(':')[1]
      elif label=='SEASON2:':
         val=""
         pattern = re.compile('\s*[,\n]\s*')
         fixed = pattern.sub(', ', buffer)
         listvalues=fixed.split(', ')
         val=[s for s in listvalues if label in s]      
         rval=val[0].split(':')[1]         
      elif label=='ALGO3:':
         val=""
         pattern = re.compile('\s*[,\n]\s*')
         fixed = pattern.sub(', ', buffer)
         listvalues=fixed.split(', ')
         #print(listvalues)
         val=[s for s in listvalues if label in s]
         #print(val)
         rval=val[0].split(':')[1]
      elif label=='ACCURACY3:':
         val=""
         pattern = re.compile('\s*[,\n]\s*')
         fixed = pattern.sub(', ', buffer)
         listvalues=fixed.split(', ')
         val=[s for s in listvalues if label in s]      
         rval=val[0].split(':')[1]
      elif label=='SEASON3:':
         val=""
         pattern = re.compile('\s*[,\n]\s*')
         fixed = pattern.sub(', ', buffer)
         listvalues=fixed.split(', ')
         val=[s for s in listvalues if label in s]      
         rval=val[0].split(':')[1]         
         
      elif label=='DATA:':
         val=""
         pattern = re.compile('\s*[:,\n]\s*')
         fixed = pattern.sub(', ', buffer)
         listvalues=fixed.split(', ')
         #print(listvalues)
         fdate=listvalues[1]
         inp=listvalues[2]
         pred=float(listvalues[3])
         acc=float(listvalues[4])
         rval=[fdate,inp,pred,acc]
      else:
         return "%s not found" % (label)
    except Exception as e:
        return "ERROR retrieving label data: %s" % e
    return rval

def retraining(maadstoken,pkey,thefile,autofeature,removeoutliers,hasseasonality,dependentvariable,url,summer,winter,shoulder,trainingpercentage,retrainingdays,retraindeploy,username='',passw='',company='',email=''):

   rn=0
   tstr=''
   
   with open(thefile, 'r') as f:
     reader = csv.reader(f)
     for row in reader:
       row = ",".join(row)
       tstr = tstr + str(row) + '\n'
       rn=rn+1
       
   head, fname = os.path.split(thefile)
   print("Please wait...training can take several minutes.")
   
   files = {'file': tstr,
    'mode':-1,        
    'type':'CSV',
    'filename':fname,
    'username': username,
    'password': passw,
    'rowcount': rn,
    'autofeature': autofeature,
    'removeoutliers': removeoutliers,
    'hasseasonality': hasseasonality,
    'company': company,
    'email': email,            
    'dependentvariable': dependentvariable,
    'title':'File Upload for Training',
    'summer':summer,
    'winter':winter,
    'shoulder':shoulder,
    'trainingpercentage':trainingpercentage,
    'retrainingdays':retrainingdays,
    'retraindeploy':retraindeploy,
    'maadstoken':maadstoken,        
    'pkey':pkey
            
   }

   #print(files)
   r = requests.post(url, files)
   msg = r.text
   #print ("Message %s" % (msg))
   
   return msg

def uploadcsvfortraining(maadstoken,thefile,autofeature,removeoutliers,hasseasonality,dependentvariable,url,throttle,summer,winter,shoulder,trainingpercentage,retrainingdays,retraindeploy,shuffle,theserverlocalname,username='',passw='',company='',email=''):

   rn=0
   tstr=''

   if len(thefile)>0:
       with open(thefile, 'r',encoding='utf-8') as f:
         reader = csv.reader(f)
         for row in reader:
           row = ",".join(row)
           tstr = tstr + str(row) + '\n'
           rn=rn+1
       head, fname = os.path.split(thefile)    
   elif len(theserverlocalname)>0:
       tstr=''
       fname=theserverlocalname
   else:
       return "ERROR: Must specify a local file, or a file in the server."
       
   
   print("Please wait...training can take several minutes.")
   
   files = {'file': tstr,
    'mode':0,        
    'type':'CSV',
    'filename':fname,
    'username': username,
    'password': passw,
    'rowcount': rn,
    'autofeature': autofeature,
    'removeoutliers': removeoutliers,
    'hasseasonality': hasseasonality,
    'company': company,
    'email': email,            
    'dependentvariable': dependentvariable,
    'title':'File Upload for Training',
    'summer':summer,
    'winter':winter,
    'shoulder':shoulder,
    'trainingpercentage':trainingpercentage,
    'retrainingdays':retrainingdays,
    'retraindeploy':retraindeploy,
    'shuffle':shuffle,
    'throttle':throttle,
    'maadstoken':maadstoken        
            
   }

   #print(files)
   r = requests.post(url, files)
   msg = r.text
   #print ("Message %s" % (msg))
   
   return msg

def getpredictions(maadstoken,attr,pkey,thefile,url,username='',passw='',company='',email=''):

   rn=0
   tstr=''

   
   if attr==0:
      tstr=thefile
         
      files = {'file': tstr,
        'mode':1,        
        'type':'CSV',
        'pkey':pkey,            
        'username': username,
        'password': passw,
    #'rowcount': rn,
    #'autofeature': autofeature,
    #'removeoutliers': removeoutliers,
    #'hasseasonality': hasseasonality,
       'company': company,
       'email': email,
       'maadstoken':maadstoken,        
    #'dependentvariable': dependentvariable,
       'title':'Do Predictions'
      }

   #print(files)
      r = requests.post(url, files)
      msg = r.text
   #print ("Message %s" % (msg))
   
      return msg


def dolistkeys(maadstoken,url,username='',passw='',company='',email=''):

   rn=0
   tstr=''

   
   files = {
      'mode':2,        
      'type':'CSV',        
      'username': username,
      'password': passw,
      'company': company,
      'email': email,
      'maadstoken':maadstoken,
     'title':'Do List keys'
   }

   #print(files)
   r = requests.post(url, files)
   msg = r.text
   #print ("Message %s" % (msg))
   
   return msg

def dolistkeyswithkey(maadstoken,pkey,url,username='',passw='',company='',email=''):

   rn=0
   tstr=''

   
   files = {
      'mode':3,
      'pkey':pkey,        
      'type':'CSV',        
      'username': username,
      'password': passw,
      'company': company,
      'email': email,
      'maadstoken':maadstoken,
     'title':'Do List keys with Key'
   }

   #print(files)
   r = requests.post(url, files)
   msg = r.text
   #print ("Message %s" % (msg))
   
   return msg

def dodeletewithkey(maadstoken,pkey,url,username='',passw='',company='',email=''):

   rn=0
   tstr=''

   
   files = {
      'mode':4,
      'pkey':pkey,        
      'type':'CSV',        
      'username': username,
      'password': passw,
      'company': company,
      'email': email,
      'maadstoken':maadstoken,
     'title':'Do Delete with Key'
   }

   #print(files)
   r = requests.post(url, files)
   msg = r.text
   #print ("Message %s" % (msg))
   
   return msg



def getpicklezip(maadstoken,pkey,url,localfolder,username='',passw='',company='',email=''):

    url = "%s/prodfiles/%s_DEPLOYTOPROD.zip" % (url,pkey)
    localname="%s/%s_DEPLOYTOPROD.zip" % (localfolder,pkey)
    try:
      urllib.request.urlretrieve(url, localname)
    except Exception as e:
      return "ERROR: %s" % e  
    #print(url)
    return "File retrieved: %s FROM %s" % (localname,url)


def sendpicklezip(maadstoken,pkey,url,localname,username='',passw='',company='',email=''):
    bn=os.path.basename(localname)
    data = {'mode':'uploads', 'username':username, 'password':passw,'company':company,'email':email,'pkey':pkey,'maadstoken':maadstoken}
    
    files = {'file': open(localname, 'rb')}
    try:
      r = requests.post(url, data=data, files=files)
    except Exception as e:
      return "ERROR: %s" % e  
    return "File Sent: %s TO %s" % (localname,url)
    
def deploytoprod(maadstoken,pkey,url,localname='',ftpserver='',ftpuser='',ftppass='',username='',passw='',company='',email=''):

    data = {'mode':'deploy', 'username':username, 'password':passw,'company':company,'email':email,'localname':localname,'pkey':pkey,'maadstoken':maadstoken,'ftpserver':ftpserver,'ftpuser':ftpuser,'ftppass':ftppass}

    #print(prodserverurl)
    bn=''

    try: 
        if len(localname)>0:
            bn=os.path.basename(localname)
            data = {'mode':'deploy', 'username':username, 'password':passw,'company':company,'email':email,'localname':bn,'maadstoken':maadstoken,'pkey':pkey,'ftpserver':ftpserver,'ftpuser':ftpuser,'ftppass':ftppass}        
            files = {'file': open(localname, 'rb')}
            r = requests.post(url, data=data, files=files)
        else:
            bn="%s_DEPLOYTOPROD.zip" % (pkey)
            data = {'mode':'deploy', 'username':username, 'password':passw,'company':company,'email':email,'localname':localname,'maadstoken':maadstoken,'pkey':pkey,'ftpserver':ftpserver,'ftpuser':ftpuser,'ftppass':ftppass}                
            r = requests.post(url, data=data)
    except Exception as e:
      return "ERROR: %s" % e  
    return "File Deployed: %s TO %s" % (bn,url)
#    return r.text

def nlp(maadstoken,url,buffer,theserverfolder='',detail=20,maxkeywords=10,username='',passw='',company='',email=''):
    isurl=0
    print("Please wait..this could take several minutes")
    if len(buffer)>0:
        if validators.url(buffer):
            isurl=1
        else:
            isurl=0
        try:    
            if os.path.isfile(buffer):  #pdf
                filename, file_extension = os.path.splitext(buffer)
                flower=file_extension.lower()
                bn=os.path.basename(buffer)
                if flower=='.pdf':         
                   files = {'file': open(buffer, 'rb')}
                elif flower=='.txt':
                   files = {'file': open(buffer, 'r')}               
                data = {'mode':'nlp1', 'username':username, 'password':passw,'company':company,'email':email,'localname':bn,'maadstoken':maadstoken,'theserverfolder':theserverfolder,'fvalue': detail,'maxkeywords': maxkeywords}
                r = requests.post(url, data=data, files=files)
            elif isurl==1:  #url
                data = {'mode':'nlp2', 'username':username, 'password':passw,'company':company,'email':email,'localname':buffer,'maadstoken':maadstoken,'fvalue': detail,'maxkeywords': maxkeywords}
                r = requests.post(url, data=data)
            else: #paste text
                data = {'mode':'nlp3', 'username':username, 'password':passw,'company':company,'email':email,'localname':buffer,'maadstoken':maadstoken,'fvalue': detail,'maxkeywords': maxkeywords}
                r = requests.post(url, data=data)
        except Exception as e:
            try:
              data = {'mode':'nlp3', 'username':username, 'password':passw,'company':company,'email':email,'localname':buffer,'maadstoken':maadstoken,'fvalue': detail,'maxkeywords': maxkeywords}
              r = requests.post(url, data=data)
            except Exception as e:
              return r.text
    elif len(theserverfolder)>0:
           data = {'mode':'nlp1', 'username':username, 'password':passw,'company':company,'email':email,'localname':buffer,'maadstoken':maadstoken,'theserverfolder':theserverfolder,'fvalue': detail,'maxkeywords': maxkeywords}
           r = requests.post(url, data=data)
        
    return r.text

def nlpaudiovideo(maadstoken,maads_rest_url,thefile='',theserverfolder='',duration=-1,offset=0,username='',passw='',company='',email=''):   
    print("Please wait..this could take several minutes")
    if len(thefile)>0:
      files = {'file': open(thefile, 'rb')}
      data = {'mode':'nlpaudiovideo', 'username':username, 'password':passw,'company':company,'email':email,'localname':thefile,'maadstoken':maadstoken,'thefolder': theserverfolder,'duration':duration,'offset':offset}
      r = requests.post(maads_rest_url, data=data, files=files)
    elif len(theserverfolder)>0:
      data = {'mode':'nlpaudiovideo', 'username':username, 'password':passw,'company':company,'email':email,'localname':thefile,'maadstoken':maadstoken,'thefolder': theserverfolder,'duration':duration,'offset':offset}
      r = requests.post(maads_rest_url, data=data)
    else:
        return "ERROR: Please choose a file or server folder"
    return r.text

def nlpocr(maadstoken,maads_rest_url,thefile='',theserverfolder='',username='',passw='',company='',email=''):
    print("Please wait..this could take several minutes")
    if len(thefile)>0:
      files = {'file': open(thefile, 'rb')}
      data = {'mode':'nlpocr', 'username':username, 'password':passw,'company':company,'email':email,'localname':thefile,'maadstoken':maadstoken,'thefolder': theserverfolder}
      r = requests.post(maads_rest_url, data=data, files=files)
    elif len(theserverfolder)>0:
      data = {'mode':'nlpocr', 'username':username, 'password':passw,'company':company,'email':email,'localname':thefile,'maadstoken':maadstoken,'thefolder': theserverfolder}
      r = requests.post(maads_rest_url, data=data)
    else:
        return "ERROR: Please choose a file or server folder"
    return r.text
    
#csvfile,iscategory,maads_rest_url,trainingpercentage,retrainingdays,retraindeploy
#12. maads.nlpclassify(MAADSTOKEN,iscategory,maads_rest_url,csvfile,theserverlocalname,throttle,csvonly,trainingpercentage,retrainingdays,retraindeploy)
#maads.nlpclassify(token, 1,maadsrest,csvfile,'',-1,csvonly,'',tp)
def nlpclassify(maadstoken,iscategory,maads_rest_url,thefile='',theserverlocalname='',throttle=-1,csvonly=0,username='',trainingpercentage=75,retrainingdays=0,retraindeploy=0,passw='',company='',email=''):
    print("Please wait..this could take several minutes")
    tstr=''
    rn=0
    if len(thefile)>0:
        with open(thefile, 'r', encoding='utf8') as f:
         reader = csv.reader(f)
         for row in reader:
           #print(row)  
           rowstr = ",".join(row)
          # print(len(row))
           if len(row)>2:
               print("Ignored ROW %d: Improperly formatted CSV.  You have too many commas separating your data." % (rn+1))
           elif len(row)==2 and len(row[0])>1 and len(row[1])>1:
               buf=row[1]
               buf=buf.replace(","," ")
               buf2 = re.sub('[^a-zA-Z0-9 \n\.]', '', buf)
               buf2=buf2.replace("\n", "").strip()
               buf2=buf2.replace("\r", "").strip()
               row[1]=buf2

               buf=row[0]
               buf=buf.replace(","," ")
               buf2 = re.sub('[^a-zA-Z0-9 \n\.]', '', buf)
               buf2=buf2.replace("\n", "").strip()
               buf2=buf2.replace("\r", "").strip()

               row[0]=buf2
               rowstr = ",".join(row)
               tstr = tstr + str(rowstr) + '\n'
           else:
               print("Ignored ROW %d: Improperly formatted CSV." % (rn+1))
           rn=rn+1
        base=os.path.basename(thefile)
        filename=os.path.splitext(base)[0]
    elif len(theserverlocalname)>0:
        tstr=''
        filename=theserverlocalname
    else:
        return "ERROR: Must specify a local file, or a file in the server"
        
    files = {'file': tstr,
        'mode':'nlpclassify',        
        'type':'CSV',
        'iscategory':iscategory,            
        'username': username,
        'password': passw,
        'trainingpercentage': trainingpercentage,
        'retrainingdays': retrainingdays,
        'retraindeploy': retraindeploy,
        'company': company,
        'email': email,
        'filename':filename,
        'csvonly':csvonly,
        'throttle':throttle,
        'maadstoken':maadstoken,     
    #'dependentvariable': dependentvariable,
        'title':'Do NLP Classify'
      }

    r = requests.post(maads_rest_url, files)
    msg = r.text

    if csvonly==1:
      localname=username + '_' + filename + '_nlpclassify_' + str(iscategory) + '_.csv'
      baseurl=urljoin(maads_rest_url,'/')
      url = "%smaadsweb/csvtemps/%s" % (baseurl,localname)
      #localname="%s" % (localname)
      try:
        urllib.request.urlretrieve(url, localname)
        return msg
      except Exception as e:
        return "ERROR retrieving NLP CSV: %s" % e

    return msg

def genpdf(maadstoken,maads_rest_url,pkey,urltomaadsserver,savetofolder,username='',passw='',company='',email=''):
    files = {'mode':'genpdf',        
        'username': username,
        'password': passw,
        'company': company,
        'email': email,
        'maadstoken':maadstoken,     
        'pkey':pkey     
      }

    r = requests.post(maads_rest_url, files)
    msg = r.text
# retrieve file
    try:
      url = "%s/maadsweb/pdfreports/%s.pdf" % (urltomaadsserver,pkey)
      localname="%s/%s.pdf" % (savetofolder,pkey)
      urllib.request.urlretrieve(url, localname)
      return "PDF retrieved: %s" % localname
    except Exception as e:  
      return "ERROR: Retrieving PDF: %s" % e 

def optimize (maadstoken,maads_rest_url,algo1,ismin=1,objeq='1,1,1',a1cons=1,boundslimits='none',forceupdate=0,algo2='',algo3='',a2cons=1,a3cons=1,iters=100,step=4,perc='min_0_max_0'):

    if len(algo1)<=0:
        return "ERROR: Algo 1 must be specified"

    
    files = {'mode':'optimize',        
        'algo1': algo1,
        'algo2': algo2,
        'algo3': algo3,
        'forceupdate': forceupdate,
        'boundslimits': boundslimits,     
        'maadstoken':maadstoken,     
        'a1cons':a1cons,
        'a2cons':a2cons,
        'a3cons':a3cons,
        'ismin':ismin,
        'rowlen':iters,
        'step':step,
        'perc':perc,     
        'objeq':objeq     
      }
    try:
      r = requests.post(maads_rest_url, files)
      msg = r.text
    except Exception as e:
      return "ERROR Optimizing.  Check your parameters."  
   
    return msg

    
def algoinfo(maadstoken,maads_rest_url,pkey,isrest=0,username='',passw='',company='',email=''):
    files = {'mode':'algoinfo',        
        'username': username,
        'password': passw,
        'company': company,
        'email': email,
        'maadstoken':maadstoken,     
        'pkey':pkey,
        'isrest':isrest     
      }

    r = requests.post(maads_rest_url, files)
    msg = r.text
   
    return msg

def nlpgeosentiment(maadstoken,maads_rest_url,lat,long,radius,searchterms,numtweets=50,wordcount=300,username='',passw='',company='',email=''):

    if len(searchterms)>0:
        searchterms=searchterms.replace(","," ")
        files = {'mode':'nlpgeosentiment',        
            'lat': lat,
            'long': long,
            'radius': radius,
            'searchterms': searchterms,
            'numtweets': numtweets,
            'wordcount': wordcount,             
            'maadstoken':maadstoken
          }

        r = requests.post(maads_rest_url, files)
        msg = r.text
    else:
       return "ERROR: Enter search terms" 
   
    return msg

def featureselectionjson(maadstoken,maads_rest_url,pkey,username='',passw='',company='',email=''):
    files = {'mode':'featureselection',        
        'username': username,
        'password': passw,
        'company': company,
        'email': email,
        'maadstoken':maadstoken,     
        'pkey':pkey     
      }

    r = requests.post(maads_rest_url, files)
    msg = r.text
   
    return msg
    
#getpicklezip('demouser','demouser0828','OTICS','sebastian.maurice@otics.ml','demouser_acnstocksdatatest_csv','http://www.otics.ca/maadsweb','c:/maads')
