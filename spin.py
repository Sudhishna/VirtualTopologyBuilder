import jinja2
import json
import os
import threading
from time import sleep
import subprocess
from threading import Timer
import time
from pprint import pprint
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
import re

campus_info = {"campuses":[{"fabric":1, "spine":2, "leaf":2, "server":2}]}

'''
def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def per_campus(start,end,leaf,spine):
  links = leaf * spine
  total = leaf + spine

  dict = []
  for num in range(1,spine+1):
    spine_id = num
    spine_ports = range(num+start, links+1+start, spine)
    end_list = []
    end_list.append(end)
    if num % 2 == 0 and num != spine:
      end += 1
      end_list.append(end)
    spine_ports.extend(end_list)
    #dict.update({spine_id:spine_ports})
    dict.append(spine_ports)

  l_ports = list(chunks(range(1+start, links+1+start), spine))
  for num,ports in enumerate(l_ports):
    leaf_id = num + 1 + spine
    leaf_ports = ports
    #dict.update({leaf_id:leaf_ports})
    dict.append(leaf_ports)


  return dict
'''

'''
def between_spines(start,end,spine1,spine2):
  links = spine1 * spine2
  total = spine1 + spine2

  dict = []
  for num in range(1,spine+1):
    #spine_id = num
    spine_ports = range(num+start, links+1+start, spine)
    dict.append(spine_ports)

  l_ports = list(chunks(range(1+start, links+1+start), spine))
  for num,ports in enumerate(l_ports):
    leaf_id = num + 1 + spine
    leaf_ports = ports
    dict.append(leaf_ports)

  return dict

ports_map = {}
'''

'''
start = 0
end = 0
ports = []
for campus in campus_info["campuses"]:
  leaf = campus["leaf"]
  spine = campus["spine"]
  fabric = campus["fabric"]
  server = campus["server"]
  total = leaf * spine
  end += total
  ports.extend(per_campus(start,end+1,leaf,spine))
  start +=  total + spine - 1
  end += spine - 1

dev_num = 1
for port in ports:
  ports_map.update({dev_num:port})
  dev_num += 1

spine_list = []
couter = 1
for campus in campus_info["campuses"]:
  spine_list.append(campus["spine"])


counter = 1
spine_lst = []
spine_ports = []
for index,spine in enumerate(spine_list):
  if counter != len(campus_info["campuses"]):
    spine1 = spine_list[index]
    spine2 = spine_list[index+1]
    total = spine1 * spine2
    end += total
    ports1 = between_spines(start,end,spine1,spine2)
    spine_ports.extend(ports1)
    start += total
  counter += 1
'''
inventory_file = "inventory"
open(inventory_file, 'w').close()

spine_id_list = []
spine_counter = 0
spine_count = 0
name_list = []
for index,campus in enumerate(campus_info["campuses"]):
  leaf = campus["leaf"]
  spine = campus["spine"]
  fabric = campus["fabric"]
  server = campus["server"]
  total = fabric + leaf + spine + server
  spine_id_lst = []
  for fabric in range(fabric):
    name_list.append("fabric")
  for num in range(spine_counter+1,spine + spine_counter + 1,1):
    spine_counter = num
    name_list.append("spine")
    spine_id_lst.append(spine_counter)
  spine_id_list.extend(spine_id_lst)
  spine_count += 1
  if spine_count % 2 == 0 and spine_count != len(campus_info["campuses"]):
    spine_id_list.extend(spine_id_lst)
  spine_counter += leaf
  for name in range(leaf):
    name_list.append("leaf")
  for name in range(server):
    name_list.append("server")

'''
for spine_id,spine_port in zip(spine_id_list,spine_ports):
  ports_map[spine_id].extend(spine_port)
'''

#ports_map = {1: [1, 2, 3, 4, 5, 6], 2: [5, 6, 7, 8, 9, 10], 3: [1, 7, 11, 12, 13, 14], 4: [2, 8, 13, 14, 15, 16], 5: [3, 9, 17, 18, 19, 20], 6: [4, 10, 19, 20, 21, 22], 7: [11, 15, 23, 24, 25, 26], 8: [12, 16, 25, 26, 27, 28], 9: [17, 21, 29, 30, 31], 10: [18, 22, 30, 31, 32],11: [23, 27], 12: [24, 28], 13: [29, 32]}
ports_map = {14: [41,42], 15: [41,43,44,45,46], 16: [42,45,46,47,48], 17: [43,47,49,50,51,52], 18: [44,48,49,50,53,54], 19: [51,53], 20: [52,54]}

