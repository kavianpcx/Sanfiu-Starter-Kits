# Sanfiu Starter Kits

Reusable website starters with a real backend, database, and clear setup instructions. Each kit lives in its own folder and is designed to be rebranded and extended.

## Kits

| Kit | Type | Stack | Status | Download |
|---|---|---|---|---|
| [Sanfiu Market](templates/ecommerce/sanfiu-market/) | Online store | Django, SQLite/PostgreSQL, HTML, CSS | Preview | [ZIP](downloads/sanfiu-market.zip) |
| [Sanfiu Live](templates/events/sanfiu-live/) | Event discovery and booking | Django, SQLite/PostgreSQL, HTML, CSS | Preview | [ZIP](downloads/sanfiu-live.zip) |
| [Sanfiu Marketplace](templates/marketplace/sanfiu-marketplace/) | Multi-seller marketplace | Django, SQLite/PostgreSQL, HTML, CSS | Preview | [ZIP](downloads/sanfiu-marketplace.zip) |

Open a kit's README for features, local setup, sample data, and deployment notes. The source is organized by kit so it can be copied into a separate project or downloaded with the repository.

## Project goals

- Complete, working front ends and back ends, not static mockups.
- Local database setup and realistic sample content.
- Simple rebranding through editable text, colors, and images.
- An index here that links to every kit and its setup guide.

## Contributing a kit

Add each new starter under `templates/<category>/<kit-name>/` and include a dedicated README with its stack, configuration, database setup, local run commands, and deployment requirements.

The first two examples cover product sales and capacity-limited event reservations. Additional kits should live in separate folders and include their own backend, data model, admin workflow, sample content, and setup guide.

See the [roadmap](ROADMAP.md) for the next planned starter types. Regenerate individual source archives with `python scripts/package_templates.py` after changing a kit.

