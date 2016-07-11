#!/usr/bin/env python
# dumps pfsense backups for pfsense 2.3+ to a specified directory
import mechanize
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import time
import os
from os import listdir
import re
import gzip

# EDIT BELOW OPTIONS TO SUIT YOUR ENVIRONMENT
user = 'admin' # pfsense login name - make sure this user has permission to dump backups 
passwd = 'somepassword' # the above users password
backupdir = '/some/directory' # where you want backups to be stored
ip_address = '10.1.1.1' # the IP address of the pfsense server
retention_time = 30 # how long in days to keep old backups
compression = 0 # whether or not you want the dumps compressed after dumping - I don't use this myself since it dumps to a compressed zfs volume.
# STOP EDITS

now = int(time.time())

def get_backup():
    br = mechanize.Browser()
    br.set_handle_robots(False)
    response = br.open('https://' + ip_address + '/index.php')
    br.form = list(br.forms())[0]
    
    control = br.form.find_control('usernamefld')
    control.value = user
    
    control = br.form.find_control('passwordfld')
    control.value = passwd
    
    response = br.submit()
    
    for link in br.links():
        if 'Backup' in link.text:
            br.click_link(link)
            response = br.follow_link(link)
            break
    
    br.form = list(br.forms())[0]
    br.find_control("donotbackuprrd").items[0].selected=False
    response = br.submit()
    xml = response.read()
    
    if compression:
        filename = '%s/pfsense-config-%d.xml.gz' % (backupdir, now)
        fh = gzip.open(filename, 'w')
    else:
        filename = '%s/pfsense-config-%d.xml' % (backupdir, now)
        fh = open(filename, 'w')
    fh.write(xml)
    fh.close()
    return

def clean_backups():
    for file in listdir(backupdir):
        try:
            epoch = re.search('pfsense-config-([0-9]{10}).xml', file)
            if now - int(epoch.group(1)) > days_to_seconds(retention_time):
                os.remove(backupdir + '/' + file)
        except AttributeError:
            continue
    return

def days_to_seconds(days):
    seconds = ( days * 86400 )
    return(seconds)

get_backup()
clean_backups()
