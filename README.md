# Ansible Role: Login User
=========

Creates an initial user for automation. Can optionally generate and/or deploy ssh keys for the user and add an ssh config entry for the project, including the user information.

Updated to support use of a single master user (and its ssh key) across ansible projects,
or to create a user (and its ssh key) per project & environment

NOTE: The latter approach is really only useful in an environment where you begin with an authenticated user (such as vagrant), but which do not have the standard user account you prefer to use for software
installation, configuration, and management.
It is useful for establishing a common, consistent environment before proceeding with your other playbooks.
If you're using Vagrant, you can run a setup playbook with the Ansible provisioner as the default (vagrant) user. Otherwise, the expectation is that configuration will be modified for it, it will run in isolation, and then the configs will be reset before proceeding.

Requirements
------------

ssh-keygen installed on the control machine, if ssh keys are to be generated.


Role Variables
--------------

1. ```project: "anseedble"```

Name of containing project - used in (default) name of generated ssh keys.


1. ```environ:  "dev"```

Environment, e.g. dev, stage, or prod - used in (default) name of generated ssh keys.


1. ```debugging: true```

Flag to control debugging output


1. ```use_master_user: false```

Flag to indicate use of a master or per-project user


1. ```deprivilege_deploy_user: false```

Flag to indicate whether to remove deploy user's sudo and login privileges.
Should only be true if `use_master_user: true` and no one else still needs to use the deploy user


1. ```login_user: "deploy"```

User account to be created. Given passwordless sudo and ssh access via ssh key authentication. Used for installing and configuring software on the server. Expected to be distinct from application service account.


1. ```local_pki_directory: "~/.ssh"```

Location of ssh config file on the control machine.


1. ```project_pki_subdirectory: "{{ local_pki_directory }}/{{ project }}"```

Location of ssh keys and vault password file on the control machine.


1. ```create_login_user_key: true```

Whether or not to generate ssh keys for the login user.


1. ```login_user_key: "{{ project }}_{{ environ }}"```

Name given to generated ssh keys. Override if `use_master_user: true`


1. ```login_user_passphrase: ""```

Passphrase for generated ssh keys. Will probably be needed for keychain, ssh agent, etc. Written to a new environment-specific vault file for per-project users, or a valuted README file for master users (on first use only).


1. ```identity_file: "{{ project_pki_subdirectory }}/{{ login_user_key }}"```

Location of the login user's ssh key. Override if `use_master_user: true`


1. ```login_user_relative_path_to_root: ""```

How to get from *the playbook that calls this role* to the project root


1. ```login_user_path_to_vars:  "{{ login_user_relative_path_to_root }}inventory/group_vars/{{ environ }}"
      login_user_vars_file:     "{{ login_user_path_to_vars }}/vars.yml"
      login_user_vault_file:    "{{ login_user_path_to_vars }}/vault.yml"```

Helper vars for pathing. Overridable if your project structure differs from the one described in [anseedble](https://github.com/dheles/anseedble).


1. ```key_type: "rsa"```

SSH key type for generated keys, e.g. rsa, dsa, ecdsa, or ed25519. ed25519 (etc) may need adjustment, as unlike other types, it requires matching key size that is usually (always?) omitted from the properties passed to the command.


1. ```key_size: 4096```

Key size in bits. e.g. 2048, 4096, or 15360 (15k) (for rsa). Must match type if using ed25519, etc.


1. ```create_ssh_config_entry:  true```

Whether or not to create an entry in the ssh config file (in the local pki directory).


1. ```login_user_grant_sudo: true```

Flag for granting login user sudo


1. ```login_user_passwwordless_sudo: false```

Flag for granting login user passwordless sudo (`login_user_grant_sudo` must be true)


1. ```login_user_sudoers: ""```

Entry in sudoers file for login user. Defaults to `ALL=(ALL) PASSWD: ALL`.


1. ```ssh_aliases: []```

Additional aliases for ssh config.
`Hostvars[item]['inventory_hostname']` and `project-environ` are included by default


1. Optional Vars:

    ```# login_user_uid:           1001
       # login_group_gid:          1001```

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

Drew Heles
