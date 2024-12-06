# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 09:56:23 2024

@author: hmuaa
"""
# so basically the last one i submitted had telnet in it but i changed it now to paramiko
import paramiko

def ssh_connect_and_configure(host, username, password, new_hostname):
    try:
        print("Connecting to device via SSH...")
        
        
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
       
        ssh_client.connect(host, username=username, password=password)
        print("Connected successfully!")
        
      
        shell = ssh_client.invoke_shell()

      
        shell.send("enable\n")
        shell.send(password + "\n")   
        shell.send("conf t\n")
        shell.send(f"hostname {new_hostname}\n")
        shell.send("end\n")
        
        #this is enabling syslog
        shell.send("logging <syslog-server-ip>\n")

        
       
        shell.send("show running-config\n")
        shell.send("exit\n")   

        
        shell.settimeout(1)
        running_config_output = ""
        while True:
            try:
                running_config_output += shell.recv(1024).decode('ascii')
            except paramiko.ssh_exception.SSHException:
                break  

       
        with open("running_config.txt", "w") as file:
            file.write(running_config_output)
        
        print("Configuration changed successfully and saved to 'running_config.txt'.")

        
        hardening_checks(running_config_output)
    
    except Exception as e:
        print(f"An issue has occurred: {e}")
    finally:
        
        ssh_client.close()

def hardening_checks(config_output):
    print("\nChecking device hardening compliance...")

 
    checks = {
        "no ip http server": "HTTP server should be disabled",
        "service password-encryption": "Service password encryption should be enabled",
        "no cdp run": "Cisco Discovery Protocol (CDP) should be disabled on Internet-facing interfaces",
        "enable secret": "Enable secret password should be set (not just 'enable password')",
        "banner login": "A login banner should be configured"
    }

    compliance_results = {}
    for command, advice in checks.items():
        compliance_results[command] = command in config_output

  
    for command, is_compliant in compliance_results.items():
        if is_compliant:
            print(f"PASS: {command} is set. ({checks[command]})")
        else:
            print(f"FAIL: {command} is NOT set. ({checks[command]})")


host = "192.168.1.1"
username = "Muaad"
password = "bobwashere"
new_hostname = "Myrouter"

if __name__ == "__main__":
    ssh_connect_and_configure(host, username, password, new_hostname)

# Function to send commands to the router
def send_commands(commands, hostname, username, password):
    try:
        # Initialize the SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Connect to the router
        client.connect(hostname=hostname, username=username, password=password)
        
        # Start an interactive shell
        shell = client.invoke_shell()
        
        # Send each command
        for command in commands:
            shell.send(command + '\n')
            # Wait for the command to be processed
            time.sleep(1)
        
        # Close the connection
        client.close()
        print("Commands sent successfully!")
    except Exception as e:
        print(f"Error: {e}")

# Commands to configure loopback and an interface
commands = [
    "enable",  # Enter privileged mode
    "configure terminal",  # Enter global configuration mode
    "interface loopback0",  # Configure loopback0
    "ip address 192.168.1.1 255.255.255.0",  # Assign IP to loopback
    "no shutdown",  # Enable loopback
    "interface gigabitEthernet0/0",  # Configure another interface
    "ip address 192.168.2.1 255.255.255.0",  # Assign IP to the interface
    "no shutdown",  # Enable the interface
    "exit",  # Exit to global config
    "exit"  # Exit config mode
]


hostname = "192.168.1.1"  
username = "Muaad"  
password = "BobWasHere"  

# Run the function
send_commands(commands, hostname, username, password)

# Commands to configure RIP
rip_commands = [
    "enable",
    "configure terminal",
    "router rip",  # Enable RIP
    "version 2",  # Use RIP version 2
    "network 192.168.1.1",  # Advertise the loopback network
    "network 192.168.2.1",  # Advertise the other network
    "exit",  # Exit RIP config
    "exit"  # Exit config mode
]

# Run the function again for RIP configuration
send_commands(rip_commands, hostname, username, password)
