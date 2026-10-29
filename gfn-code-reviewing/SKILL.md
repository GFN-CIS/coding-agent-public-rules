---
name: gfn-code-reviewing
description: Use when performing any code review. Findings must cite evidence, brand-new entities are checked for reuse, re-reviews verify fixes against current code, and scope is every line the change adds or modifies.
---
_These rules are for Code-Reviewing process._

## Required standards

Review the change against skill `gfn-code` and every technology skill that applies to it.


1. When changes introcuding brand-new entities such as a function, procedures, classes, helpers, etc. - check for reusage opportunities. Is the same or similar functionality already present and it can be reused or generalized/adopted and then reused. 
2. When doing the full-repository review, check for the opportunities for reusing as stated in previous pt and make a code more consise.
3. Every finding cites evidence: a location in the change and the rule or source it violates.
4. On re-review, verify each item reported as fixed against the current code; do not accept closure claims.
5. Scope is every line the change adds or modifies, regardless of which file it lives in or where the file came from.
6. Check that design rationale (specs, ADRs, comments) still matches the implementation it justifies.
7. Evaluate the overall solution against requirements, established architecture, applicable ADRs, and simpler approaches. Ground findings in concrete impact and distinguish defects from optional improvements.
