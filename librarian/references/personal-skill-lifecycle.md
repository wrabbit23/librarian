# Personal skill lifecycle

## Resolve capability and destination

- Read the environment's current skill-management instructions before making lifecycle changes. Keep platform-specific operations there rather than duplicating their commands in this portable creator.
- In a supporting ChatGPT environment, creation can save and install a personal skill directly into the user's skill directory. A downloadable ZIP alone does not establish installation.
- Resolve an existing skill by its frontmatter name, preserving its managed directory and identity. Distinguish personal skills from plugin-provided skills; the ability to edit local bytes does not establish ownership.
- Prefer a local-first workflow for personal skills that evolve through use: apply requested edits to the managed working copy immediately, but do not persist/publish the accumulated changes until the user explicitly says `save`, `publish`, or otherwise clearly requests persistence. A request to edit content is not, by itself, a persistence request when this workflow is in use.
- Keep skill-owned evolving state with the skill when practical. Use an optional `data/` directory for progress logs, backlogs, inventories, and similar user/project state that should travel with the skill. Do not move that state into unrelated Library files unless the user asks for that storage model.
- A hypothetical question about removal is not an uninstall request. Resolve which skills the user means before removing unrelated skills.
- Uninstall disables while retaining restorable content; permanent deletion requires an explicit deletion request. Follow the platform's actual implementation of those operations.
- Check the client surface before concluding that a lifecycle action is unavailable. In October 2026, the user found permanent deletion in the browser interface after being unable to find it in Android. Treat this as observed interface variation, not a guarantee about future versions. If a mobile control is missing, suggest checking the browser; do not invent a menu path or use the browser on the user's behalf without an authorized site task.

## Verify outcomes

- Treat local edits, structural validation, behavior checks, packaging, and persisted installation as separate outcomes. Report only outcomes supported by evidence.
- When the user requests a save, persist all intended accumulated local changes for that skill unless they scope the save more narrowly. Do not include caches, unrelated changes, or a previously failed lifecycle operation.
- Verify the persisted state after reconciliation. The current session's skill catalog and Installed tab may be cached; a stale display alone is not evidence that a verified operation failed. Suggest refreshing the Skills page when appropriate.
- Distinguish installed skills from the creator catalog. In the same session, UI uninstall removed two skills from the agent-visible personal-skill checkout while retaining them under “Created by me” with a plus button for reinstallation. Absence from the checkout or its `uninstalled/` directory therefore does not establish permanent deletion. State which collection was checked; verify creator-catalog deletion separately through a supported surface or the user's observation.
- Managed directories may be renamed to `skill-<32 hexadecimal characters>`. Preserve that directory when editing. Validate the frontmatter name normally; use the frontmatter name for the top-level folder of portable ZIP exports.

## Handle failures

- An observed creation success does not prove uninstall or deletion support. In an October 2026 session, creation succeeded but an uninstall save received HTTP 422 twice, with the skill still present in the persisted active state. This is an observation, not a universal platform limitation or diagnosis of the cause.
- If a save fails, inspect persisted state before claiming either success or failure; ambiguous error text can coexist with a successful remote change.
- Follow the management workflow's bounded retry policy for conflicts or transient failures. Repeated validation/service rejection warrants stopping and reporting that the requested operation did not persist; do not repeatedly submit it or substitute permanent deletion for uninstall.
- Before a later skill operation, inspect local state and isolate any unsaved failed change using the supported recovery workflow. Preserve recoverable content and do not silently include the failed operation in a new save.
- Keep failure explanations factual and brief. Distinguish service rejection from an automatic approval rejection; do not invent a permission requirement or ask for approval as a cure for an unsupported operation.
