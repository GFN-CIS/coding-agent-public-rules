# global-rules
These are organization-wide **public** rules intended for both humans and automated agents.

# Agent must check all the files in the repo during review.

- Keep rules language-agnostic and free of project-specific details or IP.
- Documentation and comments must be understandable to both humans and agents (do not maintain separate “human” vs “agent” versions).
- Avoid emojis in logs, comments, and documentation.
- Prefer a layered documentation approach with links to avoid duplication: detailed behavior lives closest to the code, higher-level docs link down.
- Once per session check if this local repository/module is up to date against it's upstream. Use forced pull from git to fetch the most up-to-date version of this rules.
