# Adding a starter kit

Each kit must be usable on its own. Keep it inside `templates/<category>/<kit-name>/` with its own dependency list, configuration example, database migrations, sample-data command, admin workflow, and setup guide.

## Before opening a pull request

- Explain what the starter does and list any missing integrations.
- Include local setup instructions that begin from a clean checkout.
- Keep credentials, customer data, local databases, and generated secrets out of Git.
- Use original names, copy, layouts, and assets. References can inform common workflows, but do not reuse a site's logo, source code, or proprietary imagery.
- Document what must change before production, including storage, payment, email, deployment, and security settings.
- Regenerate the individual ZIP in `downloads/` with `python scripts/package_templates.py` after changing kit files.
