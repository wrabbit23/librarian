# Skill format and packaging reference

## Purpose

Use this reference when creating, validating, or packaging a skill. It distills the stable structural conventions used by OpenAI's Skills documentation and its published skill-creator, while keeping the result portable across Agent Skills implementations.

## Contents

- Canonical layout
- `SKILL.md` and discovery metadata
- Resource directories
- Progressive disclosure
- Files to avoid
- ZIP packaging
- Primary sources

## Canonical layout

```text
skill-name/
├── SKILL.md                 # required
├── agents/                  # optional platform metadata
│   └── openai.yaml
├── references/              # optional, read as needed
├── scripts/                 # optional, executable helpers
└── assets/                  # optional, output resources/templates
```

Do not create empty directories just to match the diagram. Include only what the skill uses.

## SKILL.md

`SKILL.md` is required at the skill root.

Start it with YAML frontmatter containing at least:

```yaml
---
name: example-skill
description: Explain what the skill does and the situations in which it should be used.
---
```

For maximum portability, keep the discovery-critical metadata to `name` and `description`. Preserve supported platform-specific fields when editing an existing skill, but do not invent them.

### Name

Use lowercase ASCII letters, digits, and hyphens. Prefer a short, descriptive name and keep it at 64 characters or fewer. Name the skill directory exactly the same as the frontmatter `name`.

### Description

The description is discovery metadata. State both:

1. what capability the skill provides; and
2. the concrete requests or contexts that should activate it.

Avoid generic descriptions such as "helps with files". Do not rely on a later "When to use" section for triggering information.

## Resource directories

### references/

Put documentation, schemas, domain rules, detailed examples, or other knowledge here when the agent may need to read it while working.

Keep detailed material out of `SKILL.md` when it is conditional or large. Link each reference directly from `SKILL.md` and explain when to read it. Avoid chains where one reference is discoverable only through another reference.

For long references, provide navigational structure such as a table of contents.

### scripts/

Put executable helpers here when the operation benefits from deterministic behavior or would otherwise be repeatedly rewritten. Prefer scripts with minimal dependencies and clear command-line interfaces.

Document invocation with an explicit interpreter when appropriate:

```bash
python3 <skill-root>/scripts/example.py ...
```

This is more portable than assuming the file is executable or that the caller's working directory is the skill root.

### assets/

Put files here when they are inputs/resources for the output rather than instructions to be read into context: templates, boilerplate projects, images, sample artifacts, icons, fonts, and similar material.

### agents/

Platform-specific agent metadata can live here. OpenAI's published skill-creator recommends `agents/openai.yaml` for UI-facing metadata, but it is not the core portable skill contract. Add or regenerate platform metadata only when the target platform needs it and use that platform's current documentation for its schema.

## Progressive disclosure

Design the skill so information loads in stages:

1. name + description for discovery;
2. `SKILL.md` after the skill triggers;
3. references/assets/scripts only when needed.

This is why `SKILL.md` should contain the essential workflow and navigation rather than every detail the skill knows.

## Files to avoid

Do not add auxiliary project documentation that does not help the agent perform the skill, such as:

- `README.md`
- `INSTALLATION_GUIDE.md`
- `QUICK_REFERENCE.md`
- `CHANGELOG.md`

Also exclude secrets, `.git`, caches, virtual environments, dependency directories, generated archives, and unrelated source material.

## ZIP packaging

For ZIP upload/export, package the whole skill directory so the ZIP contains exactly one top-level folder:

```text
example-skill.zip
└── example-skill/
    ├── SKILL.md
    ├── references/
    └── scripts/
```

Do not zip only the contents of the directory into the archive root. Do not wrap the skill in two directory levels.

## Primary sources

OpenAI Skills guide:
https://developers.openai.com/api/docs/guides/tools-skills

OpenAI Plugins skill-building guide:
https://developers.openai.com/plugins/build/skills

OpenAI published skill-creator:
https://github.com/openai/skills/tree/main/skills/.system/skill-creator
