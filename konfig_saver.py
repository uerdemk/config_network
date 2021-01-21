from netmiko import ConnectHandler
from tkinter import *
import json
import datetime

username = ""
password = ""
secret = ""

ssh_fail = 0
stop = 0

with open('konfig_saver.json') as Konfig:
    Konfig_json = json.load(Konfig)

def eq_declare(eq_IP, eq_OS):
    csc = {
        "device_type": eq_OS,
        "host": eq_IP,
        "port": 22,
        "username": username,
        "password": password,
        "secret": secret
    }
    return csc

eq_list = [""] * len(Konfig_json["device_to_config"])

print("---------------------------------------------------------------------------------------------------------------")
print("---------------------------------------------------------------------------------------------------------------")

try:
    for t in range(len(Konfig_json["device_to_config"])):
        try:
            eq_list[t] = eq_declare(Konfig_json["device_to_config"][t]["ip"], Konfig_json["device_to_config"][t]["os"])
            net_connect = ConnectHandler(**eq_list[t])
            net_connect.enable()
            print("PASS!,", "Connection OK,", Konfig_json["device_to_config"][t]["ip"], ":", Konfig_json["device_to_config"][t]["device"])
            print("      Starting...")
            try:
                for command in range(len(Konfig_json["device_to_config"][t]["command"])):
                    output = net_connect.send_command(Konfig_json["device_to_config"][t]["command"][command])
                    with open(str(Konfig_json["device_to_config"][t]["device"] + "__" + str(Konfig_json["device_to_config"][t]["command"][command])), "+w") as file_name:
                        file_name.write(output)
                        print("      ended...")
            except EXCEPTION as e:
                print("      Can't write show running config to a file")
        except:
            print("FAIL!,", "SSH Connection Error,", Konfig_json["device_to_config"][t]["ip"], ":", Konfig_json["device_to_config"][t]["device"])
except EXCEPTION as e:
    print(e)

a = 1
while(a):
        print("   ")
        fake = input("Press ENTER to close...")
        a = 0
