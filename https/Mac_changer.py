#!/users/bin/env/python
import subprocess
import optparse
import re
# dir = os.makedirs("src",exist_ok=True)
# print(os.getcwd())

def change_mac(interface,new_mac):
    print("[+] changing Mac Address for ",interface,"to",new_mac)
    subprocess.call(["ifconfig",interface,"down"])
    subprocess.call(["ifconfig",interface,"hw","ether",new_mac])
    subprocess.call(["ifconfig",interface,"up"])

def get_argument():
    parser = optparse.OptionParser()
    parser.add_option("-i","--interface",dest="interface",help="Interface to change its Mac Address")
    parser.add_option("-m","--mac",dest="new_mac",help="New Mac address")
    (option, argument) = parser.parse_args()
    if not option.interface:
        parser.error("[+] Please specify an interface, Use  --help for more info")
    if not option.new_mac:
        parser.error("[+] Please specify a new Mac, use --help for more info")
    return option

def current_mac(interface):
    mac_output = subprocess.check_output("ifconfig",interface)
    mac_search = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w")
    if mac_search:
        return mac_search.group(0)
    else:
        print("[-] Could not read Mac address")
        return "Not found"

options =get_argument()
change_mac(options.interface,options.argument)
mac = current_mac(options.interface)
print("Current Mac : ",mac)