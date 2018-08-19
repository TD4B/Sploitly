#!/usr/bin/python

import nmap
import sys
import re

#CLI Colors
class term:
    @staticmethod
    def blue(value):
        return '\033[94m' + value + '\033[0m'
    @staticmethod
    def green(value):
        return '\033[92m' + value + '\033[0m'
    @staticmethod
    def fail(value):
        return '\033[91m' + value + '\033[0m'
    @staticmethod
    def warn(value):
        return '\033[93m' + value + '\033[0m'
    @staticmethod
    def bold(value):
        return '\033[1m' + value + '\033[0m'

class protocol:
    def web(self):
        self.value = value

FAIL = term.fail('[*] Invalid input params, type --help for list of commands')

if len(sys.argv) < 2:
    print FAIL
    sys.exit()

if sys.argv[1] == '--help':
    text = '[*] Sploitly Ez Scan' + '\n' + '[*] Usage:' + '\n' + '[*] ./sploitly.py <targetipaddress>'
    print term.green(text)
    sys.exit()

addr=re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",sys.argv[1])

if addr:
    def scan():
        nm = nmap.PortScanner()
        nm.scan(sys.argv[1],arguments='-p-')
        ports = nm[sys.argv[1]].all_tcp()
        print term.blue(term.bold("[*] Scan Complete!"))
        print term.blue(term.bold("[*] Open Ports: " + str(ports)))
        return ports
    print term.blue("[*] Starting portscan on specified target: ") + sys.argv[1]
    print term.blue("[*] Please wait..")
    ports = scan()
    
else:
    print FAIL
    sys.exit()

# Web protocol check.
for i in ports:
    if 80 in ports:
        protocol.web = 'http'
    # defaults to 443 for the web scanner.
    elif 443 in ports:
        protocol.web = 'https'

if protocol.web == 'http':
    i = raw_input(term.bold(term.warn("[WARNING] No SSL/TLS available for web scan, continue with HTTP? [y/n] ")))
    if 'Y' == i.upper():
        print term.blue("[*] Select Web Scan Level (1-2)")
        print term.blue("[*] 1 = Light URL Scan/Spider.")
        print term.blue("[*] 2 = Deep Vulnerability Scan.")
        i = raw_input(term.bold(term.blue("[*] Enter in Scan Level: ")))
    else:
        print term.fail("[*] Exiting...")
        sys.exit()

if protocol.web == 'https':
    print term.warn("[WARNING] Although more secure, Network could detect attack/scan via SSL Offload or WAF, continue? Y/N")


def switch(x):
    return {
        '135':'tool',
        '139':'tool',
        '445':'tool',
    }.get(x,0)



