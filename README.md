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
- **Expand any card ("bare act")** for the full verbatim BNS section text — every
  sub-section, clause, Exception, Explanation and Illustration — plus a
  **BNSS First Schedule classification table** (cognizable / bailable / court),
  a **compoundability** line (BNSS s.359), a "what changed" note, the
  corresponding IPC number, a **provenance** line, and related-card links.
- Compact **cognizable / bailable chips** on each card (sub-section aware).
- All **358 BNS sections** are embedded (text keyed by section number); **288**
  carry First Schedule classification data.
- **Sources & method** panel at the top of the page explains what is verified.
- 4 reading themes (Day / Sepia / Dark / Night), remembered in `localStorage`.
- Fully offline after first load; installable to the home screen.

### Reliability / verification (9 Sep 2026 pass)
`build-scripts/` holds the whole pipeline:
| script | does |
|--------|------|
| `parse_bns.py` | official BNS bare act (Gazette/NCRB PDF) → `bns_sections.json` (all 358 sections) |
| `parse_schedule.py` | BNSS First Schedule → `bnss_schedule.json` (classification, 288 sections) |
| `parse_compound.py` | BNSS s.359 compounding tables → `compound.json` |
| `reconcile.py` / `reconcile2.py` | diff the app's IPC↔BNS mappings against the official concordance (`concordance_uppolice.txt`) |
| `make_meta.py` | merge classification + compounding → `bns_meta.json` |
| `build_detail.py`, `build_reliability.py` | inject the JSON blobs + detail/classification UI into `index.html` |

**What was verified:** BNS section text is verbatim from the public-domain Gazette
text. Every IPC↔BNS mapping was reconciled against the official
corresponding-sections concordance; **6 mapping errors were found and fixed**
(IPC 116→BNS 56, 120→60, 145→189(3), 216→253, 372/373→98/99, 427→324(4)).
Classification is from the BNSS First Schedule.

**Still a finding aid, not an authority.** Not yet included: full IPC section
text; case-law citations. Always confirm against `indiacode.nic.in` and check for
amendments / commencement notifications (e.g. BNS 106(2)) before citing.

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
