# Installing and distributing the `zajno-motion` skill

## Install (local — single user)

The skill lives at `~/.claude/skills/zajno-motion/`. If you can read this
file, it's already installed and Claude Code will auto-discover it.

To verify:

```bash
ls ~/.claude/skills/zajno-motion/SKILL.md
```

Then in any Claude Code session, ask:

> "Use the zajno-motion skill to add a hero reveal here"

Claude will read `SKILL.md` and pull the relevant principle/example files.

## Distribute to a teammate

### Option 1 — direct copy (simplest)

```bash
# Copy the whole skill to their machine
scp -r ~/.claude/skills/zajno-motion teammate@host:~/.claude/skills/

# Or zip and share
cd ~/.claude/skills && tar czf zajno-motion.tar.gz zajno-motion/
# they:
mkdir -p ~/.claude/skills && tar xzf zajno-motion.tar.gz -C ~/.claude/skills/
```

### Option 2 — shared dotfiles repo (recommended for teams)

```bash
cd ~/.claude/skills/zajno-motion
git init && git add . && git commit -m "Zajno motion skill v1.0.0"
gh repo create yourorg/claude-skill-zajno-motion --public --source=. --push
```

Teammates install with:

```bash
cd ~/.claude/skills && git clone https://github.com/yourorg/claude-skill-zajno-motion.git zajno-motion
```

### Option 3 — vendor inside a project

Skills can also live inside a project at `.claude/skills/`. Useful when
you want the skill to ship with the codebase:

```bash
cd /path/to/your/project
mkdir -p .claude/skills
cp -R ~/.claude/skills/zajno-motion .claude/skills/
```

Claude Code prefers project-scoped skills over user-scoped ones, so this
also acts as an override if you want a project-specific tweak.

## Versioning

The `plugin.json` manifest tracks semver. Bump the version on every change:

- `MAJOR` — breaking change to the principle set or example APIs
- `MINOR` — new principle, new example, new reference doc
- `PATCH` — copy edits, bug fixes in examples, doc clarifications

Tag releases in git: `git tag v1.0.0 && git push --tags`.

## Updating

If the skill is git-managed:

```bash
cd ~/.claude/skills/zajno-motion && git pull
```

## Uninstalling

```bash
rm -rf ~/.claude/skills/zajno-motion
```

The skill disappears from Claude's available-skills list on next session.

## Verifying it works

In a fresh Claude Code session:

```
"What does the zajno-motion skill cover?"
```

Claude should list the 8 principles. If not, the skill isn't being
discovered — check that `SKILL.md` has valid frontmatter (run
`head -20 ~/.claude/skills/zajno-motion/SKILL.md` and confirm the
`name:` and `description:` keys are present).

## Plugin distribution (advanced)

For wider distribution beyond a single team, the skill can be packaged
as a Claude Code plugin. The `plugin.json` manifest in this skill is
forward-compatible with the plugin format. Future work: publish to a
plugin marketplace once the format stabilizes.
