<meta name="author" content="Marco Noce">
<meta name="description" content="Gathers facts about configured local zone on a SunOS/Oracle Solaris global zone by zoneadm">
<meta name="copyright" content="Marco Noce 2024">
<meta name="keywords" content="ansible, module, fact, solaris, zoneadm, zone">

<div align="center">

![Ansible Custom Module][ansible-shield]
![Oracle Solaris][solaris-shield]
![python][python-shield]
![license][license-shield]

</div>


### zoneadm_facts ansible custom module
#### Gathers facts about configured local zone on a SunOS/Oracle Solaris global zone by zoneadm

#### Description :

<b>zoneadm_facts</b> is a custom module for ansible that creates an ansible_facts containing the list and details of configured local zones on a SunOS/Oracle Solaris global zone

#### Repo files:

```
├── /library                
│   └── zoneadm_facts.py  ##<-- python custom module
└── zoneadm_list.yml      ##<-- ansible playbook example
```

#### Requirements :

*  This module supports SunOS/Oracle Solaris only
*  The Local Zone info are gathered from the [zoneadm] command

#### Parameters :

*  no parameters are needed

#### Attributes :

|Attribute |Support|Description                                                                         |
|----------|-------|------------------------------------------------------------------------------------|
|check_mode|full   |Can run in check_mode and return changed status prediction without modifying target.|
|facts     |full   |Action returns an ansible_facts dictionary that will update existing host facts.    |

#### Examples :

#### Tasks
```yaml
---
  # Gather local zone info
  - name: Gather facts configured local zone
    zoneadm_facts:

  # print all lz name at running STATE
  - name: Print all LZ at running STATE
    debug:
      msg: "{{ ansible_facts.zone_list  | selectattr('STATUS','equalto', 'running' ) | map(attribute='NAME') }}"

  # print lz STATUS by ID
  - name: Print STATUS of LZ ID 3
    debug:
      msg: "LZ ID 3 STATUS : {{ ansible_facts.zone_list  | selectattr('ID','equalto', '3' ) | map(attribute='STATUS') | first }}"

```
#### zone_list facts:
```json
"ansible_facts": {
  "zone_list": [
    {
      "STATUS": "running",
      "NAME": "sol10lab",
      "IP": "shared",
      "BRAND": "solaris10",
      "PATH": "/zones/sol10lab",
      "ID": "3"
    }
  ]
},
```
#### debug output from example :
```
TASK [Print STATUS of LZ ID 3] *************************************************
ok: [global_zone_host] => {
    "msg": "LZ ID 3 STATUS : running"
}
```
```
TASK [Print all LZ at running STATE] *******************************************
ok: [global_zone_host] => {
    "msg": [
        "sol9lab",
        "sol10lab"
    ]
}
```
#### Returned Facts :

*  Facts returned by this module are added/updated in the hostvars host facts and can be referenced by name just like any other host fact. They do not need to be registered in order to use them.

|Key       |Type                  |Description                                                                       |Returned|Sample            |
|----------|----------------------|----------------------------------------------------------------------------------|------- |------------------|
|zone_list |list / elements=string|Configured local Zone list                                                        |        |                  |
|ID        |string                |The local zone ID.                                                                |always  |"10"              |
|NAME      |string                |The local zone name, could match the hostname of the local zone                   |always  |"sol11lab"        |
|STATUS    |string                |The local zone status. running, installed, configured.                            |always  |"running"         |
|PATH      |string                |The local zone path.                                                              |always  |"/zones/sol11lab" |
|BRAND     |string                |The local zone brand. native, solaris10 and more.                                 |always  |"native"          |
|IP        |string                |The local zone IP or shared.                                                      |always  |"shared"          |

## Integration

1. Assuming you are in the root folder of your ansible project.

Specify a module path in your ansible configuration file.

```shell
$ vim ansible.cfg
```
```ini
[defaults]
...
library = ./library
...
```

Create the directory and copy the python modules into that directory

```shell
$ mkdir library
$ cp path/to/module library
```

2. If you use Ansible AWX and have no way to edit the control node, you can add the /library directory to the same directory as the playbook .yml file

```
├── root repository
│   ├── playbooks
│   │    ├── /library                
│   │    │   └── zoneadm_facts.py  ##<-- python custom module
│   │    └── your_playbook.yml      ##<-- you playbook
```   

[ansible-shield]: https://img.shields.io/badge/Ansible-custom%20module-blue?style=for-the-badge&logo=ansible&logoColor=lightgrey
[solaris-shield]: https://img.shields.io/badge/oracle-solaris-red?style=for-the-badge&logo=oracle&logoColor=red
[python-shield]: https://img.shields.io/badge/python-blue?style=for-the-badge&logo=python&logoColor=yellow
[license-shield]: https://img.shields.io/github/license/nomakcooper/zoneadm_facts?style=for-the-badge&label=LICENSE

[zoneadm]: https://docs.oracle.com/en/operating-systems/solaris/oracle-solaris/11.4/use-zones/using-zoneadm-command.html