portsMap = ""
counters = 1
for ports in ports_map:
  #print ports_map[ports]
  if counters == 1:
    #portsMap = '{"' + str(ports) + '"' + '=>' + str(ports_map[ports])
    portsMap = str(ports) + ":" + str(ports_map[ports])
  else:
    portsMap = portsMap + "*" + str(ports) + ":" + str(ports_map[ports])
    #portsMap = portsMap + ',' + '"' + str(ports) + '"' + '=>' + str(ports_map[ports])
  counters += 1

portsMap = portsMap.replace(" ","")
print portsMap

#serv_ports_map = {1: [], 2:[], 3: [], 4:[], 5:[], 6:[], 7:[23, 24], 8:[27, 28], 9:[29], 10:[32], 11:[], 12:[], 13:[]}
#print serv_ports_map

'''
counter = 1
servPortsMap = ""
for servPorts in serv_ports_map:
  #print serv_ports_map[servPorts]
  if counter == 1:
    #portsMap = '{"' + str(ports) + '"' + '=>' + str(ports_map[ports])
    servPortsMap = str(servPorts) + ":" + str(serv_ports_map[servPorts])
  else:
    servPortsMap = servPortsMap + "*" + str(servPorts) + ":" + str(serv_ports_map[servPorts])
    #portsMap = portsMap + ',' + '"' + str(ports) + '"' + '=>' + str(ports_map[ports])
  counter += 1

servPortsMap = servPortsMap.replace(" ","")
print servPortsMap
'''

#leaf = 2
#spine = 2

total= len(name_list)
#print name_list
#print(total)

#inventory_file = "inventory/inventory"
#open(inventory_file, 'w').close()

#f = open('sample.json', 'w')
#f.close()

def spinvm(dev_id,dev_name):
    # Sleeps a random 1 to 10 seconds
    # rand_int_var = randint(1, 10)
    #print "++++++++++" + str(number) + "**************"
    #print number
    #print dev_name
    #print portsMap
    print "\n\n"
    print 'vagrant','--vqfx-id=%s' % str(dev_id),'--ports-map=%s' % portsMap,'--dev-name=%s' % dev_name,'up'
    print "\n\n"
    subprocess.call(['vagrant','--vqfx-id=%s' % str(dev_id),'--ports-map=%s' % portsMap,'--dev-name=%s' % dev_name,'up'])
    print "Thread " + str(dev_id) +"completed spinup"
    time.sleep(300)

id_list = list(ports_map.keys())
#for i,name in zip(range(1, total+1),name_list):
for id,name in zip(id_list,name_list):
    spinvm(id,name)

'''
thread_list = []

for i,name in zip(range(1, total+1),name_list):
    #print i,name
    # Instantiates the thread
    # (i) does not make a sequence, so (i,name)
    t = threading.Timer(3.0,spinvm, args=(i,name))              
    # Sticks the thread in a list so that it remains accessible
    thread_list.append(t)

# Starts threads
for thread in thread_list:
    thread.start()
    time.sleep(300)

# This blocks the calling thread until the thread whose join() method is called is terminated.
# From http://docs.python.org/2/library/threading.html#thread-objects
for thread in thread_list:
    thread.join()
'''

# Demonstrates that the main process waited for threads to complete
print "Done creating vms"

'''
vqfxDict = {}

with open('inventory/inventory', 'r') as f:
    for line in f:
        vqfx = line.split(" ",1)[0]
        if "vqfx" in vqfx and "pfe" not in vqfx:
            vqfxDict[vqfx] = {}
            m = re.search('\w*.*ansible_host=(\w*.*?) ',line)
            host = m.group(1)
            vqfxDict[vqfx]['host'] = host
            m = re.search('\w*.*ansible_port=(\w*.*?) ',line)
            port = m.group(1)
            vqfxDict[vqfx]['port'] = port
print vqfxDict

for key,value in vqfxDict.iteritems():
    print "\n#####  Configuring: " + key + " #####\n"
    print "host " + value['host']
    print "port " + value['port']

    dev = Device(host=value['host'], user='root', password='Juniper',port=value['port'])
    dev.open()
    pprint(dev.facts)

    cu = Config(dev)
    cmd = "set system host-name " + key
    cu.load(cmd, format='set')
    cu.commit()

    dev.close()
'''
