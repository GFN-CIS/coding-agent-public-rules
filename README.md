# Agentic coding bible
These are organization-wide **public** rules intended for both humans and automated agents.

# Agent must check all the files in the repo during review.

# Specific rules
- During review, evaluate the overall solution against requirements, established architecture, applicable ADRs, and simpler approaches. Ground findings in concrete impact and distinguish defects from optional improvements.
- For CI/CD changes, apply [`specific/ci-cd.md`](specific/ci-cd.md) alongside the general rules.
- Keep rules language-agnostic and free of project-specific details or IP.
- Documentation and comments must be understandable to both humans and agents (do not maintain separate “human” vs “agent” versions).
- Avoid emojis in logs, comments, and documentation.
- Prefer a layered documentation approach with links to avoid duplication: detailed behavior lives closest to the code, higher-level docs link down.
- Once per session check if this local repository/module is up to date against it's upstream. Use forced pull from git to fetch the most up-to-date version of this rules.
