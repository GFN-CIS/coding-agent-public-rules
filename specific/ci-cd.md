# CI/CD Rules

These rules supplement `code.md` for continuous integration, builds, and deployments.

- **Verify the effective pipeline.** Check which jobs execute for relevant events and refs (branches, merge requests, tags, protected refs). Verify rule ordering, dependencies, and deployment gates. A green pipeline is insufficient when required checks did not run.
- **Reuse shared components.** Prefer established build, test, and deployment components over copied pipeline logic. Centralize shared toolchain versions; introduce consumer-specific overrides only when justified.
- **Avoid redundant builds.** If build inputs do not vary by environment or zone, build once and reuse the artifact across deployment targets. Do not confuse CI orchestration fan-out with build requirements.
- **Protect component contracts.** Identify consumers, including users of moving version references, before changing shared component inputs, outputs, or behavior. Communicate and version breaking changes according to the component's release policy.
- **Execute new gates.** A newly added quality gate must be executed at least once before merge and shown able to fail. Advisory checks are explicitly non-blocking in pipeline configuration, not by accident of tool behaviour, and their output is kept as an artifact.
- **Pin once.** Pin a toolchain version exactly once (lockfile, image digest); everywhere else, including developer-facing constraints, use compatible ranges.
