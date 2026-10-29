# Application Package engineering

Keep personal evidence outside this public repository. Use only synthetic records in tests.

The JSON Schemas define every stage boundary. A stage implementation is complete only when its schema, hash-state, failure behavior, and synthetic mutation test agree. Preserve the separation between evidence, positioning, writing, composition, change control, and release auditing.

Run the full synthetic suite and validate every changed skill before release. Never promote a candidate by bypassing a failed gate.
