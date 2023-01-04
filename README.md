# safeguard-ansible
Ansible resources for Safeguard integration

Ansible® is an open source, command-line IT automation software application written in Python. It can configure systems, deploy software, and orchestrate advanced workflows to support application deployment, system updates, and more.

Ansible’s main strengths are simplicity and ease of use. It also has a strong focus on security and reliability, featuring minimal moving parts. It uses OpenSSH for transport (with other transports and pull modes as alternatives), and uses a human-readable language that is designed for getting started quickly without a lot of training.

For more information, see <https://www.ansible.com>

## What are the Ansible resources for Safeguard integration?

Ansible uses plugins and modules to extend it's functionality. Ansible ships with a set of core plugins and modules in addition to the many plugins and can be downloaded and added to Ansible for use in playbooks and many other scenarios. This repository provides plugins that can be used to integrate Safeguard for Privileged Passwords with Ansible. These plugins allow an Ansible playbook or the AWX environment to pull credentials directly from SPP so that they can be used by Ansible to perform tasks. Two of the plugins that are available in this repository are the SPP lookup plugin and the AWX credential type plugin. For more information about these plugins, please see the individual plugin folders.

## Install

The source code for the Ansible plugins are available in this repository. In addition, each of these plugins can be installed from the PyPi python module repository.

# Contributing to the Ansible Resources for Safeguard

Is something broken or something that should be added to the Ansible resources? [Log an issue](https://github.com/OneIdentity/safeguard-ansible/issues).
