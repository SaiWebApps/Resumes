# ChatGPT skill package

Run `python scripts/install_skills.py --target chatgpt` to create one `.skill` archive for each canonical skill. Upload the front-door `application-package.skill` and the eight internal stage skills to the same workspace. The front-door archive contains the same Python runtime, schemas, package metadata, and portable launcher under `application-package/runtime/`; it does not depend on a provider-specific prompt.

The verified workflow requires filesystem execution, Python 3.11 with the declared dependencies, web or supplied-source access, DOCX/PDF rendering, and page-image inspection. When the host cannot execute the bundled runtime or lacks another capability, return the precise capability limitation rather than describing unperformed verification.
