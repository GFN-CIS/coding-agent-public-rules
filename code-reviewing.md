_These rules are for Code-Reviewing process. However, when doing code-review, you must read all appropriate files from this repository, not only this one._

1. When changes introcuding brand-new entities such as a function, procedures, classes, helpers, etc. - check for reusage opportunities. Is the same or similar functionality already present and it can be reused or generalized/adopted and then reused. 
2. When doing the full-repository review, check for the opportunities for reusing as stated in previous pt and make a code more consise.
3. Every finding cites evidence: a location in the change and the rule or source it violates.
4. On re-review, verify each item reported as fixed against the current code; do not accept closure claims.
5. Scope is every line the change adds or modifies, regardless of which file it lives in or where the file came from.
6. Check that design rationale (specs, ADRs, comments) still matches the implementation it justifies.
