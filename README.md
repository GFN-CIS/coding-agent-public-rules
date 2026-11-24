# Agentic coding bible

Organization-wide **public** coding rules for both humans and automated agents, kept
language-agnostic and free of project-specific details or IP.

Each rule set is an OpenCode/agent skill at `gfn-<name>/SKILL.md`. An agent loads
skills selectively by their `description` — only the ones relevant to the current
change — instead of reading the whole repository.

Skill IDs are globally unique, always carry the `gfn-` prefix, and the `name` in the
frontmatter must equal the directory name. CI (`scripts/check-skills.py`) enforces this.

## Skills

| Skill | Applies to |
|---|---|
| `gfn-code` | Any code change, any language (application or infrastructure) |
| `gfn-testing` | Writing or reviewing tests; any change needing test coverage |
| `gfn-code-reviewing` | Any code review |
| `gfn-code-health-check` | On-request quantitative code-health analysis (not auto-listed) |
| `gfn-python` | Python code (`.py`, `pyproject.toml`, Python tests) |
| `gfn-terraform` | Terraform / OpenTofu / terragrunt (`.tf`) |
| `gfn-ansible` | Ansible playbooks and roles |
| `gfn-ci-cd` | CI/CD pipelines, builds, deployments |
| `gfn-docker` | Dockerfiles and long-lived containers |
| `gfn-infrastructure` | Infrastructure declarations in any technology |
| `gfn-kubernetes` | Kubernetes manifests and Helm charts |

## Using the skills

The same skills ship two ways; pick one per machine.

### OpenCode 2, auto-updating (npm plugin)

Add the package to `plugins` in the global `opencode.json`:

```json
{ "plugins": ["@gfn-cis/coding-agent-public-rules@latest"] }
```

OpenCode re-resolves `@latest` on its own schedule (observed: days, not every start), and the
background service loads plugins once, so a new release lands only after both. To take it now:
`opencode plugin update`, then restart the service. Pin a version (`@0.1.0`) to freeze the rules.

### Git clone

Clone the repo and add the clone path to `skills` in `opencode.json`, e.g.
`"skills": ["/path/to/coding-agent-public-rules"]`. Update with `git pull`.

If both are configured, the clone wins: the plugin skips skill ids that are already registered.

### Other harnesses

Copy or symlink the `gfn-*` directories into the harness's own skills directory.

`gfn-code-health-check` is hidden from automatic selection by `metadata: opencode/autoinvoke: false` in OpenCode 2 (both modes); harnesses that ignore that key still see its description "use only when explicitly asked".

## Releasing

Users of the npm plugin get only tagged releases. Bump `version` in `package.json`,
merge, then push a matching tag (`git tag v0.2.0 && git push origin v0.2.0`).
`.github/workflows/release.yml` checks tag == version, runs the tests, attaches the
attested tarball to a GitHub Release and publishes it to npm via trusted publishing (OIDC).
