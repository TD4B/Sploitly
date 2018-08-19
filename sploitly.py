#!/usr/bin/python

import nmap
import sys
import re
import subprocess

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

# Web Application Enumeration Scans.

def web_scanner(type):
    print term.blue("[*] Running Nikto Scan, this may take a while..")
    output = subprocess.check_output(["nikto --host " + type + "://" + sys.argv[1]],shell=True)
    outputs = output.split("\n")
    for lines in outputs:
        if 'Server:' in lines:
            server_info = lines
    print term.green("[*] Got Server Info!")
    print term.green("[*] " + server_info)
    print term.green("[*] Nikto Scan Complete.. writing data to file..Results.txt")
    f = open("Results.txt","w")
    f.write("### Open Ports ###\n")
    f.write(str(ports) + "\n")
    f.write("### Web Scan Results ###\n")
    f.write(str(output))
    f.close()


if protocol.web == 'http':
    i = raw_input(term.bold(term.warn("[WARNING] No SSL/TLS available for web scan, continue with HTTP? [y/n] ")))
    if 'Y' == i.upper():
        web_scanner(protocol.web)
    else:
        print term.fail("[*] Exiting...")
        sys.exit()

if protocol.web == 'https':
    i = raw_input(term.green("[HTTPS] Secure Socket Layer Scan available, continue [y/n]?"))    
    if 'Y' == i.upper():
        web_scanner(protocol.web)
    else:
        print term.fail("[*] Exiting...")
        sys.exit()

# Protocol Layer Enumeration scans.

def switch(x):
    return {
        '135':'tool',
        '139':'tool',
        '445':'tool',
    }.get(x,0)



