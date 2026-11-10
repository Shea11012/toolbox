# Pi — Package Gallery Catalog

`pi-packages.csv` contains **5,249 packages** from the **2026-07-17** npm gallery snapshot
(keyword `pi-package`). This catalog was not refreshed with the Pi 1.5.0 documentation.
Package versions, availability, download counts, and compatibility may have changed.

For current package installation and manifest rules, read `extending-pi.md`.
The CSV includes package name, type, monthly downloads, version, author, description,
installation command, repository, npm URL, and update date. The classification is heuristic.

Refresh the gallery separately from the skill root:

```sh
python3 scripts/fetch-pi-packages.py
```

After a successful refresh, update the count and snapshot date here, in `SKILL.md`, and in
both README files. Documentation refreshes leave these gallery files untouched.
