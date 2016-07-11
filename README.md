# pfsense 2.3+ backup
I had a perl script to do this on 2.2, but since the update it hasn't worked. So I decided to start over with a language I'm not as familiar with.

I'm not a python guy at all so please excuse any less than ideal code in here. That said, it works fine.

You'll want to automate this with a cron job. I just symlink it into /etc/cron.daily/

You will need to install the mechanize python module, the easiest way to do that is with `pip install mechanize`
