# Spawntel Output Skills

How Spawntel's agents shape what they hand over. Each folder in `skills/` is one kind of output (a PDF document, a report, a proposal, a post) written down as a skill, so every agent on every harness produces it the same way.

## Skills

| Skill | What it makes |
|---|---|
| [spawntel-documentation](skills/spawntel-documentation/SKILL.md) | Clean, simple, fully sourced PDF documents: study guides, blueprints, explainers, handbooks |

## How a skill gets added

1. An agent makes the real output once.
2. Jay approves it.
3. The method gets written down as a skill: the steps, the rules, what to never do, plus any template or script it needs. Write down the approach, not a copy of that one output's design.
4. Open a pull request with the new folder under `skills/<name>/` and add a row to the table above.

Each skill folder holds a `SKILL.md` (name and description up top, then the method), plus `assets/` and `scripts/` only when the skill needs them.

## Using a skill

Copy the skill folder into your workspace's `.agents/skills/` folder. Codex, OpenCode and Gemini read it from there. For Claude Code, also link or copy it into `.claude/skills/`. Then ask for the output in plain words ("make me a PDF guide on...") and the agent picks the skill up.

## Fonts

`spawntel-documentation` ships Inter under the SIL Open Font License 1.1 (`assets/Inter-OFL.txt`).
