# smtp-vrfy
Test host that allow SMTP connections if they respond to VRFY requests &amp; use them to verify usernames

# Usage Information
```
usage: smtp-vrfy.py [-h] [-i <ip address>] [-u <username>]
                    [--user-list <FILE>] [--ip-list <FILE>]

Check a host for an open SMTP port and verify if a username exists on the mail
server

optional arguments:
  -h, --help          show this help message and exit
  -i <ip address>     valid IPv4 IP address
  -u <username>       username to verify
  --user-list <FILE>  file containing a list of usernames (1 username per
                      line)
  --ip-list <FILE>    file containing a list of IP addresses (1 IP per line)
```
