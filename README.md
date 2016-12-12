# Ansible Role: Login User
=========

### WIP...

Creates an initial user for automation. Can optionally generate and/or deploy ssh keys for the user and add an ssh config entry for the project, including the user information.

NOTE: This is really only useful in an environment where you begin with an authenticated user (such as vagrant), but which do not have the standard user account you prefer to use for software
installation, configuration, and management.
It is useful for establishing a common, consistent environment before proceeding with your other playbooks.
If you're using Vagrant, you can run a setup playbook with the Ansible provisioner as the default (vagrant) user. Otherwise, the expectation is that configuration will be modified for it, it will run in isolation, and then the configs will be reset before proceeding.
In such case, the following must be set in ansible.cfg
(unfortunately they won't be read as playbook vars)
(don't forget to remove them before running other plays):
remote_user = [your pre-authorized user account]
ask_pass = True
ask_sudo_pass = True

Requirements
------------

ssh-keygen installed on the control machine, if ssh keys are to be generated.


Role Variables
--------------

Available variables (with current defaults)...


    project: "anseedble"

Name of containing project - used in (default) name of generated ssh keys.


    environ:  "dev"

Environment, e.g. dev, stage, or prod - used in (default) name of generated ssh keys.


    login_user: "deploy"

User account to be created. Given passwordless sudo and ssh access via ssh key authentication. Used for installing and configuring software on the server. Expected to be distinct from application service account.


    local_pki_directory: "~/.ssh"

Location of ssh keys and config file on the control machine.


    create_login_user_key: true

Whether or not to generate ssh keys for the login user.


    login_user_key: "{{ project }}_{{ environ }}"

Name given to generated ssh keys.


    login_user_passphrase: "change me and put me in a vault file"

Passphrase for generated ssh keys. Will probably be needed for keychain, ssh agent, etc. Obviously in need of securing, probably in a vault-protected file.


    key_type: "rsa"

SSH key type for generated keys, e.g. rsa, dsa, ecdsa, or ed25519. ed25519 (etc) may need adjustment, as unlike other types, it requires matching key size that is usually (always?) omitted from the properties passed to the command.


    key_size: 4096

Key size in bits. e.g. 2048, 4096, or 15360 (15k) (for rsa). Must match type if using ed25519, etc.


    create_ssh_config_entry:  true

Whether or not to create an entry in the ssh config file (in the local pki directory).


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

CC0

Author Information
------------------

Drew Heles
