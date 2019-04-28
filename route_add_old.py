#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

import os

DOCUMENTATION = '''
---
module: route_add_del
short_description: Manage dynamic routing tables on linux platform
description:
  - Check and add or remove dynamic routing on linux platform.

author: Nick Holmes April 2018
'''

EXAMPLES = '''
- name: Add dynamic route - host
  route_add_del:
    type=host
	ip=10.34.209.54
	netmask=
	gateway=10.34.209.1
	device=eth2
	state=present
  register: result

- name: Delete dynamic route - host
  route_add_del:
    type=host
    ip=10.34.209.54
	netmask=
    state=absent
  register: result

- name: Add dynamic route - network
  route_add_del:
    type=net
	ip=10.34.209.54
	netmask=255.255.255.0
	gateway=10.34.209.1
	device=eth2
	state=present
  register: result

- name: Delete dynamic route -network
  route_add_del:
    type=net
    ip=10.34.209.54
	netmask=255.255.255.0
    state=absent
  register: result

'''

# route add -host [IP] gw [IP] [DEV]
# route del -host [IP]
# route add -net [IP] netmask [IP] gw [IP] [DEV]
# route del -net [IP] netmask [IP]


# handy helper for calling system calls.
# calls AnsibleModule.run_command and prints a more appropriate message
# exec_path - path to file to execute, with all its arguments.
#   E.g "/sbin/ip -o link show"
# failure_msg - what message to print on failure
def run_cmd(module, exec_path, failure_msg):
  (rc, out, err) = module.run_command(exec_path)
  if rc == 1:
    module.fail_json(msg=failure_msg)
  return out


def single_route_check_run(module):
  output = run_cmd(module,
      '/sbin/ip route show %s' % (module.prefix),
      '/sbin/ip failed to execute. Check if prog exists')
  # if route is found, output will not be blank
  if len(output.splitlines()) > 0:
    return True
  return False


def check_if_route_exists(module):
  timeout = 0
  # Start loop
  while True:
    # if route is found, return True
    if single_route_check_run(module):
      return True
    # if timeout occurs return False
    elif timeout == module.timeout:
      return False
    # otherwise sleep for poll interval and repeat the test
    else:
      timeout += 1
      time.sleep(module.poll_interval)


def main():
    
	fields = {
        "type": {"required": True, "type": "str"},
        "ip": {"required": True, "type": "str"},
        "netmask": {"required": False, "type": "str"},
        "gateway": {"default": False, "type": "str"},
        "device": {"default": True, "type": "str"},
        "state": {
            "default": "present",
            "choices": ['present', 'absent'],
            "type": 'str'
        },
		#"prefix": {"required": True, "type": "str"},
		"timeout": {"default": 5, "type": "int"},
    }
	
	module = AnsibleModule(argument_spec=fields)
    is_error, has_changed, result = choice_map.get(
        module.params['state'])(module.params)
		
	#module = AnsibleModule(
    #    argument_spec=dict(
    #        prefix=dict(required=True, type='str'),
    #        timeout=dict(default=5, type='int'),
    #    ),
    #)

    # define some hardcoded variables
    # polling interval in sec between each ip route show execution
    module.poll_interval = 1

    # function runs a check.
    # If after timeout it will return false
    return_val = check_if_route_exists(module)
    if return_val is True:
        module.exit_json(changed=False, msg="Route Found")
    else:
        module.fail_json(msg="Route not Found. Check Routing Configuration")

# import module snippets
from ansible.module_utils.basic import *
import time

# notice lots of modules don't have this __name__.
# Wonder if its not required?
if __name__ == '__main__':
    main()