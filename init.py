#!/usr/bin/python #1
# -*- coding: utf-8 -*- #2

import os #3

def main(): #4

	module = AnsibleModule( #5
		argument_spec = dict( #6
			runlevel=dict(default=None, type='str'), #7
		), #8
) #9

# Ansible helps us run commands #10
rc, out, err = module.run_command('/sbin/runlevel') #11
if rc != 0: #12
	module.fail_json(msg="Could not determine current runlevel.",
		rc=rc, err=err) #13

# Get the runlevel, exit if its not what we expect #14
last_runlevel, cur_runlevel = out.split(' ', 1) #15
cur_runlevel = cur_runlevel.rstrip() #16
if len(cur_runlevel) > 1: #17
	module.fail_json(msg="Got unexpected output from runlevel.",
		rc=rc) #18

# Do we need to change anything #19
if (module.params['runlevel'] is None or
	module.params['runlevel'] == cur_runlevel): #20
		module.exit_json(changed=False, runlevel=cur_runlevel) #21

# Check if we are root #22
uid = os.geteuid() #23
if uid != 0: #24
	module.fail_json(msg="You need to be root to change the
		runlevel") #25

# Attempt to change the runlevel #26
rc, out, err = module.run_command('/sbin/init %s' %
module.params['runlevel']) #27
if rc != 0: #28
	module.fail_json(msg="Could not change runlevel.", rc=rc,
		err=err) #29

# Tell ansible the results #30
	module.exit_json(changed=True, runlevel=cur_runlevel) #31

# include magic from lib/ansible/module_common.py #32
#<<INCLUDE_ANSIBLE_MODULE_COMMON>> #33
main() #34