
# Task: Quantitative Code-Health Analysis of `<TARGET>`

You are performing a **read-only quantitative analysis** of `<TARGET>` using the **RP/OP** pressure model defined below, plus standard supporting metrics. Use real tools — do NOT eyeball the code. All assumptions must be stated explicitly.

---

## Step 0 — Locate & profile the target

1. Find `<TARGET>` (index/grep/glob — whichever is best).
2. **Detect primary language(s)**: count files by extension (use `scc`/`tokei`/`cloc`/ad-hoc count). If multi-language, either pick the dominant language and state it, or analyze each separately.
3. **Confirm scope**: list analyzed files, total LOC, and exclusions (tests, generated code, vendored deps, fixtures, mirror worktrees, sample/dev configs). Be explicit.
4. If `<TARGET>` doesn't exist or has no tractable codebase → **stop and report**.

---

## Step 1 — Methodology (fixed formulas)

### A. Refactoring Pressure (RP)

```
RP = 0.6 × Peak + 0.4 × Base

combined = max_complexity × 0.6 + p90_complexity × 0.4
Peak     = 100 × (1 − exp(−0.08 × combined)) × scale
density  = (total_complexity / loc) × 100
Base     = 100 × (1 − exp(−0.02 × density × scale))
```

- CC over all functions/methods. `loc` = code lines (no blanks, no comments). Default `scale = min(1, loc/5000)` — state your choice.

### B. Overengineering Pressure (OP)

Build an **intra-project dependency graph** (modules and/or classes).

```
class_score = (0.35·fan_out_norm + 0.25·fan_in_norm + 0.25·depth_norm + 0.15·centrality_norm) × 100
OP          = (0.4·coupling_norm + 0.6·avg_class_score_norm) × 100
```

- `depth` — inheritance (preferred) or import-chain (state which). External base = +1.
- `centrality` — betweenness on the dep graph.
- `coupling` — edge density of dep graph OR average fan_out (state which).
- Normalize each to [0, 1] (min-max or a sensible cap — document).

### C. Combined Score with imbalance penalty

```
Score = (RP + OP) + k × |RP − OP|     # default k = 0.5
```

Report RP, OP, Score, and the penalty term separately.

### Verdict semantics

- `RP ≫ OP` → vermicelli / dense branchy logic.
- `OP ≫ RP` → abstraction labyrinth.
- both low → healthy. Both high → diffusely degraded (not "balanced").

---

## Step 2 — Tooling discovery (do NOT use a hardcoded list)

You need tools for: **(a) cyclomatic complexity per function**, **(b) LOC excluding blanks/comments**, **(c) type-check / lint signal**, **(d) dependency-graph extraction**, **(e) maintainability index or equivalent**, **(f) graph metrics (centrality, cycles)**, **(g) tabular aggregation**.

You must **discover the current best-fit tools at the moment this prompt is run**. Do NOT rely on your training-time knowledge of tool names — that snapshot may be stale or wrong. Procedure:

1. **Check what's already installed.** Try the obvious candidates you remember; if a tool is on `PATH` and produces sensible output on a single file, you can use it.
2. **For each missing slot, research current options.** Acceptable research paths, in order of preference:
   - Look at the project's own configs (`pyproject.toml`, `package.json`, `go.mod`, `Cargo.toml`, `.golangci.yml`, `.eslintrc`, `pre-commit-config.yaml`, CI files) — whatever the team already uses is usually a fine choice and won't conflict with their assumptions.
   - Web search (if web access is available) with a query like `"<language> cyclomatic complexity cli 2026"` or `"<language> dependency graph static analysis"`. Restrict to results from the last ~24 months.
   - Awesome-lists for the language (`awesome-<lang>`, `awesome-static-analysis`) — they're usually maintained.
   - Package registry top-results: `pypi.org`, `npmjs.com`, `crates.io`, `pkg.go.dev`, etc. — sort by recent activity / downloads.
