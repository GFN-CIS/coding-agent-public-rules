# Ansible Rules

- Always prefer using Ansible modules and roles instead of shell scripting.
- Avoid creating shell scripts from templates. Prefer standard shell + input data approach.
- Avoid using global become for hosts. Use become only where needed on per-task or per-block level.


  
