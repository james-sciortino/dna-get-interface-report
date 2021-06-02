from config import  DNA_FQDN, \
                    DNA_PORT, \
                    DNA_USER, \
                    DNA_PASS, \
                    DNA_SWITCHES, \
                    DNA_AUTH_API, \
                    DNA_DEVICE_API, \
                    DNA_INTERFACE_API
import requests
import json
from requests.auth import HTTPBasicAuth
import urllib3
from datetime import date
from prettytable import PrettyTable
import csv
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # Silence the insecure warning due to SSL Certificate

today = date.today() # Set  data and time
todays_date = today.strftime("%m-%d-%y") # Set  data and time format 

header_row = ['Switch Name', 'Switch Model', 'UP Access Ports', 'UP Module Ports', 'Total UP Ports', 'Total DOWN Ports', 'Total Ports']
device_table = PrettyTable(header_row)
device_table.padding_width = 1

headers = {'content-type': "application/json", 'x-auth-token': ""}

def dnac_login():
    """
    Use the REST API to Log into an DNA Center and retrieve ticket
    """
    url = "https://{}:{}{}".format(DNA_FQDN, DNA_PORT, DNA_AUTH_API)
    try:
    # Make Login request and return the response body
        response = requests.request("POST", url, auth=HTTPBasicAuth(DNA_USER, DNA_PASS),
                                headers=headers, verify=False)
    except requests.exceptions.ConnectionError:
        print("Unable to connect to address ", url)
        exit(1)
    
    if response.status_code != 200:
        print(
            "Login failed. Status code {}".format(
                response.status_code
            )
        )
    #Return the Token
    try:
        token = response.json()["Token"]
        print("Your token is {}".format(token))
        return token

    except KeyError:
        print("No token found in authentication response.")
        print("Response body: ")
        print(response.text)
        exit(1)

def network_switches(token):
    ids = []
    hostnames = []
    platforms = []
    switch_details = []
    for device in DNA_SWITCHES:
        url = "https://{}:{}{}?hostname={}".format(DNA_FQDN, DNA_PORT, DNA_DEVICE_API, device)
        headers["x-auth-token"] = token
        response = requests.get(url, headers=headers, verify=False)
        output = response.json()['response']
        for x in output:
            ids.append(x["id"])
            hostnames.append(x["hostname"])
            platforms.append(x["platformId"])
    for id, host, platform in (zip(ids, hostnames, platforms)):
        switch_details.extend([(id, host, platform)])
    return switch_details

def network_interfaces(token, hostname, id, series): 
    total_up = []
    total_down = []
    total_ports  = []
    switch_info = []
    url = "https://{}:{}{}{}".format(DNA_FQDN, DNA_PORT, DNA_INTERFACE_API, id)
    headers["x-auth-token"] = token
    response = requests.get(url, headers=headers, verify=False)
    output = response.json()['response']

    for interface in output:
        if interface["interfaceType"] == "Physical":
            if "GigabitEthernet0/0" != interface["portName"]:
                if "Bluetooth" not in interface["portName"]:
                    if "App" not in interface["portName"]:
                        total_ports.extend([(interface["portName"],interface["status"])])
                        if interface["adminStatus"] == "UP":
                            if interface["status"] == "up":
                                total_up.extend([(interface["portName"],interface["status"])])

    for interface in output:
        if interface["status"] == "down":
            if interface["interfaceType"] == "Physical":
                if "GigabitEthernet0/0" != interface["portName"]:
                    if "Bluetooth" not in interface["portName"]:
                        if "App" not in interface["portName"]:
                            total_down.extend([(interface["portName"],interface["status"])])
    switch_info.insert(0, hostname)
    switch_info.insert(1, series)
    module_ports = []
    access_ports = []

    if series == "C9410R":
        module = re.compile(r'(^\D+[5-6])(/0)(/\w)')
        access = re.compile(r'(^\D+[^5-6])(/0)(/\w)')
        for key, value in total_up:
            if "TwentyFiveGigE" in key and value == "up":
                for key, value in reversed(total_down):
                    if "TenGigabitEthernet" in key and "down" in value:
                        x = key,value
                        total_down.remove(x)
                        total_ports.remove(x)
                    if "FortyGigabitEthernet" in key and "down" in value:
                        x = key,value
                        total_down.remove(x)
                        total_ports.remove(x)
            elif "FortyGigabitEthernet" in key and value == "up:":
                for key, value in reversed(total_down):
                    if "TwentyFiveGigE" in key and "down" in value:
                        x = key,value
                        total_down.remove(x)
                        total_ports.remove(x)
                    if "TenGig" in key and "down" in value:
                        x = key,value
                        total_down.remove(x)
                        total_ports.remove(x)
            else:
                continue

    elif series == "C9300L-48UXG-4X" or "C9300-48UXM":
        module = re.compile(r'(^\D+[1-8])(/1)(/[1-8])')
        access = re.compile(r'(^\D+[1-8])(/0)(/\w)')

    try:
        for inter in total_up:
            mod = re.search(module, str(inter))
            if mod is not None:
                module_ports.append(mod.group())
        for inter in reversed(total_up):
            acc = re.search(access, str(inter))
            if acc is not None:
                access_ports.append(acc.group())
    except AttributeError:
        print("No such Attribute!")
        pass
    total_up = (len(total_up))
    total_ports = (len(total_ports))
    total_down = (len(total_down))
    module_ports = (len(module_ports))
    access_ports = (len(access_ports))
    return total_up, total_down, total_ports, switch_info, module_ports, access_ports, response

def spacer():
    print("+"+"-"*45+"+")

# Entry point for program
if __name__ == "__main__":

    # Step 1. Call the DNA Center API Authentication API with your DNA Center IP address, username, and password to generate an auth-x token for subsequent API calls.
    spacer()
    print("Geting DNA Auth Token ...")
    login = dnac_login()

    # Step 2. Call the DNA Center API Get Device list to identify all Device UUIDs based on a comma-seperated list of hostnames
    spacer()
    print("Searching DNA Center Inventory for the following switches: {}...".format(DNA_SWITCHES))
    switches = network_switches(login)
    print("Detailed interface output stored in flash memory")

    # Step 3. Generate CSV Template
    spacer()
    print("Creating .CSV Template...")
    csv_table = [header_row]

    # Step 4a. Call the DNA Center API **Get Device Interface count** to iterate through all Device IDs and identify all *available* interfaces, all *down* interfaces, and all *up* interfaces ( excluding Bluetooth, Management, and App interfaces, etc.)
    # Step 4b. Use regex to generate accurate interface report for specific switch model types. Modify as needed!
    print("Generating detailed report for each switch..")
    spacer()
    for id, hostname, series in switches:
        interfaces = network_interfaces(login, hostname, id, series)
        up = interfaces[0]
        down = interfaces[1]
        total = interfaces[2]
        info = interfaces[3]
        modules = interfaces[4]
        access = interfaces[5]
        for x in up, down, total, info, modules, access:
            device_table.add_row([info[0],series,access,modules,up,down,total])
            csv_table.append([info[0],info,access,modules,up,down,total])
            break

    #Step 5. Output a PrettyTable report of the analysis on your terminal.
    print(device_table)

    #Step 6. Generate a .CSV file report with with additional switch info, which can be shared with management. 
    spacer()
    print("Generating .CSV Report...")
    with open('port-report-{}.csv'.format(todays_date), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(csv_table)

    print("CSV report created in working directory: port-report-{}.csv".format(todays_date))