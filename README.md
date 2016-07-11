# pfsense 2.3+ backup

## Requirements
* python 2.7.9+ - can use https://launchpad.net/~fkrull/+archive/ubuntu/deadsnakes on ubuntu 14.04
```bash
sudo add-apt-repository ppa:fkrull/deadsnakes
sudo apt-get update
sudo apt-get install python2.7
```
* python mechanize 
```bash
sudo apt-get install python-pip
pip install mechanize
```

I had a perl script to do this on 2.2, but since the update it hasn't worked. So I decided to start over with a language I'm not as familiar with.

I'm not a python guy at all so please excuse any less than ideal code in here. That said, it works fine.

You'll want to automate this with a cron job. I just symlink it into /etc/cron.daily/
```bash
ln -sv /path/to/backup-pfsense.py /etc/cron.daily
```

