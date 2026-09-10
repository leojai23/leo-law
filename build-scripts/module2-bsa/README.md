# Module 2 — BSA ⇄ Evidence Act — groundwork (not shipped yet)

## Status (2026-09-09)

| Layer | State |
|-------|-------|
| **BSA full text** | ✅ done — `bsa_sections.json`, all 170 sections parsed from the NCRB enacted-Act PDF (`bsa_full.txt`) and checked against the Act's own arrangement of sections (0 real mismatches). Parser: `parse_bsa.py`. |
| **BSA ⇄ IEA mapping** | ❌ not reliable yet — the official concordance (`bsa_concordance.txt`, from UP Police) is a two-column PDF that PyMuPDF flattens in an inconsistent column order, so the alternation parser (`parse_bsa_concordance.py`) and the heading-similarity fallback (`bsa_map_by_heading.py`) both desync. **Do not ship `bsa_map.json` / `bsa_rows.json`.** Needs a clean machine-readable concordance, or a manual section-by-section pass. Same blocker as roadmap item 1.1 (IPC full text). |
| **UI (module switcher)** | ⬜ not started — index.html needs a tab control to swap the active dataset + text/meta blobs. |

## Next steps
1. Obtain a clean BSA↔IEA concordance (official CSV/table), or verify the ~170 mappings by hand against `bsa_concordance.txt` de-wrapped (the reliable method used for the BNS pass).
2. Build `bsa_rows.json` (one row per BSA section: `{bsa, iea, heading, status, whatChanged}`).
3. Refactor `index.html` for a module switcher; wire in `bsa_sections.json` + `bsa_rows.json`.
4. No First Schedule classification applies (BSA is evidence law, not offences).
