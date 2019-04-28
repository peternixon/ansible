#!/usr/bin/python

#import os

DOCUMENTATION = '''
---
module: route_dynamic
short_description: Manage dynamic routing tables on linux platform - add or remove
description:
  - Add or remove dynamic routing on linux platform.

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

  linux commands are as follows (reference only)
  
  # route add -host [IP] gw [IP] [DEV]
  # route del -host [IP]
  # route add -net [IP] netmask [IP] gw [IP] [DEV]
  # route del -net [IP] netmask [IP]
  
'''
def route_host(module, params):

    rou_typ = "-" + params['rou_typ']
    host = params['host']
    gw = params['gw']
    netmask = params['netmask']
    dev = params['dev']
    state = params['state']

    if state == "present":
        state = "add"	
    else:
        state = "del"

    route_path = module.get_bin_path('route', required=True)

    args = [route_path, state, rou_typ, host,

            "gw", gw, dev]

    (rc, stdout, stderr) = module.run_command(args)

    if rc == 0:
        has_changed=True
        is_error=False
        return is_error, has_changed, stderr
    else:
        has_changed=False
        is_error=True
    return is_error, has_changed, stderr

def route_net(module, params):

    rou_typ = "-" + params['rou_typ']
    host = params['host']
    gw = params['gw']
    netmask = params['netmask']
    dev = params['dev']
    state = params['state']

    if state == "present":
        state = "add"	
    else:
        state = "del"

    route_path = module.get_bin_path('route', required=True)

    args = [route_path, state, rou_typ, host,

            "netmask", netmask, "gw", gw, dev]

    (rc, stdout, stderr) = module.run_command(args)

    if rc == 0:
        has_changed=True
        is_error=False
        return is_error, has_changed, stderr
    else:
        has_changed=False
        is_error=True
    return is_error, has_changed, stderr
	
def main():

    fields = {
	 
			## add or del
            "state": {
				"default": "present", 
				"choices": [ "present", "absent" ], 
				"type": "str"
			},	
			
			## host or net
			"rou_typ": {
				"default": "host", 
				"choices": [ "host", "net" ], 
				"type": "str"
			}, 
			
			## IP or host
			"host": {
				"required": True, 
				"type": "str"
			}, 				 
			
			## gateway address
            "gw": {
				"required": True, 
				"type": "str"
			},
			
			## netmask
			"netmask": {
				"required": False, 
				"type": "str"
			},

			## network interface
            "dev": {
				"required": True, 
				"type": "str"
			},

    }

    choice_map = {
        "host": route_host,
        "net": route_net
    }

	
	# now call the module required
    module = AnsibleModule(argument_spec=fields)
    params = module.params

    is_error, has_changed, result = choice_map.get(params['rou_typ'])(module, params)
	
    if not is_error:
        if params['state'] == "present":
           txt = "added"
           txt2 = "to"
        else:
           txt = "deleted"
           txt2 = "from"
           msg="Successfully %s %s %s %s routing table" % (txt, params['rou_typ'],  params['host'], txt2)
        module.exit_json(changed=True, msg=msg, meta=result)
    else:
        if params['state'] == "present":
           txt = "add"
           txt2 = "to"
        else:
           txt = "delete"
           txt2 = "from"
        msg="Cannot %s %s %s %s routing table - stderr %s" % (txt, params['rou_typ'],  params['host'], txt2, result)
        module.fail_json(changed=False, msg=msg, meta=result)



from ansible.module_utils.basic import *

main()

