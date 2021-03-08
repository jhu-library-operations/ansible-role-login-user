# Ansible Role: Login User
=========

So far, only tested for https://github.com/jhu-library-applications/catalyst-ansible when using vagrant.

What it does if {{ using_vagrant }} == true:
1. Creates {{ login_group }}.
2. Creates {{ login_user }}.
3. Installs {{ sshkey_dir }}/{{ sshkey_name }} or {{ login_user }}.
4. Configures passwordless sudo for {{ login_user }}.

Requirements
------------
1. Assumes that SSH key pair exists. E.g. ~/.ssh/id_rsa and id_rsa.pub
2. ~/.ansible.ini file similar to this:
```
[cross-project]
remote_user = jgara1
login_user  = jgara1
login_group = msel-operations

[dev]
remote_user = jgara1
login_user  = jgara1
login_group = msel-operations
```
3. catalyst-ansible/setup.yml file like this:
```---
- name: create login user for installation & configuration
  hosts: all

  vars:
    sshkey_dir: "~/.ssh"
    sshkey_name: "id_rsa.pub"
    using_vagrant: true

  roles:
  - { role: login-user, tags: ['login-user'] }

```


Role Variables
--------------

1. ```using_vagrant: true```

      Signal that we are deploying to vagrant.
      
2. ```login_user: "<jhedid>" & login_group: "<jhed-group>"```

      User account to be created. Pulled from ~/.ansible.ini. Used for installing and configuring software on the server. Expected to be distinct from application service account (e.g. tomcat, apache, catalyst, etc.).
      Example ~/.ansible.ini file:
```
[cross-project]
remote_user = jgara1
login_user  = jgara1
login_group = msel-operations

[dev]
remote_user = jgara1
login_user  = jgara1
login_group = msel-operations
```

3. ```sshkey_dir: "~/.ssh"```

      Location of ssh keys.

4. ```sshkey_name: "id_rsa.pub"```


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


