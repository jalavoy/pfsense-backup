#!/usr/bin/env python
"""dumps pfsense backups for pfsense 2.3+ to a specified directory"""
import mechanize
import ssl
ssl._create_default_https_context = ssl._create_unverified_context # pylint: disable=W0212
import time
import os
from os import listdir
import re
import gzip

# EDIT BELOW OPTIONS TO SUIT YOUR ENVIRONMENT
USER = 'admin' # pfsense login name - make sure this user has permission to dump backups 
PASSWORD = 'somepassword' # the above users password
BACKUPDIR = '/some/directory' # where you want backups to be stored
HOST = '10.1.1.1' # the IP address of the pfsense server
RETENTION_DAYS = 30 # how long in days to keep old backups
COMPRESSION = 0 # whether or not you want the dumps compressed after dumping
# STOP EDITS

NOW = int(time.time())

def get_backup():
    """logs into the web interface and generates the backup"""
    browser = mechanize.Browser()
    browser.set_handle_robots(False)
    response = browser.open('https://' + HOST + '/index.php')
    browser.form = list(browser.forms())[0]

    control = browser.form.find_control('usernamefld')
    control.value = USER

    control = browser.form.find_control('passwordfld')
    control.value = PASSWORD

    response = browser.submit()

    for link in browser.links():
        if 'Backup' in link.text:
            browser.click_link(link)
            response = browser.follow_link(link)
            break

    browser.form = list(browser.forms())[0]
    browser.form.find_control("donotbackuprrd").items[0].selected = False
    response = browser.submit()
    xml = response.read()

    if COMPRESSION:
        filename = '%s/pfsense-config-%d.xml.gz' % (BACKUPDIR, NOW)
        output = gzip.open(filename, 'w')
    else:
        filename = '%s/pfsense-config-%d.xml' % (BACKUPDIR, NOW)
        output = open(filename, 'w')
    output.write(xml)
    output.close()
    return

def clean_backups():
    """cleans old backups"""
    for dump in listdir(BACKUPDIR):
        try:
            epoch = re.search('pfsense-config-([0-9]{10}).xml', dump)
            if NOW - int(epoch.group(1)) > days_to_seconds(RETENTION_DAYS):
                os.remove(BACKUPDIR + '/' + dump)
        except AttributeError:
            continue
    return

def days_to_seconds(days):
    """converts days to seconds for epoch calculation"""
    seconds = (days * 86400)
    return seconds

get_backup()
clean_backups()
