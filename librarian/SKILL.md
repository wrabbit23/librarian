---
name: librarian
description: Create, find, load, and maintain personal skills; capture lasting corrections and preferences in the appropriate skill. Use when asked for Librarian, skill creation or discovery, URL or catalog skill loading, or saving feedback into a named skill. Do not interrupt unrelated tasks merely to suggest saving preferences.
---

# Librarian

Manage reusable knowledge through separate, small skills. Preserve the distinction between using instructions in this conversation and installing or updating a saved personal skill.

## Startup update check

At the first Librarian activation in each conversation, automatically read [references/updates.md](references/updates.md) and check the configured upstream release. Check again only when explicitly requested. This is an instruction executed when the skill is loaded, not a background service or a guarantee that the host will activate Librarian at chat startup. Continue the user's task if the check cannot complete.

## Route the request

- For discovery, catalog browsing, or loading a URL, read [references/skill-loading.md](references/skill-loading.md).
- For corrections, retrospective learning, or remembering a preference in another skill, read [references/feedback.md](references/feedback.md).
- For any request to create a new personal skill, use Librarian's authoring and personal-skill lifecycle directly. Do not fall back to a generic ZIP-only, artifact-template, or unrelated skill-creation workflow unless the user explicitly asks for that output or capability.
- For revision of an existing personal skill, use the same Librarian lifecycle. Offer the Librarian feedback hook for skills intended to evolve through use.
- Keep domain work in the managed skill; Librarian handles discovery, organization, and maintenance. Do not claim automatic background monitoring or guaranteed dependency activation.

## Core workflow

1. Determine the skill's purpose from concrete user requests it should handle. Do not over-design for hypothetical cases.
2. Choose a short hyphen-case name. Keep discovery metadata precise: the `description` must say both what the skill does and when it should trigger.
3. Decide what belongs where before writing:
   - `SKILL.md`: essential procedure, decision rules, tool/resource navigation, and non-obvious constraints.
   - `references/`: documentation or domain knowledge the agent should read only when relevant.
   - `scripts/`: repeatable or deterministic operations worth executing instead of rewriting.
   - `assets/`: templates, boilerplate, images, sample artifacts, or other files meant to be copied or used in outputs rather than read as instructions.
   - `data/`: optional user- or project-specific state that should travel with a personal skill, such as progress logs, backlogs, inventories, or other evolving records. Prefer this over unrelated Library files when the data belongs to the skill.
   - `agents/`: optional platform-specific metadata. Add only when useful and supported by the target platform.
4. Prefer existing relevant installed skills over duplicating their guidance. If a Markdown, style, document, spreadsheet, presentation, coding, or domain skill already covers part of the task, reference/use it rather than copying its rules into the new skill.
5. Keep `SKILL.md` lean. Move detailed background, long examples, schemas, and variant-specific guidance to directly linked files under `references/`.
6. Use explicit, portable script invocation such as `python3 <skill-root>/scripts/tool.py ...`. Do not rely on executable bits or the caller's working directory.
7. Run every new or modified helper script on a representative input when practical.
8. For personal skills that evolve through use, prefer a local-first edit cycle: apply requested changes to the skill's working copy immediately, keep evolving skill-owned state inside the skill (typically under `data/`), and do not persist/publish the accumulated changes until the user explicitly says `save`, `publish`, or otherwise clearly requests persistence.
9. When persistence is requested, validate the completed skill, fix all errors, review warnings, and save through the environment's personal-skill workflow when available. Export a ZIP only when requested.

## Personal skills in ChatGPT

Read [references/personal-skill-lifecycle.md](references/personal-skill-lifecycle.md) before creating, saving, updating, installing, uninstalling, or deleting a personal skill in a managed environment. Use the available skill-management skill for current routing and persistence requirements. Direct installation may be supported; do not assume a ZIP is the only delivery option.

## Start a new skill

Resolve this skill's directory as `CREATOR_DIR`, then run:

```bash
python3 "$CREATOR_DIR/scripts/init_skill.py" <skill-name> \
  --path <parent-directory> \
  --description "<what it does and when to use it>" \
  --resources references,scripts,assets
```

Only request resource directories the skill actually needs. After scaffolding, replace the generated placeholder body with the real procedure and add only useful resources.

## Validate

Run:

```bash
python3 "$CREATOR_DIR/scripts/validate_skill.py" <path-to-skill>
```

Treat validation errors as blockers. Review warnings intentionally rather than automatically silencing them.

The validator checks the common structural rules plus several practical failure modes: empty metadata, folder/name mismatch, malformed names, unfinished scaffold text, suspicious extra documentation, broken local Markdown links, unreferenced reference files, deep reference nesting, symlinks, and Python syntax errors.

## Package for export

Run:

```bash
python3 "$CREATOR_DIR/scripts/package_skill.py" <path-to-skill> --output <skill-name>.zip
```

The packager validates first and writes a deterministic ZIP with one top-level folder named after the skill. It excludes common cache/VCS junk and refuses symlinks.

## Editing an existing skill

Preserve the user's existing design unless it causes a concrete problem. Make narrow changes in the working copy and re-run affected scripts as needed. For personal skills that use the local-first model, accumulate those edits locally and persist them only when the user explicitly requests a save or publish. When persistence is requested, validate and save through the supported lifecycle. Repackage only for a requested export. Do not add infrastructure merely because this creator supports it.

## Authoring rules

- Write instructions for another capable agent, not a novice human tutorial.
- Prefer outcomes, constraints, and decision rules over verbose explanation.
- Keep triggering guidance in the frontmatter `description`; the body may not be loaded until after the skill is selected.
- Link every reference file directly from `SKILL.md` and say when it should be read.
- Avoid duplicate information across `SKILL.md` and `references/`.
- Avoid deeply nested references.
- Do not add `README.md`, installation guides, changelogs, or similar auxiliary documentation unless the user explicitly needs them as part of the skill's function.
- Do not hardcode platform-specific metadata or invocation syntax into an otherwise portable skill unless the target platform requires it.
- Do not bundle secrets, credentials, caches, virtual environments, dependency trees, generated archives, or unrelated project files.

## References

Read [references/skill-format.md](references/skill-format.md) when checking structure, packaging, or OpenAI-specific conventions.

Read [references/authoring-principles.md](references/authoring-principles.md) when deciding how much instruction to include, how to split resources, or how to design triggering behavior.

Read [references/backlog.md](references/backlog.md) when maintaining Librarian or investigating known issues. Keep deferred decisions and preserved assets intact unless the user authorizes changing them.
