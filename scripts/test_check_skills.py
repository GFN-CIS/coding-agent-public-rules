"""Self-test for check-skills.py using throwaway directory trees."""
import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path

# load by path: the hyphen in check-skills.py makes it unimportable by name
_spec = importlib.util.spec_from_file_location(
    "check_skills", Path(__file__).resolve().parent / "check-skills.py")
check_skills = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(check_skills)


def write(root, rel, text):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def make_passing_tree(root):
    write(root, "gfn-code/SKILL.md",
          "---\nname: gfn-code\ndescription: Use when changing code\n---\nbody\n")
    write(root, "README.md", "# rules\n")


class CheckSkillsTest(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.root)

    def check(self):
        return check_skills.collect_errors(self.root)

    def test_passing_tree(self):
        make_passing_tree(self.root)
        self.assertEqual(self.check(), [])

    def test_missing_frontmatter(self):
        write(self.root, "gfn-code/SKILL.md", "body only\n")
        self.assertTrue(any("frontmatter" in e for e in self.check()))

    def test_missing_name(self):
        write(self.root, "gfn-code/SKILL.md",
              "---\ndescription: Use when changing code\n---\n")
        self.assertTrue(any("no 'name'" in e for e in self.check()))

    def test_empty_description(self):
        write(self.root, "gfn-code/SKILL.md",
              "---\nname: gfn-code\ndescription:\n---\n")
        self.assertTrue(any("no non-empty 'description'" in e for e in self.check()))

    def test_name_differs_from_directory(self):
        write(self.root, "gfn-code/SKILL.md",
              "---\nname: gfn-other\ndescription: Use when x\n---\n")
        self.assertTrue(any("does not match directory" in e for e in self.check()))

    def test_bad_name_pattern(self):
        write(self.root, "gfn-code/SKILL.md",
              "---\nname: Code\ndescription: Use when x\n---\n")
        self.assertTrue(any("does not match pattern" in e for e in self.check()))

    def test_duplicate_names(self):
        write(self.root, "gfn-a/SKILL.md",
              "---\nname: gfn-a\ndescription: Use when x\n---\n")
        write(self.root, "gfn-b/SKILL.md",
              "---\nname: gfn-a\ndescription: Use when y\n---\n")
        self.assertTrue(any("duplicate skill name 'gfn-a'" in e for e in self.check()))

    def test_nested_skill(self):
        write(self.root, "gfn-code/SKILL.md",
              "---\nname: gfn-code\ndescription: Use when x\n---\n")
        write(self.root, "gfn-code/nested/SKILL.md",
              "---\nname: gfn-nested\ndescription: Use when x\n---\n")
        self.assertTrue(any("must live directly under" in e for e in self.check()))

    def test_stray_root_rule(self):
        make_passing_tree(self.root)
        write(self.root, "python.md", "# old-style rule\n")
        self.assertTrue(any("python.md" in e for e in self.check()))

    def test_skill_dir_without_skill_md(self):
        make_passing_tree(self.root)
        write(self.root, "gfn-foo/skill.md", "misspelled\n")
        self.assertTrue(any("gfn-foo/" in e for e in self.check()))

    def test_readme_with_description(self):
        make_passing_tree(self.root)
        write(self.root, "README.md",
              "---\nname: readme\ndescription: Use when x\n---\n")
        self.assertTrue(any("README.md" in e for e in self.check()))

    def test_block_scalar_description(self):
        write(self.root, "gfn-code/SKILL.md",
              "---\nname: gfn-code\ndescription: >\n  Use when changing\n  code\n---\nbody\n")
        self.assertEqual(self.check(), [])
        meta, err = check_skills.parse_frontmatter(
            (self.root / "gfn-code" / "SKILL.md").read_text(encoding="utf-8"))
        self.assertIsNone(err)
        self.assertEqual(meta["description"].strip(), "Use when changing code")

    def test_empty_body(self):
        write(self.root, "gfn-code/SKILL.md",
              "---\nname: gfn-code\ndescription: Use when changing code\n---\n")
        self.assertTrue(any("body is empty" in e for e in self.check()))

    def test_description_too_long(self):
        write(self.root, "gfn-code/SKILL.md",
              f"---\nname: gfn-code\ndescription: {'x' * 1025}\n---\nbody\n")
        self.assertTrue(any("description exceeds 1024" in e for e in self.check()))

    def test_unknown_referenced_id(self):
        make_passing_tree(self.root)
        write(self.root, "gfn-code/SKILL.md",
              "---\nname: gfn-code\ndescription: Use when changing code\n---\nsee `gfn-nope`\n")
        errors = self.check()
        self.assertTrue(any("gfn-nope" in e for e in errors))
        self.assertTrue(any("gfn-code/SKILL.md" in e for e in errors))

    def test_agents_md_allowed(self):
        make_passing_tree(self.root)
        write(self.root, "AGENTS.md", "# agent instructions\n")
        self.assertEqual(self.check(), [])

    def test_metadata_not_mapping(self):
        write(self.root, "gfn-code/SKILL.md",
              "---\nname: gfn-code\ndescription: Use when changing code\nmetadata: nope\n---\nbody\n")
        self.assertTrue(any("metadata must be a mapping" in e for e in self.check()))


if __name__ == "__main__":
    unittest.main()
