# Skill authoring principles

## Keep the skill smaller than the task domain

A skill is procedural leverage, not a complete textbook. Assume the consuming agent already has broad general knowledge. Add what is specific, reusable, easy to forget, organization-specific, or operationally important.

## Start from concrete use cases

Before adding machinery, identify several representative requests the skill should handle. Use them to decide what reusable resources are actually justified.

A script is justified when deterministic execution or repeated code matters. A reference is justified when background material is genuinely needed at execution time. An asset is justified when an output needs a reusable source file or template.

## Make discovery discriminating

The description should be broad enough to catch intended requests but narrow enough not to hijack neighboring tasks. Mention meaningful boundaries when confusion with another skill is likely.

Prefer:

```yaml
description: Create and update PostgreSQL migration plans, including dependency ordering, rollback steps, and deployment checks. Use for schema-change planning and migration review; do not use for general SQL query writing.
```

over:

```yaml
description: Helps with databases.
```

## Keep the body procedural

Useful body content includes:

- ordered workflows when order matters;
- selection rules between tools or modes;
- invariants that must be preserved;
- references to supporting files and when to load them;
- exact commands for deterministic helpers;
- failure handling that would not be obvious to a capable agent.

Avoid explaining ordinary concepts the agent already knows.

## Compose with other skills

When another installed skill already owns a specialty such as Markdown style, document generation, spreadsheet formatting, presentation design, PDF handling, or a particular API, use that skill rather than cloning its entire rule set.

The new skill should define its domain-specific orchestration and constraints. This reduces duplication and keeps improvements to shared skills reusable.

Do not assume a named companion skill exists on every platform. Phrase dependencies conditionally unless the environment guarantees them.

## References should be directly discoverable

Link references from `SKILL.md` rather than constructing a chain of references that the agent has to discover recursively. When a reference is relevant only to a particular branch, say so next to the link.

If a reference becomes large, add headings and navigation so an agent can inspect only the relevant section.

## Scripts should be boring

Prefer small, deterministic, inspectable scripts with minimal dependencies. Give them command-line help and nonzero exit codes on failure. Keep data transformation in scripts and judgment in the agent unless there is a reason to do otherwise.

Use explicit interpreters (`python3`, `node`, etc.) unless execution permissions and runtime are guaranteed.

## Validate observable behavior

A structural validator can catch packaging errors but cannot prove the skill is good. For important skills, test representative prompts and check observable outcomes: correct files, preserved invariants, successful commands, expected transformations, or other concrete behavior.

Avoid elaborate benchmarking infrastructure unless the skill's risk or scale makes it worthwhile.

## Prefer narrow iteration

When real use reveals a failure, repair the specific cause. Do not accumulate a universal rule for every one-off example. Remove obsolete rules as the skill evolves.
