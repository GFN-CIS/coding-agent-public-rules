---
name: gfn-infrastructure
description: Use when writing or reviewing infrastructure declarations in any technology (Terraform, Helm, cloud config). Covers native functions over templating, configuration at its natural ownership scope, and tracing the deployed path for externally reachable changes.
---
# General infrastructure declaration/coding rules 

1. Never use templating to get some info when system provides appropriate functions to get it. Consider using system's functions
2. Place configuration at its natural ownership scope (global, environment, service, or component). Shared environment facts belong at environment scope; service invariants belong in service definitions or shared templates. Avoid repeating the same fact at narrower scopes.
3. For changes to externally reachable behavior, trace the deployed path through routing, runtime configuration, services, and consumers. Verify behavior against the target deployment topology; local checks may miss environment-specific routing and policies.
