# -*- coding: utf-8 -*-
import subprocess
import os
import random

scriptPath = os.path.abspath(__file__)
scriptDir = os.path.split(scriptPath)[0]

output = subprocess.check_output(
         [r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe',
                             '-ExecutionPolicy',
                             'Unrestricted',
                             scriptDir + '\\PowerShellScripts\\GetAllRules.ps1'],
         shell=True)

rules = output.decode()
separatedRules = rules.split('\r'+'\n'+'\r')
separatedRules.remove('')
numberOfRules = int(input('Please enter the number of rules to display: '))
if numberOfRules <= 0:
    print('Sorry, the entered number should be more than 0')
    quit()
elif numberOfRules > len(separatedRules):
    print('Sorry, the entered number exceeds the total number of rules')
    quit()
print('')
selectedRules = []
while numberOfRules > 0:
    r = random.randint(0, len(separatedRules))
    selectedRules.append(separatedRules[r])
    numberOfRules -= 1


enabled = 0
disabled = 0
inbound = 0
outbound = 0
print('Firewall rules:')
for rule in selectedRules:
    parameter = rule.split('\r'+'\n')
    name = parameter[0][25:]
    print(name)

    enabledCount = []
    for p in parameter:
        if 'Enabled' in p:
            enabledCount.append(p)
    for element in enabledCount:
        if 'True' in element:
            enabled += 1
        if 'False' in element:
            disabled += 1

    boundCount = []
    for p in parameter:
        if 'Direction' in p:
            boundCount.append(p)
    for element in boundCount:
        if 'Inbound' in element:
            inbound += 1
        if 'Outbound' in element:
            outbound += 1

print('')
print('Inbound:', inbound)
print('Outbound', outbound)
print('')
print('Enabled:', enabled)
print('Disabled:', disabled)
