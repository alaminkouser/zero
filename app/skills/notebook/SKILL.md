---
name: notebook
description: >
  Maintain and organize the repository as a structured,
  Zettelkasten-style Markdown knowledge base while preserving its existing
  conventions and tooling.
---

# notebook

#notebook

Based on the observation of the repository, here is the detailed structure,
maintenance guidelines, and findings for the notebook.

## 📂 Repository Structure

#repository #structure

The repository is organized as a structured knowledge base (Zettelkasten-style)
using Markdown files.

| File/Dir           | Info                | Naming          |
| :----------------- | :------------------ | :-------------- |
| `DATES/`           | Chronological notes | `YYYY/MM/DD.md` |
| `PERSONS/`         | Profiles            | `kebab-case.md` |
| `RULES/`           | Rules directory     | N/A             |
| `.vscode/`         | Editor settings     | N/A             |
| `README.md`        | Entry point         | Lowercase       |
| `.marksman.toml`   | Marksman config     | N/A             |
| `.prettierrc.toml` | Prettier config     | N/A             |

---

## ⚒️ Maintenance & Naming Rules

#naming #rules

To maintain the integrity and consistency of the notebook, follow these rules:

### Naming Conventions

#naming

- **Filenames**: All filenames (especially in `PERSONS/`) must use
  **`kebab-case`**.
- **Dates**: Day files must be exactly two digits (e.g., `01.md`, `05.md`) and
  stored in `YYYY/MM/` subdirectories.

### Wiki Links

#wiki #wikiLinks

- **Format**: Use `[[path/to/file|Display Text]]` or `[[path/to/file]]`.
- **Extension**: **Do not** include the `.md` extension in wiki links.
  - ✅ `[[PERSONS/al-amin-kouser]]`
  - ❌ `[[PERSONS/al_amin_kouser.md]]`
- **Style**: The `.marksman.toml` is configured with
  `wiki.style = "file-path-stem"` to support this.

### Content Standards

#standard #content

- **Alerts**: Use GitHub-style callouts for important information:
  - `> [!NOTE]` for general info.
  - `> [!WARNING]` for critical warnings.
  - `> [!CAUTION]` for closed or dangerous items (e.g., closed bank accounts).
- **Tags**: Use `#hashtags` (e.g., `#calendar`, `#website`, `#bankAccount`) to
  categorize content within files.

---

## 🔍 Key Findings

| Finding                   | Details                               |
| :------------------------ | :------------------------------------ |
| **Strict Date Hierarchy** | Deep nesting (`Year -> Month -> Day`) |
| **Tooling Integration**   | Prettier, Markdownlint, Marksman      |
| **Structured Data**       | Data in `txt` code blocks             |
| **Link Consistency**      | Cross-referencing via wiki links      |

## 📝 Maintenance Checklist

#checklist

- [ ] Ensure all new files in `PERSONS/` use `kebab-case`.
- [ ] Run `prettier` before committing to keep formatting consistent.
- [ ] Verify that all wiki links are functional and do not contain `.md`.
- [ ] Use the specific directory structure for new daily entries:
      `DATES/YYYY/MM/DD.md`.
