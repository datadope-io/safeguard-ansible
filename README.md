# Ansible Resources for Safeguard Integration

## What is Ansible?

Ansible is an automation platform for handling the deployment and maintenance of devices. For more information, see <https://www.ansible.com>

## What are the Ansible resources for Safeguard integration?

Ansible uses plugins and modules to extend it's functionality. Ansible ships with a set of core plugins and modules in addition to the many plugins that can be downloaded and added to Ansible for use in playbooks and many other scenarios. This repository provides plugins that can be used to integrate Safeguard for Privileged Passwords (SPP) with Ansible. These plugins allow an Ansible playbook or the Ansible Automation Platform environment to pull credentials directly from SPP so that they can be used by Ansible to perform tasks. Two of the plugins that are available in this repository are the SPP lookup plugin and the Ansible Automation Platform credential type plugin. For more information about these plugins, please see the individual plugin folders.

## Contents

### Safeguard Plugins for Ansible

The Safeguard Credentials lookup plugin allows Ansible to fetch a credential from SPP through the Application to Application (A2A) API. For more information, please see <https://github.com/OneIdentity/safeguard-ansible/tree/main/collection/oneidentity/safeguard/plugins>.

### Safeguard Credential Type plugin for Ansible Automation Platform

The Safeguard Credential Type plugin is configured using the Ansible Automation Platform web interface and allows Ansible to define an SPP credential. For more information, please see <https://github.com/OneIdentity/safeguard-ansible/tree/main/credential_type_plugin>.

## Contributing to the Ansible Resources for Safeguard

Is something broken or something that should be added to the Ansible resources for Safeguard integration? [Log an issue](https://github.com/OneIdentity/safeguard-ansible/issues).
