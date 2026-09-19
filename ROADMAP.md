# Leo-Law — Roadmap

An offline-first reference notebook for **Indian lawyers, with a Tamil Nadu focus**.
Single-file PWA, same house style as Leo-Interview / Leo-Health. Live at
<https://leojai23.github.io/leo-law/>.

**Design principle:** every screen must be *reliable enough for a practitioner to
refer to*, not just a study aid. Statutory text only from the Gazette / India Code
(public domain); every fact carries a provenance line; every mapping is reconciled
against the official concordance; case law is citation + own-words ratio only —
never copied notes or headnotes.

Status legend:  ✅ done · 🔜 next · ⬜ planned · ⏸ deferred
Effort: **S** ≈ hours · **M** ≈ a session or two · **L** ≈ multi-session

---

## Phase 0 — Module 1 foundation ✅

- ✅ BNS ⇄ IPC quick converter — two-way section/keyword search, family filters,
  3 status groups (Mapped/Renumbered · New in BNS · Omitted), 4 reading themes,
  offline PWA, deployed to GitHub Pages
- ✅ 152 mapped provisions (the common ones a litigator reaches for)
- ✅ Full verbatim **BNS text for all 358 sections** (Gazette source, parser-QA'd),
  expandable per card — sub-sections, Exceptions, Explanations, Illustrations
- ✅ **BNSS First Schedule classification** (cognizable / bailable / triable-by)
  for 288 sections + sub-sections; compact chips on cards, full table in detail
- ✅ **Compoundability** line (BNSS s.359(1)/(2))
- ✅ **Mapping reconciliation** against the official IPC–BNS concordance —
  6 errors found and fixed (see Changelog)
- ✅ Per-section **provenance** line + top-of-page **"Sources & method"** panel

---

## Phase 1 — finish Module 1 to practitioner grade

| # | Item | Deliverable | Effort | Status |
|---|------|-------------|--------|--------|
| 1.1 | **Full IPC bare-act text** | old IPC section shown verbatim beside the BNS one (currently only the number) | M | ⏸ **parked (decision 2026-09-09)** — no authoritative IPC 1860 full-text source is reachable by the fetcher (India Code PDF 403s, legislative.gov.in refused, web.archive blocked, HTML mirrors are ToC-only). Resume when an official IPC PDF is supplied and dropped into the repo, or if we later accept section-by-section extraction from a mirror (lower confidence). Proceeding to Phase 2.1 in the meantime. |
| 1.2 | **Second-source text diff** | diff all 358 BNS texts against a 2nd *enacted*-Act source; stamp each "text verified" | M | 🟡 **partial** — structural verification passed (358/358 sections; every heading matches the Act's own table of contents; no boundary/merge/drop errors). Full body char-diff still pending: India Code 403s and the PRS PDF is the *Bill*, not the enacted Act. |
| 1.3 | **Punishment pull-out** | a clean "Punishment" line per sub-section, extracted from the text, not paraphrased | S | ⬜ |
| 1.4 | **Amendment / commencement tracker** | flag provisions not yet in force or later amended (BNS 106(2) etc.); a dated "as in force on…" line | S (ongoing) | ⬜ |
| 1.5 | **Landmark case pointers** | citation + one-line ratio only, for the top ~40 offences (*Mithu*, *Joseph Shine*, *Navtej Johar*, …) | M | ⬜ |
| 1.6 | **In-text cross-reference links** | "see section 122" becomes a tap-through inside the section text | S | ⬜ |

---

## Phase 2 — the other two new-code converters

Same engine and reliability method (Gazette text + official concordance + Schedule).

| # | Item | Notes | Effort | Status |
|---|------|-------|--------|--------|
| 2.1 | **BSA ⇄ Evidence Act** | 170 sections — smallest, fastest confidence-builder | M | 🟡 **partial** — BSA full text done & verified (170/170 sections, checked vs the Act's arrangement of sections). **Mapping blocked** on the same two-column-PDF problem as 1.1: the official BSA↔IEA concordance flattens in inconsistent column order, so auto-parsing desyncs. Needs a clean concordance or a manual pass. UI module-switcher not started. Groundwork in `build-scripts/module2-bsa/`. |
| 2.2 | **BNSS ⇄ CrPC** | 531 sections — procedure, bail provisions, limitation for cognizance, magistrate powers | L | ⬜ |

---

## Phase 3 — practice modules (task-oriented)

| # | Item | Deliverable | Effort | Status |
|---|------|-------------|--------|--------|
| 3.1 | **s.138 NI Act** | notice-period calculator, limitation dates, ingredients, stage checklist, draft skeletons | M | ⬜ |
| 3.2 | **Bail** | regular / anticipatory / default: grounds, checklist, which court, BNSS section map | M | ⬜ |
| 3.3 | **Limitation Act ready-reckoner** | searchable table of the ~137 Articles (period + when time runs) | S | ⬜ |
| 3.4 | **Court-fees & suit valuation** | Central Act first, then TN (see Phase 4) | M | ⬜ |
| 3.5 | **Standard drafts & checklists** | plaint, WS, bail application, 138 complaint, vakalat | M | ⬜ |
| 3.6 | **Suggest from case facts** | paste/upload case-sheet text → ranked candidate provisions, offline keyword-overlap engine (no network, nothing stored) | M | ✅ **done** 2026-09-09 |

---

## Phase 4 — Tamil Nadu layer *(the differentiator)*

| # | Item | Deliverable | Effort | Status |
|---|------|-------------|--------|--------|
| 4.1 | **TN state amendments** | to CPC / CrPC→BNSS / Rent Control / Land Reforms | M | ⬜ |
| 4.2 | **TN Court-Fees & Suits Valuation Act** | ready-reckoner | M | ⬜ |
| 4.3 | **TN enactments index** | TN Prohibition, TN Public Property, Pannaiyal Protection, TNPID, etc. | M | ⬜ |
| 4.4 | **Deep links** | Madras HC cause list & JUDIS, eCourts case status, DLSA | S | ⬜ |
| 4.5 | **Local practice notes** | jurisdiction, presentation, filing quirks — clearly marked "practice note, not law" | M (ongoing) | ⬜ |

---

## Phase 5 — Tamil-language layer

| # | Item | Deliverable | Effort | Status |
|---|------|-------------|--------|--------|
| 5.1 | **Tamil gloss** under each section | plain-language, labelled "not an official translation" | L | ⬜ |
| 5.2 | **Tamil UI toggle** | | S | ⬜ |
| 5.3 | **Bilingual search** | type "கொலை" → murder / BNS 103 | M | ⬜ |

---

## Phase 6 — platform & trust

| # | Item | Deliverable | Effort | Status |
|---|------|-------------|--------|--------|
| 6.1 | **Unified search** across all modules from one box | | M | ⬜ |
| 6.2 | **Versioned changelog** in-app | "what changed since you last opened" + a data-version stamp | S | ⬜ |
| 6.3 | **Update pipeline** | re-run `build-scripts/` when the Gazette/Schedule changes | S | ⬜ |
| 6.4 | **Disclaimer / terms page** | "finding aid, not legal advice, verify the Gazette" | S | ⬜ |
| 6.5 | **Leo-Hub tile** + shared styling | | S | ⬜ |
| 6.6 | Optional: packaged offline bundle / installable desktop | | M | ⏸ |

---

## Cross-cutting rules (in force now)

- Statutory text **only** from Gazette / India Code (public domain, s.52(1)(q)
  Copyright Act 1957). **Never** copy SCC / Manupatra / Devgan notes or headnotes.
- Every fact carries a **provenance** line.
- Every mapping is **reconciled against the official IPC–BNS concordance**.
- Case law = **citation + own-words ratio only**.
- Every module keeps the standing disclaimer: *finding aid, not an authority;
  confirm against the Gazette; check for amendments and commencement notifications.*

---

## Suggested order

**Phase 1** (complete the module people actually rely on) → **2.1 BSA converter**
(fast win) → **3.1 s.138 module** → **Phase 4 TN layer**.

---

## Changelog

### 2026-09-09 — 3.6 Suggest from case facts
- New mode toggle: **Browse sections** / **Suggest from case facts**. In suggest
  mode, paste or upload (`.txt`) case-sheet text and get a ranked list of
  candidate provisions built from the *existing* embedded data (152 rows + 358
  BNS section texts) — no new data, no network call, nothing persisted.
- **Design (client-side, no dependencies):** a compact TF-IDF-style scorer over
  two weighted fields per provision — a "core" field (title/gist/note/BNS
  heading, high weight) and a "body" field (the BNS definition text with
  Illustrations stripped, low weight). Light suffix-stemming so
  robbed/robbing/robbery collide.
- **Reliability calibration — the important part.** The first version was
  actively dangerous: unrelated text ("my neighbour parked his car…") scored
  *higher* than genuine matches and confidently topped with "Marrying again
  during the lifetime of a spouse." Fixed by (1) excluding Illustrations from
  the index (they use everyday scenario words that caused false hits), (2)
  gating every result on **≥2 distinct term matches in the curated core
  fields** (title/gist/heading) or an exact phrase match — a single stray word
  can never qualify a result on its own. Verified against 6+ unrelated fact
  patterns (all now return zero results) and 8+ genuine fact patterns
  (dowry, 420 cheating, acid attack, stalking, rape, theft, murder — all
  surface the right provision at or near #1). Chose **precision over recall**:
  it will go silent rather than guess wrong when the case text's wording
  diverges a lot from the statutory vocabulary (a documented, disclosed
  limitation) — the wrong trade-off for a lawyer's tool is a confident wrong
  answer, not a missed one.
- `sw` cache → `leo-law-v5`.

### 2026-09-09 — decision: park 1.1, start 2.1
- Full IPC bare-act text (1.1) parked pending an authoritative source. Moving to
  Phase 2.1 (BSA ⇄ Evidence Act) so momentum isn't lost. 1.1 resumes when an
  official IPC PDF is available.
- **2.1 groundwork:** BSA enacted-Act PDF obtained (NCRB, 98 pp); parsed all 170
  sections (`parse_bsa.py` → `bsa_sections.json`), verified against the Act's own
  arrangement of sections — 0 real mismatches. BSA↔IEA concordance obtained but
  its two-column layout flattens in inconsistent order, so auto-mapping is not
  yet reliable — same blocker class as 1.1. Groundwork parked in
  `build-scripts/module2-bsa/`; mapping + module-switcher UI still to do.

### 2026-09-09 — Phase 1 start (partial)
- **1.2 structural verification:** re-parsed the enacted BNS table of contents
  from the NCRB PDF independently of the body-text parse; all 358 sections
  present, every body heading matches the ToC heading, no boundary errors.
  (`build-scripts/verify_toc.py`)
- **1.1 blocked:** could not obtain an authoritative full-text IPC 1860 source
  (India Code PDF 403; legislative.gov.in connection refused; web.archive.org
  unavailable; HTML mirrors serve table-of-contents only). Deferred pending a
  supplied PDF or a decision to use a lower-confidence mirror.
- Confirmed the PRS "BNS 2023" PDF is the **Bill** (137 pp, "ARRANGEMENT OF
  CLAUSES", s.3 = "General Explanations and expressions"), not the enacted Act —
  not usable as a second source for a text diff.

### 2026-09-09 — reliability pass
- Reconciled all 152 IPC↔BNS mappings against the official concordance.
  Fixed 6 mapping errors:
  - IPC **116** → BNS **56** (was 51)
  - IPC **120** → BNS **60** (was 55)
  - IPC **145** → BNS **189(3)** (was 189(5))
  - IPC **216** → BNS **253** (was 251)
  - IPC **372 / 373** → BNS **98 / 99** (was 145 / 146 — also wrong subject)
  - IPC **427** → BNS **324(4)** (was 324(3) — reverted a bad earlier fix)
- Added BNSS First Schedule classification (288 sections) + compoundability.
- Added provenance lines + "Sources & method" panel.

### 2026-09-09 — detail view
- Embedded all 358 BNS sections (Gazette text); expandable "bare act" per card
  with sub-sections, Exceptions, Explanations, Illustrations, related-section links.

### 2026-09-09 — launch
- Module 1 BNS⇄IPC converter, 152 provisions, deployed to GitHub Pages.
