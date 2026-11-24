#!/usr/bin/env node
/**
 * CI check: the npm tarball carries exactly the tracked rule files.
 *
 * Every git-tracked file in a gfn-<name> folder must be in `npm pack` output (otherwise
 * plugin mode would lack files that clone mode has), and nothing from scripts/
 * or tests may leak in. Reads `npm pack --dry-run --json`; exits 1 on mismatch.
 */
import { execFileSync } from "node:child_process";

const packed = new Set(JSON.parse(execFileSync("npm", ["pack", "--dry-run", "--json"], { encoding: "utf8" }))[0].files.map((f) => f.path));
const tracked = execFileSync("git", ["ls-files", "gfn-*"], { encoding: "utf8" }).split("\n").filter(Boolean);
const missing = tracked.filter((f) => !packed.has(f));
const stray = [...packed].filter((f) => f.startsWith("scripts/") || f.endsWith(".test.js"));
for (const f of missing) console.error(`ERROR: tracked but not packed: ${f}`);
for (const f of stray) console.error(`ERROR: packed but must not be: ${f}`);
if (missing.length || stray.length) process.exit(1);
console.log(`OK: ${tracked.length} rule files packed`);
