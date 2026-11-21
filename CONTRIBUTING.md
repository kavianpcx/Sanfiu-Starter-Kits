# Adding a starter kit

Keep each project independent under `templates/<category>/<kit-name>/`. Include its own dependency list, environment example, migrations, sample-data command, admin workflow, English UI copy, and setup guide.

## Before opening a pull request

- Add a preview image under `previews/` and make its README gallery image link directly to that kit's ZIP in `downloads/`.
- Add the kit to the root README gallery and to `scripts/package_templates.py`.
- Explain features, setup, sample credentials if any, and missing integrations.
- Keep secrets, customer data, local databases, and generated credentials out of Git.
- Use original names, copy, layouts, and assets. Do not reuse another site's logo, source code, or proprietary imagery.
- Document production changes, including storage, payments, email, security, and deployment.
- State that remote sample photos and third-party services are not covered by this repository's MIT license.
- Regenerate ZIP archives with `python scripts/package_templates.py`.
