/**
 * OpenCode 2 plugin entry: registers the gfn-* skills shipped in this package.
 * See src/skills.js for the loader and README.md for the two install modes.
 */

import path from "node:path";
import { fileURLToPath } from "node:url";

import { loadSkills } from "./src/skills.js";

const ROOT = path.dirname(fileURLToPath(import.meta.url));

export default {
  id: "gfn-coding-rules",
  async setup(ctx) {
    const skills = loadSkills(ROOT);
    await ctx.skill.transform((editor) => {
      for (const skill of skills) {
        // A skill already known (e.g. from a git clone listed in "skills") wins,
        // so enabling both install modes never yields duplicates.
        if (!editor.get(skill.id)) editor.add(skill);
      }
    });
  },
};
