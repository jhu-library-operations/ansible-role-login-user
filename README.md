# Ansible Role: Login User
=========

So far, only tested for https://github.com/jhu-library-applications/catalyst-ansible when using vagrant.

What it does if {{ using_vagrant }} == true:
1. Creates {{ login_group }}.
2. Creates {{ login_user }}.
3. Installs ~/.ssh/id_rsa.pub for {{ login_user }}.
4. Configures passwordless sudo for {{ login_user }}.

Requirements
------------
1. Assumes that ~/.ssh/id_rsa.pub exists.
2. It is necessary to first edit catalyst-ansible/setup.yml similar to this:
```---
- name: create login user for installation & configuration
  hosts: all

  vars:
    remote_user: jgara1
    login_user: jgara1
    login_group: msel-operations
    using_vagrant: true

  roles:
  - { role: login-user, tags: ['login-user'] }

```


Role Variables
--------------

1. ```using_vagrant: true```

      Signal that we are deploying to vagrant.
      
3. ```login_user: "<jhedid>"```

      User account to be created. Given passwordless sudo and ssh access via ssh key authentication. Used for installing and configuring software on the server. Expected to be distinct from application service account (e.g. tomcat, apache, catalyst, etc.).

1. ```local_ssh_directory: "~/.ssh"```

      Location of ssh config file on the control machine.

1. ```login_user_passwordless_sudo: true```

      Flag for granting login user passwordless sudo.

1. ```login_user_sudoers: ""```

      Entry in sudoers file for login user. Defaults to `ALL=(ALL) PASSWD: ALL`.

1. Optional Vars:

```
       login_user_uid:           1001
       login_group_gid:          1001
```

      Optional UID and GID for login user and group

1. ```# login_group:              "{{ login_user }}"```

      Optional group for login user. Will be created if provided & does not already exist.


Dependencies
------------

none


Example Playbook
----------------

    - hosts: servers
      roles:
         - { role: login-user }


If needed, a master ansible ini file can be created by creating a playbook like:

    - name: create master ansible ini file
      hosts: oriole
      connection: local

      tasks:
      - name: create master ansible ini file
        include_role:
          name: login-user
          tasks_from: create_ini
        vars:
          remote_user: "[your JHED]"
          login_user: "[your JHED]"
          login_group: "developers"
          password: "[your password for dev VMs]"

...and then running it like:

    ansible-playbook create_ini.yml -v

... or if you prefer supplying your vars on the command-line, omit them from the playbook and run:

    ansible-playbook create_ini.yml -v -e "remote_user=user login_user=user login_group=group password=password"

Vars can then be read from the created file like so:

    login_password:         "{{ lookup('ini', 'login_password section=dev file=~/.ansible.ini') }}"


Additionally, the encryption of a given password can be accomplished by creating a playbook like so:

    - name: encrypt provided password
      hosts: default
      connection: local

      tasks:
      - name: encrypt provided password
        include_role:
          name: login-user
          tasks_from: encrypt_password

...and then running it like:

    ansible-playbook encrypt_password.yml -v -e "password=password"


License
-------

CC0

Author Information
------------------


