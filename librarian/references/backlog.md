# Librarian backlog

## LIB-001 — Preserve the custom skill icon

- Status: Deferred; use the generic icon for now.
- Added: October 3, 2026 (America/Chicago).
- Goal: Display the simple teal-and-cream owl with copper glasses in the Skills UI.
- Preserved asset: `assets/librarian-owl.svg` inside the Librarian skill. Native vector SVG, 64 × 64 with a matching viewBox. Keep this file bundled for future use.

### Verified observations

1. Saving owl artwork at `assets/icon.svg` succeeded initially, but a subsequent service-generated reconciliation replaced it with a generic icon.
2. Saving the owl under `assets/librarian-owl.svg` preserved that asset. Setting `icon_small` and `icon_large` in `agents/openai.yaml` to it did not persist: reconciliation reset both to `assets/icon.svg`.
3. Librarian's initializer does not write icon metadata. The built-in metadata generator accepts custom icon paths and does not force the generic path. No local template cause was found.
4. The reset happened after the accepted save and before the persisted readback. The internal service operation is not visible.

### Hypothesis, not established cause

The service may regenerate icon files and references from separately stored skill metadata. Do not treat this as a confirmed diagnosis or assume an SVG compatibility problem.

### Next investigation

Identify a supported skill-details or metadata operation for setting a custom icon. Inspect browser editing controls or documented management capabilities. Avoid repeating file-only saves until there is a materially different approach.

### Acceptance criteria

- Both icon references and the intended artwork survive reconciliation and later readback.
- The Skills UI displays the owl after refresh.
- The owl remains bundled and Librarian's behavior is preserved.

### Current decision

Leave the generic display icon in place. Retain the owl asset unchanged; connect it when the supported mechanism is understood. Do not make further icon changes now.
