---
name: gfn-ansible
description: Use when writing or reviewing Ansible playbooks and roles, e.g. `playbook.yml`, `roles/`, or `ansible.cfg`. Prefers modules over shell scripting, per-task become, and input validation/asserts before any system change.
---
## Required standards

Apply together with skills `gfn-code` and `gfn-infrastructure`.

# Ansible Rules

- Always prefer using Ansible modules and roles instead of shell scripting.
- Avoid creating shell scripts from templates. Prefer standard shell + input data approach.
- Avoid using global become for hosts. Use become only where needed on per-task or per-block level.
- Input validations/system/environment assession and asserts within playbook/role should be made, if possible, before any changes introduced by role are made to the system.



  
