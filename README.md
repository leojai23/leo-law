# Leo-Law

A private, offline-first reference notebook for Indian lawyers — same single-file PWA
style as Leo-Interview / Leo-Health.

## Module 1 — BNS ⇄ IPC quick converter

Two-way lookup between the **Indian Penal Code, 1860** and the **Bharatiya Nyaya
Sanhita, 2023** (in force 1 July 2024).

- Type an **IPC** number → get the **BNS** section, and vice-versa.
- Also searches the offence name / keywords (murder, cheating, acid, dowry…).
- Filter by family (homicide, hurt, property, sexual offences, women & marriage,
  forgery, defamation, State offences…).
- Three status groups: **Mapped/Renumbered**, **New in the BNS**, **Omitted/decriminalised**.
- 4 reading themes (Day / Sepia / Dark / Night), remembered in `localStorage`.
- Fully offline after first load; installable to the home screen.

### Files
| file | purpose |
|------|---------|
| `index.html` | the whole app — markup, styles, data, logic in one file |
| `manifest.json` | PWA manifest |
| `sw.js` | cache-first service worker — **bump `CACHE` string on every content edit** |
| `icon.svg` | app icon (scales-of-justice mark) |

### Data status — read before relying on it
The dataset in `index.html` (`var DATA = [...]`) is a **hand-compiled seed of 152
provisions**. Key mappings across every chapter cluster (homicide, hurt, acid,
endangerment, public-servant offences, kidnapping, sexual offences, theft/robbery/
dacoity, breach of trust, cheating, mischief, trespass, forgery, currency,
defamation, intimidation) were **spot-checked against devgan.in bare-act text on
2026-09-09**; the mischief-by-fire / s.427 rows were corrected in that pass. The
BNS still folds most IPC offences into sub-sections of combined provisions and a
few are genuinely not 1:1. **Verify every entry against:**

- India Code — BNS 2023 & IPC 1860 (`indiacode.nic.in`)
- The Ministry of Home Affairs / PRS Legislative Research IPC↔BNS comparison charts
- `devgan.in` (cross-referenced bare acts with old↔new mapping)

Not legal advice. IPC still governs offences committed before 1 July 2024.

## Next modules (planned)
- BNSS ⇄ CrPC and BSA ⇄ Evidence Act converters
- s.138 NI Act practice module (notice timeline, drafts, checklist)
- Limitation Act ready-reckoner
- Tamil Nadu specifics: court fees, state amendments, cause-list / eCourts / JUDIS links
- Tamil-language glosses

## Deploy
Static — push to a `leojai23/leo-law` repo, enable GitHub Pages on `main` / root,
add the tile to Leo-Hub.
