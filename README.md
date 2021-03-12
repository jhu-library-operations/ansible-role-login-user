# Ansible Role: Login User
=========

So far, only tested for https://github.com/jhu-library-applications/catalyst-ansible when using vagrant.

What it does if {{ using_vagrant }} == true:
1. Adds group {{ login_group }}.
2. Adds user {{ login_user }}.
3. Installs {{ sshkey_dir }}/{{ sshkey_name }} for {{ login_user }}.
4. Configures passwordless sudo for {{ login_user }}.

What it does if {{ using_vagrant }} == false:
1. Absolutely nothing.

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


License
-------


Author Information
------------------

J. Gara
