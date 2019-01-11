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

vqfxDict = {}

with open('inventory', 'r') as f:
    for line in f:
        vqfx = line.split(" ",1)[0]
        if ("srv" in vqfx) or ("vqfx" in vqfx and "pfe" not in vqfx):
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

    if "vqfx" in key:
        dev = Device(host=value['host'], user='root', password='Juniper',port=value['port'])
        dev.open()
        pprint(dev.facts)

        cu = Config(dev)
        config_set = '''
        set system host-name {hostname}
        set protocols lldp interface all
        '''.format(hostname=key)
        print config_set

        cu.load(config_set, format='set')
        cu.commit()

        dev.close()
