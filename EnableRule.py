import os
import subprocess
import random


scriptPath = os.path.abspath(__file__)
scriptDir = os.path.split(scriptPath)[0]

# Firstly, we'll get all firewall rules

output = subprocess.check_output(
         [r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe',
                             '-ExecutionPolicy',
                             'Unrestricted',
                             scriptDir+'\\PowerShellScripts\\GetAllRules.ps1'],
         shell=True)

rules = output.decode()
separatedRules = rules.split('\r'+'\n'+'\r')
separatedRules.remove('')

# Then we'll get random rule which is disabled

ruleName = ''
isEnabled = True
while isEnabled is True:
    r = random.randint(0, len(separatedRules))
    randomRule = separatedRules[r]
    parameters = randomRule.split('\r'+'\n')
    name = parameters[0][25:]
    for parameter in parameters:
        if 'Enabled               :' in parameter:
            enabledParameter = parameter
            if 'False' in enabledParameter:
                isEnabled = False
                ruleName = name
                break

# now let's compose the script for getting this rule by its name

relativePath = "PowerShellScripts/GetRuleByName.ps1"
absoluteFilePath = os.path.join(scriptDir, relativePath)
getRuleByNameFile = open(absoluteFilePath, 'w')
getRuleByNameFile.write('Get-NetFirewallRule -Name '+'"'+ruleName+'"')
getRuleByNameFile.close()

print('Firewall rule which was disabled:')

# and execute the script to show that this rule is disabled

output = subprocess.Popen(
         [r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe',
                             '-ExecutionPolicy',
                             'Unrestricted',
                             scriptDir+'\\PowerShellScripts\\GetRuleByName.ps1'],
         shell=True)
output.wait()

# let's compose the script to enable this rule

relativePath = "PowerShellScripts/EnableRuleByName.ps1"
absoluteFilePath = os.path.join(scriptDir, relativePath)
enableRuleByNameFile = open(absoluteFilePath, 'w')
enableRuleByNameFile.write('Enable-NetFirewallRule -Name '+'"'+ruleName+'"')
enableRuleByNameFile.close()

# and execute the script to enable the rule

output = subprocess.Popen(
         [r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe',
                             '-ExecutionPolicy',
                             'Unrestricted',
                             scriptDir+'\\PowerShellScripts\\EnableRuleByName.ps1'],
         shell=True)
output.wait()

# then let's display the rule to make sure that it is enabled
print('Now the rule is enabled: ')
output = subprocess.Popen(
         [r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe',
                             '-ExecutionPolicy',
                             'Unrestricted',
                             scriptDir+'\\PowerShellScripts\\GetRuleByName.ps1'],
         shell=True)
output.wait()

# now compose the script to disable rule

relativePath = "PowerShellScripts/DisableRuleByName.ps1"
absoluteFilePath = os.path.join(scriptDir, relativePath)
disableByNameFile = open(absoluteFilePath, 'w')
disableByNameFile.write('Disable-NetFirewallRule -Name '+'"'+ruleName+'"')
disableByNameFile.close()

# and execute the script

output = subprocess.Popen(
         [r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe',
                             '-ExecutionPolicy',
                             'Unrestricted',
                             scriptDir+'\\PowerShellScripts\\DisableRuleByName.ps1'],
         shell=True)
output.wait()

# now let's display the rule to make sure that it is disabled as it was before
print('Now the rule is back disabled:')
output = subprocess.Popen(
         [r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe',
                             '-ExecutionPolicy',
                             'Unrestricted',
                             scriptDir+'\\PowerShellScripts\\GetRuleByName.ps1'],
         shell=True)
output.wait()

# Let's clean up all PowerShell scripts since they are composed dynamically

relativePath = "PowerShellScripts/GetRuleByName.ps1"
absoluteFilePath = os.path.join(scriptDir, relativePath)
getRuleByNameFile = open(absoluteFilePath, 'w').close()

relativePath = "PowerShellScripts/DisableRuleByName.ps1"
absoluteFilePath = os.path.join(scriptDir, relativePath)
disableRuleByNameFile = open(absoluteFilePath, 'w').close()

relativePath = "PowerShellScripts/EnableRuleByName.ps1"
absoluteFilePath = os.path.join(scriptDir, relativePath)
enableRuleByNameFile = open(absoluteFilePath, 'w').close()