3. **Verify each candidate before adopting it**:
   - Last release within ~18 months (or actively maintained — recent commits).
   - Supports the target language version.
   - Produces machine-readable output (JSON, SARIF, CSV, or stable text) — if it only prints a human-readable summary, it's much harder to aggregate.
   - Installable without root / system pollution (language package manager, single binary, container).
   - License is acceptable for the project.
4. **Pick one tool per metric slot.** Briefly note **why** (e.g. "team already uses it", "only one that emits JSON", "covers all source files including .pyi"). If two tools disagree on a number, prefer the one closest to the team's existing toolchain and report the delta.
5. **Install into an isolated environment** under `docs/artifacts/.toolchain/<lang>/` (venv, local npm prefix, GOBIN, cargo install --root, etc.). Never `sudo`. Never modify global state.

**Fallback path — if the language has no good tooling at all** (or you can't get anything to run in this environment):

- Use **`tree-sitter`** (or `ast-grep`) as a universal AST extractor and write a small script to compute CC, fan-in/fan-out yourself.
- Use the language's own AST library if there's a host runtime available (e.g. `ast` in Python, `@typescript-eslint/parser` in JS).
- If even that fails, **stop and report** — do not invent numbers from a regex grep.

### What to put in the report about tooling

A required `Tools used` table:

| Metric | Tool | Version | Why this one | Output format |
|--------|------|---------|--------------|---------------|

Anything you discovered but rejected (and why) goes in `Limitations & assumptions`.

---

## Step 3 — Supporting analysis

- Per-file: LOC, total CC, max CC, density, MI (or equivalent). Top-10 worst by each.
- Top-10 functions/methods by CC with `file:line`.
- Top-10 classes/modules by `class_score`.
- Type-check/lint signal: error & warning totals, top-10 files by count, error-rule histogram (summarize categories, don't dump every line).
- Cycle detection in dep graph.

Aggregate via DataFrame/table. Save raw per-entity data as CSV under `docs/artifacts/<target>_metrics_<timestamp>.csv`.

---

## Step 4 — Diagnosis

1. Dominant pressure: RP-heavy / OP-heavy / healthy / diffusely degraded.
2. 3–5 concrete hot spots, each with a one-line metric-based reason.
3. Pressure cluster: name the sub-package/dir dragging the score if any.
4. **Fix 3 things** — ranked by leverage, each with an expected delta in RP/OP/Score.

Be honest: if the project is clean, say so. If a metric is non-informative for this codebase (no inheritance, no internal coupling), say so. If a measurement artifact dominates the numbers, explain it.

---

## Definition of done

1. Scope confirmed: files, LOC, exclusions.
2. **`Tools used` table** is present and every number in the report is traceable to a tool in it.
3. RP, OP, Score computed; scale / normalization / `k` documented.
4. Top-N tables present for: files, functions, classes, MI, type-check.
5. Dep graph stats: nodes, edges, density, cycles.
6. Raw CSVs saved under `docs/artifacts/`.
7. Diagnosis names dominant pressure, hot spots with metric reasons, fix-3 with expected deltas.
8. Limitations & assumptions explicit (including which candidate tools you considered and rejected).

If you hit a hard blocker (no tooling installable, language unsupported, target empty) → stop and report. Don't fabricate.

---

## Return format

Single Markdown report:

1. **Scope** — root, files, LOC, language mix, exclusions.
2. **Tools used** — the table from §2.
3. **Methodology** — formulas, scale/normalization, `k`.
4. **Headline numbers** — RP, OP, Score, penalty, verdict.
5. **Top-N tables**.
6. **Dep graph stats**.
7. **Diagnosis** — hot spots with metric reasons.
8. **Fix 3 things** — with expected Score delta.
9. **Limitations & assumptions** — including rejected tool candidates.
10. **Artifacts** — paths to CSVs, scripts, isolated toolchain envs under `docs/artifacts/`.

Dense, quantitative. Numbers before narrative.

---

### Placeholders

- `<TARGET>` — directory/component/repo path.
- Optionally pass `LANGUAGE=<lang>` to skip auto-detection.
