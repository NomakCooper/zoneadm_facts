#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2024, Marco Noce <nce.marco@gmail.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: zoneadm_facts
author:
    - Marco Noce (@NomakCooper)
description:
    - Gathers facts about configured local zone on a SunOS/Oracle Solaris global zone by zoneadm.
    - This module currently supports SunOS Family, Oracle Solaris 10/11.
requirements:
  - zoneadm
short_description: Gathers facts about configured local zone
notes:
  - |
    This module shows the list of zones in the running, installed and configured state.
'''

EXAMPLES = r'''
- name: Gather facts configured local zone
  zoneadm_facts:

- name: Print STATUS of LZ ID 3
  debug:
    msg: "LZ ID 3 STATUS : {{ ansible_facts.zone_list  | selectattr('ID','equalto', '3' ) | map(attribute='STATUS') | first }}"

- name: Print all LZ at running STATE
  debug:
    msg: "{{ ansible_facts.zone_list  | selectattr('STATUS','equalto', 'running' ) | map(attribute='NAME') }}"
'''

RETURN = r'''
ansible_facts:
  description: Dictionary containing details of Solaris local zone
  returned: always
  type: complex
  contains:
    zone_list:
      description: A list of configured local zone.
      returned: if local zones are found by zoneadm
      type: list
      contains:
        ID:
          description: The local zone ID.
          returned: always
          type: str
          sample: "10"
        NAME:
          description: The local zone name, could match the hostname of the local zone
          returned: always
          type: str
          sample: "sol11lab"
        STATUS:
          description: The local zone status. running, installed, configured.
          returned: always
          type: str
          sample: "running"
        PATH:
          description: The local zone path.
          returned: always
          type: str
          sample: "/zones/sol11lab"
        BRAND:
          description: The local zone brand. native, solaris 10 and more.
          returned: always
          type: str
          sample: "native"
        IP:
          description: The local zone IP or shared.
          returned: always
          type: str
          sample: "shared"
'''

import platform
from ansible.module_utils.common.text.converters import to_native
from ansible.module_utils.basic import AnsibleModule


def zone_parse(raw):

    results = list()

    lines = raw.splitlines()

    # skip headers ( skip header and global zone row )
    # ID NAME             STATUS     PATH                           BRAND    IP
    #  0 global           running    /                              native   shared

    lines = lines[2:]

    for line in lines:
        cells = line.split(None, 6)
        try:
            if len(cells) == 6:
                ID, NAME, STATUS, PATH, BRAND, IP = cells
        except ValueError:
            # unexpected stdout from zoneadm
            raise EnvironmentError(
                'Expected `zoneadm` table layout " ID,NAME,STATUS,PATH,BRAND,IP" \
                but got something else: {0}'.format(line)
            )

        result = {
            'ID': ID,
            'NAME': NAME,
            'STATUS': STATUS,
            'PATH': PATH,
            'BRAND': BRAND,
            'IP': IP,
        }
        results.append(result)
    return results


def main():
    command_args = ['list', '-i', '-c', '-v']
    commands_map = {
        'zoneadm': {
            'args': [],
            'parse_func': zone_parse
        },
    }
    module = AnsibleModule(
        argument_spec=dict(
            # no arguments necessary
        ),
        supports_check_mode=True,
    )

    commands_map['zoneadm']['args'] = command_args

    if platform.system() != 'SunOS':
        module.fail_json(msg='This module requires SunOS.')

    result = {
        'changed': False,
        'ansible_facts': {
            'zone_list': [],
        },
    }

    try:
        command = None
        bin_path = None
        for c in sorted(commands_map):
            bin_path = module.get_bin_path(c, required=False)
            if bin_path is not None:
                command = c
                break

        if bin_path is None:
            raise EnvironmentError(msg='Unable to find any of the supported commands in PATH: {0}'.format(", ".join(sorted(commands_map))))

        args = commands_map[command]['args']
        rc, stdout, stderr = module.run_command([bin_path] + args)
        if rc == 0:
            parse_func = commands_map[command]['parse_func']
            results = parse_func(stdout)

            for lz in results:
                result['ansible_facts']['zone_list'].append(lz)
    except (KeyError, EnvironmentError) as e:
        module.fail_json(msg=to_native(e))

    module.exit_json(**result)


if __name__ == '__main__':
    main()
