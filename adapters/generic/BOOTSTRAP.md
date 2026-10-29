# Generic agent bootstrap

The bundle is self-contained: it includes the canonical `skills/`, Python engine under `src/`, public JSON Schemas, package metadata, and a portable `bin/application-pack` launcher. Expose `skills/` to the host's Agent Skills discovery mechanism. Make `application-package` the user-facing entrypoint and keep the other skills available for `next-action.json` stage requests.

Run `bin/application-pack capabilities --profile /path/to/private-profile` from the unpacked bundle. The launcher uses Python 3.11 or newer and reports missing Python dependencies precisely; `python -m pip install .` installs those declared dependencies and a normal command-line entrypoint.

Provide these host capabilities for a complete release:

- read and write access to the run and private profile directories;
- execution of the bundled `bin/application-pack` CLI;
- access to official opportunity sources or supplied snapshots;
- DOCX and PDF generation, rendering, text extraction, hashing, and page-image inspection;
- access to a distinct reviewer model when available.

A host without the required artifact capabilities may produce schema-valid draft content but must return a capability report instead of a released package.
