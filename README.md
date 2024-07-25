<div align="center">

![Ansible Custom Module][ansible-shield]
![Oracle Solaris][solaris-shield]
![python][python-shield]

</div>


### zoneadm_facts ansible custom module
#### Gathers facts about configured local zone on a SunOS/Oracle Solaris global zone by zoneadm

#### Description :

<b>zoneadm_facts</b> is a custom module for ansible that creates an ansible_facts containing the list and details of configured local zones on a SunOS/Oracle Solaris global zone

#### Repo files:

```
├── /library                
│   ├── zoneadm_facts.py  ##<-- python custom module
└── zoneadm_list.yml      ##<-- ansible playbook example
```

#### Requirements :

*  This module currently supports SunOS/Oracle Solaris only
*  The Local Zone info are gathered from the [zoneadm] command

#### Parameters :

*  no parameters are needed

#### Attributes :

|Attribute |Support|Description                                                                         |
|----------|-------|------------------------------------------------------------------------------------|
|check_mode|full   |Can run in check_mode and return changed status prediction without modifying target.|
|facts     |full   |Action returns an ansible_facts dictionary that will update existing host facts.    |

#### Examples :

```yaml

```

[ansible-shield]: https://img.shields.io/badge/Ansible-custom%20module-blue?style=for-the-badge&logo=ansible&logoColor=lightgrey
[solaris-shield]: https://img.shields.io/badge/oracle-solaris-red?style=for-the-badge&logo=oracle&logoColor=red
[python-shield]: https://img.shields.io/badge/python-blue?style=for-the-badge&logo=python&logoColor=yellow

[zoneadm]: https://docs.oracle.com/en/operating-systems/solaris/oracle-solaris/11.4/use-zones/using-zoneadm-command.html
