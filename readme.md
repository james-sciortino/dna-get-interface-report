# DNA-Get-Interface-Report
This code is for the Cisco DNA Center Platform and has been tested on following Cisco Catalyst 9300 and 9400 switch models: *C9300L-48UXG-4X, C9300-48UXM, C9410R*
You can update regular expressions within the code to get more accurate reports on different model types. 
This code utilizes three DNA Center APIs: 'Get Token', 'Get Device by ID' and 'Get Interface info by Id' 
This script is intended for network engineers tasked with providing interfaces reports on a per-switch basis.
A .CSV file will be generated at the end of this script.

# Summary
This code is particularly useful when you need to output a report of available interfaces across multiple switches.

For example, imagine you have a campus building that currently has five switches. Management expects that the business will add additional cubicles and users to each floor, and needs port density report for the building on a per-floor basis.
You want to perform capacity planning to understand how many additional switches you will need for this building.
Run this code yo generate a .CSV report with the utilization details:
    - Count of UP Access Ports
    - Count of UP Module Ports (or, Uplinks)
    - Count of Total UP Ports
    - Count of Total DOWN  Ports
    - Count of Total Ports

# How it works
This Python code intends to accomplish the following tasks:
- Step 1. Identify all Device IDs based on a comma-seperated list of hostnames (provided at the terminal)
- Step 2. Iterate through all Device IDs. Identify all *available* interfaces, all *down* interfaces, and all *up* interfaces ( excluding Bluetooth, Management, and App interfaces).
- Step 3. Leverage regex to parse specific interface reports for access ports and module ports, depending on the switch model.
- Step 4. Output a PrettyTable report for each switch.
- Step 5. *Optional* Output a .CSV file report with with additional switch info, which can be provided to management. 

# For Fabric Enabled or Non-Fabric Enabled Switches:
This code is particularly useful when you need to output a report of available interfaces across multiple switches.
For example, if you have a campus building that currently has five floors -- and two Catalyst 9300 switches per floor.
Management expects that the business will add additional cubicles and users to each floor, and needs port density report for the building on a per-floor basis.
Run this code to generate the current utilization report. 

# How to use
1. Update "config.py" with your DNA information, including hostname, port, username, password, and comma-seperated list of switch hostnames.
    - Do not modify any of the API calls below "# DNA API Calls"   

2. Make sure your folder has the following two files:
    - config.py - contains DNA IP, port, username, password - and YANG data models for DNA API calls
    - main.py - primary script

3. From a bash or PowerShell terminal, run the following command:
    - python main.py

4. To verify all required packages are installed:
    - pip install -r requirements.txt

Example Use-Case:
Imagine you have a building on your Campus LAN which the business plans to expand with new users, new cubicles, new Access Points, etc. 
Your manager tasks you with generating a report of *existing* active interfaces on the *existing* switches in the building, to better understand how many new switches are required.
    - The generated report will detail how many *access* ports are used, how many *module* (or, *uplink*) interfaces are used, and how many interfaces are currently available.
    - You will be presented with a PrettyTable in your Bash or PowerShell terminal with this report, and a .CSV file will be created with this report. 
    - The .CSV file will be titled with today's date, and can be shared with management. 

In this scenario, we have three Cisco Catalyst switches: Two Catalyst 9300 Series Switches, and one Catalyst 9400 Series Switch:

$ python main.py 
+--------------------------------------+-------------------------------------+-----------------+-----------------+----------------+------------------+-------------+
|             Switch Name              |    Switch Model   | UP Access Ports | UP Module Ports | Total UP Ports | Total DOWN Ports | Total Ports |
+--------------------------------------+-------------------------------------+-----------------+-----------------+----------------+------------------+-------------+
|             Switch-1                 |  C9300L-48UXG-4X  |        3        |        0        |       3        |        49        |      52     |
|             Switch-2                 |    C9300-48UXM    |        5        |        1        |       6        |        47        |      52     |
|             Switch-3                 |      C9410R       |        2        |        2        |       4        |        52        |      56     |
+--------------------------------------+-------------------------------------+-----------------+-----------------+----------------+------------------+-------------+
