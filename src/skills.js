/**
 * Skill loader for the OpenCode 2 plugin entry (index.js).
 *
 * OpenCode 2 has no config hook, so a plugin cannot add a skills directory;
 * it reads each <root>/gfn-<name>/SKILL.md itself and registers the result through
 * ctx.skill.transform. The entry mirrors what OpenCode 2.1 builds for a skill
 * found in a configured directory, so both install modes (git clone + "skills",
 * npm plugin) yield identical skills:
 *   - id: the skill folder name; name: frontmatter name, else the folder name
 *   - description: frontmatter description, when present
 *   - autoinvoke: metadata["opencode/autoinvoke"], else false when
 *     "disable-model-invocation" is truthy, else unset
 *   - path: absolute SKILL.md path; content: the body after the frontmatter
 */

import fs from "node:fs";
import path from "node:path";

import { parse } from "yaml";

// "---" on the first line, then everything up to the next "---" line; LF or CRLF.
const FRONTMATTER_RE = /^---[ \t]*\r?\n(?:([\s\S]*?)\r?\n)?---[ \t]*(?:\r?\n|$)/;
const SKILL_DIR_RE = /^gfn-/;

/**
 * Lenient boolean, the same coercion OpenCode applies to frontmatter flags.
 * @param {unknown} value
 * @returns {boolean | undefined}
 */
export function toBool(value) {
  if (typeof value === "boolean") return value;
  if (typeof value === "number") return value === 1 ? true : value === 0 ? false : undefined;
  if (typeof value !== "string") return undefined;
  const v = value.trim().toLowerCase();
  if (["true", "yes", "on", "1"].includes(v)) return true;
  if (["false", "no", "off", "0"].includes(v)) return false;
  return undefined;
}

/**
 * Build a skill entry from SKILL.md text. Pure function, no I/O.
 * Throws when the file has no valid YAML mapping frontmatter. OpenCode's own
 * directory loader skips such files; we fail fast instead, because every
 * published SKILL.md passed scripts/check-skills.py, so a broken one means a
 * corrupted package and must not silently drop a rule set.
 *
 * @param {string} dirName  skill folder name
 * @param {string} file     absolute SKILL.md path
 * @param {string} text     SKILL.md contents
 */
export function parseSkill(dirName, file, text) {
  const src = String(text).replace(/^\uFEFF/, "");
  const m = FRONTMATTER_RE.exec(src);
  if (!m) throw new Error(`${file}: missing frontmatter`);
  let fields;
  try {
    fields = parse(m[1] ?? "") ?? {};
  } catch (cause) {
    throw new Error(`${file}: frontmatter is not valid YAML`, { cause });
  }
  if (typeof fields !== "object" || Array.isArray(fields)) {
    throw new Error(`${file}: frontmatter is not a mapping`);
  }
  const meta = fields.metadata;
  const explicit =
    meta && typeof meta === "object" && !Array.isArray(meta) ? toBool(meta["opencode/autoinvoke"]) : undefined;
  const autoinvoke = explicit ?? (toBool(fields["disable-model-invocation"]) ? false : undefined);
  return {
    id: dirName,
    name: typeof fields.name === "string" && fields.name ? fields.name : dirName,
    ...(typeof fields.description === "string" ? { description: fields.description } : {}),
    ...(autoinvoke === undefined ? {} : { autoinvoke }),
    path: file,
    content: src.slice(m[0].length),
  };
}

/**
 * Read every <root>/gfn-<name>/SKILL.md. Only gfn-* folders are scanned so that
 * nothing outside the rule set (node_modules, scripts) is ever picked up.
 * A gfn-* folder without a readable SKILL.md throws (see parseSkill for why).
 * @param {string} root  package root
 */
export function loadSkills(root) {
  const skills = [];
  for (const entry of fs.readdirSync(root, { withFileTypes: true })) {
    if (!entry.isDirectory() || !SKILL_DIR_RE.test(entry.name)) continue;
    const file = path.join(root, entry.name, "SKILL.md");
    skills.push(parseSkill(entry.name, file, fs.readFileSync(file, "utf8")));
  }
  return skills.sort((a, b) => a.id.localeCompare(b.id));
}
