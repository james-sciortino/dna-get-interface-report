# DNA-Get-Interface-Report
This code is for the Cisco DNA Center Platform and has been tested on following Cisco Catalyst 9300 and 9400 switch models: **C9300L-48UXG-4X, C9300-48UXM, C9410R**

This code is intended for network engineers tasked with providing interfaces reports on a per-switch basis.

Note:
- You can update regular expressions within the code to get more accurate reports on different model types. 
- This code utilizes three DNA Center APIs: 'Get Token', 'Get Device by ID' and 'Get Interface info by Id' 
- A .CSV file will be generated at the end of this script.

# Summary
This code is particularly useful when you need to output a report of available interfaces across multiple switches.

For example, imagine the following:
- You have a campus building that currently has five switches. 
- The business plans to add additional cubicles and users to each floor. 
- The network team needs to properly plan and budget for increase port density per floor.

Run this to generate a .CSV report of interface utilizaton for each switch to properly plan and budget the network expansion with the following details:
- Count of UP Access Ports
- Count of UP Module Ports (or, Uplinks)
- Count of Total UP Ports
- Count of Total DOWN  Ports
- Count of Total Ports

# How it works
This code intends to accomplish the following tasks:
- Step 1.  Call the DNA Center API **Authentication API** with your DNA Center IP address, username, and password to generate an auth-x token for subsequent API calls.(*note: DNA parameters must be updated in config.py*)
- Step 2. Call the DNA Center API **Get Device list** to identify all Device UUIDs based on a comma-seperated list of hostnames (*note: device list parameter must be updated in config.py*).
- Step 3. Generate CSV Template
- Step 4a. Call the DNA Center API **Get Device Interface count** to iterate through all Device IDs and identify all *available* interfaces, all *down* interfaces, and all *up* interfaces ( excluding Bluetooth, Management, and App interfaces, etc.)
- Step 4b. Leverage regex to generate specific interface reports for access ports and module ports, depending on the switch series.
- Step 5. Output a PrettyTable report of the analysis on your terminal.
- Step 6. Generate a .CSV file report with with additional switch info, which can be shared with management. 

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
