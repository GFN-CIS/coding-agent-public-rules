/**
 * Tests for the OpenCode 2 plugin: src/skills.js (loader) and index.js (entry).
 *
 * Covers: parity of the registered skill entry with OpenCode 2.1's directory
 * loader (id, name, autoinvoke coercion, content), fail-fast on broken files,
 * the shipped rule set loading in full, and dedup against skills that are
 * already registered (git clone mode). Not covered: OpenCode itself loading
 * the plugin; that was checked by a live smoke test against OpenCode 2.1.3.
 *
 * Run: npm test
 */

import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { test } from "node:test";
import { fileURLToPath } from "node:url";

import plugin from "../index.js";
import { loadSkills, parseSkill, toBool } from "./skills.js";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

/**
 * Frontmatter flags are coerced the way OpenCode coerces them.
 *
 * Validates: src/skills.js::toBool
 * Assertion: "Off"/0/false read as false, "yes"/1/true as true, anything else as unset,
 * so a skill is hidden from auto-selection in plugin mode exactly when it is in clone mode.
 */
test("toBool coerces flags like OpenCode", () => {
  assert.equal(toBool(false), false);
  assert.equal(toBool("Off"), false);
  assert.equal(toBool(" yes "), true);
  assert.equal(toBool(1), true);
  assert.equal(toBool(0), false);
  assert.equal(toBool(2), undefined);
  assert.equal(toBool("maybe"), undefined);
  assert.equal(toBool(null), undefined);
});

/**
 * A SKILL.md becomes the entry OpenCode builds for a discovered skill.
 *
 * Validates: src/skills.js::parseSkill
 * Assertion: id from the folder, name and description from frontmatter, CRLF handled,
 * content is the body without frontmatter.
 */
test("parseSkill builds the entry OpenCode builds", () => {
  const s = parseSkill("gfn-x", "/r/gfn-x/SKILL.md", '---\r\nname: gfn-x\r\ndescription: "d: e"\r\n---\r\n# Body\n');
  assert.deepEqual(s, { id: "gfn-x", name: "gfn-x", description: "d: e", path: "/r/gfn-x/SKILL.md", content: "# Body\n" });
});

/**
 * autoinvoke precedence matches OpenCode.
 *
 * Validates: src/skills.js::parseSkill
 * Assertion: metadata["opencode/autoinvoke"] wins; otherwise a truthy
 * disable-model-invocation gives false; with neither, autoinvoke stays unset.
 */
test("parseSkill takes autoinvoke from metadata, then disable-model-invocation", () => {
  assert.equal(parseSkill("a", "/a", "---\nmetadata:\n  opencode/autoinvoke: false\n---\nb").autoinvoke, false);
  assert.equal(parseSkill("a", "/a", "---\ndisable-model-invocation: true\n---\nb").autoinvoke, false);
  assert.equal(
    parseSkill("a", "/a", "---\ndisable-model-invocation: true\nmetadata:\n  opencode/autoinvoke: true\n---\nb").autoinvoke,
    true,
  );
  assert.equal("autoinvoke" in parseSkill("a", "/a", "---\nname: a\n---\nb"), false);
});

/**
 * A skill without a frontmatter name is named after its folder.
 *
 * Validates: src/skills.js::parseSkill
 */
test("parseSkill falls back to the folder name", () => {
  assert.equal(parseSkill("dir", "/d", "---\ndescription: x\n---\nb").name, "dir");
});

/**
 * A broken SKILL.md fails loudly instead of vanishing.
 *
 * Validates: src/skills.js::parseSkill
 * Assertion: missing, invalid or non-mapping frontmatter throws an error naming the file,
 * so a corrupted package cannot silently drop a rule set.
 */
test("parseSkill throws on broken frontmatter", () => {
  assert.throws(() => parseSkill("d", "/x/SKILL.md", "no frontmatter"), /\/x\/SKILL\.md/);
  assert.throws(() => parseSkill("d", "/x/SKILL.md", "---\n: [\n---\nb"), /\/x\/SKILL\.md/);
  assert.throws(() => parseSkill("d", "/x/SKILL.md", "---\n- a\n---\nb"), /\/x\/SKILL\.md/);
});

/**
 * Only gfn-* folders are scanned, and a gfn-* folder without SKILL.md fails.
 *
 * Validates: src/skills.js::loadSkills
 * Method: build a throwaway package root in a private temp dir.
 */
test("loadSkills scans only gfn-* folders and fails on a missing SKILL.md", () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "gfn-skills-"));
  try {
    for (const name of ["gfn-a", "other"]) fs.mkdirSync(path.join(dir, name));
    fs.writeFileSync(path.join(dir, "gfn-a", "SKILL.md"), "---\nname: gfn-a\n---\nbody");
    fs.writeFileSync(path.join(dir, "other", "SKILL.md"), "---\nname: other\n---\nbody");
    assert.deepEqual(loadSkills(dir).map((s) => s.id), ["gfn-a"]);
    fs.mkdirSync(path.join(dir, "gfn-empty"));
    assert.throws(() => loadSkills(dir), { code: "ENOENT" });
  } finally {
    fs.rmSync(dir, { recursive: true, force: true });
  }
});

/**
 * The shipped rule set loads in full.
 *
 * Validates: src/skills.js::loadSkills on this repository
 * Assertion: every gfn-* folder yields a skill whose name equals its id, and
 * gfn-code-health-check stays out of automatic selection in plugin mode.
 */
test("every shipped skill loads and health-check is not auto-invoked", () => {
  const skills = loadSkills(ROOT);
  const dirs = fs.readdirSync(ROOT).filter((n) => n.startsWith("gfn-")).sort();
  assert.deepEqual(skills.map((s) => s.id), dirs);
  for (const s of skills) assert.equal(s.name, s.id);
  assert.equal(skills.find((s) => s.id === "gfn-code-health-check").autoinvoke, false);
});

/**
 * The plugin registers all skills and never overrides one that is already registered.
 *
 * Validates: index.js setup via ctx.skill.transform
 * Assertion: with a clone-mode gfn-code already present, it is kept untouched and
 * the rest are added, so enabling both install modes yields no duplicates.
 * Method: a fake editor backed by a Map, the shape of OpenCode's SkillEditor.
 */
test("plugin adds skills and keeps ones already registered", async () => {
  const existing = { id: "gfn-code", name: "gfn-code", path: "/clone/gfn-code/SKILL.md", content: "x" };
  const store = new Map([[existing.id, existing]]);
  const editor = { get: (id) => store.get(id), add: (s) => store.set(s.id, s) };
  await plugin.setup({ skill: { transform: async (fn) => fn(editor) } });
  assert.equal(store.get("gfn-code"), existing);
  assert.equal(store.size, loadSkills(ROOT).length);
});
