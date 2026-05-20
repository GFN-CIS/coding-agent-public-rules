# Global Coding Rules (Language-Agnostic)

This document defines organization-wide, **language-agnostic** engineering rules.
It intentionally avoids project-, framework-, vendor-, and repository-specific guidance.

## Non-negotiables

- **Language**: production code comments, docstrings, commit messages, and public-facing developer docs must be written in **English**.
- **No secrets / no sensitive data**: never hardcode credentials, tokens, private keys, internal URLs, customer data, or any confidential identifiers.
- **No environment-specific hardcoding**: domains, tenant/customer names, branding assets, and deployment-specific behavior must be driven by **configuration**, not `if/else` forks.
- **Consistency over preference**: follow the established style within a file/module/package unless there is a deliberate refactor.

## Code quality

- **Correctness first**: make behavior explicit; avoid “magic” defaults that change silently across environments.
- **Separation of concerns**: keep business logic independent from presentation, transport, and persistence layers.
- **Single responsibility**: functions/classes/modules should have one clear purpose.
- **DRY, but not dogmatic**: deduplicate only when it reduces total complexity and maintenance cost.
- **Keep it readable**: prefer clear names and small units of code over clever tricks.

## Over engineering
- Avoid excessive configurability. Always consider during the plan phase does something should be configurable or it could be constant? If unsure - ask user directly with list of all configuration entities you doubt about.

## Naming consistency
- Some languages platforms or frameworks can denote best practices for naming styles and structures. In this case the model should consider it as well and choose best fit approach.
- entities names styling should be consistent within parent entity->module->project for same entity classes. e.g. if parent entity uses snake_case for variables - model should use it, if parent uses CamelCase for variables - model should use it and so forth.  
- entities naming structure should  be consistent within project for the same class and function of entities. For example, if some flag variables within module has structure flag_entity_flagname model should consider use it instead of, say entity_flag_flagname, or only flagname. 

## Error handling (fail fast)

- Do not swallow errors to “keep things running” if correctness is impacted.
- Avoid excessive fallbacks. Default to **fail fast** when correctness or data integrity is at risk.
- If a fallback is proposed, agree on the fallback plan with the user upfront (scope, triggering conditions, logging/metrics, and how/when to remove it).
- Catch **specific** error types; avoid blanket catches unless you are:
  - implementing a well-defined fallback,
  - limiting the try/catch scope,
  - logging context,
  - and returning to a safe, predictable state.
- Prefer returning structured errors or raising exceptions over returning ambiguous values.

## Logging & observability

- Use the project’s logging system (not ad-hoc printing).
- Logs must be actionable: include identifiers and context, but **never** include secrets.
- Avoid emojis in logs.
- Choose appropriate log levels and avoid high-volume noise on hot paths.
- When logging errors, include enough information to debug (and include stack traces where appropriate).

## Security basics

- Treat all external input as untrusted: validate, sanitize, and encode appropriately.
- Prefer safe-by-default APIs; only bypass escaping/safety checks with a clear justification.
- Apply least privilege: scope permissions, credentials, and access as narrowly as possible.
- Avoid dynamic code execution (e.g., eval/templated SQL) unless there is no safer alternative and it is reviewed.

## Backward compatibility

 - Do not maintain backward compatibility unless explicitly instructed.
 - If you see potential backward compatibility issues - ask user explicitly wether to maintain backward compatibility.

## Configuration & portability

- Configuration should be explicit, versioned (when appropriate), and documented.
- Keep environment differences in config, not in code forks.
- Do not duplicate configuration across multiple places without a single source of truth.

## Documentation

- Document **why** something is done, not only **what** is done.
- Documentation and comments must be understandable to both humans and automated agents.
  - Do not duplicate the same content as separate “for humans” and “for agents” versions.
- Avoid emojis in documentation and comments.
- Avoid documentation duplication by using a layered approach and links:
  - **Function/method docstrings**: detailed behavior/contract, inputs/outputs, edge cases.
  - **Class/module docs**: the big picture, invariants, and links to the relevant functions/methods for details.
  - **Module/package README**: the most general overview (architecture/usage), linking to module/class docs.
- Any deviation from the project’s current ideology/architecture or from common best practices must be documented: what we changed and why.
- Functions/methods/classes must include docstrings (or the language’s equivalent structured API documentation comments) in the same style/format adopted by the repository (be consistent within the project).
- Keep docs close to the code they describe (README in the relevant directory/module): function/methods/classes/modules - in appropriate docstrings. Packages - in readme.md within package folder.
- Update documentation when changing behavior, public APIs, or operational requirements.

## Development practices

- Before writing new code, first analyze the project for existing functionality that can be reused (internal utilities, shared modules, existing services, established patterns).
- For platform/framework/language-specific rules, in addition to this file, also check relevant files in the `specific` folder.
- Avoid ad-hoc solutions. New changes must fit the project’s architecture and established patterns.
- Avoid “hotfixes” when a proper solution is feasible. If a hotfix is unavoidable, align it with the user and document the trade-offs and follow-up plan.
- Follow the code-organization principles used in the project (e.g., OOP-style codebases should remain OOP; modular codebases should remain modular; functional codebases should remain functional). If the requested functionality does not fit existing approaches, agree on the approach with the user before introducing a new paradigm.
- Avoid unnecessary abstractions and overengineering.
  - A strong signal an extracted helper is unnecessary is when it is called from only one place, and:
    - the caller is under ~300 lines,
    - inlining the logic would not reduce readability,
    - inlining would not push the caller over ~300 lines,
    - and there is no serious reason to keep it separate (e.g., a stable public API, reuse expected soon, complex test isolation, performance constraints, security boundaries).
- Regularly sanity-check that we are not reinventing the wheel: prefer mature, actively maintained libraries/tools (as of 2026) over bespoke implementations.
- When introducing or using external dependencies, keep them up to date (as of 2026) unless the project documentation explicitly pins or forbids specific versions.
- When considering a library/framework/plugin/etc., always verify that it is updated frequently enough and that the chosen version is current for the year 2026.
- Always check for leftover/dead code introduced by refactors (unused functions, unreachable branches, stale TODOs, commented-out blocks). Ask the user for permission before removing it, and remove it only with explicit user approval.

## Testing (general expectations)

- Add/adjust tests when changing behavior.
- Prefer fast, deterministic tests; isolate external dependencies.
- Fix the root cause rather than encoding known bugs into tests.

## Size & maintainability (guidelines)

- If a function/method becomes hard to scan, split it.
- If a file/module becomes a “dumping ground”, reorganize around responsibilities.
- Prefer cohesive modules over large, interdependent ones.

## Private information

 - The exploration/intermediary artifacts like subagent code analysis results must never be committed.
 - All PII and infrastructure identification items must be replaced with example-style entities. e.g. domains - with example.com, usernames - with relevant example users, IP address with respective TEST-NET-1,2,3 IPs. Emails - with example emails and so forth.
 - When appropriate - the placeholders and monikers could be used.
 - The same applies to documentation and plans that goes to commit.
